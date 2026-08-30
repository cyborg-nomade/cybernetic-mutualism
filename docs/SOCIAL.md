# social distribution runbook

## current procedure

| Destination | Procedure | Cost |
| --- | --- | --- |
| Facebook Page | Jetpack Social, requested by the repository publisher | Included |
| X | Share the published post manually from a phone | Free |

WordPress.com supports automatic sharing to a Facebook Page but does not
currently support automatic posting to X. The project will not use a paid IFTTT
subscription merely to bridge that gap.

Official references:

- [WordPress.com automatic social posting](https://wordpress.com/support/post-automatically-to-social-media/)
- [Jetpack mobile social setup](https://apps.wordpress.com/support/mobile/posts-and-pages/share-posts-and-products-to-social-media/)
- [Jetpack Social troubleshooting](https://jetpack.com/support/jetpack-social/troubleshooting-jetpack-social/)
- [WordPress.com post API and its `publicize` control](https://developer.wordpress.com/docs/api/1/post/sites/%24site/posts/new/)

## Facebook: connection and repository publications

The Facebook Page is already connected. The manifesto nevertheless failed to
appear because the first version of the repository publisher used the Core-style
WordPress endpoint without explicitly requesting Jetpack Social distribution.
The publisher now uses WordPress.com's documented `publicize` control.

It requests Facebook sharing only when:

- a new post is created directly with status `publish`; or
- a repository-created draft is changed to `publish` for the first time.

Edits to an already-published post explicitly suppress social sharing, avoiding
duplicate Facebook posts. The manifesto should not be used to retest this
because it has already been published and shared manually; use the next new post.

On a phone, confirm the connection once in the Jetpack app:

1. Open **My Site → More → Social** for **Antinomia Imediata**.
2. Expand the Facebook connection and confirm that it names the intended Page.
3. If the option is available, enable **Mark the connection as shared**. This is
   important when an API or a WordPress user other than the connection owner
   performs the publication.
4. If the next new post still fails, disconnect and reconnect Facebook there,
   approve Page-posting permissions again, and test with a genuinely new post.

## X: free manual procedure on mobile

After the WordPress post and its Facebook share have been verified:

1. Open the published post in the Jetpack app or a mobile browser.
2. Use **Share** and select X. If X is absent from the share sheet, copy the
   canonical post URL and open X directly.
3. Add a short, post-specific introduction rather than sharing only the title.
4. Paste or retain the canonical URL and wait for its preview to appear.
5. Publish from the intended X account.

A useful default composition is:

```text
[One sentence stating the post's central claim or question.]

[Post title]
[Canonical URL]
```

This manual step is intentionally part of the editorial pass: it allows the X
message to fit the argument and avoids maintaining a brittle paid integration.
If WordPress.com restores native X support later, the procedure can be revisited.

## verification for the next new post

1. Run the repository workflow with `draft` first and review the rendered post.
2. Run it once with `publish`.
3. Confirm the post on the Facebook Page and inspect its link preview.
4. Share the post to X manually.
5. If Facebook is absent, record the WordPress post URL and publication time,
   then check the shared-connection setting before reconnecting Facebook.

Do not test by repeatedly reverting the same WordPress post to draft and
republishing it. Jetpack Social deliberately avoids auto-sharing republished
posts, and the repository publisher also suppresses sharing for an existing
published post.
