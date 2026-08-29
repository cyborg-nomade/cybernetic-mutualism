from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.publish_wordpress import build_payload, load_document, render_html


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
        self.assertEqual(payload["categories"], [1, 2])
        self.assertIn("<strong>important</strong>", payload["content"])

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


if __name__ == "__main__":
    unittest.main()
