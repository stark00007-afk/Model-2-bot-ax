"""CLI: python -m agent.main draft | preview | publish | reject <id>"""
import sys
from datetime import datetime
from pathlib import Path

import yaml

from . import draft, preview, publish, search, store


def load_cfg() -> dict:
    return yaml.safe_load(Path("config.yaml").read_text())


def cmd_draft(cfg: dict) -> None:
    used = {i["topic"]["link"] for i in store.all_items()}
    topics = [t for t in search.find_topics(cfg["niche_keywords"]) if t["link"] not in used]
    made = 0
    for topic in topics:
        if made >= cfg["posts_per_run"]:
            break
        texts = draft.draft_posts(topic, cfg)
        if not texts:
            continue
        store.save(
            {
                "id": store.new_id(),
                "created": store.now().isoformat(),
                "topic": topic,
                "status": "pending",
                "previewed_at": None,
                "posts": {p: {"text": t, "status": "pending"} for p, t in texts.items()},
            }
        )
        made += 1
    print(f"drafted {made} item(s)")


def cmd_preview(cfg: dict) -> None:
    for item in store.all_items():
        if item["status"] == "pending" and not item["previewed_at"]:
            preview.send(item, cfg)
            item["previewed_at"] = store.now().isoformat()
            store.save(item)
            print(f"previewed {item['id']}")


def cmd_publish(cfg: dict) -> None:
    for item in store.all_items():
        if item["status"] != "pending" or not item["previewed_at"]:
            continue
        age = (store.now() - datetime.fromisoformat(item["previewed_at"])).total_seconds() / 60
        if age < cfg["min_preview_minutes"]:
            print(f"{item['id']}: preview window not over yet ({age:.0f} min)")
            continue
        for name, post in item["posts"].items():
            if post["status"] != "pending":
                continue
            fn = publish.PUBLISHERS.get(name)
            if cfg["dry_run"]:
                post["status"] = "dry_run"
            elif fn is None:
                post["status"] = "unsupported"
            else:
                try:
                    post["id"] = fn(post["text"])
                    post["status"] = "published"
                except Exception as exc:  # keep going; one platform failing must not block others
                    post["status"] = "failed"
                    post["error"] = type(exc).__name__
        item["status"] = "done"
        store.save(item)
        print(f"processed {item['id']}: " + ", ".join(f"{k}={v['status']}" for k, v in item["posts"].items()))


def cmd_reject(item_id: str) -> None:
    item = store.load(item_id)
    if item["status"] == "pending":
        item["status"] = "rejected"
        store.save(item)
        print(f"rejected {item_id}")
    else:
        print(f"{item_id} is already {item['status']}, nothing to reject")


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cmd = sys.argv[1]
    if cmd == "reject":
        cmd_reject(sys.argv[2])
        return
    if Path("PAUSED").exists():
        print("PAUSED file present, doing nothing")
        return
    cfg = load_cfg()
    {"draft": cmd_draft, "preview": cmd_preview, "publish": cmd_publish}[cmd](cfg)


if __name__ == "__main__":
    main()
