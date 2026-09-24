#!/usr/bin/env python3
"""Content-hash state for idempotent WeChat draft creation.

This script never handles credentials or uploads. It only remembers the last
successfully created draft for an article-plus-assets fingerprint.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolved_file(value: str, label: str) -> Path:
    path = Path(value).expanduser().resolve()
    if not path.is_file():
        raise ValueError(f"{label} is not a readable file: {path}")
    return path


def build_manifest(article_value: str, asset_values: list[str]) -> dict[str, Any]:
    article = resolved_file(article_value, "article")
    assets = [resolved_file(value, "asset") for value in asset_values]
    entries = [{"path": str(article), "sha256": sha256_file(article)}]
    entries.extend({"path": str(asset), "sha256": sha256_file(asset)} for asset in assets)

    digest = hashlib.sha256()
    for entry in entries:
        digest.update(entry["path"].encode("utf-8"))
        digest.update(b"\0")
        digest.update(entry["sha256"].encode("ascii"))
        digest.update(b"\0")
    return {"fingerprint": digest.hexdigest(), "article": entries[0], "assets": entries[1:]}


def load_state(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def emit(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    def common_arguments(command: argparse.ArgumentParser) -> None:
        command.add_argument("--state", required=True, help="Path to state JSON")
        command.add_argument("--article", required=True, help="Final article HTML")
        command.add_argument("--asset", action="append", default=[], help="Cover or inline asset; repeat as needed")

    check = subparsers.add_parser("check", help="Check whether this exact draft was already created")
    common_arguments(check)
    record = subparsers.add_parser("record", help="Record a successful draft creation")
    common_arguments(record)
    record.add_argument("--media-id", required=True, help="media_id returned by WeChat draft/add")

    args = parser.parse_args()
    try:
        manifest = build_manifest(args.article, args.asset)
        state_path = Path(args.state).expanduser().resolve()
        state = load_state(state_path)
    except ValueError as error:
        emit({"status": "invalid_input", "error": str(error)})
        return 2

    if args.command == "check":
        if state and state.get("fingerprint") == manifest["fingerprint"] and state.get("media_id"):
            emit({
                "status": "already_published",
                "fingerprint": manifest["fingerprint"],
                "media_id": state["media_id"],
                "published_at": state.get("published_at"),
            })
        else:
            emit({"status": "needs_publish", "fingerprint": manifest["fingerprint"]})
        return 0

    state_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": 1,
        "fingerprint": manifest["fingerprint"],
        "article": manifest["article"],
        "assets": manifest["assets"],
        "media_id": args.media_id,
        "published_at": datetime.now(timezone.utc).isoformat(),
    }
    state_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    emit({"status": "recorded", "fingerprint": manifest["fingerprint"], "media_id": args.media_id})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
