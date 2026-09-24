#!/usr/bin/env python3
"""Deterministic operations for the GULIAI daily-signature Skill."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Callable
from zoneinfo import ZoneInfo


BASELINE_WIDTH = 1024
BASELINE_HEIGHT = 1536
WEEKDAYS_ZH = ("星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日")
DEFAULT_CONFIG = Path(__file__).resolve().parent.parent / "state" / "local-config.json"


class ValidationError(ValueError):
    """Raised when an artifact cannot be safely published."""


def resolve_target_date(intent: str, today: date | None = None) -> dict[str, str]:
    normalized = intent.strip().lower()
    current = today or date.today()
    offsets = {
        "today": 0,
        "今天": 0,
        "tomorrow": 1,
        "明天": 1,
        "yesterday": -1,
        "昨天": -1,
    }
    if normalized in offsets:
        target = current + timedelta(days=offsets[normalized])
    else:
        candidate = normalized.replace(".", "-").replace("/", "-")
        try:
            target = datetime.strptime(candidate, "%Y-%m-%d").date()
        except ValueError as exc:
            raise ValidationError(f"无法识别日期：{intent}") from exc
    return {
        "date": target.isoformat(),
        "date_display": target.strftime("%Y.%m.%d"),
        "weekday": WEEKDAYS_ZH[target.weekday()],
    }


def visible_char_count(text: str) -> int:
    return len(re.sub(r"\s+", "", text))


def validate_copy_text(text: str) -> dict[str, int]:
    content = text.lstrip("\ufeff").strip()
    if not content:
        raise ValidationError("朋友圈文案为空")
    lines = content.splitlines()
    if content.startswith("---"):
        raise ValidationError("朋友圈文案不能包含 YAML Frontmatter")
    if any(line.lstrip().startswith("#") for line in lines):
        raise ValidationError("朋友圈文案不能包含 Markdown 标题")
    metadata_pattern = re.compile(r"^(date|weekday|theme|poster|source)\s*:", re.IGNORECASE)
    if any(metadata_pattern.match(line.strip()) for line in lines[:8]):
        raise ValidationError("朋友圈文案不能包含元数据")
    count = visible_char_count(content)
    if not 80 <= count <= 130:
        raise ValidationError(f"朋友圈正文需为 80–130 个可见字符，当前为 {count}")
    paragraphs = [part for part in re.split(r"\n\s*\n", content) if part.strip()]
    if not 2 <= len(paragraphs) <= 5:
        raise ValidationError(f"朋友圈正文需有 2–5 个自然段，当前为 {len(paragraphs)}")
    return {"visible_char_count": count, "paragraph_count": len(paragraphs)}


def scale_placement(
    placement: dict[str, int],
    width: int,
    height: int,
    *,
    baseline_width: int = BASELINE_WIDTH,
    baseline_height: int = BASELINE_HEIGHT,
) -> dict[str, int]:
    x_scale = width / baseline_width
    y_scale = height / baseline_height
    return {
        "x": round(placement["x"] * x_scale),
        "y": round(placement["y"] * y_scale),
        "width": round(placement["width"] * x_scale),
        "height": round(placement["height"] * y_scale),
    }


def _binary(name: str) -> str:
    found = shutil.which(name)
    if found:
        return found
    homebrew = Path("/opt/homebrew/bin") / name
    if homebrew.is_file():
        return str(homebrew)
    raise ValidationError(f"缺少必需命令：{name}")


def _run(command: list[str], *, capture_bytes: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        command,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=not capture_bytes,
    )


def probe_dimensions(path: Path | str) -> tuple[int, int]:
    image_path = Path(path)
    if not image_path.is_file():
        raise ValidationError(f"图片不存在：{image_path}")
    result = _run(
        [
            _binary("ffprobe"),
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height",
            "-of",
            "csv=s=x:p=0",
            str(image_path),
        ]
    )
    try:
        width_text, height_text = result.stdout.strip().split("x", 1)
        return int(width_text), int(height_text)
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"无法读取图片尺寸：{image_path}") from exc


def _rgb_hash(path: Path, video_filter: str) -> str:
    result = _run(
        [
            _binary("ffmpeg"),
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(path),
            "-vf",
            video_filter,
            "-frames:v",
            "1",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "rgb24",
            "-",
        ],
        capture_bytes=True,
    )
    return hashlib.sha256(result.stdout).hexdigest()


def load_config(path: Path | str = DEFAULT_CONFIG) -> dict[str, Any]:
    config_path = Path(path)
    if not config_path.is_file():
        raise ValidationError(f"本地配置不存在：{config_path}")
    config = json.loads(config_path.read_text(encoding="utf-8"))
    required = ("canvas", "portrait", "qr", "logo", "output_directory")
    missing = [key for key in required if key not in config]
    if missing:
        raise ValidationError(f"本地配置缺少字段：{', '.join(missing)}")
    return config


def compose_brand_assets(
    base_path: Path | str,
    output_path: Path | str,
    config: dict[str, Any],
) -> dict[str, str]:
    base = Path(base_path)
    output = Path(output_path)
    qr_path = Path(config["qr"]["path"])
    logo_path = Path(config["logo"]["path"])
    for required in (base, qr_path, logo_path):
        if not required.is_file():
            raise ValidationError(f"素材不存在：{required}")

    width, height = probe_dimensions(base)
    canvas = config.get("canvas", {})
    baseline_width = int(canvas.get("width", BASELINE_WIDTH))
    baseline_height = int(canvas.get("height", BASELINE_HEIGHT))
    if width * 3 != height * 2:
        raise ValidationError(f"底图必须为 2:3，当前为 {width}x{height}")
    qr = scale_placement(
        config["qr"]["placement"],
        width,
        height,
        baseline_width=baseline_width,
        baseline_height=baseline_height,
    )
    logo = scale_placement(
        config["logo"]["placement"],
        width,
        height,
        baseline_width=baseline_width,
        baseline_height=baseline_height,
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    filter_complex = (
        f"[1:v]scale={qr['width']}:{qr['height']}:flags=neighbor[qr];"
        f"[2:v]scale={logo['width']}:{logo['height']}:flags=lanczos[logo];"
        f"[0:v][qr]overlay={qr['x']}:{qr['y']}:format=auto[withqr];"
        f"[withqr][logo]overlay={logo['x']}:{logo['y']}:format=auto"
    )
    _run(
        [
            _binary("ffmpeg"),
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(base),
            "-i",
            str(qr_path),
            "-i",
            str(logo_path),
            "-filter_complex",
            filter_complex,
            "-frames:v",
            "1",
            str(output),
        ]
    )
    output_width, output_height = probe_dimensions(output)
    source_hash = _rgb_hash(
        qr_path,
        f"scale={qr['width']}:{qr['height']}:flags=neighbor",
    )
    poster_hash = _rgb_hash(
        output,
        f"crop={qr['width']}:{qr['height']}:{qr['x']}:{qr['y']}",
    )
    if source_hash != poster_hash:
        output.unlink(missing_ok=True)
        raise ValidationError("合成后的二维码像素与源图不一致")
    return {
        "dimensions": f"{output_width}x{output_height}",
        "source_qr_hash": source_hash,
        "poster_qr_hash": poster_hash,
        "output": str(output),
    }


def validate_package(
    poster_path: Path | str,
    copy_path: Path | str,
    config: dict[str, Any],
) -> dict[str, Any]:
    poster = Path(poster_path)
    copy_file = Path(copy_path)
    if not copy_file.is_file():
        raise ValidationError(f"朋友圈文案不存在：{copy_file}")
    width, height = probe_dimensions(poster)
    expected_width = int(config["canvas"]["width"])
    expected_height = int(config["canvas"]["height"])
    if (width, height) != (expected_width, expected_height):
        raise ValidationError(
            f"海报尺寸应为 {expected_width}x{expected_height}，当前为 {width}x{height}"
        )
    copy_result = validate_copy_text(copy_file.read_text(encoding="utf-8"))
    qr = scale_placement(
        config["qr"]["placement"],
        width,
        height,
        baseline_width=expected_width,
        baseline_height=expected_height,
    )
    qr_path = Path(config["qr"]["path"])
    source_hash = _rgb_hash(qr_path, f"scale={qr['width']}:{qr['height']}:flags=neighbor")
    poster_hash = _rgb_hash(poster, f"crop={qr['width']}:{qr['height']}:{qr['x']}:{qr['y']}")
    if source_hash != poster_hash:
        raise ValidationError("最终海报中的二维码与源图不一致")
    return {
        "dimensions": f"{width}x{height}",
        "copy": copy_result,
        "source_qr_hash": source_hash,
        "poster_qr_hash": poster_hash,
    }


def publish_package(
    staged_poster: Path | str,
    staged_copy: Path | str,
    output_directory: Path | str,
    *,
    replace_func: Callable[[Path | str, Path | str], None] = os.replace,
) -> dict[str, str]:
    poster = Path(staged_poster)
    copy_file = Path(staged_copy)
    output_dir = Path(output_directory)
    if not poster.is_file() or not copy_file.is_file():
        raise ValidationError("待发布的海报和朋友圈文案必须同时存在")
    output_dir.mkdir(parents=True, exist_ok=True)
    final_poster = output_dir / "今日日签海报.png"
    final_copy = output_dir / "朋友圈文案.md"
    backup_dir = Path(tempfile.mkdtemp(prefix=".daily-signature-backup-", dir=output_dir))
    backup_poster = backup_dir / final_poster.name
    backup_copy = backup_dir / final_copy.name
    had_poster = final_poster.is_file()
    had_copy = final_copy.is_file()
    if had_poster:
        shutil.copy2(final_poster, backup_poster)
    if had_copy:
        shutil.copy2(final_copy, backup_copy)
    try:
        replace_func(poster, final_poster)
        replace_func(copy_file, final_copy)
    except Exception:
        if had_poster:
            os.replace(backup_poster, final_poster)
        else:
            final_poster.unlink(missing_ok=True)
        if had_copy:
            os.replace(backup_copy, final_copy)
        else:
            final_copy.unlink(missing_ok=True)
        raise
    finally:
        shutil.rmtree(backup_dir, ignore_errors=True)
    return {"poster": str(final_poster), "copy": str(final_copy)}


def write_local_config(args: argparse.Namespace) -> dict[str, Any]:
    config_path = Path(args.config)
    paths = {
        "portrait": Path(args.portrait),
        "logo": Path(args.logo),
        "qr": Path(args.qr),
    }
    missing = [str(path) for path in paths.values() if not path.is_file()]
    if missing:
        raise ValidationError(f"素材不存在：{', '.join(missing)}")
    config = {
        "version": 1,
        "timezone": args.timezone,
        "output_directory": str(Path(args.output_dir).expanduser().resolve()),
        "canvas": {"width": BASELINE_WIDTH, "height": BASELINE_HEIGHT},
        "portrait": {"path": str(paths["portrait"].expanduser().resolve())},
        "qr": {
            "path": str(paths["qr"].expanduser().resolve()),
            "placement": {"x": 28, "y": 1260, "width": 224, "height": 224},
        },
        "logo": {
            "path": str(paths["logo"].expanduser().resolve()),
            "placement": {"x": 650, "y": 1323, "width": 320, "height": 213},
        },
    }
    config_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = config_path.with_suffix(config_path.suffix + ".tmp")
    temporary.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, config_path)
    return config


def _json_print(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    resolve = subparsers.add_parser("resolve-date", help="解析今天、明天、昨天或明确日期")
    resolve.add_argument("--when", required=True)
    resolve.add_argument("--today", help="测试或回放用基准日期，格式 YYYY-MM-DD")
    resolve.add_argument("--timezone", default="Asia/Shanghai")

    configure = subparsers.add_parser("configure", help="写入本机私有素材与输出配置")
    configure.add_argument("--config", default=str(DEFAULT_CONFIG))
    configure.add_argument("--portrait", required=True)
    configure.add_argument("--logo", required=True)
    configure.add_argument("--qr", required=True)
    configure.add_argument("--output-dir", required=True)
    configure.add_argument("--timezone", default="Asia/Shanghai")

    compose = subparsers.add_parser("compose", help="把真实二维码和官方 Logo 叠加到底图")
    compose.add_argument("--config", default=str(DEFAULT_CONFIG))
    compose.add_argument("--base", required=True)
    compose.add_argument("--output", required=True)

    validate = subparsers.add_parser("validate", help="检查海报、二维码和纯文案包")
    validate.add_argument("--config", default=str(DEFAULT_CONFIG))
    validate.add_argument("--poster", required=True)
    validate.add_argument("--copy", required=True)

    publish = subparsers.add_parser("publish", help="验证后安全替换每日固定文件")
    publish.add_argument("--config", default=str(DEFAULT_CONFIG))
    publish.add_argument("--poster", required=True)
    publish.add_argument("--copy", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "resolve-date":
            if args.today:
                today = datetime.strptime(args.today, "%Y-%m-%d").date()
            else:
                today = datetime.now(ZoneInfo(args.timezone)).date()
            _json_print(resolve_target_date(args.when, today))
        elif args.command == "configure":
            _json_print(write_local_config(args))
        elif args.command == "compose":
            config = load_config(args.config)
            _json_print(compose_brand_assets(args.base, args.output, config))
        elif args.command == "validate":
            config = load_config(args.config)
            _json_print(validate_package(args.poster, args.copy, config))
        elif args.command == "publish":
            config = load_config(args.config)
            validate_package(args.poster, args.copy, config)
            result = publish_package(args.poster, args.copy, config["output_directory"])
            result["validation"] = validate_package(result["poster"], result["copy"], config)
            _json_print(result)
        return 0
    except (ValidationError, OSError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
