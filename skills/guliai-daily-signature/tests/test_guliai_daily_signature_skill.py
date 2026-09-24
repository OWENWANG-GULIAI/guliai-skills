import importlib.util
import json
import os
import tempfile
import unittest
from argparse import Namespace
from datetime import date
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
OPS_PATH = SKILL_DIR / "scripts" / "daily_signature_ops.py"


def load_ops():
    if not OPS_PATH.is_file():
        raise AssertionError(f"missing implementation: {OPS_PATH}")
    spec = importlib.util.spec_from_file_location("daily_signature_ops", OPS_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_ppm(path: Path, width: int, height: int, pixel):
    path.write_bytes(
        f"P6\n{width} {height}\n255\n".encode("ascii")
        + bytes(pixel) * width * height
    )


class DateResolutionTests(unittest.TestCase):
    def test_tomorrow_resolves_date_and_chinese_weekday(self):
        ops = load_ops()
        result = ops.resolve_target_date("tomorrow", date(2026, 9, 15))
        self.assertEqual(
            result,
            {
                "date": "2026-09-16",
                "date_display": "2026.09.16",
                "weekday": "星期三",
            },
        )

    def test_explicit_date_is_verified_without_trusting_supplied_weekday(self):
        ops = load_ops()
        result = ops.resolve_target_date("2026-09-20", date(2026, 9, 15))
        self.assertEqual(result["weekday"], "星期日")


class CopyValidationTests(unittest.TestCase):
    VALID_COPY = (
        "很多人总想等自己准备得更充分，\n"
        "再去表达、再去行动。\n\n"
        "但真正的能力，并不是在等待中突然出现，\n"
        "而是在一次次真实尝试里慢慢长出来。\n\n"
        "说出来，做出来，听见反馈，再回头打磨。\n\n"
        "每一次行动，都会让模糊的经验更加清晰，\n"
        "也让专业一步步变成可以交付的成果。"
    )

    def test_accepts_publishable_copy_only(self):
        ops = load_ops()
        result = ops.validate_copy_text(self.VALID_COPY)
        self.assertGreaterEqual(result["visible_char_count"], 80)
        self.assertLessEqual(result["visible_char_count"], 130)
        self.assertEqual(result["paragraph_count"], 4)

    def test_rejects_frontmatter_or_heading(self):
        ops = load_ops()
        for invalid in (
            "---\ndate: 2026-09-16\n---\n" + self.VALID_COPY,
            "# 朋友圈文案\n\n" + self.VALID_COPY,
        ):
            with self.subTest(invalid=invalid[:20]):
                with self.assertRaises(ops.ValidationError):
                    ops.validate_copy_text(invalid)


class PlacementAndCompositionTests(unittest.TestCase):
    def test_configure_keeps_default_logo_fully_on_canvas(self):
        ops = load_ops()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            portrait = root / "portrait.ppm"
            logo = root / "logo.ppm"
            qr = root / "qr.ppm"
            for path in (portrait, logo, qr):
                write_ppm(path, 8, 8, (255, 255, 255))

            config = ops.write_local_config(
                Namespace(
                    config=str(root / "state" / "local-config.json"),
                    portrait=str(portrait),
                    logo=str(logo),
                    qr=str(qr),
                    output_dir=str(root / "output"),
                    timezone="Asia/Shanghai",
                )
            )
            placement = config["logo"]["placement"]
            self.assertLessEqual(
                placement["y"] + placement["height"],
                config["canvas"]["height"],
            )

    def test_scales_baseline_placements_proportionally(self):
        ops = load_ops()
        placement = ops.scale_placement(
            {"x": 28, "y": 1260, "width": 224, "height": 224},
            2048,
            3072,
            baseline_width=1024,
            baseline_height=1536,
        )
        self.assertEqual(
            placement,
            {"x": 56, "y": 2520, "width": 448, "height": 448},
        )

    def test_composition_preserves_nearest_neighbor_qr_pixels(self):
        ops = load_ops()
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            base = temp / "base.ppm"
            qr = temp / "qr.ppm"
            logo = temp / "logo.ppm"
            output = temp / "poster.png"
            write_ppm(base, 1024, 1536, (246, 241, 232))
            write_ppm(qr, 8, 8, (0, 0, 0))
            write_ppm(logo, 16, 8, (211, 151, 0))
            config = {
                "canvas": {"width": 1024, "height": 1536},
                "qr": {
                    "path": str(qr),
                    "placement": {"x": 28, "y": 1260, "width": 224, "height": 224},
                },
                "logo": {
                    "path": str(logo),
                    "placement": {"x": 650, "y": 1343, "width": 320, "height": 160},
                },
            }
            result = ops.compose_brand_assets(base, output, config)
            self.assertEqual(result["dimensions"], "1024x1536")
            self.assertEqual(result["source_qr_hash"], result["poster_qr_hash"])
            self.assertTrue(output.is_file())


class PublicationTests(unittest.TestCase):
    def test_failed_second_replace_restores_previous_pair(self):
        ops = load_ops()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            output_dir = root / "output"
            output_dir.mkdir()
            final_poster = output_dir / "今日日签海报.png"
            final_copy = output_dir / "朋友圈文案.md"
            final_poster.write_bytes(b"old-poster")
            final_copy.write_text("old-copy", encoding="utf-8")
            staged_poster = root / "new.png"
            staged_copy = root / "new.md"
            staged_poster.write_bytes(b"new-poster")
            staged_copy.write_text("new-copy", encoding="utf-8")

            calls = 0

            def fail_once_on_second(source, destination):
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError("simulated second replacement failure")
                os.replace(source, destination)

            with self.assertRaises(OSError):
                ops.publish_package(
                    staged_poster,
                    staged_copy,
                    output_dir,
                    replace_func=fail_once_on_second,
                )

            self.assertEqual(final_poster.read_bytes(), b"old-poster")
            self.assertEqual(final_copy.read_text(encoding="utf-8"), "old-copy")


class SkillContractTests(unittest.TestCase):
    def test_layout_contract_reserves_clear_footprints_for_real_assets(self):
        contract_path = SKILL_DIR / "references" / "layout-contract.json"
        self.assertTrue(contract_path.is_file())

        contract = json.loads(contract_path.read_text(encoding="utf-8"))
        self.assertEqual(contract["canvas"], {"width": 1024, "height": 1536})
        self.assertEqual(
            contract["clear_footprints"]["qr"],
            {"x": 0, "y": 1230, "width": 280, "height": 306},
        )
        self.assertEqual(
            contract["clear_footprints"]["logo"],
            {"x": 620, "y": 1315, "width": 404, "height": 221},
        )
        self.assertEqual(
            set(contract["base_forbidden"]),
            {
                "person",
                "hands",
                "clothing",
                "furniture",
                "objects",
                "text",
                "placeholder_blocks",
                "qr_or_logo_artwork",
            },
        )

    def test_skill_has_discoverable_entrypoint_and_required_resources(self):
        required = [
            SKILL_DIR / "SKILL.md",
            SKILL_DIR / "agents" / "openai.yaml",
            SKILL_DIR / "references" / "visual-system.md",
            SKILL_DIR / "references" / "content-sourcing.md",
            SKILL_DIR / "references" / "copy-guide.md",
            SKILL_DIR / "references" / "asset-contract.md",
            SKILL_DIR / "references" / "qa-checklist.md",
            SKILL_DIR / "references" / "layout-contract.json",
            OPS_PATH,
        ]
        missing = [str(path) for path in required if not path.is_file()]
        self.assertEqual(missing, [])

        skill_text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: guliai-daily-signature", skill_text)
        self.assertIn("description: Use when", skill_text)
        self.assertIn("**REQUIRED SUB-SKILL:** Use imagegen", skill_text)

    def test_source_skill_excludes_private_runtime_state_and_assets(self):
        text_files = [
            path
            for path in SKILL_DIR.rglob("*")
            if path.is_file() and path.suffix in {".md", ".py", ".yaml", ".json"}
        ]
        forbidden = (
            str(Path("/") / "Users") + "/",
            "\\" + "Users" + "\\",
            "local-config.json" + ".tmp",
        )
        matches = [
            str(path)
            for path in text_files
            if any(value in path.read_text(encoding="utf-8") for value in forbidden)
        ]
        self.assertEqual(matches, [])
        self.assertFalse((SKILL_DIR / "state").exists())
        image_assets = sorted(
            path.relative_to(SKILL_DIR).as_posix()
            for path in SKILL_DIR.rglob("*")
            if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg"}
        )
        self.assertEqual(
            image_assets,
            [
                "assets/guliai-logo-on-light.png",
                "examples/monday-restart.png",
                "examples/tuesday-reframe.png",
                "examples/wednesday-action.png",
            ],
        )


if __name__ == "__main__":
    unittest.main()
