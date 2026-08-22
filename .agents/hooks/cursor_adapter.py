"""Contrato Cursor por evento.
ALLOW: shell/MCP = permission allow; beforeSubmitPrompt = continue true.
ASK de beforeShellExecution / beforeMCPExecution: permission ask + exit 0.
ASK de preToolUse / beforeReadFile: deny + exit 2 (ask no enforced).
preToolUse incluye MCP:.* porque Cloud no corre beforeMCPExecution: ASK de MCP
acaba en deny si ese hook dispara (en local, deny gana si corren ambos).
No emitir {} en ALLOW de shell: no es el contrato F3.
"""
from __future__ import annotations

from policy_engine import Decision, PolicyResult

ASK_NATIVE = {
    "beforeshellexecution",
    "beforemcpexecution",
}


def cursor_emit(result: PolicyResult, event: str) -> tuple[dict, int]:
    ev = event.lower().replace("_", "")
    msg = f"{result.rule_id}: {result.reason}"
    if ev == "beforesubmitprompt":
        if result.decision == Decision.ALLOW:
            return {"continue": True}, 0
        return {"continue": False, "user_message": msg}, 2
    if result.decision == Decision.ALLOW:
        return {"permission": "allow"}, 0
    if result.decision == Decision.ASK and ev in ASK_NATIVE:
        return {
            "permission": "ask",
            "user_message": msg,
            "agent_message": msg,
        }, 0
    return {
        "permission": "deny",
        "user_message": msg,
        "agent_message": msg,
    }, 2
