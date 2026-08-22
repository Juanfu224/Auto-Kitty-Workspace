"""Contrato Claude: PreToolUse vs UserPromptSubmit.
ALLOW léxico = silencio ({} + 0): el hook no decide; no emitir permissionDecision allow.
No copiar el permission allow de Cursor: en Claude allow salta el prompt nativo.
ASK = permissionDecision ask. DENY = deny + exit 2. defer fuera de alcance.
Exit 1 nunca (fail-open en Claude).
"""
from __future__ import annotations

from policy_engine import Decision, PolicyResult

def claude_emit(result: PolicyResult, event: str) -> tuple[dict, int]:
    ev = event.lower().replace("_", "")
    msg = f"{result.rule_id}: {result.reason}"
    if ev in {"userpromptsubmit", "usersubmitprompt"}:
        if result.decision == Decision.ALLOW:
            return {}, 0
        return {"decision": "block", "reason": msg}, 2
    if result.decision == Decision.ALLOW:
        return {}, 0
    perm = "ask" if result.decision == Decision.ASK else "deny"
    body = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": perm,
            "permissionDecisionReason": msg,
        }
    }
    return body, (0 if perm == "ask" else 2)
