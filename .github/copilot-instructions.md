# Nika workflows (`*.nika.yaml`) — Copilot brief

Nika workflows are audited BEFORE they run. The loop: author from a
skeleton (`nika new --from '?'` lists them) → `nika check <file>` after
EVERY edit → repair from the diagnostics (`nika explain NIKA-XXXX`) →
only a clean file reaches a human.

Rules the validator enforces:
- Envelope `nika: v1` · one verb per task (`infer` · `exec` · `invoke` ·
  `agent`) · the verb IS the task key.
- Any `${{ tasks.X }}` reference needs `depends_on: [X]`.
- `invoke` arguments live under `args:` · secrets come from the
  environment (`${{ secrets.X }}`) — never inline.
- Never invent syntax: `nika schema` is the JSON Schema · `nika catalog`
  / `nika tools` name the providers and builtins.
- Cost honesty: unknown spend is declared, never rounded to $0 · a local
  model is unpriced, never « free ».

See AGENTS.md (scaffolded by `nika init`) for the full contract.
