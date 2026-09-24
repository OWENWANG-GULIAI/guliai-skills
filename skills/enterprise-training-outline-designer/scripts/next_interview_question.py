#!/usr/bin/env python3
"""Print one adaptive next discovery question from a Training Brief JSON file."""

import json
import sys
from pathlib import Path

QUESTIONS = [
    ("desired_outcomes", "为了先锁定课程结果，培训结束后你最希望学员实际能够完成什么工作成果或行为？"),
    ("target_learners", "这次培训的学员是谁？请说明岗位、人数，以及他们目前在该主题上的经验或基础。"),
    ("business_problem", "在这些工作中，客户最希望优先改善的真实业务场景或痛点是什么？"),
    ("duration", "这次培训计划安排多长时间？是否已有明确的起止时间或天数？"),
    ("delivery_mode", "培训形式已经确定为线上、线下还是混合吗？"),
    ("practice_design", "是否希望安排实操？若安排，使用统一案例还是学员自己的真实工作内容？"),
    ("available_materials", "客户是否可以提供脱敏后的案例、模板、制度、旧课件或其他真实材料？"),
    ("constraints", "是否有设备、软件、保密、合规或组织协同方面的限制需要提前纳入设计？"),
]


def has_value(value):
    return value not in (None, "", [], {})


def main():
    if len(sys.argv) != 2:
        print("Usage: python next_interview_question.py <brief.json>")
        raise SystemExit(2)
    path = Path(sys.argv[1])
    try:
        brief = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[ERROR] Cannot read Training Brief: {exc}")
        raise SystemExit(2)
    if not isinstance(brief, dict):
        print("[ERROR] Training Brief must be a JSON object.")
        raise SystemExit(2)

    for field, question in QUESTIONS:
        if not has_value(brief.get(field)):
            print(f"[STATE] discovery\n[FIELD] {field}\n[QUESTION] {question}")
            return
    print("[STATE] brief_confirmation\n[OK] Core discovery is complete. Present the Course Requirement Confirmation Sheet.")


if __name__ == "__main__":
    main()
