# Marco Public Package Design

## Goal

Publish the locally verified cream French bulldog Codex pet as a public GitHub repository named `codex-pet-marco`. The pet's package identity is `marco` and its display name is `Marco`.

## Repository contents

- `pet/pet.json`: Codex pet manifest with ID `marco`.
- `pet/spritesheet.webp`: the verified 1536 x 1872 transparent cream spritesheet.
- `install.sh`: macOS/Linux installer that downloads to a temporary directory, verifies SHA-256 checksums, backs up an existing Marco installation, and installs into `${CODEX_HOME:-$HOME/.codex}/pets/marco`.
- `SHA256SUMS`: hashes for the two package files.
- `scripts/validate_pet.py`: dependency-free validation of manifest fields, RIFF/WebP dimensions, alpha-capable spritesheet format, and checksums.
- `tests/test_validate_pet.py`: focused validator tests using the repository package.
- `README.md`: preview, install and manual-install instructions, restart/refresh guidance, integrity caveat, and provenance.

## Publication

Create `zzzhouzhenzz/codex-pet-marco` as a public GitHub repository with `main` as the default branch. The README will offer a reviewable one-command installer using the raw GitHub URL.

GitHub publication does not register the pet with the separate `codex-pets.net` service, so the repository will not claim that `npx codex-pets add marco` works.

## Attribution and licensing

Marco is a cream recolor of Frankie, published by Arty on `codex-pets.net`. The README will link to the upstream listing and describe the modification. Because the upstream package exposes no license, this repository will not add a license or imply rights beyond attribution.

## Verification gates

- Manifest ID, display name, sprite path, and kind match the package.
- The spritesheet is 1536 x 1872 WebP with alpha support.
- Package SHA-256 checksums match `SHA256SUMS`.
- The installer passes `sh -n` and uses a temporary staging directory plus backup-before-replace behavior.
- Tests pass before the first commit and again before publication.
- The pushed GitHub repository is public and its default branch resolves to the verified commit.
