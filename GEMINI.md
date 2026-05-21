# Antigravity Usage

## Description
A CLI tool to track token usage and costs across all Antigravity and Gemini CLI/IDE sessions with 100% data accuracy.

## Tech Stack
- Python 3 (Standard Library Only)

## Architecture: Modular Collectors + Smart Pricing Engine
- **Collectors:** `GeminiCLICollector` (active), `AntigravityCLICollector` (stub), `AntigravityIDECollector` (stub).
- **Pricing — Tiered Loading:** Local Cache → LiteLLM community database → Repo Override (`pricing.json`) → Hardcoded Defaults.
- **Fuzzy Matching:** Maps local model strings (e.g., `-preview`, `-canary`) to standardized pricing entries.
- **Multi-Provider:** Supports Gemini and Anthropic (Claude) model pricing.
- **Auto-Update:** 24-hour cache TTL for remote pricing data.

## Conventions
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code.
- Ensure **zero external dependencies** are added. Use `urllib.request` and `json` for all networking/parsing.
- Output format must remain consistent with the bullet-point style with source breakdown.
- **No AI Attribution:** Do not include "Co-authored-by" or any other AI/agent attributions in commit messages.

## Release Process
- Update `pricing.json` if manual overrides are required.
- Update `README.md` if features change.
- Commit using Conventional Commits.
