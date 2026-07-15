#!/usr/bin/env python3
"""Validate the Marco Codex pet package without third-party dependencies."""

from __future__ import annotations

import json
from pathlib import Path
import sys


EXPECTED_MANIFEST = {
    "id": "marco",
    "displayName": "Marco",
    "spriteVersionNumber": 2,
    "spritesheetPath": "spritesheet.webp",
    "kind": "animal",
}
EXPECTED_SIZE = (1536, 2288)


def read_webp_info(path: Path) -> tuple[int, int, bool]:
    """Return width, height, and alpha support from a WebP container."""
    data = path.read_bytes()
    if len(data) < 20 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        raise ValueError("not a RIFF WebP file")

    offset = 12
    while offset + 8 <= len(data):
        chunk_type = data[offset : offset + 4]
        chunk_size = int.from_bytes(data[offset + 4 : offset + 8], "little")
        payload = offset + 8
        end = payload + chunk_size
        if end > len(data):
            raise ValueError("truncated WebP chunk")

        if chunk_type == b"VP8L":
            if chunk_size < 5 or data[payload] != 0x2F:
                raise ValueError("invalid VP8L header")
            bits = int.from_bytes(data[payload + 1 : payload + 5], "little")
            width = (bits & 0x3FFF) + 1
            height = ((bits >> 14) & 0x3FFF) + 1
            has_alpha = bool((bits >> 28) & 1)
            return width, height, has_alpha

        if chunk_type == b"VP8X":
            if chunk_size < 10:
                raise ValueError("invalid VP8X header")
            flags = data[payload]
            width = int.from_bytes(data[payload + 4 : payload + 7], "little") + 1
            height = int.from_bytes(data[payload + 7 : payload + 10], "little") + 1
            return width, height, bool(flags & 0x10)

        offset = end + (chunk_size & 1)

    raise ValueError("WebP has no supported VP8L or VP8X image header")


def validate_package(package_dir: Path) -> list[str]:
    errors: list[str] = []
    manifest_path = package_dir / "pet.json"
    spritesheet_path = package_dir / "spritesheet.webp"

    if not manifest_path.is_file():
        errors.append("missing pet.json")
    else:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid pet.json: {exc}")
        else:
            for key, expected in EXPECTED_MANIFEST.items():
                if manifest.get(key) != expected:
                    errors.append(
                        f"pet.json {key!r} must be {expected!r}, got {manifest.get(key)!r}"
                    )

    if not spritesheet_path.is_file():
        errors.append("missing spritesheet.webp")
    else:
        try:
            width, height, has_alpha = read_webp_info(spritesheet_path)
        except (OSError, ValueError) as exc:
            errors.append(f"invalid spritesheet.webp: {exc}")
        else:
            if (width, height) != EXPECTED_SIZE:
                errors.append(
                    f"spritesheet.webp must be {EXPECTED_SIZE[0]}x{EXPECTED_SIZE[1]}, "
                    f"got {width}x{height}"
                )
            if not has_alpha:
                errors.append("spritesheet.webp must support alpha transparency")

    return errors


def main() -> int:
    package_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parents[1] / "pet"
    errors = validate_package(package_dir)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Marco pet package is valid: {package_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
