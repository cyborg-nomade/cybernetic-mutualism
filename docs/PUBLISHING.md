# publishing to antinomia imediata

## outcome

Markdown in this repository is the source of truth. A local command or a manual
GitHub Actions run converts one document to HTML and creates or updates a post on
[Antinomia Imediata](https://antinomiaimediata.wordpress.com/).

Publication is never triggered merely by pushing a commit. Both local and CI
workflows default to a WordPress draft, and the GitHub workflow defaults to a
dry run.

## architecture

1. A publishable Markdown file carries TOML front matter.
2. `scripts/publish_wordpress.py` validates the metadata and renders Markdown to
   HTML.
3. The publisher queries WordPress by slug.
4. It creates the post when the slug is new or updates the matching post when it
   already exists.
5. WordPress remains the public presentation layer; Git history remains the
   editorial record.

The integration uses the standard WordPress.com REST endpoint:

```text
https://public-api.wordpress.com/wp/v2/sites/109675820/posts
```

The numeric site ID is public and stable. The access token is secret.

## one-time WordPress authentication

WordPress.com requires an OAuth2 bearer token for authenticated calls to
`public-api.wordpress.com`. Its current official setup process is:

1. Register a WordPress.com application to obtain a client ID and client secret.
2. If the account uses two-factor authentication, create a WordPress.com
   application password.
3. Exchange the client credentials and WordPress credentials/application
   password for an OAuth2 access token.
4. Store only the resulting token in GitHub as the Actions secret
   `WORDPRESS_ACCESS_TOKEN`.

Follow the official documentation rather than committing any credential:

- <https://developer.wordpress.com/docs/api/getting-started/>
- <https://developer.wordpress.com/docs/api/oauth2/>

The repository does not need the WordPress username, account password,
application password, client ID, or client secret after the bearer token has
been obtained.

## configure GitHub Actions

In the GitHub repository:

1. Open **Settings → Secrets and variables → Actions**.
2. Create a repository secret named `WORDPRESS_ACCESS_TOKEN`.
3. Paste the WordPress.com OAuth2 access token.

The site ID is already configured in the workflow and is not sensitive.

## local setup

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Validate and preview the WordPress payload without credentials:

```bash
.venv/bin/python scripts/publish_wordpress.py MANIFESTO.md --dry-run
```

Create or update a WordPress draft:

```bash
export WORDPRESS_ACCESS_TOKEN="..."
.venv/bin/python scripts/publish_wordpress.py MANIFESTO.md
```

Publish immediately only after reviewing the draft or dry-run output:

```bash
.venv/bin/python scripts/publish_wordpress.py MANIFESTO.md --status publish
```

The `WORDPRESS_SITE_ID` environment variable can override the configured site
ID if this tool is later reused for another site.

## GitHub Actions procedure

1. Open **Actions → Publish to WordPress → Run workflow**.
2. Enter the repository-relative Markdown path.
3. Keep `draft` selected for an editorial preview.
4. Keep **Dry run** enabled for the first run.
5. Inspect the action log.
6. Run again with **Dry run** disabled to create the draft.
7. Review the draft in WordPress.
8. When ready, run with status `publish` and **Dry run** disabled.

Using a stable slug makes subsequent runs update the same post.

## recovery and failure handling

- A failed API request does not modify the Markdown source.
- If rendering is wrong, fix the Markdown and rerun with the same slug.
- If the wrong status was selected, change it in WordPress or rerun with the
  intended status.
- If a token is exposed, revoke it in WordPress.com immediately and replace the
  GitHub secret.
- Do not change a published post's slug merely to revise its title; doing so
  creates a second post instead of updating the first.
