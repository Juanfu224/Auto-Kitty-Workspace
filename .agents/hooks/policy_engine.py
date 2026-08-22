#!/usr/bin/env python3
"""Motor de política. Best-effort léxico. No es AST de shell ni DLP.

shellDeny se aplica a `command` por defecto. Una regla puede declarar
`surfaces: ["command", "content"]` (p. ej. HS_HMAC_DISABLE) para inspeccionar
también el blob de Write/Edit. No mezclar rm -rf de documentación con el gate
de terminal.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

class Decision(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    ASK = "ask"

@dataclass(frozen=True)
class PolicyResult:
    decision: Decision
    rule_id: str
    reason: str

PROMPT_EVENTS = {
    "beforesubmitprompt",
    "userpromptsubmit",
    "usersubmitprompt",
}

READ_EVENTS = {
    "beforereadfile",
}

# Cap haystacks before regex (ReDoS / latency). Normal edits stay under this.
HAYSTACK_CAP = 256 * 1024

POLICY_PATH = re.compile(
    r"(?:^|/)\.agents/(?:hooks|policy)(?:/|$)",
    re.I,
)

POLICY_SHELL = re.compile(
    # python3 omitted on purpose: hook is `python3 .agents/hooks/guard.py`.
    r"(?:(?:[>&|]|tee|rm|mv|cp|truncate|sed|perl|python|rsync|dd|ln|install|node|nodejs|ruby|php|awk)\b).{0,120}\.agents/(?:hooks|policy)\b",
    re.I,
)

COMMAND_KEYS = (
    "command",
    "cmd",
    "script",
    "url",
)

CURSOR_EVENTS = {
    "beforeShellExecution",
    "beforeMCPExecution",
    "preToolUse",
    "beforeReadFile",
    "beforeSubmitPrompt",
}

CLAUDE_EVENTS = {
    "PreToolUse",
    "UserPromptSubmit",
}

class PolicyError(Exception):
    """Configuración irresoluble o contrato inválido."""

def has_deny(root: Path) -> bool:
    return (root / ".agents" / "policy" / "deny.json").is_file()

def resolve_root(payload: dict[str, Any] | None = None) -> Path:
    payload = payload or {}
    candidates: list[Path] = []
    roots = payload.get("workspace_roots")
    if isinstance(roots, list):
        for value in roots:
            if isinstance(value, str) and value.strip():
                candidates.append(Path(value).expanduser().resolve())
    cwd = payload.get("cwd")
    if isinstance(cwd, str) and cwd.strip():
        candidates.append(Path(cwd).expanduser().resolve())
    here = Path(__file__).resolve()
    if len(here.parts) >= 3:
        candidates.append(here.parents[2])
    candidates.append(Path.cwd().resolve())
    seen: set[Path] = set()
    for start in candidates:
        if start in seen:
            continue
        seen.add(start)
        for probe in (start, *start.parents):
            if has_deny(probe):
                return probe
    raise PolicyError("workspace_root_unresolved")

def load_configs(
    root: Path | None = None,
    payload: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    root = root or resolve_root(payload)
    with (root / ".agents" / "policy" / "policy.json").open(encoding="utf-8") as fh:
        policy = json.load(fh)
    with (root / ".agents" / "policy" / "deny.json").open(encoding="utf-8") as fh:
        deny = json.load(fh)
    if not isinstance(policy, dict) or not isinstance(deny, dict):
        raise PolicyError("policy.json o deny.json no son objetos")
    return policy, deny

def _expand_ansi_c_escapes(body: str) -> str:
    """Decode escapes inside a bash $'…' body (hex/octal/simple)."""
    out: list[str] = []
    i = 0
    n = len(body)
    while i < n:
        if body[i] != "\\" or i + 1 >= n:
            out.append(body[i])
            i += 1
            continue
        nxt = body[i + 1]
        if nxt == "x" and i + 3 < n and re.fullmatch(r"[0-9A-Fa-f]{2}", body[i + 2 : i + 4]):
            out.append(chr(int(body[i + 2 : i + 4], 16)))
            i += 4
            continue
        if nxt in "01234567":
            m = re.match(r"([0-7]{1,3})", body[i + 1 :])
            if m:
                out.append(chr(int(m.group(1), 8) & 0xFF))
                i += 1 + len(m.group(1))
                continue
        simple = {
            "n": "\n",
            "t": "\t",
            "r": "\r",
            "\\": "\\",
            "'": "'",
            '"': '"',
            "a": "\a",
            "b": "\b",
            "e": "\x1b",
            "f": "\f",
            "v": "\v",
        }
        out.append(simple.get(nxt, nxt))
        i += 2
    return "".join(out)


_ANSI_C_QUOTE = re.compile(r"\$'((?:\\.|[^'\\])*)'")


def _expand_ansi_c_quotes(cmd: str) -> str:
    return _ANSI_C_QUOTE.sub(lambda m: _expand_ansi_c_escapes(m.group(1)), cmd)


def normalize_command(cmd: str) -> str:
    """Best-effort lexical variants. No Base64 decode, no AST."""
    if not cmd:
        return ""
    variants: list[str] = [cmd]
    ansi = _expand_ansi_c_quotes(cmd)
    if ansi != cmd:
        variants.append(ansi)
    stripped = re.sub(r"\\(.)", r"\1", ansi)
    stripped = re.sub(r"[ \t]+", " ", stripped)
    if stripped not in variants:
        variants.append(stripped)

    def _add(v: str) -> None:
        v = v.strip()
        if v and v not in variants:
            variants.append(v)

    # Quoted: bash -c 'inner' / -c "inner"
    for m in re.finditer(
        r"""(-c|--command)\s+(['"])(.*?)\2""",
        stripped,
        flags=re.I | re.DOTALL,
    ):
        _add(m.group(3))
    # Unquoted: bash -c rm -rf ./src  → rest of line after -c
    for m in re.finditer(
        r"""(?:^|[\s;|&])(?:(?:ba|z|k)?sh|bash)(?:\.exe)?\s+-c\s+(?![\'"])(.+)$""",
        stripped,
        flags=re.I,
    ):
        _add(m.group(1))

    # Unquote flag tokens on every variant.
    extra: list[str] = []
    for v in list(variants):
        d = re.sub(
            r"""['"](-{1,2}[A-Za-z0-9][A-Za-z0-9_-]*)['"]""",
            r"\1",
            v,
        )
        d = re.sub(r"[ \t]+", " ", d)
        if d != v and d not in variants and d not in extra:
            extra.append(d)
    variants.extend(extra)
    if len(variants) == 1:
        return cmd
    return "\n".join(variants)

def coerce_tool_input(payload: dict[str, Any]) -> dict[str, Any]:
    """Cursor beforeMCPExecution: tool_input is a JSON string. preToolUse: dict."""
    value = payload.get("tool_input")
    if value is None:
        value = payload.get("toolInput")
    if isinstance(value, dict):
        return value
    if isinstance(value, str) and value.strip():
        stripped = value.strip()
        if stripped[:1] in "{[":
            try:
                parsed = json.loads(stripped)
            except json.JSONDecodeError:
                return {}
            if isinstance(parsed, dict):
                return parsed
    return {}

def _add_path(found: list[str], seen: set[str], value: object) -> None:
    if isinstance(value, str) and value.strip() and value not in seen:
        seen.add(value)
        found.append(value)

def extract_paths(payload: dict[str, Any]) -> list[str]:
    found: list[str] = []
    seen: set[str] = set()
    for key in ("file_path", "filePath", "filepath", "path"):
        _add_path(found, seen, payload.get(key))
    inner = coerce_tool_input(payload)
    for key in ("file_path", "filePath", "filepath", "path"):
        _add_path(found, seen, inner.get(key))
    attachments = payload.get("attachments")
    if isinstance(attachments, list):
        for item in attachments:
            if isinstance(item, dict):
                for key in ("file_path", "filePath", "filepath", "path"):
                    _add_path(found, seen, item.get(key))
    return found

def extract_command(payload: dict[str, Any]) -> str:
    chunks: list[str] = []
    for key in ("command", "url", "tool_name", "toolName"):
        val = payload.get(key)
        if isinstance(val, str) and val.strip():
            chunks.append(val)
    inner = coerce_tool_input(payload)
    for key in COMMAND_KEYS:
        val = inner.get(key)
        if isinstance(val, str) and val.strip():
            chunks.append(val)
    raw = payload.get("tool_input")
    if raw is None:
        raw = payload.get("toolInput")
    if isinstance(raw, str) and raw.strip():
        chunks.append(raw)
    return "\n".join(chunks)

def extract_path(payload: dict[str, Any]) -> str:
    paths = extract_paths(payload)
    return paths[0] if paths else ""

def extract_prompt(payload: dict[str, Any]) -> str:
    for key in ("prompt", "text"):
        val = payload.get(key)
        if isinstance(val, str) and val.strip():
            return val
    return ""

def extract_file_body(payload: dict[str, Any]) -> str:
    val = payload.get("content")
    if isinstance(val, str):
        return val
    inner = coerce_tool_input(payload)
    for key in ("content", "contents", "old_string", "oldString"):
        if isinstance(inner.get(key), str):
            return inner[key]
    return ""

def extract_edit_blob(payload: dict[str, Any]) -> str:
    chunks: list[str] = []
    for src in (coerce_tool_input(payload), payload):
        if not isinstance(src, dict):
            continue
        for key in ("new_string", "newString", "contents"):
            val = src.get(key)
            if isinstance(val, str):
                chunks.append(val)
        edits = src.get("edits")
        if isinstance(edits, list):
            for edit in edits:
                if isinstance(edit, dict):
                    for key in ("new_string", "newString", "new_line"):
                        val = edit.get(key)
                        if isinstance(val, str):
                            chunks.append(val)
    return "\n".join(chunks)

def path_looks_secret(file_path: str, patterns: list[str]) -> bool:
    if not file_path:
        return False
    return any(re.search(pat, file_path) for pat in patterns)

def cap_text(value: str, limit: int = HAYSTACK_CAP) -> str:
    if not value or len(value) <= limit:
        return value
    return value[:limit]

def push_is_protected(command: str, branches: list[str]) -> bool:
    if not command or not branches:
        return False
    names = "|".join(re.escape(str(b)) for b in branches)
    return bool(
        re.search(
            rf"\bpush\b[\s\S]*(?:"
            rf"\s(?:origin|upstream)\s+(?:refs/heads/)?(?:{names})(?:\s|$|:)"
            rf"|HEAD:(?:{names})(?:\s|$)"
            rf")",
            command,
            re.I,
        )
    )

def is_locked_install(command: str, substrings: list[str]) -> bool:
    low = command.lower()
    return any(str(s).lower() in low for s in substrings)

def to_decision(mode: str) -> Decision:
    m = (mode or "deny").lower()
    if m == "ask":
        return Decision.ASK
    if m == "allow":
        return Decision.ALLOW
    return Decision.DENY

def validate_event(runtime: str, event: str) -> None:
    allowed = {"cursor": CURSOR_EVENTS, "claude": CLAUDE_EVENTS}
    if runtime not in allowed or event not in allowed[runtime]:
        raise PolicyError(f"EVENT_RUNTIME_MISMATCH:{runtime}:{event}")

def is_policy_path(file_path: str) -> bool:
    if not file_path:
        return False
    normalized = file_path.replace("\\", "/")
    return bool(POLICY_PATH.search(normalized))

def evaluate(
    *,
    runtime: str,
    event: str,
    payload: dict[str, Any],
    policy: dict[str, Any],
    deny: dict[str, Any],
) -> PolicyResult:
    if not runtime or not event:
        return PolicyResult(
            Decision.DENY, "HS_FAILCLOSED", "runtime y event son obligatorios"
        )
    if runtime not in {"cursor", "claude"}:
        return PolicyResult(Decision.DENY, "HS_FAILCLOSED", "runtime desconocido")
    try:
        validate_event(runtime, event)
    except PolicyError:
        return PolicyResult(
            Decision.DENY, "HS_FAILCLOSED", "evento incompatible con el runtime"
        )

    profile = str(policy.get("profile", "standard")).lower()
    git_cfg = policy.get("git") if isinstance(policy.get("git"), dict) else {}
    pkg_cfg = (
        policy.get("package_install")
        if isinstance(policy.get("package_install"), dict)
        else {}
    )
    branches = git_cfg.get("protected_branches") or ["main", "master", "production"]
    if not isinstance(branches, list):
        branches = ["main", "master", "production"]

    command = cap_text(normalize_command(extract_command(payload)))
    paths = extract_paths(payload)
    prompt = cap_text(extract_prompt(payload))
    edit_blob = cap_text(extract_edit_blob(payload))
    secret_paths = deny.get("secretPathPatterns") or []
    flags = re.IGNORECASE | re.DOTALL
    tool_name = str(payload.get("tool_name") or payload.get("toolName") or "")
    event_key = event.lower().replace("_", "")
    tool_l = tool_name.lower()

    mutating_policy = any(is_policy_path(p) for p in paths)
    if mutating_policy:
        reading = event_key in READ_EVENTS or tool_l in {"read", "grep", "glob"}
        if not reading:
            return PolicyResult(
                Decision.DENY,
                "HS_POLICY_MUTATION",
                "no mutar hooks ni policy del repo",
            )
    if command and POLICY_SHELL.search(command):
        return PolicyResult(
            Decision.DENY,
            "HS_POLICY_MUTATION",
            "no mutar hooks ni policy del repo",
        )

    for pat in secret_paths:
        if any(re.search(pat, p) for p in paths):
            return PolicyResult(
                Decision.DENY, "HS_SECRET_PATH", "lectura/escritura de secreto"
            )
        if command and re.search(pat, command):
            return PolicyResult(
                Decision.DENY, "HS_SECRET_PATH", "comando apunta a secreto"
            )

    haystack_parts = [command, prompt, edit_blob]
    if any(path_looks_secret(p, secret_paths) for p in paths):
        haystack_parts.append(cap_text(extract_file_body(payload)))
    secret_haystack = cap_text(" ".join(p for p in haystack_parts if p))

    for pat in deny.get("secretContentPatterns") or []:
        if secret_haystack and re.search(pat, secret_haystack):
            return PolicyResult(
                Decision.DENY,
                "HS_SECRET_CONTENT",
                "posible secreto en argumentos o prompt",
            )

    if event_key in PROMPT_EVENTS and prompt:
        lowered = prompt.lower()
        for marker in deny.get("injectionMarkers") or []:
            if isinstance(marker, str) and marker and marker.lower() in lowered:
                return PolicyResult(
                    Decision.DENY, "ASI01", "marcador de inyección en prompt"
                )

    for rule in deny.get("shellDeny") or []:
        regex = rule.get("regex")
        rid = str(rule.get("id") or "HS")
        if not regex:
            continue
        surfaces = rule.get("surfaces")
        if not isinstance(surfaces, list) or not surfaces:
            surfaces = ["command"]
        blobs: list[str] = []
        if "command" in surfaces and command:
            blobs.append(command)
        if "content" in surfaces and edit_blob:
            blobs.append(edit_blob)
        haystack = " ".join(blobs)
        if not haystack or not re.search(regex, haystack, flags):
            continue
        reason = str(rule.get("reason") or "deny")
        if rid in {"HS_GIT_FORCE", "HS_GIT_RESET_HARD", "HS_GIT_CLEAN_FDX"}:
            return PolicyResult(Decision.DENY, rid, reason)
        if rid == "HS_GIT_PUSH":
            if push_is_protected(command, [str(b) for b in branches]):
                return PolicyResult(
                    Decision.DENY, "HS_GIT_PUSH_PROTECTED", "push a rama protegida"
                )
            if profile in {"strict", "ci"}:
                return PolicyResult(Decision.DENY, rid, f"perfil {profile}: git push deny")
            push_mode = str(git_cfg.get("push") or rule.get("mode") or "ask")
            return PolicyResult(to_decision(push_mode), rid, reason)
        if rid == "IG_PACKAGE_INSTALL":
            locked = pkg_cfg.get("locked_substrings") or []
            if pkg_cfg.get("allow_locked_without_prompt") and is_locked_install(
                command, [str(s) for s in locked]
            ):
                return PolicyResult(
                    Decision.ALLOW, "IG_PACKAGE_LOCKED", "locked install allow"
                )
            pkg_mode = (
                "deny"
                if profile in {"strict", "ci"}
                else str(pkg_cfg.get("default") or rule.get("mode") or "ask")
            )
            return PolicyResult(to_decision(pkg_mode), rid, reason)
        return PolicyResult(to_decision(str(rule.get("mode") or "deny")), rid, reason)

    return PolicyResult(Decision.ALLOW, "DEFAULT_ALLOW", "No rule matched")
