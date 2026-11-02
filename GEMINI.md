# Antigravity Usage

## Description
A CLI that reports Google **Antigravity** conversation activity and estimated
cost for the last 2 months. Same one-line-per-month format as oc-usage /
ccusage. Scoped to Antigravity CLI only; the separate Gemini CLI is not a data source.

## Tech Stack
- Python 3 (Standard Library Only, `urllib`, `json`, `sqlite3`).

## Why this design
The CLI reader extracts model-response counts from local SQLite stores.
Token counts are estimated using `ASSUMED_TOKENS_PER_TURN`, not measured
from each response. Keep this distinction explicit in output and docs.

So usage is sourced from Antigravity's local conversation SQLite stores
(`gen_metadata.data.field1.field19` gives the per-turn model id, which feeds
both the per-month turn counts and the cost estimate). Cost is an
**estimate**: assumed per-turn tokens (`ASSUMED_TOKENS_PER_TURN`) × live
per-model rates from models.dev. The estimate is documented as such in the
README because the reader does not recover per-turn token counts.

## Architecture (SOLID, single-responsibility units)
- **`PricingEngine`**, fetches live per-million rates from the models.dev
  database every run (same source oc-usage uses, with the same generic
  $0-subscription → real-rate resolution); on failure falls back to the
  last successful cache, flagged stale. No pricing is bundled in source.
- **`ConversationStore`**, opens `~/.gemini/antigravity-cli/conversations/*.db`
  in read-only SQLite mode and
  aggregates per-month: estimated tokens (real per-model turn counts from
  `gen_metadata.data.field1.field19` × `ASSUMED_TOKENS_PER_TURN`) and cost
  (those tokens × live rates).
- **`Renderer`**, formats the per-month activity block.

## Conventions
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/).
- **Zero external dependencies**, standard library only.
- **Cost is always an estimate, always documented.** The CLI reader does not
  recover per-turn token counts, so cost uses assumed per-turn
  tokens × live models.dev rates. If a future Antigravity release exposes real
  per-token usage, swap the estimate for the real calculation at that point.
- **Read-only on Antigravity state**, every SQLite open uses `?mode=ro`.
- **No AI Attribution** in commit messages.

## Release Process
- Update `README.md` whenever features change (source of truth).
- Commit using Conventional Commits.

## CLI compatibility and verification

The supported source is the dedicated Antigravity CLI SQLite store. App and
IDE history are outside scope. [README.md](README.md) documents source paths,
estimate limitations, and pricing behavior.

Run `python3 -m unittest discover -v` and
`python3 -m py_compile antigravity-usage test_usage.py` before committing.
No typechecker is configured. Run `./antigravity-usage` and compare source
DB size and modification time before and after the run.
