# nika-actions-starter

AI-workflow receipts in your CI. Every pull request gets a static verdict,
posted as a sticky comment: what each `.nika.yaml` workflow would do, an
honest cost floor, which secrets it wants, the DAG. Checked before a single
token is ever spent. Nothing is executed.

## See it live

The CI in this repo runs on its own pull requests. Open the Pull requests
tab and read the sticky **Nika check** comment on any of them: that is
exactly what you get in your own repo, day one.

## Use it

1. Click **Use this template** (top right).
2. That is it. On your first push and every PR after, the check runs and the
   verdict lands as a comment. No API key, no model server, no secrets: the
   check is fully static.

Prove it locally too (single binary):

```bash
brew install supernovae-st/tap/nika
nika check flows/pr-risk-review.nika.yaml
```

## What is inside

| File | What it does |
|---|---|
| `flows/pr-risk-review.nika.yaml` | the signature flow: read a PR diff, judge its risk, comment only when it is high. Declares its tightest permits (git and one MCP tool, everything else default-deny) |
| `flows/daily-brief.nika.yaml` | a simple offline-provable flow: fetch a feed, brief it with a local model, save |
| `.github/workflows/nika.yml` | the CI: runs the action on every flow, posts the sticky verdict, fork-safe by design |
| `AGENTS.md`, `.agents/`, `.vscode/` | written by `nika init`: teaches your coding agent and your editor about `.nika.yaml` files |

## Why a verdict in your CI

The interesting failures in AI work happen before the model is even called:
a workflow that spends more than you think, a secret that flows into the
wrong step, a plan that does not do what the file says. `nika check` catches
those statically. Putting it in CI means the receipt shows up where your team
already looks: on the PR.

The action does check-only and zero-secret by default. It never grants
`pull_request_target`. On fork PRs the token is read-only, so the verdict
lands in the step summary instead of a comment. Execution is not this
action's job.

## Add the badge

```md
[![nika check](https://github.com/YOUR_ORG/YOUR_REPO/actions/workflows/nika.yml/badge.svg)](https://github.com/YOUR_ORG/YOUR_REPO/actions/workflows/nika.yml)
```

Docs: https://docs.nika.sh · The action: https://github.com/supernovae-st/nika-action · Engine (AGPL-3.0): https://github.com/supernovae-st/nika
