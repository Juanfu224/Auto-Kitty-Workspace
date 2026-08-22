#!/usr/bin/env python3
"""Entrada fail-closed. --runtime y --event required. Solo exit 0 o 2."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HOOKS = Path(__file__).resolve().parent
if str(HOOKS) not in sys.path:
    sys.path.insert(0, str(HOOKS))

from claude_adapter import claude_emit  # noqa: E402
from cursor_adapter import cursor_emit  # noqa: E402
from policy_engine import (  # noqa: E402
    Decision,
    PolicyError,
    PolicyResult,
    evaluate,
    load_configs,
)

class FailClosedParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        sys.stderr.write("HS_FAILCLOSED: runtime y event son obligatorios\n")
        sys.stdout.write("{}")
        raise SystemExit(2)

def emit(runtime: str, event: str, result: PolicyResult) -> int:
    if runtime == "cursor":
        body, code = cursor_emit(result, event)
    elif runtime == "claude":
        body, code = claude_emit(result, event)
    else:
        body, code = {}, 2
    sys.stdout.write(json.dumps(body, ensure_ascii=False))
    if result.decision != Decision.ALLOW:
        sys.stderr.write(f"{result.rule_id}: {result.reason}\n")
    return code

def build_parser() -> argparse.ArgumentParser:
    parser = FailClosedParser()
    parser.add_argument("--runtime", required=True, choices=("cursor", "claude"))
    parser.add_argument("--event", required=True)
    return parser

def main() -> int:
    args = build_parser().parse_args()
    runtime = args.runtime
    event = args.event
    fail = PolicyResult(
        Decision.DENY, "HS_FAILCLOSED", "fail-closed: config or parse error"
    )
    raw = sys.stdin.read().lstrip("\ufeff")
    try:
        loaded = json.loads(raw) if raw.strip() else {}
        if not isinstance(loaded, dict):
            return emit(runtime, event, fail)
        policy, deny = load_configs(payload=loaded)
        result = evaluate(
            runtime=runtime,
            event=event,
            payload=loaded,
            policy=policy,
            deny=deny,
        )
        return emit(runtime, event, result)
    except PolicyError:
        return emit(runtime, event, fail)
    except Exception:
        return emit(runtime, event, fail)

if __name__ == "__main__":
    sys.exit(main())
