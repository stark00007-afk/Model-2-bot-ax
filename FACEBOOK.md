# Facebook setup

Posts go to a Facebook **Page** (not a personal profile) through Meta's official Graph API.

1. Create a Facebook Page for the project at facebook.com/pages/create if you don't have one.
2. Go to developers.facebook.com, create an app (type: Business or Other), and keep it in Development mode. As an admin of your own app you can post to your own Page without app review.
3. Open Graph API Explorer (developers.facebook.com/tools/explorer), pick your app, and request a User token with the permissions `pages_manage_posts`, `pages_read_engagement` and `pages_show_list`.
4. Exchange it for a long-lived user token, then ask for your Pages: GET `/me/accounts`. The answer lists each Page with its `id` and `access_token`.
   A Page token made from a long-lived user token does not expire on a timer. Meta's "Access Token Debugger" shows the exact expiry.
5. Save the Page `id` as `FACEBOOK_PAGE_ID` and its `access_token` as `FACEBOOK_PAGE_TOKEN` in GitHub secrets. Never paste them into the repo or chat.
6. If posts fail with an "API version" error, set the repo variable-style secret `FACEBOOK_API_VERSION` to a current version from Meta's docs.
