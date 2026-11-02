# Contributing to Antigravity Usage

Thank you for your interest in contributing! We welcome all improvements, from bug reports to new feature ideas.

## Engineering Standards

To keep the tool lightweight, fast, and secure, all contributions must adhere to these standards:

1.  **Zero External Dependencies:** Use only the Python 3 standard library. Do not add `requirements.txt` or any third-party packages.
2.  **Antigravity-only Scope:** Track Google Antigravity CLI only. Do not reintroduce the separate Gemini CLI as a data source.
3.  **Cost Is Always An Estimate, Always Documented:** The CLI reader does not recover per-turn token counts, so cost uses assumed per-turn tokens (`ASSUMED_TOKENS_PER_TURN` table) × live per-model rates from models.dev (same source oc-usage uses). If a future Antigravity release exposes real per-token usage, swap the estimate for the real calculation at that point.
4.  **Read-only on Antigravity State:** Every SQLite open must use `?mode=ro`. Do not mutate Antigravity's live stores.
5.  **Single Responsibility:** Each concern stays an isolated class (`PricingEngine`, `ConversationStore`, `Renderer`).

## Commit & Pull Request Rules

-   **Conventional Commits:** Use the [Conventional Commits](https://www.conventionalcommits.org/) format (e.g., `feat:`, `fix:`, `docs:`, `chore:`).
-   **No AI Attribution:** **Do not** include "Co-authored-by" or any other AI/agent attributions in your commit messages.
-   **Atomic Changes:** Keep PRs focused on a single fix or feature.

## Development Setup

The project is a standalone Python script. No installation is required.

### Testing your changes

1.  Run the script locally: `./antigravity-usage`.
2.  Verify read-only behaviour: `stat` a conversation DB before and after a
    run; mtime and size must be unchanged.
3.  Pricing is fetched fresh on every run. The fallback cache is
    `~/.cache/antigravity-usage/models-dev.json`.

## Code of Conduct

Be respectful, professional, and constructive in all interactions.

## CLI compatibility and verification

The supported source is the dedicated Antigravity CLI SQLite store. App and
IDE history are outside scope. [README.md](README.md) documents source paths,
estimate limitations, and pricing behavior.

Run `python3 -m unittest discover -v` and
`python3 -m py_compile antigravity-usage test_usage.py` before committing.
No typechecker is configured. Run `./antigravity-usage` and compare source
DB size and modification time before and after the run.
