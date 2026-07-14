from pathlib import Path
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
            (1536, 1872, True),
        )


if __name__ == "__main__":
    unittest.main()
