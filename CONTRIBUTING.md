# Contributing to Antigravity Usage

Thank you for your interest in contributing! We welcome all improvements, from bug reports to new feature ideas.

## Engineering Standards

To keep the tool lightweight, fast, and secure, all contributions must adhere to these standards:

1.  **Zero External Dependencies:** Use only the Python 3 standard library. Do not add `requirements.txt` or any third-party packages.
2.  **Antigravity-only Scope:** Track Google Antigravity (CLI + IDE) only. Do not reintroduce the deprecated Gemini CLI as a data source.
3.  **Live Pricing Only:** Rates must be fetched live online (LiteLLM) every run. Never bundle a static `pricing.json`.
4.  **Single Responsibility:** Each concern stays an isolated class (`AntigravityAuth`, `CloudCodeClient`, `PricingEngine`, `UsageLedger`, `Renderer`).

## Commit & Pull Request Rules

-   **Conventional Commits:** Use the [Conventional Commits](https://www.conventionalcommits.org/) format (e.g., `feat:`, `fix:`, `docs:`, `chore:`).
-   **No AI Attribution:** **Do not** include "Co-authored-by" or any other AI/agent attributions in your commit messages.
-   **Atomic Changes:** Keep PRs focused on a single fix or feature.

## Development Setup

The project is a standalone Python script. No installation is required.

### Testing Your Changes
1.  Run the script locally: `./antigravity-usage` (live account + history).
2.  Test history/pricing in isolation: `./antigravity-usage --no-live` after appending a sample line to `~/.gemini/antigravity-cli/usage-ledger.jsonl`.
3.  Verify the hook end-to-end: `./antigravity-usage --install-hook`, then run an Antigravity turn and confirm a new ledger line.

## Code of Conduct

Be respectful, professional, and constructive in all interactions.
