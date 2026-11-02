# Antigravity Usage

A lightweight, zero-dependency CLI that reports Google **Antigravity**
conversation activity and estimated cost for the last 2 months. Same
one-line-per-month format as [`oc-usage`](https://github.com/sst/opencode)
and [`ccusage`](https://github.com/ryoppippi/ccusage).

## Scope

Google Antigravity only (CLI + IDE). The original **Gemini CLI is deprecated**
(end of service 2026-06-18) and is intentionally **not** a data source.

## How it works

Antigravity is billed as a flat-rate subscription, so Google does not surface
per-token usage to subscribers in any client-readable form. Local conversation
files are SQLite + protobuf BLOBs (not encrypted, but token counts are not
persisted in them), the JSONL transcripts carry no `UsageMetadata`, and the
CloudCode API's `retrieveUserQuota` returns only REQUEST-type quota (not
tokens).

So this tool reads Antigravity's local SQLite conversation stores directly
and aggregates per-month:

- **Tokens** — estimated, from real per-model turn counts (extracted from
  `gen_metadata` BLOBs) × assumed per-turn token sizes typical for agentic
  coding.
- **Cost** — those estimated tokens × live per-model rates from
  [models.dev](https://models.dev) (the same source
  [`oc-usage`](https://github.com/sst/opencode) uses), fetched fresh every
  run.

Both figures are estimates — treat them as a ballpark, not an invoice.

## Install

```bash
git clone https://github.com/gigaprakosa/antigravity-usage.git
cd antigravity-usage
chmod +x antigravity-usage
# optional: put it on your PATH
ln -sf "$(pwd)/antigravity-usage ~/.local/bin/agy-usage"
```

## Usage

```bash
agy-usage
```

That's it — no flags, no subcommands.

### Example output

```text
📊 Antigravity Usage (last 2 months):
• 2026-06: 7,211,600 tokens, Cost: $4.18
```

If the live pricing fetch fails, the last good rates are reused and a
`pricing is STALE` warning is printed on stderr.

## Data sources

| Source | What it provides | Path |
|--------|------------------|------|
| Conversation activity | Per-model turn counts | `~/.gemini/antigravity-cli/conversations/*.db` and `~/.gemini/antigravity/conversations/*.db` (read-only) |
| Pricing | Live per-million rates | [models.dev](https://models.dev/api.json) (same source oc-usage uses) |

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

This project is licensed under the [MIT License](LICENSE).

## Compatibility checkpoint

Run regression checks with `python3 -m unittest discover -v` and syntax checks
with `python3 -m py_compile antigravity-usage`. No typechecker is configured.

The App, CLI, and separate IDE conversation directories are scanned for
SQLite stores, including `~/.gemini/antigravity-ide/conversations`.
Legacy `.pb` history is not decoded yet, so full IDE compatibility is pending.
Tokens are labeled estimated in CLI output. Missing pricing displays unknown.
