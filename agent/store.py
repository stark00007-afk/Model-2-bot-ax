"""Tiny file-based queue: one JSON file per draft in queue/."""
import json
import re
import secrets
from datetime import datetime, timezone
from pathlib import Path

QUEUE = Path("queue")
ID_RE = re.compile(r"^[0-9]{8}-[0-9]{4}-[a-z0-9]{4}$")


def now() -> datetime:
    return datetime.now(timezone.utc)


def new_id() -> str:
    return now().strftime("%Y%m%d-%H%M-") + secrets.token_hex(2)


def valid_id(item_id: str) -> bool:
    return bool(ID_RE.match(item_id))


def save(item: dict) -> None:
    QUEUE.mkdir(exist_ok=True)
    (QUEUE / f"{item['id']}.json").write_text(json.dumps(item, indent=2, ensure_ascii=False))


def load(item_id: str) -> dict:
    if not valid_id(item_id):
        raise ValueError("invalid draft id")
    return json.loads((QUEUE / f"{item_id}.json").read_text())


def all_items() -> list[dict]:
    if not QUEUE.exists():
        return []
    return [json.loads(p.read_text()) for p in sorted(QUEUE.glob("*.json"))]
