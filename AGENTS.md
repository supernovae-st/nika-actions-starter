# AGENTS.md — Nika workflows in this repo

Nika is a sovereign AI workflow engine. Workflows are `*.nika.yaml` files,
**audited before they run**. (This guide is scaffolded by `nika init`.)

## The loop
- **Author** · `nika new --from <template> <file>.nika.yaml` (or write one —
  the envelope is `nika: v1` + `workflow: <kebab-id>` + `tasks:`).
- **Check** · `nika check <file>` — the static audit BEFORE any run (schema ·
  DAG · CEL · effects · permits · cost). Exit `0` clean · `2` findings.
- **Run** · `nika run <file>` — execute · live render. Exit `0` ok · `1` failed.
  Inputs ride `--var key=value` (repeatable · unknown keys refused); a run
  paused on a `nika:prompt` resumes with `--resume <trace> --answer
  <task>=<value>` (confirm gates take booleans: `--answer approve=true`).
- **Pin** · `nika test <file> --update` writes `<file>.golden.json` from an
  offline mock run; `nika test <file>` replays and compares — deterministic,
  zero keys, the CI gate.
- **Diagnose** · `nika doctor` — the environment (providers · keys · config).
  `nika welcome` is the short mirror (machine · workspace · next commands).
- **Context** · `nika context --json` — the whole workspace truth in one
  call (every workflow audited · recent runs · costs · capped and says
  so). Read it before proposing edits.
- **Explain** · `nika explain NIKA-XXXX` teaches one error code ·
  `nika explain <file>` narrates a workflow (waves · cost · touches · how
  to run) — read it before handing a workflow to a human.
- **Wire** · `nika wire <cursor|vscode|windsurf|claude|codex|all>` — point an
  agent client's MCP config at the real oracle (idempotent · preserves other
  servers).

## The four verbs (exactly one per task)
`infer` (an LLM call) · `exec` (a shell command) · `invoke` (a `nika:` builtin
or MCP tool) · `agent` (a multi-turn ReAct loop).

## Hard rules (the validator enforces these — they catch ~90% of LLM errors)
- One verb per task · the verb IS the task key (never a `verb:` field).
- Any `${{ tasks.X }}` reference needs `depends_on: [X]` (arrays always).
- Quote any YAML scalar that STARTS with `${{` (an unquoted leading `${{`
  breaks the parse).
- `invoke` arguments live under `args:` (not `input:` / `params:`).
- `when:` is a `${{ }}` CEL boolean or the literal `true`/`false` — a bare
  string is rejected. `size()` is the only CEL function.
- `nika:write` needs `content:` · `nika:done` is valid only inside `agent.tools`.
- snake_case task ids · kebab-case `workflow:`.

## Don't invent structure — route to a skeleton
`nika new --from '?'` lists the embedded skeletons · `nika examples list` /
`show <slug>` reads a runnable example that exercises a construct ·
`nika schema` is the JSON Schema · `nika spec --canon` is the SSOT ·
`nika catalog` names the providers/models · `nika tools` names the `nika:`
builtins. Copy, fill, check.

## Cost honesty (never hide unknown spend)
- `nika check` prints the ceiling BEFORE any token · `≥ $X FLOOR` means an
  unbounded task exists — name why, never round unknown to $0.
- A local model is unpriced compute, **never « free »**.
- `nika run <file> --max-cost-usd <n>` blocks BEFORE the call that would
  cross the cap.

## Understand · replay · prove
- `nika inspect <file>` — static anatomy: tasks · verbs · wave groups · cost.
- `nika graph <file> --format mermaid|dot|json` — the ONE graph projector.
- `nika trace show|replay <run>` — the flight recorder (every run records).
- `nika trace verify <run>` — the journal is hash-chained: verify it after a
  run that matters, cite the trace instead of trusting a memory of the run.
- `nika dap` — step a recorded run under a debugger UI, forward AND back.

## Servers (stdio · for editors and agent clients)
`nika lsp` (language server) · `nika mcp` (MCP: check/explain/schema/examples
as tools) · `nika completions <shell>` generates shell completions.

## Discipline
- Every effect is gated by `permits:` (default-deny · `nika check --infer-permits`
  prints the tightest boundary).
- Secrets come from the environment (`${{ secrets.X }}`) — never inline.
- `nika check` must be clean before `nika run` (audit-before-run is enforced).
