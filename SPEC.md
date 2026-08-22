# SPEC.md — Auto-Kitty-Workspace

**Versión:** 0.1 — 2026-08-22
**Estado:** Borrador | Aprobado

> Contrato de dominio inmutable durante una tarea activa. El código se deriva de aquí, no al revés.
> Cambios: nueva sección y/o bump de versión **entre** tareas. Criterios de una tarea = petición + sección relevante.

## 1. Visión y fuera de alcance

### Visión
<una frase: quién, qué, valor>

### Objetivos funcionales
1. <comportamiento observable>
2. …

### Objetivos no funcionales
- Latencia p95:
- Disponibilidad:
- Accesibilidad:
- Privacidad (base legal, minimización, retención):
- Idempotencia:

### Fuera de alcance
- …

## 2. Arquitectura

- Estilo: <modular monolith | hex | eventos | …>
- Límites de confianza: <cliente | API | workers | terceros>
- Diagrama (texto):

```
cliente → API → dominio → persistencia
                → cola → workers
```

- Integraciones: <nombre, dirección, PII sí/no, firma>

## 3. Modelo de datos

### Entidades
| Entidad | Invariantes | PII |
|---|---|---|
| | | |

### Enums / máquinas de estado
| Máquina | Estados | Transiciones legales | Ilegales |
|---|---|---|---|
| | | | |

### Persistencia
- Motor:
- Transacciones obligatorias cuando:
- Claves / unicidad:

## 4. API / contratos

- Auth: <sesión | token | mTLS>
- Versionado:
- Errores: <forma estable>
- Endpoints:

| Método | Ruta | Auth | Idempotente | Notas |
|---|---|---|---|---|
| | | | | |

## 5. Flujos

1. <nombre>: precondiciones → pasos → postcondiciones → fallos
2. …

## 6. No funcionales detallados

- Rate limit:
- Observabilidad (qué no loguear):
- Backups / RPO / RTO:

## 7. Estrategia de pruebas

Qué **debe fallar** si se rompe el contrato:

| Contrato | Test / comando |
|---|---|
| | |

Cobertura mínima de transiciones de estado: todas las legales + rechazo de ilegales.
