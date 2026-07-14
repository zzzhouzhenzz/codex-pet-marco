from pathlib import Path
import os
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class InstallerTests(unittest.TestCase):
    def run_installer(self, codex_home: Path) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["CODEX_HOME"] = str(codex_home)
        env["MARCO_BASE_URL"] = ROOT.as_uri()
        return subprocess.run(
            ["sh", str(ROOT / "install.sh")],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_installs_and_backs_up_existing_marco(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            codex_home = Path(temporary_directory) / "codex"

            first = self.run_installer(codex_home)
            self.assertEqual(first.returncode, 0, first.stderr)

            installed = codex_home / "pets" / "marco"
            self.assertEqual(
                (installed / "pet.json").read_bytes(),
                (ROOT / "pet" / "pet.json").read_bytes(),
            )
            self.assertEqual(
                (installed / "spritesheet.webp").read_bytes(),
                (ROOT / "pet" / "spritesheet.webp").read_bytes(),
            )

            (installed / "pet.json").write_text("old installation\n", encoding="utf-8")
            second = self.run_installer(codex_home)
            self.assertEqual(second.returncode, 0, second.stderr)

            backups = list((codex_home / "pets").glob("marco.backup-*"))
            self.assertEqual(len(backups), 1)
            self.assertEqual(
                (backups[0] / "pet.json").read_text(encoding="utf-8"),
                "old installation\n",
            )


if __name__ == "__main__":
    unittest.main()
