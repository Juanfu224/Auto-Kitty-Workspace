---
name: epic-workflow
description: >
  Activate at the start of any new feature, task, or non-trivial bug fix.
  Guides EPIC: Explore (read SPEC section + SHIELD if sensitive) → Plan (Plan Mode; ephemeral DAG or Spec Kit feature tasks)
  → Implement (one DAG node) → Confirm (tests for acceptance).
  Do NOT activate for: documentation-only edits, config tweaks under 5 lines, or single-file
  changes with no cross-cutting impact.
license: MIT
metadata:
  author: project
---

# EPIC — Spec-Driven Development

El código es artefacto de `SPEC.md`. Criterios = petición + sección SPEC. DAG de sesión gitignored; si hay Spec Kit, `plan.md`/`tasks.md` de la feature son válidos.

## E — Exploración
1. Extraer criterios; ≤ 2 preguntas si ambiguo.
2. Leer **sección** SPEC. SHIELD si auth/webhooks/PII/dos stores/jobs/admin/infra.
3. MCP / docs locales versionadas antes de APIs.
4. No escribir producto.

## P — Planificación
1. Plan Mode si multi-archivo o arquitectura.
2. DAG `{id, deps, files, acceptance, shield_refs, autonomy}`. Opcional `.scratch/dag.json`.
3. Spec Kit activo: usar `specs/<feature>/tasks.md`; no duplicar como SoT de sesión.
4. No implementar hasta aprobación si Plan Mode.

## I — Implementación
1. Un nodo. Tipado estático del lenguaje del repo, si existe. Sin secrets hardcodeados.
2. Autocurar lint/test del nodo. Desvío de SPEC → STOP.
3. Ruido → subagente test-runner / mcp-analyzer.

## C — Confirmación
1. Tests de `acceptance[]` verdes.
2. No commit sin instrucción explícita. Push según perfil (`ask` en standard; deny en strict/ci y a protegidas). Nunca force-push.
3. Purge dumps de `.scratch/`. `/clear` si cambia el dominio.

## Precedencia
Contexto AAIF: chat > AGENTS.md más cercano (conflicto; varios runtimes concatenan root→cwd). Enforcement: política administrada / sandbox > hooks (Cursor failClosed; Claude exit 2, crash = fail-open) > Markdown. No mutar `.agents/hooks/` ni `.agents/policy/`.
