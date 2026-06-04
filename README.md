# Antigravity Usage

A lightweight, zero-dependency CLI tool that reports your Google **Antigravity**
account usage: live plan/quota straight from the API, plus token cost from a
local ledger priced with up-to-the-minute online rates.

## Scope

This tool tracks **Google Antigravity only** — the Antigravity CLI (`agy`) and
the Antigravity IDE. The original **Gemini CLI is deprecated** (end of service
**2026-06-18**, per Google's "Transitioning Gemini CLI to Antigravity CLI"
announcement) and is intentionally **not** a data source.

## How it works

Antigravity does not store historical token usage anywhere readable — local
conversation files are encrypted, transcripts carry no token counts, and the API
exposes current quota but no usage history. So this tool reports the two sources
that *are* authoritative:

1. **Live account** — queries the Google CloudCode API for your tier and
   per-model quota remaining, authenticating with your existing Antigravity
   session (no extra login).
2. **Token cost history** — an optional Antigravity `Stop` hook records each
   turn's token usage to a local ledger, which is then priced using **live online
   rates fetched every run** (no bundled price list).

## Features

- **Live tier & quota:** plan name and per-model quota remaining with reset times.
- **Always-current pricing:** rates are fetched live from the community-standard
  [LiteLLM database](https://github.com/BerriAI/litellm) on every run; the last
  successful fetch is cached and reused (flagged stale) only if the source is
  unreachable. No `pricing.json` is shipped.
- **Forward token capture:** a one-command hook install records real per-turn
  token counts (Gemini and Claude models) going forward.
- **Multi-provider pricing:** Gemini and Claude/Anthropic models.
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

Show live account state plus any captured token history:

```bash
antigravity-usage
```

Install the hook so token usage is recorded going forward (run once):

```bash
antigravity-usage --install-hook
```

Skip the live lookup and show captured history only:

```bash
antigravity-usage --no-live
```

### Example output

```text
🛰️  Antigravity — Live Account
• Plan: Gemini Code Assist in Google One AI Pro (you@example.com)
• Quota remaining (resets per window):
    gemini-2.5-pro               [████████████] 100.0%  (REQUESTS, reset 2026-06-05 15:21)
    gemini-3.1-flash-lite        [██████████··]  84.0%  (REQUESTS, reset 2026-06-05 15:21)

📊 Captured token usage (1 month(s)), priced live:
• 2026-06: 9,300 tokens, Cost: $0.09
```

> Token history starts empty and accrues only after you install the hook and use
> Antigravity. Historical usage from before installation is not recoverable.

## Data sources

| Source | What it provides | Path / Endpoint |
|--------|------------------|-----------------|
| CloudCode API | Live tier + per-model quota | `cloudcode-pa.googleapis.com` (`loadCodeAssist`, `retrieveUserQuota`) |
| Auth | Refresh token for the API | Antigravity IDE `state.vscdb`, fallback `~/.gemini/oauth_creds.json` |
| Usage ledger | Forward-captured per-turn tokens | `~/.gemini/antigravity-cli/usage-ledger.jsonl` (written by the `Stop` hook) |
| Pricing | Live per-million rates | [LiteLLM raw JSON](https://raw.githubusercontent.com/BerriAI/litellm/main/model_prices_and_context_window.json) |

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

This project is licensed under the [MIT License](LICENSE).
