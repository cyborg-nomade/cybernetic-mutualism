from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import call, patch

from scripts.publish_wordpress import (
    build_payload,
    load_document,
    render_html,
    upsert_post,
)


class PublishWordPressTests(unittest.TestCase):
    def write_document(self, contents: str) -> Path:
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        path = Path(temporary_directory.name) / "post.md"
        path.write_text(contents, encoding="utf-8")
        return path

    def test_load_document_parses_toml_front_matter(self) -> None:
        path = self.write_document(
            """+++
title = "a title"
slug = "a-title"
status = "draft"
+++

# hello
"""
        )

        document = load_document(path)

        self.assertEqual(document.metadata["title"], "a title")
        self.assertEqual(document.metadata["slug"], "a-title")
        self.assertIn("# hello", document.markdown_body)

    def test_build_payload_renders_html_and_overrides_status(self) -> None:
        path = self.write_document(
            """+++
title = "a title"
slug = "a-title"
status = "draft"
category_ids = [1, 2]
+++

This is **important**.
"""
        )

        payload = build_payload(load_document(path), "publish")

        self.assertEqual(payload["status"], "publish")
        self.assertTrue(payload["publicize"])
        self.assertEqual(payload["categories"], [1, 2])
        self.assertIn("<strong>important</strong>", payload["content"])

    def test_draft_payload_does_not_request_social_sharing(self) -> None:
        path = self.write_document(
            """+++
title = "a title"
slug = "a-title"
status = "draft"
+++

text
"""
        )

        self.assertFalse(build_payload(load_document(path))["publicize"])

    def test_invalid_slug_is_rejected(self) -> None:
        path = self.write_document(
            """+++
title = "a title"
slug = "Not A Slug"
+++

text
"""
        )

        with self.assertRaisesRegex(ValueError, "slug"):
            load_document(path)

    def test_render_html_supports_footnotes(self) -> None:
        rendered = render_html("statement[^1]\n\n[^1]: source")

        self.assertIn("footnote", rendered)
        self.assertIn("source", rendered)

    @patch("scripts.publish_wordpress.api_request")
    def test_new_published_post_requests_social_sharing(self, request) -> None:
        payload = {
            "title": "a title",
            "slug": "a-title",
            "status": "publish",
            "content": "<p>text</p>",
            "publicize": True,
        }
        created = {"ID": 42, "status": "publish", "slug": "a-title"}
        request.side_effect = [None, created]

        action, result = upsert_post("123", "token", payload)

        self.assertEqual(action, "created")
        self.assertEqual(result, created)
        self.assertEqual(
            request.call_args_list,
            [
                call(
                    "GET",
                    "https://public-api.wordpress.com/rest/v1.1/sites/123/posts/slug:a-title?context=edit",
                    "token",
                    not_found_ok=True,
                ),
                call(
                    "POST",
                    "https://public-api.wordpress.com/rest/v1.1/sites/123/posts/new",
                    "token",
                    payload,
                ),
            ],
        )

    @patch("scripts.publish_wordpress.api_request")
    def test_editing_published_post_suppresses_duplicate_sharing(self, request) -> None:
        payload = {
            "title": "a title",
            "slug": "a-title",
            "status": "publish",
            "content": "<p>revision</p>",
            "publicize": True,
        }
        existing = {"ID": 42, "status": "publish", "slug": "a-title"}
        updated = existing | {"content": "<p>revision</p>"}
        request.side_effect = [existing, updated]

        action, result = upsert_post("123", "token", payload)

        self.assertEqual(action, "updated")
        self.assertEqual(result, updated)
        update_payload = request.call_args_list[1].args[3]
        self.assertFalse(update_payload["publicize"])

    @patch("scripts.publish_wordpress.api_request")
    def test_publishing_existing_draft_requests_social_sharing(self, request) -> None:
        payload = {
            "title": "a title",
            "slug": "a-title",
            "status": "publish",
            "content": "<p>text</p>",
            "publicize": True,
        }
        existing = {"ID": 42, "status": "draft", "slug": "a-title"}
        published = existing | {"status": "publish"}
        request.side_effect = [existing, published]

        action, _ = upsert_post("123", "token", payload)

        self.assertEqual(action, "updated")
        update_payload = request.call_args_list[1].args[3]
        self.assertTrue(update_payload["publicize"])


if __name__ == "__main__":
    unittest.main()
