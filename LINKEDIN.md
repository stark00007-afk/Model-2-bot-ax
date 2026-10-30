# LinkedIn setup

Posts go to your personal profile through LinkedIn's official API.

1. Go to https://www.linkedin.com/developers/apps and click Create app. LinkedIn requires a Company Page to link the app; create a free one if you don't have one.
2. On the app's Products tab, request **Share on LinkedIn** and **Sign In with LinkedIn using OpenID Connect**. Both are self-serve.
3. On the Auth tab, add a redirect URL (for example https://localhost/callback). Copy the Client ID and Client Secret into a private notes app. Never put them in the repo.
4. Open this address in your browser, replacing the CAPS parts (the scope list has spaces, so use %20):
   https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=CLIENT_ID&redirect_uri=REDIRECT_URL&scope=openid%20profile%20w_member_social
   Approve it. The browser lands on your redirect URL with `?code=...` at the end. Copy that code. It expires in a few minutes.
5. Exchange the code for a token (run on your own computer, not in the repo):
   curl -X POST https://www.linkedin.com/oauth/v2/accessToken -d grant_type=authorization_code -d code=CODE -d redirect_uri=REDIRECT_URL -d client_id=CLIENT_ID -d client_secret=CLIENT_SECRET
   Copy `access_token` from the answer. This is `LINKEDIN_ACCESS_TOKEN`.
6. Get your person id:
   curl -H "Authorization: Bearer ACCESS_TOKEN" https://api.linkedin.com/v2/userinfo
   Take the `sub` value and save `urn:li:person:SUB_VALUE` as `LINKEDIN_PERSON_URN`.

The token lasts about 60 days. When posts start failing with "failed" in `queue/`, repeat steps 4 and 5 and update the secret.
