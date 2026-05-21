# Antigravity Usage

A lightweight, zero-dependency CLI tool to aggregate and display token usage and cost statistics from your local Antigravity and Gemini CLI/IDE sessions.

## Overview

Antigravity Usage scans your local session logs to provide a definitive summary of token consumption and estimated costs across all Antigravity surfaces — CLI, IDE, and the original Gemini CLI. It features a "Smart Pricing Engine" that automatically stays up-to-date with the latest API rates for both Gemini and Claude models.

## Features

- **Multi-Source Collection:** Aggregates usage seamlessly from all Gemini and Antigravity CLI/IDE tools into a single view.
- **Smart Pricing Engine:** Automatically fetches the latest pricing data from the community-standard [LiteLLM database](https://github.com/BerriAI/litellm).
- **Multi-Provider Support:** Handles both Gemini and Claude/Anthropic model pricing.
- **100% Data Accuracy:** Tracks all token types, including standard input/output, thought tokens (reasoning), cached context, and tool-generated tokens.
- **Advanced Billing Rules:** Correctly applies billing nuances (e.g., thought tokens at output rates, discounted cache reads).
- **Source Breakdown:** Shows per-source token totals alongside the monthly summary.
- **Automatic Discovery:** Seamlessly locates session logs in the default data directories.
- **Zero Dependencies:** Pure Python 3 using only the standard library for maximum portability and security.

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

3. (Optional) Add an alias or symlink to your shell profile (e.g., `~/.zshrc` or `~/.bashrc`) for easier access:

   **Option A: Alias**
   ```bash
   echo "alias antigravity-usage='$(pwd)/antigravity-usage'" >> ~/.zshrc
   source ~/.zshrc
   ```

   **Option B: Symlink**
   ```bash
   sudo ln -s $(pwd)/antigravity-usage /usr/local/bin/antigravity-usage
   ```

## Usage

Simply run the command from your terminal:

```bash
antigravity-usage
```

### Example Output

```text
📊 Antigravity Usage (last 2 months):
• 2026-04: 7,436,411 tokens, Cost: $2.72
  └─ all-tools: 7,436,411 tokens
• 2026-05: 235,909,871 tokens, Cost: $90.50
  └─ all-tools: 235,909,871 tokens
```

## Data Sources

| Source | Status | Path |
|--------|--------|------|
| All Tools (Gemini CLI, Antigravity CLI & IDE) | ✅ Active | `~/.gemini/tmp/*/chats/*.jsonl` |

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

This project is licensed under the [MIT License](LICENSE).
