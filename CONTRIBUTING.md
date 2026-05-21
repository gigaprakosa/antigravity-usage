# Contributing to Antigravity Usage

Thank you for your interest in contributing! We welcome all improvements, from bug reports to new feature ideas.

## Engineering Standards

To keep the tool lightweight, fast, and secure, all contributions must adhere to these standards:

1.  **Zero External Dependencies:** Use only the Python 3 standard library. Do not add `requirements.txt` or any third-party packages.
2.  **Smart Pricing Integrity:** If adding support for new models, ensure they are compatible with the fuzzy matching logic in the Smart Pricing Engine.
3.  **Data Accuracy:** Changes to the parsing logic must be verified against raw session logs.
4.  **Collector Pattern:** New data sources should be implemented as a subclass of `UsageCollector` and registered in the `COLLECTORS` list.

## Commit & Pull Request Rules

-   **Conventional Commits:** Use the [Conventional Commits](https://www.conventionalcommits.org/) format (e.g., `feat:`, `fix:`, `docs:`, `chore:`).
-   **No AI Attribution:** **Do not** include "Co-authored-by" or any other AI/agent attributions in your commit messages.
-   **Atomic Changes:** Keep PRs focused on a single fix or feature.

## Development Setup

The project is a standalone Python script. No installation is required.

### Testing Your Changes
1.  Run the script locally: `./antigravity-usage`
2.  Verify the output format remains consistent with the bullet-point style with source breakdown.
3.  If you are testing pricing updates, you can temporarily modify `pricing.json` to see how overrides are handled.

## Code of Conduct

Be respectful, professional, and constructive in all interactions.
