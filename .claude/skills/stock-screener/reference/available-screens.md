# Available Stock Screens

## Predefined Screens

### 1. Momentum
**Command:** `--screen momentum`

**Description:** Stocks with strong upward momentum and positive technical signals.

**Criteria:**
- RSI between 50-70 (strong but not overbought)
- Price above 50-day SMA
- Price above 200-day SMA
- P/E ratio under 50
- Technical weight: 70%

**Best for:** Trend followers looking for stocks in established uptrends.

---

### 2. Oversold Quality
**Command:** `--screen oversold`

**Description:** Quality stocks that are technically oversold, potential bounce candidates.

**Criteria:**
- RSI under 35 (oversold)
- Price above 200-day SMA (long-term uptrend intact)
- P/E ratio under 25
- ROE above 10%
- Technical weight: 60%

**Best for:** Contrarian investors looking for quality stocks on pullbacks.

---

### 3. Deep Value
**Command:** `--screen value`

**Description:** Undervalued stocks with solid fundamentals and dividends.

**Criteria:**
- P/E ratio under 15
- Price/Book under 2.0
- Dividend yield above 2%
- Debt/Equity under 1.0
- ROE above 8%
- Technical weight: 30%

**Best for:** Value investors seeking cheap stocks with margin of safety.

---

### 4. Quality Growth
**Command:** `--screen quality`

**Description:** High-quality companies with strong returns and low debt.

**Criteria:**
- ROE above 15%
- Debt/Equity under 0.5
- P/E ratio under 35
- Price above 200-day SMA
- Technical weight: 40%

**Best for:** Long-term investors seeking quality compounders.

---

### 5. Technical Buy Setup
**Command:** `--screen technical_buy`

**Description:** Stocks with bullish technical setups near support.

**Criteria:**
- RSI between 30-45 (oversold but recovering)
- Price above 200-day SMA (uptrend)
- Price below 50-day SMA (pullback)
- Technical weight: 80%

**Best for:** Technical traders looking for pullback entries in uptrends.

---

## Custom Screens

You can create custom screens by passing JSON criteria:

```bash
python3 stock_screener.py --custom '{"rsi_max": 30, "pe_max": 20, "roe_min": 0.12}'
```

### Available Criteria Parameters

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| rsi_min | float | Minimum RSI value |
| rsi_max | float | Maximum RSI value |
| pe_max | float | Maximum P/E ratio |
| pb_max | float | Maximum Price/Book |
| roe_min | float | Minimum ROE (decimal, e.g., 0.15 = 15%) |
| debt_equity_max | float | Maximum Debt/Equity ratio |
| dividend_yield_min | float | Minimum dividend yield (decimal) |
| above_sma_50 | bool | Require price > 50 SMA |
| above_sma_200 | bool | Require price > 200 SMA |
| below_sma_50 | bool | Require price < 50 SMA |
| volume_surge | bool | Require volume > 1.5x average |
| technical_weight | float | Weight for technical (0-1) |

---

## Sector Filters

Use `--sector` to filter by sector:

- Technology
- Healthcare
- Financial Services
- Consumer Cyclical
- Consumer Defensive
- Industrials
- Energy
- Utilities
- Real Estate
- Basic Materials
- Communication Services

---

## Examples

```bash
# Momentum stocks in tech sector
python3 stock_screener.py --screen momentum --sector Technology --limit 10

# Oversold value stocks
python3 stock_screener.py --screen oversold --limit 5

# Quality stocks with large market cap
python3 stock_screener.py --screen quality --min-market-cap 50000000000

# Custom screen for dividend stocks
python3 stock_screener.py --custom '{"dividend_yield_min": 0.03, "pe_max": 20, "debt_equity_max": 0.5}'
```



