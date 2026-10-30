"""Send a draft preview to Discord through a webhook."""
import os

import requests


def send(item: dict, cfg: dict) -> None:
    url = os.environ["DISCORD_WEBHOOK_URL"]
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    reject_link = f"https://github.com/{repo}/actions/workflows/reject.yml" if repo else ""
    mode = "DRY RUN, will not post" if cfg["dry_run"] else "posts in ~30 min unless rejected"

    fields = [
        {"name": p.upper(), "value": post["text"][:900] + ("…" if len(post["text"]) > 900 else ""), "inline": False}
        for p, post in item["posts"].items()
    ]
    embed = {
        "title": f"Preview: {item['topic']['title'][:200]}",
        "url": item["topic"]["link"],
        "description": f"Draft `{item['id']}`\n{mode}\nTo reject: run the Reject workflow with this id\n{reject_link}",
        "fields": fields,
        "color": 0xF5A623,
    }
    r = requests.post(url, json={"embeds": [embed]}, timeout=20)
    r.raise_for_status()
