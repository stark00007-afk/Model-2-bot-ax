# Social agent

Twice a day this repo searches niche news, drafts posts with Claude, previews them in Discord, and posts them 30 minutes later unless you reject them.

## How a day works

| Time (IST) | Step | What happens |
|---|---|---|
| 07:30 / 17:30 | draft | Searches Google News for your keywords, writes drafts, saves them in `queue/` |
| 08:30 / 18:30 | preview | Sends each new draft to your Discord channel |
| 09:00 / 19:00 | publish | Posts drafts that were previewed 20+ minutes ago and not rejected |

Your 30 minutes a day: read the two previews, reject anything off, and tweak `STYLE_GUIDE.md` when the tone drifts.

## Setup

1. Push this folder to your public GitHub repo.
2. In the repo go to Settings > Secrets and variables > Actions and add:
   - `ANTHROPIC_API_KEY`
   - `DISCORD_WEBHOOK_URL` (Discord: channel settings > Integrations > Webhooks)
   - `X_API_KEY`, `X_API_SECRET`, `X_ACCESS_TOKEN`, `X_ACCESS_SECRET` (X developer portal, app with read and write permission)
   - `LINKEDIN_ACCESS_TOKEN`, `LINKEDIN_PERSON_URN` (see LINKEDIN.md; the token expires about every 60 days)
   - `FACEBOOK_PAGE_ID`, `FACEBOOK_PAGE_TOKEN` (see FACEBOOK.md)
3. Settings > Actions > General > Workflow permissions: choose "Read and write permissions".
4. Edit `config.yaml` (keywords, platforms). Leave `dry_run: true` first.
5. Run the **Agent** workflow by hand: draft, then preview. Check Discord.
6. When the previews look right, set `dry_run: false`.

## Controls

- **Reject a draft:** run the **Reject** workflow and paste the draft id from the Discord message. This works from the GitHub mobile app too.
- **Edit a draft:** change the text in `queue/<id>.json` before the publish step.
- **Kill switch:** add an empty file named `PAUSED` to the repo root. Every step stops until you delete it.

## Public repo warnings

- Drafts in `queue/` are public, including rejected ones. Do not put anything private in the style guide or config.
- Secrets live only in GitHub Actions secrets. Never paste keys into files or issues.
- Search results are untrusted text. The drafting prompt tells Claude to treat headlines as topics only, but keep the preview step on until you trust the output.

## Status

- Working: search, drafting, Discord preview, reject, X (paused in config), LinkedIn and Facebook publishing (LinkedIn and Facebook untested against the live APIs), dry-run, kill switch.
- Not built yet: Instagram publisher . Snapchat has no posting API, so it stays manual. Platforms marked `enabled: false` in `config.yaml` are skipped.
