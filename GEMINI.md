# Antigravity Usage

## Description
A CLI tool to report Google **Antigravity** account usage — live tier/quota plus
forward-captured token cost. Scoped to Antigravity (CLI + IDE) only; the legacy
Gemini CLI is deprecated (EOL 2026-06-18) and is **not** a data source.

## Tech Stack
- Python 3 (Standard Library Only — `urllib`, `json`, `sqlite3`, `base64`).

## Why this design
Antigravity does not persist historical token usage in any readable form: the
local conversation store (`~/.gemini/antigravity-cli/conversations/*.pb`) is
encrypted (macOS Keychain "Antigravity Safe Storage"), the JSONL transcripts and
IDE `state.vscdb` carry no token counts, and per-response `UsageMetadata` is
discarded. The CloudCode API exposes current quota but **no** historical-usage
endpoint. So usage is sourced from the two authoritative places that exist.

## Architecture (SOLID, single-responsibility units)
- **`AntigravityAuth`** — mints a Bearer for the user's own account. Extracts the
  refresh token from the IDE state DB (`state.vscdb` → `oauthToken` → nested
  protobuf, field 3), falls back to `~/.gemini/oauth_creds.json`, and refreshes
  against Google OAuth. OAuth client pairs are discovered from the public `agy`
  binary; every id × secret combination is tried so the correct pair self-selects.
- **`CloudCodeClient`** — `cloudcode-pa.googleapis.com`:
  `v1internal:loadCodeAssist` (tier) and `v1internal:retrieveUserQuota` (per-model
  quota remaining).
- **`PricingEngine`** — fetches live per-million rates from the LiteLLM database
  **every run**; on failure falls back to the last successful cache, flagged
  stale. No pricing data is bundled in the repo.
- **`UsageLedger`** — reads the JSONL ledger appended by the Antigravity `Stop`
  hook and aggregates by month → model.
- **`Renderer`** — formats the live account block and the priced history.
- **Hook (`--install-hook`)** — writes a `Stop` hook + recorder that captures
  per-turn `model`/token counts into `~/.gemini/antigravity-cli/usage-ledger.jsonl`.

## Conventions
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/).
- **Zero external dependencies** — standard library only.
- Pricing is always live online; never reintroduce a static `pricing.json`.
- **No AI Attribution** in commit messages.

## Release Process
- Update `README.md` whenever features change (source of truth).
- Commit using Conventional Commits.
