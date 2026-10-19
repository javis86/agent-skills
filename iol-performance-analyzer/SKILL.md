---
name: iol-performance-analyzer
description: >-
  Use when fetching, calculating, or analyzing month-to-date (MTD) or period-over-period
  financial performance, earnings, stock splits, and loss/gain causes of an InvertirOnline (IOL) portfolio.
---

# IOL Portfolio MTD Earnings & Performance Analyzer

This skill provides a structured procedure and helper tools to fetch an InvertirOnline (IOL) portfolio's current state, retrieve historical prices from a baseline date (e.g., the last day of the previous month), adjust for corporate actions (like stock splits or stock dividends), account for capital flows (deposits/withdrawals/subscriptions), and perform a comprehensive financial performance analysis.

## Security & Privacy Considerations

* **Credential & Secret Protection:** Never hardcode IOL credentials, API tokens, or session tokens in scripts, documentation, or version-controlled files. Authenticate strictly via environment variables or secure MCP configurations.
* **Confidential Portfolio Data:** Live portfolio holdings, transaction histories, and cash balances constitute private financial data. Never commit live portfolio JSON exports or real account identifiers to git.
* **Safe Working Directory:** When saving temporary portfolio snapshots for calculation, place them in local git-ignored directories (e.g., `/tmp` or scratch directories excluded via `.gitignore`).
* **Input Validation:** Use hardened calculation scripts (such as `scripts/calc_mtd.py`) that enforce file size limits, schema checks, and finite numeric validation.

## Workflow

### 1. Retrieve Current Portfolio & Cash Balance
*   Call `get_portfolio` to fetch current assets, unit prices, and quantities.
*   Call `get_balance` to get the current cash balance in ARS and USD.

### 2. Fetch Account Activities
*   Call `get_activities` for the target period (e.g., start of the month to current date) to identify:
    *   External capital inflows/outflows (Deposits, Withdrawals).
    *   Dividend payments (Cash dividends or Stock dividends).
    *   FCI Subscriptions/Redemptions.
    *   Asset trades (Buys/Sells).

### 3. Retrieve Baseline Price History
*   For each asset in the portfolio, call `get_price_history` using the baseline date (e.g., last day of the previous month) to find the baseline close price.
*   **Important:** `get_price_history` works for Equities, CEDEARs, Bonds (ONs), and Mutual Funds (FCI) on the `BCBA` market.

### 4. Adjust for Corporate Actions & Capital Flows
*   **Stock Splits / Stock Dividends:** If a stock split or stock dividend occurred (e.g., YPFD 10-for-1 split in late July/early August 2026), you must adjust the starting share count and unit price to match the new share structure.
    $$\text{Adjusted Start Price} = \frac{\text{Pre-split Price}}{\text{Split Ratio}}$$
    $$\text{Adjusted Start Quantity} = \text{Pre-split Quantity} \times \text{Split Ratio}$$
*   **FCI Subscriptions:** For mutual funds subscribed during the period, calculate earnings by subtracting the capital subscribed during the month from the final valuation:
    $$\text{Net Fund Earnings} = \text{Current Value} - \text{Baseline Value} - \text{Capital Subscribed}$$
*   **Cash Flow Valuation:** Do not count capital transfers between cash and funds as earnings. MTD Earnings must represent capital appreciation/depreciation, not deposits:
    $$\text{Portfolio MTD Earnings} = (\text{Final Portfolio Value} - \text{Initial Portfolio Value}) - \text{External Deposits}$$

### 5. Execute the Math
*   Use the python script [calc_mtd.py](./scripts/calc_mtd.py) to automatically parse the starting and ending portfolios and calculate net earnings per asset and for the overall portfolio:
    ```bash
    python3 scripts/calc_mtd.py --portfolio path/to/portfolio.json
    ```

### 6. Perform Cause-of-Loss/Gain Analysis
*   **Local Stocks:** Check local financial news for the S&P Merval index. Determine if a general index correction or profit-taking is impacting local stocks (e.g., YPFD, PAMP).
*   **CEDEARs (US Tech & Global Stocks):** Assess global market performance and financial dollar movements (MEP/CCL). CEDEARs in ARS often appreciate if the local dollar exchange rate rises, acting as an inflation/devaluation hedge.
*   **USD Money Market Funds:** Explain that minor fluctuations in dollar funds (e.g., IOLDOLD, ADCGLOA) are normal results of management fees or small yield fluctuations in short-term corporate debt.
