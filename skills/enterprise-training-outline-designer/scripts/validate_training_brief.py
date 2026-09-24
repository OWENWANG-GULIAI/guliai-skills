#!/usr/bin/env python3
"""Report the next permitted state for an enterprise-training Training Brief JSON."""

import json
import sys
from pathlib import Path

CORE_FIELDS = {
    "desired_outcomes": "培训后希望实现的成果",
    "target_learners": "学员对象与基础",
    "business_problem": "优先解决的真实业务问题",
    "duration": "培训时长",
}
DISCOVERY_FIELDS = {
    "delivery_mode": "线上、线下或混合形式",
    "practice_design": "实操方式",
    "available_materials": "可使用的真实案例、模板或材料",
    "constraints": "设备、合规或保密等约束",
}
DELIVERY_FIELDS = {
    "output_format": "输出形式",
    "branding_confirmed": "是否需要品牌化",
    "template_confirmed": "是否有现成模板",
}


def has_value(value):
    return value not in (None, "", [], {})


def read_payload(path_text):
    path = Path(path_text)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"[ERROR] File not found: {path}")
        raise SystemExit(2)
    except json.JSONDecodeError as exc:
        print(f"[ERROR] Invalid JSON: {exc}")
        raise SystemExit(2)
    if not isinstance(payload, dict):
        print("[ERROR] Training Brief must be a JSON object.")
        raise SystemExit(2)
    return path, payload


def labels_missing(payload, fields):
    return [label for key, label in fields.items() if not has_value(payload.get(key))]


def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_training_brief.py <brief.json>")
        raise SystemExit(2)

    path, payload = read_payload(sys.argv[1])
    missing_core = labels_missing(payload, CORE_FIELDS)
    missing_discovery = labels_missing(payload, DISCOVERY_FIELDS)
    brief_confirmed = payload.get("brief_confirmed") is True
    missing_delivery = labels_missing(payload, DELIVERY_FIELDS)

    print(f"[OK] Parsed Training Brief: {path.name}")
    if missing_core:
        print("[STATE] discovery")
        print("[BLOCK] Do not generate a course outline. Ask exactly one next question.")
        print(f"[NEXT GAP] {missing_core[0]}")
        return

    if not brief_confirmed:
        print("[STATE] brief_confirmation")
        print("[BLOCK] Show the Course Requirement Confirmation Sheet and wait for user confirmation.")
        if missing_discovery:
            print("[NOTE] These optional fields remain unavailable: " + "；".join(missing_discovery))
        return

    if missing_delivery:
        print("[STATE] delivery_confirmation")
        print("[BLOCK] Do not create Word or HTML files yet.")
        print(f"[NEXT GAP] {missing_delivery[0]}")
        return

    print("[STATE] generation")
    print("[OK] The brief and delivery choices are confirmed; generate only the selected output format.")


if __name__ == "__main__":
    main()
