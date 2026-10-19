# IOL Performance Analyzer Skill for Gemini CLI

Calculates and analyzes Month-To-Date (MTD) and period-over-period financial returns, capital flow adjustments, and corporate actions (e.g. stock splits) for InvertirOnline (IOL) portfolios.

## Features

- **Corporate Action Adjustments**: Correctly handles stock splits and stock dividends (e.g. YPFD 10-for-1 split).
- **Cash Flow Normalization**: Disaggregates external deposits and fund subscriptions from true capital appreciation.
- **Security Hardened**: Strictly validates input JSON schemas, rejects unbounded payloads, enforces numeric sanity, and isolates sensitive financial records from git tracking.
- **Multi-Currency Support**: Segregates ARS and USD asset valuations and performance metrics.

## Usage

Ask Gemini CLI to analyze your IOL performance:

> "Analyze my IOL portfolio performance for this month, adjust for any stock splits or cash deposits, and explain the main drivers of gains and losses."

Or run the calculation script directly:

```bash
python3 scripts/calc_mtd.py --portfolio examples/portfolio_data.json
```

## Security & Hardening

1. **No Hardcoded Secrets**: Authentication is handled exclusively through MCP tools or environment variables. No tokens or API keys are stored in scripts or markdown files.
2. **Data Exclusion**: Live portfolio files (`portfolio*.json`, `balance*.json`, `activities*.json`) are excluded via `.gitignore` to prevent leaking private holdings or tax IDs. Only sanitized dummy fixtures (`examples/portfolio_data.json`) are committed.
3. **Safe Parsing**: `scripts/calc_mtd.py` enforces maximum file size limits (10 MB), validates finite numbers, and sanitizes currency inputs.

## Project Structure

- `SKILL.md`: Metadata, prompt guidance, and analysis workflow.
- `scripts/calc_mtd.py`: Hardened performance calculation script.
- `examples/portfolio_data.json`: Anonymized sample portfolio fixture.
- `.gitignore`: Skill-specific ignore rules for credentials and financial exports.
