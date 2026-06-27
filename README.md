# Antigravity Usage

A lightweight, zero-dependency CLI tool that reports your Google **Antigravity**
account usage: live plan/quota straight from the API, plus conversation activity
read directly from Antigravity's own local stores.

## Scope

This tool tracks **Google Antigravity only** — the Antigravity CLI (`agy`) and
the Antigravity IDE. The original **Gemini CLI is deprecated** (end of service
**2026-06-18**, per Google's "Transitioning Gemini CLI to Antigravity CLI"
announcement) and is intentionally **not** a data source.

## How it works

Antigravity is billed as a flat-rate subscription, so Google does not surface
per-token usage to subscribers in any client-readable form. Local conversation
files are SQLite + protobuf BLOBs (not encrypted, but token counts are not
persisted in them), the JSONL transcripts carry no `UsageMetadata`, and the
CloudCode API's `retrieveUserQuota` returns only REQUEST-type quota (not
tokens). `retrieveUserQuotaSummary` is 403 for normal accounts.

So this tool reports usage from the two authoritative client-readable sources:

1. **Live account** — queries the Google CloudCode API for your tier and
   per-model quota remaining, authenticating with your existing Antigravity
   session (no extra login).
2. **Conversation activity** — reads Antigravity's local SQLite conversation
   stores directly and aggregates them into per-month conversation counts,
   step totals, and an **estimated** cost (assumed per-turn tokens × live
   per-model rates from LiteLLM).

## Features

- **Live tier & quota:** plan name and per-model quota remaining with reset times.
- **Conversation activity:** per-month conversations, steps, and estimated
  cost — sourced from Antigravity's own `conversations/*.db`.
- **Live pricing:** per-model rates fetched fresh from
  [LiteLLM](https://github.com/BerriAI/litellm) every run, with last-good
  cache reused (flagged stale) only if the source is unreachable.
- **Read-only:** every SQLite store is opened with `?mode=ro` — Antigravity's
  live state is never locked or mutated.
- **Zero dependencies:** pure Python 3 standard library.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/gigaprakosa/antigravity-usage.git
   cd antigravity-usage
   ```

2. Make the script executable:
   ```bash
   chmod +x antigravity-usage
   ```

3. (Optional) Add an alias or symlink for easier access:
   ```bash
   echo "alias antigravity-usage='$(pwd)/antigravity-usage'" >> ~/.zshrc
   source ~/.zshrc
   ```

## Usage

Show live account state plus conversation activity:

```bash
antigravity-usage
```

Skip the live lookup and show activity only:

```bash
antigravity-usage --no-live
```

The `--install-hook` flag is **deprecated and a no-op**. An earlier version of
this tool installed an Antigravity `Stop` hook to capture per-turn tokens; that
approach was removed because the `Stop` event payload does not carry token
counts (per Antigravity's official hook documentation at
`antigravity.google/docs/hooks`) and Antigravity does not persist per-token
usage client-side. Activity is now read directly from local stores, no hook
needed.

### Example output

```text
🛰️  Antigravity — Live Account
• Plan: Gemini Code Assist in Google One AI Pro (you@example.com)
• Quota remaining (resets per window):
    gemini-2.5-flash             [████████████] 100.0%  (REQUESTS, reset 2026-06-28 09:27)
    gemini-2.5-pro               [████████████] 100.0%  (REQUESTS, reset 2026-06-28 09:27)

📊 Antigravity Usage (last 2 months):
• 2026-06: 44 conversations, 3,036 steps, est. $4.18
```

> Activity accrues from the moment Antigravity first runs and writes to its
> local stores. No setup, hook, or daemon is required on your part.
>
> **Cost is an estimate.** Antigravity does not persist per-token usage
> client-readably, so we use assumed per-turn token counts (typical for
> agentic coding) × live per-model rates from
> [LiteLLM](https://github.com/BerriAI/litellm). Treat the dollar figure as
> a ballpark, not an invoice. If the live pricing fetch fails, the last good
> rates are reused and a `pricing is STALE` warning is printed.

## Data sources

| Source | What it provides | Path / Endpoint |
|--------|------------------|-----------------|
| CloudCode API | Live tier + per-model quota | `cloudcode-pa.googleapis.com` (`loadCodeAssist`, `retrieveUserQuota`) |
| Auth (refresh token) | Bearer for the API | Antigravity IDE `state.vscdb` (`antigravityUnifiedStateSync.oauthToken`), fallback `~/.gemini/oauth_creds.json` |
| Conversation activity | Conversation count, step totals, model mix | `~/.gemini/antigravity-cli/conversations/*.db` and `~/.gemini/antigravity/conversations/*.db` (read-only) |

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

This project is licensed under the [MIT License](LICENSE).
