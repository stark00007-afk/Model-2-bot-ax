# Full setup, Facebook first

Do the parts in order. Each part ends with a check so you know it worked. Keep every key in a private notes app and never paste keys into chat, files, or the repo.

## Part 1: Shared basics (needed for every platform, about 30 min)

1. **GitHub repo.** Create a public repo. Unzip `social-agent.zip` and upload everything, including the hidden `.github` folder. Check: the Actions tab shows workflows named Agent and Reject.
2. **Claude API key.** At console.anthropic.com create an API key and add a small credit. This is billed separately from the Claude chat plan.
3. **Discord webhook.** In your server open the channel settings, then Integrations, then Webhooks, then New Webhook, and copy the URL.
4. **Add secrets.** In the repo go to Settings, then Secrets and variables, then Actions, and add `ANTHROPIC_API_KEY` and `DISCORD_WEBHOOK_URL`.
5. **Permissions.** Settings, then Actions, then General, then Workflow permissions: choose Read and write.
6. **Test with no platform keys.** Actions tab, run Agent with `draft`, then run it again with `preview`. Check: a draft appears in Discord. `dry_run` is on, so nothing posts.

## Part 2: Facebook (about 45 min)

1. Create a Facebook **Page** for the project (facebook.com/pages/create). Posts go to the Page, not your personal profile.
2. Go to developers.facebook.com, create an app, and keep it in Development mode. As admin of your own app you can post to your own Page without app review. Meta changes these screens often, so choose the options about managing your Page.
3. Open Graph API Explorer (developers.facebook.com/tools/explorer), choose your app, and generate a User token with `pages_manage_posts`, `pages_read_engagement`, `pages_show_list`.
4. Turn it into a long-lived user token: call `/oauth/access_token?grant_type=fb_exchange_token&client_id=APP_ID&client_secret=APP_SECRET&fb_exchange_token=SHORT_TOKEN`. The App Secret is private. Never put it in the repo.
5. Call `/me/accounts` with the long-lived token. Find your Page and copy its `id` and `access_token`.
6. Add secrets `FACEBOOK_PAGE_ID` and `FACEBOOK_PAGE_TOKEN`.
7. Check: run Agent `draft`, then `preview`. Discord should show a FACEBOOK section.
8. Go live on Facebook: after several good previews, set `dry_run: false` in `config.yaml`. The first real post is the live test, so read the preview carefully.

## Part 3: LinkedIn (about 45 min)

Follow `LINKEDIN.md`. Add `LINKEDIN_ACCESS_TOKEN` and `LINKEDIN_PERSON_URN`. The token expires about every 60 days.

## Part 4: Instagram (not built yet)

Needs an Instagram Business or Creator account linked to your Facebook Page. Every post needs an image, so I will add picture cards first.

## Part 5: X (paused)

Set `enabled: true` for `x` in `config.yaml` once you have the four keys. Add `X_API_KEY`, `X_API_SECRET`, `X_ACCESS_TOKEN`, `X_ACCESS_SECRET`.

## Snapchat

No posting tool exists. Enable it in `config.yaml` only if you want the caption in Discord to post by hand.

## Files in the repo

- `config.yaml`: platforms on or off, keywords, `dry_run`.
- `STYLE_GUIDE.md`: your writing voice.
- `agent/`: search, draft, preview, publish code.
- `.github/workflows/`: the schedule and the Reject button.
- `queue/`: saved drafts (public).
- `FACEBOOK.md`, `LINKEDIN.md`, `SETUP.md`: guides.
- `PAUSED`: create an empty file with this name to stop everything.
