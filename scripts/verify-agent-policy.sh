#!/usr/bin/env sh
# Exit 2 si falta el lock, no hay líneas GNU, o hay drift. Requiere sha256sum (GNU coreutils).
set -eu
if command -v git >/dev/null 2>&1 && git rev-parse --show-toplevel >/dev/null 2>&1; then
  ROOT=$(git rev-parse --show-toplevel)
else
  ROOT=$(pwd)
fi
cd "$ROOT"
LOCK=".agents/policy/integrity.sha256"
if [ ! -f "$LOCK" ]; then
  echo "missing $LOCK" >&2
  exit 2
fi
if ! command -v sha256sum >/dev/null 2>&1; then
  echo "sha256sum required" >&2
  exit 2
fi
if ! grep -qE '^[0-9a-fA-F]{64}  ' "$LOCK"; then
  echo "no GNU checksum lines in $LOCK" >&2
  exit 2
fi
if grep -qvE '^[0-9a-fA-F]{64}  |^[[:space:]]*$' "$LOCK"; then
  echo "non-checksum lines in $LOCK (comments/placeholders not allowed)" >&2
  exit 2
fi
sha256sum -c "$LOCK" || exit 2
