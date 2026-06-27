# Antigravity Usage

## Description
A CLI that reports Google **Antigravity** conversation activity and estimated
cost for the last 2 months. Same one-line-per-month format as oc-usage /
ccusage. Scoped to Antigravity (CLI + IDE) only; the legacy Gemini CLI is
deprecated (EOL 2026-06-18) and is **not** a data source.

## Tech Stack
- Python 3 (Standard Library Only — `urllib`, `json`, `sqlite3`).

## Why this design
Antigravity is billed as a flat-rate subscription, so Google does not surface
per-token usage to subscribers in any client-readable form. Specifically:
- The local conversation store (`~/.gemini/antigravity-cli/conversations/*.db`
  and the antigravity/ sibling) is plain SQLite with protobuf BLOB columns,
  not encrypted — but `UsageMetadata` is not persisted in any of the tables
  (`steps.step_payload`, `gen_metadata.data`, `trajectory_metadata_blob.data`).
- The JSONL transcripts at `~/.gemini/antigravity-cli/brain/<uuid>/.system_generated/logs/transcript.jsonl` discard `UsageMetadata`.
- The CloudCode `retrieveUserQuota` endpoint returns only REQUEST-type quota
  (`tokenType: "REQUESTS"`), not token counts.
- The CloudCode `retrieveUserQuotaSummary` endpoint is 403 Forbidden for
  normal subscriber accounts.
- Antigravity hook events (`PreToolUse`, `PostToolUse`, `PreInvocation`,
  `PostInvocation`, `Stop`) do not include token counts in their stdin
  payloads — confirmed against the official hook spec at
  `antigravity.google/docs/hooks`.

So usage is sourced from Antigravity's local conversation SQLite stores
(`gen_metadata.data.field1.field19` gives the per-turn model id, which feeds
both the per-month turn counts and the cost estimate). Cost is an
**estimate**: assumed per-turn tokens (`ASSUMED_TOKENS_PER_TURN`) × live
per-model rates from LiteLLM. The estimate is documented as such in the
README because the real per-turn token counts are not recoverable.

## Architecture (SOLID, single-responsibility units)
- **`PricingEngine`** — fetches live per-million rates from the LiteLLM
  database every run; on failure falls back to the last successful cache,
  flagged stale. No pricing is bundled in source.
- **`ConversationStore`** — opens `~/.gemini/antigravity-cli/conversations/*.db`
  and `~/.gemini/antigravity/conversations/*.db` in read-only SQLite mode and
  aggregates per-month: estimated tokens (real per-model turn counts from
  `gen_metadata.data.field1.field19` × `ASSUMED_TOKENS_PER_TURN`) and cost
  (those tokens × live rates).
- **`Renderer`** — formats the per-month activity block.

## Conventions
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/).
- **Zero external dependencies** — standard library only.
- **Cost is always an estimate, always documented.** Antigravity doesn't
  persist per-token usage client-readable, so cost uses assumed per-turn
  tokens × live LiteLLM rates. If a future Antigravity release exposes real
  per-token usage, swap the estimate for the real calculation at that point.
- **Read-only on Antigravity state** — every SQLite open uses `?mode=ro`.
- **No AI Attribution** in commit messages.

## Release Process
- Update `README.md` whenever features change (source of truth).
- Commit using Conventional Commits.
