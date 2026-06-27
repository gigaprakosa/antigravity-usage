# Antigravity Usage

## Description
A CLI tool to report Google **Antigravity** account usage — live tier/quota
plus conversation activity read from Antigravity's own local stores. Scoped to
Antigravity (CLI + IDE) only; the legacy Gemini CLI is deprecated
(EOL 2026-06-18) and is **not** a data source.

## Tech Stack
- Python 3 (Standard Library Only — `urllib`, `json`, `sqlite3`, `base64`).

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

So usage is sourced from the two authoritative places that ARE client-readable:
the live CloudCode API for tier/quota, and Antigravity's local conversation
SQLite stores for activity metrics.

The tool deliberately does **not** estimate USD cost. Without a reliable
per-token source, any cost figure would be fabricated.

## Architecture (SOLID, single-responsibility units)
- **`AntigravityAuth`** — mints a Bearer for the user's own account. Walks the
  `antigravityUnifiedStateSync.oauthToken` envelope field-by-field
  (b64 → wrapper.f1 → inner.f2 → payload.f1 → b64 → OAuthTokenInfo.f3 =
  refresh_token), falls back to `~/.gemini/oauth_creds.json`, then refreshes
  against Google OAuth using a client pair scanned from the public `agy`
  binary (cached after first successful refresh — no credentials ship in this
  source).
- **`CloudCodeClient`** — `cloudcode-pa.googleapis.com`:
  `v1internal:loadCodeAssist` (tier) and `v1internal:retrieveUserQuota`
  (per-model quota remaining).
- **`ConversationStore`** — opens `~/.gemini/antigravity-cli/conversations/*.db`
  and `~/.gemini/antigravity/conversations/*.db` in read-only SQLite mode and
  aggregates: conversation count, step totals (per `step_type`), per-month
  buckets, and the model mix (from `gen_metadata.data.field1.field19`).
- **`Renderer`** — formats the live account block and the activity block.

## Conventions
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/).
- **Zero external dependencies** — standard library only.
- **No cost estimation** — never reintroduce a fabricated USD figure. If a
  future Antigravity release exposes real per-token usage, add it then.
- **Read-only on Antigravity state** — every SQLite open uses `?mode=ro`.
- **No AI Attribution** in commit messages.

## Release Process
- Update `README.md` whenever features change (source of truth).
- Commit using Conventional Commits.
