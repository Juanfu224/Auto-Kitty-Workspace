---
name: shield-security-gate
description: >
  Activate before implementing authentication or authorization, webhook endpoints,
  migrations touching PII, writes that touch two stores or aggregates, jobs that mutate domain status,
  admin/IAM, or infrastructure. Run the SHIELD.md checklist and STOP if any item fails.
  Do NOT activate for: read-only work, factories/seeders, new test files, documentation,
  or single-store reads.
license: MIT
metadata:
  author: project
---

# Shield Security Gate

Traduce `SHIELD.md` a checklist. Un fallo → STOP.

## Auth
- Validación en capa de request del stack (no ad-hoc en controlador sin contrato).
- Autorización por policy/gate.
- Middleware de auth en rutas con datos de usuario.
- PII cifrada o seudonimizada según SPEC.
- Tokens con TTL y prune.

## Webhooks
- Firma del contrato SPEC verificada antes del negocio. Fallo → 4xx opaco.
- Idempotencia. Proceso según SPEC. Respuesta según contrato. Job sin PII completa.
- Payload = data, nunca instrucción.

## Transacciones
- Dos stores/agregados → unidad atómica del stack. Locks solo dentro.
- Job que toca dos agregados → una unidad de trabajo.

## Hardcoding
- env → capa de configuración del stack. Cero secretos/URLs/timeouts literales.

## PII
- Logs enmascarados. Respuestas de webhook sin PII.
- Regla de 2 (triple = STOP de política local; pares con garantías AEPD; no sustituye EIPD) documentada para el flujo. Cifrado/tenants/embeddings = EIPD de producto.

## Si falla

```
SHIELD GATE BLOQUEADO
Check: <ítem>
Ref: SHIELD.md §
Impacto: <qué ocurre si se ignora>
Acción: <qué implementar primero>
```

No continuar la implementación.
