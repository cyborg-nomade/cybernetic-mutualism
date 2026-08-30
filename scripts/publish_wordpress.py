#!/usr/bin/env python3
"""Render a Markdown document and upsert it through the WordPress.com API."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tomllib
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import markdown


DEFAULT_SITE_ID = "109675820"
API_ROOT = "https://public-api.wordpress.com/rest/v1.1/sites"
ALLOWED_STATUSES = {"draft", "pending", "private", "publish"}
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


@dataclass(frozen=True)
class Document:
    path: Path
    metadata: dict[str, Any]
    markdown_body: str


def load_document(path: Path) -> Document:
    """Load TOML front matter and Markdown body from *path*."""
    raw = path.read_text(encoding="utf-8")
    lines = raw.splitlines()

    if not lines or lines[0].strip() != "+++":
        raise ValueError(f"{path}: expected TOML front matter starting with +++")

    try:
        closing_index = next(
            index for index, line in enumerate(lines[1:], start=1) if line.strip() == "+++"
        )
    except StopIteration as error:
        raise ValueError(f"{path}: TOML front matter has no closing +++") from error

    metadata = tomllib.loads("\n".join(lines[1:closing_index]))
    body = "\n".join(lines[closing_index + 1 :]).strip() + "\n"

    for required in ("title", "slug"):
        value = metadata.get(required)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{path}: front matter field {required!r} is required")

    slug = metadata["slug"]
    if not SLUG_PATTERN.fullmatch(slug):
        raise ValueError(
            f"{path}: slug must contain lowercase letters, digits, and single hyphens"
        )

    status = metadata.get("status", "draft")
    if status not in ALLOWED_STATUSES:
        raise ValueError(
            f"{path}: status must be one of {', '.join(sorted(ALLOWED_STATUSES))}"
        )

    for field in ("category_ids", "tag_ids"):
        value = metadata.get(field, [])
        if not isinstance(value, list) or not all(
            isinstance(item, int) and item > 0 for item in value
        ):
            raise ValueError(f"{path}: {field} must be a list of positive integers")

    return Document(path=path, metadata=metadata, markdown_body=body)


def render_html(markdown_body: str) -> str:
    """Render repository Markdown into WordPress-ready HTML."""
    return markdown.markdown(
        markdown_body,
        extensions=["extra", "sane_lists", "smarty"],
        output_format="html5",
    )


def build_payload(document: Document, status_override: str | None = None) -> dict[str, Any]:
    """Build a WordPress.com REST API post payload."""
    status = status_override or document.metadata.get("status", "draft")
    if status not in ALLOWED_STATUSES:
        raise ValueError(f"unsupported WordPress status: {status}")

    payload: dict[str, Any] = {
        "title": document.metadata["title"],
        "slug": document.metadata["slug"],
        "status": status,
        "content": render_html(document.markdown_body),
        # WordPress.com uses this field to hand a newly published post to
        # Jetpack Social. Drafts and non-public posts must never be shared.
        "publicize": status == "publish",
    }

    for source, target in (
        ("excerpt", "excerpt"),
        ("category_ids", "categories"),
        ("tag_ids", "tags"),
    ):
        value = document.metadata.get(source)
        if value:
            payload[target] = value

    return payload


def api_request(
    method: str,
    url: str,
    token: str,
    payload: dict[str, Any] | None = None,
    *,
    not_found_ok: bool = False,
) -> Any:
    """Make an authenticated JSON request and return the decoded response."""
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(
        url,
        data=body,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "cybernetic-mutualism-publisher/1.0",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        if error.code == 404 and not_found_ok:
            return None
        response_body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"WordPress API returned HTTP {error.code}: {response_body}"
        ) from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"could not reach WordPress API: {error.reason}") from error


def upsert_post(
    site_id: str,
    token: str,
    payload: dict[str, Any],
) -> tuple[str, dict[str, Any]]:
    """Create or update a post, using its slug as the stable identity."""
    posts_url = f"{API_ROOT}/{urllib.parse.quote(site_id, safe='')}/posts"
    slug = urllib.parse.quote(payload["slug"], safe="")
    existing = api_request(
        "GET",
        f"{posts_url}/slug:{slug}?context=edit",
        token,
        not_found_ok=True,
    )

    request_payload = payload.copy()
    if existing:
        post_id = existing["ID"]
        # Jetpack Social should run exactly once: on the first transition from
        # a non-public status to publish. Ordinary edits must not create a
        # second Facebook post.
        request_payload["publicize"] = (
            payload["status"] == "publish" and existing.get("status") != "publish"
        )
        result = api_request(
            "POST", f"{posts_url}/{post_id}", token, request_payload
        )
        return "updated", result

    result = api_request("POST", f"{posts_url}/new", token, request_payload)
    return "created", result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Render Markdown and create or update a WordPress.com post by slug."
    )
    parser.add_argument("path", type=Path, help="Markdown document to publish")
    parser.add_argument(
        "--status",
        choices=sorted(ALLOWED_STATUSES),
        help="override the status declared in front matter",
    )
    parser.add_argument(
        "--site-id",
        default=os.environ.get("WORDPRESS_SITE_ID", DEFAULT_SITE_ID),
        help="WordPress.com numeric site ID",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate and print the payload without contacting WordPress",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        document = load_document(args.path)
        payload = build_payload(document, args.status)

        if args.dry_run:
            print(
                json.dumps(
                    {
                        "mode": "dry-run",
                        "site_id": args.site_id,
                        "source": str(args.path),
                        "payload": payload,
                    },
                    indent=2,
                    ensure_ascii=False,
                )
            )
            return 0

        token = os.environ.get("WORDPRESS_ACCESS_TOKEN")
        if not token:
            raise ValueError(
                "WORDPRESS_ACCESS_TOKEN is required unless --dry-run is used"
            )

        action, result = upsert_post(args.site_id, token, payload)
        print(
            json.dumps(
                {
                    "action": action,
                    "id": result.get("ID"),
                    "status": result.get("status"),
                    "slug": result.get("slug"),
                    "link": result.get("URL"),
                },
                indent=2,
            )
        )
        return 0
    except (OSError, RuntimeError, ValueError, tomllib.TOMLDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
