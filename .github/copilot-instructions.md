# Nika workflows (`*.nika`) — Copilot brief

Nika workflows are audited BEFORE they run. The loop: author from a
skeleton (`nika compile --list` lists them) → `nika check <file>` after
EVERY edit → `nika check <file> --fix` heals the mechanical renames →
repair the rest from the diagnostics (`nika explain NIKA-XXXX`) →
only a clean file reaches a human.

Rules the validator enforces:
- Envelope `nika: <id>` · one verb per task (`infer` · `exec` · `invoke` ·
  `agent`) · the verb IS the task key.
- `tasks.X` is read at the boundary only: `with: { alias: ${{ tasks.X.output }} }`
  is the data edge · `after: { X: success }` orders without data · the
  body reads `${{ with.alias }}`.
- `invoke` nests BOTH its keys: `tool:` and `args:` sit INSIDE `invoke:`,
  never at task level · a builtin also needs its `permits.tools` entry
  beside the `permits.fs`/`permits.net` grant for what it touches.
- Secrets come from the environment (`${{ secrets.X }}`) — never inline.
- Never invent syntax: `nika spec --schema` is the JSON Schema · `nika catalog`
  / `nika catalog --tools` name the providers and builtins.
- Cost honesty: unknown spend is declared, never rounded to $0 · a local
  model is unpriced, never « free ».

See AGENTS.md (scaffolded by `nika init`) for the full contract.
