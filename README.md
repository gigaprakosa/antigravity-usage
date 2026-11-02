# Antigravity Usage

A lightweight, zero-dependency CLI that reports Google **Antigravity**
conversation activity and estimated cost for the last 2 months. Same
one-line-per-month format as [`oc-usage`](https://github.com/sst/opencode)
and [`ccusage`](https://github.com/ryoppippi/ccusage).

## Scope

Google Antigravity CLI only. The separate Gemini CLI is not a data source.

## How it works

The CLI SQLite reader extracts model-response counts from `gen_metadata`
protobuf fields. The report estimates tokens from those counts; it does not
measure the tokens used by each turn.

So this tool reads Antigravity's local SQLite conversation stores directly
and aggregates per-month:

- **Tokens**, estimated, from real per-model turn counts (extracted from
  `gen_metadata` BLOBs) × assumed per-turn token sizes typical for agentic
  coding.
- **Cost**, those estimated tokens × live per-model rates from
  [models.dev](https://models.dev) (the same source
  [`oc-usage`](https://github.com/sst/opencode) uses), fetched fresh every
  run.

Both figures are estimates, treat them as a ballpark, not an invoice.

## Install

```bash
git clone https://github.com/gigaprakosa/antigravity-usage.git
cd antigravity-usage
chmod +x antigravity-usage
# optional: put it on your PATH
ln -sf "$(pwd)/antigravity-usage" ~/.local/bin/agy-usage
```

## Usage

```bash
agy-usage
```

That's it, no flags, no subcommands.

### Example output

```text
📊 Antigravity Usage (last 2 months):
• 2026-06: 7,211,600 estimated tokens, Cost: $4.18
```

If the live pricing fetch fails, a usable cache supplies fallback rates.
Without usable pricing, cost displays `unknown`. The CLI emits its stale
pricing warning on stderr when the fetch fails.

## Data sources

| Source | What it provides | Path |
|--------|------------------|------|
| Conversation activity | Per-model turn counts | `~/.gemini/antigravity-cli/conversations/*.db` (read-only) |
| Pricing | Live per-million rates | [models.dev](https://models.dev/api.json) (same source oc-usage uses) |

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

This project is licensed under the [MIT License](LICENSE).

## CLI compatibility and verification

Only `~/.gemini/antigravity-cli/conversations/*.db` is scanned by default.
App and IDE stores, backups, and legacy `.pb` files are outside scope.
Tokens and API-equivalent costs are estimates. Conversation activity is
assigned to the database modification month (UTC), not each turn's date.
Missing pricing displays `Cost: unknown`.

Run `python3 -m unittest discover -v` and
`python3 -m py_compile antigravity-usage test_usage.py`.
No typechecker is configured. Run `./antigravity-usage` for a live check.
