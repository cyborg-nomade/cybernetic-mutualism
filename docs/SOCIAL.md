# social distribution runbook

## current capability

| Destination | Automatic route | Mobile setup | Cost |
| --- | --- | --- | --- |
| Facebook Page | Jetpack Social | Jetpack app | Included |
| X | RSS → IFTTT → X | IFTTT app | IFTTT Pro |

WordPress.com no longer supports automatic posting to X through Jetpack Social.
The blog's public RSS feed is therefore the cleanest trigger independent of how
a post was published:

<https://antinomiaimediata.wordpress.com/feed/>

Official references:

- [WordPress.com automatic social posting](https://wordpress.com/support/post-automatically-to-social-media/)
- [Jetpack mobile social setup](https://apps.wordpress.com/support/mobile/posts-and-pages/share-posts-and-products-to-social-media/)
- [IFTTT service limits and X availability](https://help.ifttt.com/hc/en-us/articles/1260803229749-IFTTT-Service-Rate-Limits)

## connect the Facebook Page on mobile

1. Open the Jetpack app and select **Antinomia Imediata** under **My Site**.
2. Tap **More → Social**.
3. Select **Facebook** and tap **Connect**.
4. Complete Facebook login in the browser sheet that opens.
5. Select the intended Facebook Page, not a personal timeline.
6. Approve the permissions required to create Page posts.
7. Return to Jetpack and confirm that the Page appears as connected.
8. If offered, enable **Mark the connection as shared** so API publications and
   other authorised WordPress users can use the connection.

On this WordPress.com site, new posts are auto-shared after a connection is
active. A post published before connection will not be auto-shared retroactively;
share or reshare the manifesto manually.

## connect X through IFTTT on mobile

X posting is a paid IFTTT action. Confirm the current Pro price before
subscribing.

1. Install and open the IFTTT mobile app.
2. Create an Applet and choose **RSS Feed** as **If This**.
3. Choose **New feed item**.
4. Enter `https://antinomiaimediata.wordpress.com/feed/` as the feed URL.
5. Choose **X/Twitter** as **Then That**.
6. Select **Post a tweet** and authorise the intended X account.
7. Compose the action from IFTTT ingredients, for example:

   ```text
   [Entry title]

   [Entry URL]
   ```

8. Save and enable the Applet.
9. Enable IFTTT failure notifications so expired X authorisation is visible.

IFTTT triggers only for feed items first observed after the Applet is enabled.
It will not automatically post the already-published manifesto.

## verification

For the next new post:

1. Publish a WordPress draft first and confirm its rendering.
2. Publish the post.
3. Confirm the Facebook Page post and its link preview.
4. Check the IFTTT activity log and resulting X post.
5. Record failures before manually retrying, to avoid duplicates.

Do not test by repeatedly reverting the same WordPress post to draft and
republishing it; Jetpack Social deliberately avoids auto-sharing republished
posts.
