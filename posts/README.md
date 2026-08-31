# posts

This directory contains publishable essays whose canonical source is Markdown.

Each post starts with TOML front matter delimited by `+++`:

```markdown
+++
title = "example title"
slug = "example-title"
status = "draft"
excerpt = "optional summary"
+++

# example title

post text goes here.
```

keep the level-one heading in the Markdown source so the document remains
self-contained in the repository. the publisher omits a leading `<h1>` from the
WordPress body because WordPress renders the front-matter title separately.

Supported fields are:

- `title` — required.
- `slug` — required; also serves as the stable update key.
- `status` — optional, defaults to `draft`.
- `excerpt` — optional.
- `category_ids` — optional list of existing numeric WordPress category IDs.
- `tag_ids` — optional list of existing numeric WordPress tag IDs.

Use the same slug for later revisions. The publisher updates the existing
WordPress post instead of creating a duplicate.
