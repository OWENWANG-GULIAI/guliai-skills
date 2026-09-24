#!/usr/bin/env python3
"""Normalize TXT, Markdown, or CSV chat exports to a stable JSON envelope."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable


DATE_SPEAKER_RE = re.compile(
    r"^(?P<time>\d{4}[-/.年]\d{1,2}[-/.月]\d{1,2}(?:日)?(?:\s+|\s*T\s*)\d{1,2}:\d{2}(?::\d{2})?)\s+(?P<speaker>\S.+?)\s*$"
)
SPEAKER_TIME_RE = re.compile(r"^(?P<speaker>[^\s:：]{1,40})\s+(?P<time>\d{1,2}:\d{2}(?::\d{2})?)\s*$")
INLINE_RE = re.compile(r"^(?P<speaker>[^\s:：][^:：]{0,39})[：:][ \t]*(?P<message>.+)$")

HEADER_ALIASES = {
    "time": ("time", "时间", "发送时间", "日期"),
    "speaker": ("speaker", "发送人", "昵称", "成员"),
    "message": ("message", "内容", "消息", "正文"),
    "message_type": ("message_type", "类型", "消息类型"),
    "group_name": ("group_name", "group", "群名称", "来源群"),
    "reply_to": ("reply_to", "回复", "回复对象", "引用"),
    "source": ("source", "来源"),
}


def clean(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def find_header(fieldnames: Iterable[str] | None, logical_name: str) -> str | None:
    names = {name.strip(): name for name in fieldnames or [] if name}
    for alias in HEADER_ALIASES[logical_name]:
        if alias in names:
            return names[alias]
    return None


def make_message(
    index: int,
    *,
    group_name: str | None,
    time: str | None,
    speaker: str | None,
    message: str,
    message_type: str | None = "text",
    reply_to: str | None = None,
    source: str | None = "wechat",
    raw_text: str | None = None,
) -> dict[str, Any]:
    return {
        "message_id": f"{index:04d}",
        "group_name": clean(group_name) or "未知",
        "time": clean(time),
        "speaker": clean(speaker) or "未知",
        "message_type": clean(message_type) or "text",
        "message": message.strip(),
        "reply_to": clean(reply_to),
        "source": clean(source) or "wechat",
        "raw_text": (raw_text if raw_text is not None else message).strip(),
    }


def parse_csv(path: Path, group_name: str | None, source: str) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        message_field = find_header(reader.fieldnames, "message")
        if not message_field:
            raise ValueError("CSV 缺少消息列；支持 message/内容/消息/正文")
        fields = {name: find_header(reader.fieldnames, name) for name in HEADER_ALIASES}
        messages: list[dict[str, Any]] = []
        for row in reader:
            content = clean(row.get(message_field))
            if not content:
                continue
            row_group = clean(row.get(fields["group_name"])) if fields["group_name"] else None
            row_source = clean(row.get(fields["source"])) if fields["source"] else None
            messages.append(
                make_message(
                    len(messages) + 1,
                    group_name=group_name or row_group,
                    time=row.get(fields["time"]) if fields["time"] else None,
                    speaker=row.get(fields["speaker"]) if fields["speaker"] else None,
                    message=content,
                    message_type=row.get(fields["message_type"]) if fields["message_type"] else "text",
                    reply_to=row.get(fields["reply_to"]) if fields["reply_to"] else None,
                    source=row_source or source,
                    raw_text=content,
                )
            )
        return messages


def split_blocks(text: str) -> list[str]:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    return [block.strip() for block in re.split(r"\n\s*\n", normalized) if block.strip()]


def parse_text(path: Path, group_name: str | None, source: str) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8-sig")
    messages: list[dict[str, Any]] = []
    for block in split_blocks(text):
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue

        first = lines[0]
        match = DATE_SPEAKER_RE.match(first) or SPEAKER_TIME_RE.match(first)
        if match and len(lines) > 1:
            content = "\n".join(lines[1:]).strip()
            messages.append(
                make_message(
                    len(messages) + 1,
                    group_name=group_name,
                    time=match.group("time"),
                    speaker=match.group("speaker"),
                    message=content,
                    source=source,
                    raw_text=block,
                )
            )
            continue

        inline = INLINE_RE.match(first)
        if inline:
            content_lines = [inline.group("message"), *lines[1:]]
            messages.append(
                make_message(
                    len(messages) + 1,
                    group_name=group_name,
                    time=None,
                    speaker=inline.group("speaker"),
                    message="\n".join(content_lines),
                    source=source,
                    raw_text=block,
                )
            )
            continue

        messages.append(
            make_message(
                len(messages) + 1,
                group_name=group_name,
                time=None,
                speaker=None,
                message="\n".join(lines),
                source=source,
                raw_text=block,
            )
        )
    return messages


def build_quality(messages: list[dict[str, Any]], input_format: str) -> dict[str, Any]:
    missing_time = sum(message["time"] is None for message in messages)
    missing_speaker = sum(message["speaker"] == "未知" for message in messages)
    warnings = []
    if not messages:
        warnings.append("未解析到可用消息")
    if missing_time:
        warnings.append("部分消息缺少时间，时间趋势结论应降低可信度")
    if missing_speaker:
        warnings.append("部分消息缺少发送人，人物与关系结论应降低可信度")
    return {
        "input_format": input_format,
        "message_count": len(messages),
        "missing_time_count": missing_time,
        "missing_speaker_count": missing_speaker,
        "unique_speaker_count": len({m["speaker"] for m in messages if m["speaker"] != "未知"}),
        "warnings": warnings,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="将 TXT、Markdown 或 CSV 微信群聊天记录标准化为 JSON；不会进行语义删减或外部上传。"
    )
    parser.add_argument("--input", required=True, help="输入文件路径（.txt、.md、.markdown、.csv）")
    parser.add_argument("--group-name", help="覆盖输入中的群名称")
    parser.add_argument("--source", default="wechat", help="来源标识，默认 wechat")
    parser.add_argument("--compact", action="store_true", help="输出紧凑 JSON")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    path = Path(args.input).expanduser()
    if not path.is_file():
        print(f"输入文件不存在：{path}", file=sys.stderr)
        return 2

    suffix = path.suffix.lower()
    try:
        if suffix == ".csv":
            messages = parse_csv(path, args.group_name, args.source)
            input_format = "csv"
        elif suffix in {".txt", ".md", ".markdown"}:
            messages = parse_text(path, args.group_name, args.source)
            input_format = suffix.lstrip(".")
        else:
            print("不支持的格式；此脚本支持 TXT、Markdown、CSV。Excel、Word、PDF 请先提取文本。", file=sys.stderr)
            return 2
    except (OSError, UnicodeError, csv.Error, ValueError) as exc:
        print(f"解析失败：{exc}", file=sys.stderr)
        return 2

    envelope = {
        "schema_version": "1.0",
        "group_name": args.group_name or (messages[0]["group_name"] if messages else "未知"),
        "messages": messages,
        "quality": build_quality(messages, input_format),
    }
    indent = None if args.compact else 2
    print(json.dumps(envelope, ensure_ascii=False, indent=indent))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
