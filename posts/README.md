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

Supported fields are:

- `title` — required.
- `slug` — required; also serves as the stable update key.
- `status` — optional, defaults to `draft`.
- `excerpt` — optional.
- `category_ids` — optional list of existing numeric WordPress category IDs.
- `tag_ids` — optional list of existing numeric WordPress tag IDs.

Use the same slug for later revisions. The publisher updates the existing
WordPress post instead of creating a duplicate.
