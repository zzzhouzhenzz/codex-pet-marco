from pathlib import Path
import json
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_pet import read_webp_info, validate_package


class PackageTests(unittest.TestCase):
    def test_repository_package_is_valid(self):
        self.assertEqual(validate_package(ROOT / "pet"), [])

    def test_spritesheet_dimensions_and_alpha(self):
        self.assertEqual(
            read_webp_info(ROOT / "pet" / "spritesheet.webp"),
            (1536, 2288, True),
        )

    def test_manifest_declares_sprite_version_2(self):
        manifest = json.loads((ROOT / "pet" / "pet.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["spriteVersionNumber"], 2)


class ReadmeTests(unittest.TestCase):
    def test_readme_describes_the_independent_v2_art(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("original character art", readme)

    def test_repository_has_no_legacy_upstream_attribution(self):
        checked_paths = [ROOT / "README.md", *sorted((ROOT / "docs").rglob("*.md"))]
        combined = "\n".join(
            path.read_text(encoding="utf-8") for path in checked_paths
        ).lower()
        forbidden_phrases = ("fran" + "kie", "by ar" + "ty", "recolor" + " of")
        for phrase in forbidden_phrases:
            self.assertNotIn(phrase, combined)


if __name__ == "__main__":
    unittest.main()
