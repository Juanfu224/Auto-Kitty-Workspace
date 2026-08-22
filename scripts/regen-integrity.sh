#!/usr/bin/env sh
# Generate .agents/policy/integrity.sha256 for the CURRENT repo (destination after INIT).
# Run from the git root that already has hooks/policy/settings materialized.
set -eu
if command -v git >/dev/null 2>&1 && git rev-parse --show-toplevel >/dev/null 2>&1; then
  ROOT=$(git rev-parse --show-toplevel)
else
  ROOT=$(pwd)
fi
cd "$ROOT"
if [ ! -f .agents/hooks/guard.py ]; then
  echo "missing .agents/hooks/guard.py under $ROOT" >&2
  exit 2
fi
if ! command -v sha256sum >/dev/null 2>&1; then
  echo "sha256sum required" >&2
  exit 2
fi
mkdir -p .agents/policy
sha256sum \
  .agents/hooks/policy_engine.py \
  .agents/hooks/cursor_adapter.py \
  .agents/hooks/claude_adapter.py \
  .agents/hooks/guard.py \
  .agents/policy/policy.json \
  .agents/policy/deny.json \
  .cursor/hooks.json \
  .cursor/sandbox.json \
  .claude/settings.json \
  > .agents/policy/integrity.sha256
echo "wrote .agents/policy/integrity.sha256"
