---
name: mcp-analyzer
description: >
  Reduce MCP or CLI payloads larger than ~2000 tokens.
  Write raw JSON to .scratch/, extract fields, delete the dump.
  Do NOT activate for small structured replies already under 500 tokens.
---

# mcp-analyzer

1. Escribir payload en `.scratch/mcp.json` (gitignored).
2. Extraer solo campos pedidos con `jq` o `python3`.
3. Borrar el dump.
4. Devolver JSON `{ "status": "ok", "summary": "...", "data": { } }` ≤ 500 tokens.
Prohibido: devolver el payload crudo al padre. Prohibido: persistir PII.
