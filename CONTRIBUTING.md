# Contributing to Antigravity Usage

Thank you for your interest in contributing! We welcome all improvements, from bug reports to new feature ideas.

## Engineering Standards

To keep the tool lightweight, fast, and secure, all contributions must adhere to these standards:

1.  **Zero External Dependencies:** Use only the Python 3 standard library. Do not add `requirements.txt` or any third-party packages.
2.  **Antigravity-only Scope:** Track Google Antigravity (CLI + IDE) only. Do not reintroduce the deprecated Gemini CLI as a data source.
3.  **No Fabricated Costs:** Never estimate or display USD cost. Antigravity does not persist per-token usage in any client-readable form (see `GEMINI.md` for the full investigation), so any cost figure would be invented rather than measured. If a future Antigravity release exposes real per-token usage, cost support can be added at that point.
4.  **Read-only on Antigravity State:** Every SQLite open must use `?mode=ro`. Never lock or mutate Antigravity's live stores.
5.  **Single Responsibility:** Each concern stays an isolated class (`AntigravityAuth`, `CloudCodeClient`, `ConversationStore`, `Renderer`).

## Commit & Pull Request Rules

-   **Conventional Commits:** Use the [Conventional Commits](https://www.conventionalcommits.org/) format (e.g., `feat:`, `fix:`, `docs:`, `chore:`).
-   **No AI Attribution:** **Do not** include "Co-authored-by" or any other AI/agent attributions in your commit messages.
-   **Atomic Changes:** Keep PRs focused on a single fix or feature.

## Development Setup

The project is a standalone Python script. No installation is required.

### Testing Your Changes
1.  Run the script locally: `./antigravity-usage` (live account + activity).
2.  Test activity in isolation: `./antigravity-usage --no-live`.
3.  Verify read-only behaviour: `stat` a conversation DB before and after a
    run; mtime and size must be unchanged.
4.  If you touch `AntigravityAuth`, delete `~/.gemini/antigravity-usage-token.json`
    to force a fresh OAuth refresh and confirm the live block still renders.

## Code of Conduct

Be respectful, professional, and constructive in all interactions.
