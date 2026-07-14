#!/bin/sh
set -eu

base_url=${MARCO_BASE_URL:-https://raw.githubusercontent.com/zzzhouzhenzz/codex-pet-marco/main}
base_url=${base_url%/}
codex_home=${CODEX_HOME:-"$HOME/.codex"}
pets_dir="$codex_home/pets"
destination="$pets_dir/marco"
temporary_directory=$(mktemp -d "${TMPDIR:-/tmp}/marco-install.XXXXXX")

cleanup() {
  rm -rf "$temporary_directory"
}
trap cleanup EXIT HUP INT TERM

download() {
  remote_path=$1
  local_path=$2
  curl -fsSL "$base_url/$remote_path" -o "$local_path"
}

hash_file() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1" | awk '{print $1}'
  elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$1" | awk '{print $1}'
  else
    printf '%s\n' "Marco installer requires sha256sum or shasum." >&2
    return 1
  fi
}

expected_hash() {
  package_path=$1
  awk -v package_path="$package_path" '$2 == package_path {print $1}' \
    "$temporary_directory/SHA256SUMS"
}

verify_download() {
  package_path=$1
  local_path=$2
  expected=$(expected_hash "$package_path")
  actual=$(hash_file "$local_path")
  if [ -z "$expected" ] || [ "$expected" != "$actual" ]; then
    printf '%s\n' "Checksum verification failed for $package_path." >&2
    return 1
  fi
}

download SHA256SUMS "$temporary_directory/SHA256SUMS"
download pet/pet.json "$temporary_directory/pet.json"
download pet/spritesheet.webp "$temporary_directory/spritesheet.webp"

verify_download pet/pet.json "$temporary_directory/pet.json"
verify_download pet/spritesheet.webp "$temporary_directory/spritesheet.webp"

staged="$temporary_directory/marco"
mkdir -p "$staged" "$pets_dir"
cp "$temporary_directory/pet.json" "$staged/pet.json"
cp "$temporary_directory/spritesheet.webp" "$staged/spritesheet.webp"

if [ -e "$destination" ]; then
  backup="${destination}.backup-$(date +%Y%m%d-%H%M%S)"
  mv "$destination" "$backup"
  printf '%s\n' "Backed up existing Marco to $backup"
fi

mv "$staged" "$destination"
printf '%s\n' "Installed Marco to $destination"
printf '%s\n' "In Codex, open Settings > Pets, select Refresh, choose Marco, then enter /pet."
