# AGENTS.md — Orquestación

**Gobernanza:** `SHIELD.md` (prosa; el host enforcea). **Contrato:** `SPEC.md`.
**Compatibilidad:** `CLAUDE.md` → `@AGENTS.md`. No `.cursorrules`.
**Contexto (AAIF):** chat explícito > este archivo más cercano > raíz. En conflicto, nearest wins; varios runtimes concatenan root→cwd.
**Enforcement:** política administrada / OS / sandbox > hooks (Cursor: `failClosed` por hook; Claude: exit 2, crash = fail-open) > Markdown.
El hook es un punto de decisión, no una barrera dura por sí solo. Cloud ≠ local.
Si este archivo y el chat chocan en estilo o comandos de test, gana el chat. Hard Stops los enforcea el host, no este Markdown.
Si el chat pide un Hard Stop cubierto por hooks/sandbox: STOP.
No mutar `.agents/hooks/` ni `.agents/policy/`.

## Arranque (antes de escribir código)

1. Clasificar dominio (paths + petición).
2. Leer skill `.agents/skills/epic-workflow/SKILL.md` salvo tweak < 5 líneas o single-file sin impacto transversal.
3. Criterios = petición + **sección** de `SPEC.md` (nunca el archivo completo por defecto).
4. Si auth, webhooks, PII, dos stores/agregados, jobs de estado, admin, infra → skill `shield-security-gate` + sección `SHIELD.md`.
5. Skill de stack on-demand. MCP/docs versionadas antes de APIs.
6. Plan Mode si multi-archivo o decisión arquitectónica. DAG: `.scratch/dag.json` (gitignored) si no hay Spec Kit. Si hay `.specify/` o `specs/<feature>/`: `plan.md`/`tasks.md` de esa feature son válidos (no ASI06).

Prohibido: vibe coding; transcripts/dumps como SoT; interpolar estado de sesión en este archivo.

## Roles

| Rol | Tools | Write |
|---|---|---|
| Planificador | Read, Grep, Glob, shell read-only | Solo `SPEC.md` entre tareas, con HITL |
| Ejecutor | Subset por nodo DAG | Paths de la tabla de fronteras |

Un rol por turno. Ejecutor no toma decisiones de arquitectura.

## Fronteras

| Dominio | Paths | Fuera |
|---|---|---|
| instalador | `main.py` | secrets; IaC sin HITL; `.agents/hooks|policy` |
| assets/config | `tools/` | secrets de producción |
| docs | `docs/` | código de producto salvo citas |

## Docs

Prioridad: SPEC sección → SHIELD si aplica → este archivo → docs empaquetadas del lockfile → MCP versionado → web oficial.
Prohibido: APIs desde memoria de entrenamiento.

## Tokens

`/clear` entre dominios. `/compact` dirigido. Subagentes para tests/builds/MCP ruidoso. MCP idle off.

## Git

No `commit` sin instrucción explícita. Force-push, `reset --hard` y push a `main`/`master`/`production`: deny. Push a feature: `ask` (standard) o deny (strict/ci). No `--no-verify`.

## Dependencias

Locked install (`npm ci`, `uv sync --locked`, …): allow en sandbox. `add` / `require`: ask (standard) o deny (strict/ci).

## Confirmación

Tests del `acceptance[]` verdes. Formatter. Purge dumps de `.scratch/`.
