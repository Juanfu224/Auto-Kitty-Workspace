---
name: test-runner
description: >
  Run project test suites without polluting parent context.
  Activate when running more than 3 tests, full groups, or debugging failures.
  Do NOT activate for single assertion edits with no run.
---

# test-runner

Ejecutar el comando de test del stack (leer `AGENTS.md` / nested AGENTS para el binario).
No corregir código. No imprimir tests verdes.
Devolver únicamente JSON `{status, summary, counts, failures, shield}`: status pass|fail|error_env; summary ≤ 240 chars; sin logs verdes ni secretos.
Si el fallo es de entorno (servicios de BD, caché, red), `status=error_env`.
