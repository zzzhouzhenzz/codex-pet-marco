# Marco Public Package Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a directly installable, validated public GitHub package for the cream French bulldog Codex pet Marco.

**Architecture:** Keep the Codex-native package in `pet/`, validate it with one dependency-free Python module, and install it with a reviewable POSIX shell script that verifies repository checksums and backs up an existing installation. GitHub is the canonical source; `codex-pets.net` registration remains out of scope.

**Tech Stack:** Codex pet JSON/WebP package, Python 3 standard library, POSIX shell, Git, GitHub CLI.

## Global Constraints

- Repository: public `zzzhouzhenzz/codex-pet-marco`, default branch `main`.
- Pet identity: ID `marco`, display name `Marco`, kind `animal`.
- Spritesheet: WebP, 1536 x 2288, alpha-capable, with `spriteVersionNumber: 2`.
- Artwork: original Marco v2 character art created from the cream French bulldog photo reference.
- Licensing: add no license unless the repository owner explicitly chooses one.
- Do not claim `npx codex-pets add marco` support.

---

### Task 1: Package and validator

**Files:**
- Create: `pet/pet.json`
- Create: `pet/spritesheet.webp`
- Create: `scripts/validate_pet.py`
- Create: `tests/test_validate_pet.py`
- Create: `SHA256SUMS`

**Interfaces:**
- Produces: `validate_package(package_dir: pathlib.Path) -> list[str]` and a CLI returning 0 on success.

- [ ] **Step 1: Write the failing tests**

```python
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
            (1536, 2288, True),
        )
```

- [ ] **Step 2: Run the tests and verify the validator import fails**

Run: `python -m unittest discover -s tests -v`
Expected: FAIL because `validate_pet` does not exist.

- [ ] **Step 3: Add the Marco manifest and copy the verified spritesheet**

```json
{
  "id": "marco",
  "displayName": "Marco",
  "description": "A cute smiling classic cream French bulldog digital pet.",
  "spritesheetPath": "spritesheet.webp",
  "kind": "animal"
}
```

Copy the approved cool-cream Marco v2 atlas to `pet/spritesheet.webp` without modifying bytes.

- [ ] **Step 4: Implement dependency-free manifest and WebP validation**

Implement `read_webp_info()` for VP8L and VP8X headers, `validate_package()` for the exact Marco manifest contract, and `main()` for CLI output. Reject missing files, wrong identity, wrong dimensions, and spritesheets without alpha.

- [ ] **Step 5: Generate checksums and run the tests**

Run: `shasum -a 256 pet/pet.json pet/spritesheet.webp > SHA256SUMS`

Run: `python -m unittest discover -s tests -v`
Expected: 2 tests pass.

- [ ] **Step 6: Commit**

```bash
git add pet scripts tests SHA256SUMS
git commit -m "feat: package Marco pet"
```

### Task 2: Safe installer and documentation

**Files:**
- Create: `install.sh`
- Create: `README.md`

**Interfaces:**
- Consumes: raw `pet/pet.json`, `pet/spritesheet.webp`, and `SHA256SUMS` from the `main` branch.
- Produces: `${CODEX_HOME:-$HOME/.codex}/pets/marco` plus a timestamped backup when replacing an existing install.

- [ ] **Step 1: Write installer behavior checks**

Use a temporary `CODEX_HOME`, override `MARCO_BASE_URL` with a local `file://` fixture served by Python's HTTP server, run `install.sh`, and assert both files install. Run it again after changing the installed manifest and assert a `marco.backup-*` directory exists.

- [ ] **Step 2: Verify the checks fail because the installer is absent**

Run: `python -m unittest discover -s tests -v`
Expected: FAIL for the installer tests.

- [ ] **Step 3: Implement `install.sh`**

The POSIX shell installer must use `set -eu`, `mktemp -d`, a cleanup trap, `curl -fsSL`, `sha256sum` or `shasum -a 256`, exact checksum matching, backup-before-replace, and a final path plus refresh/restart message. Default base URL:

```text
https://raw.githubusercontent.com/zzzhouzhenzz/codex-pet-marco/main
```

- [ ] **Step 4: Write README**

Include a visible Marco preview, the one-command installer, manual installation, validation command, refresh/restart guidance, checksum caveat, the separation from `codex-pets.net`, and the original-art provenance. Do not add a license badge or license claim.

- [ ] **Step 5: Verify shell syntax and all tests**

Run: `sh -n install.sh`
Expected: exit 0.

Run: `python -m unittest discover -s tests -v`
Expected: all tests pass.

- [ ] **Step 6: Commit**

```bash
git add install.sh README.md tests
git commit -m "feat: add verified Marco installer"
```

### Task 3: Publish and verify GitHub

**Files:**
- Modify: none.

**Interfaces:**
- Produces: public repository `https://github.com/zzzhouzhenzz/codex-pet-marco` with `main` resolving to the local verified commit.

- [ ] **Step 1: Run the full local verification gate**

Run: `python scripts/validate_pet.py && sh -n install.sh && python -m unittest discover -s tests -v && git diff --check && test -z "$(git status --porcelain)"`
Expected: validator success, all tests pass, no whitespace errors, and clean worktree.

- [ ] **Step 2: Create the public repository and push**

```bash
gh repo create zzzhouzhenzz/codex-pet-marco --public --source=. --remote=origin --push --description "Marco, a classic cream French bulldog pet for Codex"
```

- [ ] **Step 3: Verify remote visibility and commit identity**

Run: `gh repo view zzzhouzhenzz/codex-pet-marco --json visibility,defaultBranchRef,url`
Expected: `PUBLIC`, default branch `main`.

Run: `test "$(git rev-parse HEAD)" = "$(git ls-remote origin refs/heads/main | cut -f1)"`
Expected: exit 0.
