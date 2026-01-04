---
name: stock-screener
description: Use this skill to screen and discover stocks based on technical indicators (RSI, MACD, trends) or fundamental metrics (P/E, ROE, growth). Returns a ranked list of stocks matching criteria. Available screens: momentum, growth, value, quality, oversold, technical_buy, tech_momentum. Invoke when users want to find stocks matching specific criteria, discover investment opportunities, or screen for stocks in a particular category.
---

# Stock Screener Skill

This skill enables Claude to screen and discover stocks based on configurable technical and fundamental criteria. It uses the FMP API to fetch market data and returns a ranked list of stocks matching the specified criteria.

## When to Use This Skill

Use this skill when:
- User wants to find stocks matching specific criteria
- User asks for "oversold stocks" or "momentum stocks"
- User wants to screen for value stocks or quality stocks
- User needs to discover stocks in a specific sector
- User wants a ranked list of investment opportunities
- User asks "what stocks should I look at today?"

**Examples:**
- "Find me 5 growth stocks"
- "Screen for momentum stocks in tech sector"
- "What are the best value stocks right now?"
- "Screen for growth, value, and momentum stocks"
- "Find oversold quality stocks"
- "Give me today's top momentum picks"

## Core Capabilities

### 1. Predefined Screens

| Screen Type | Description | Key Criteria |
| ----------- | ----------- | ------------ |
| `momentum` | Stocks with strong upward momentum | RSI 50-70, above all MAs, volume increasing |
| `growth` | High-growth companies (ignores P/E) | Revenue growth >15%, EPS growth >20%, PEG <3 |
| `value` | Undervalued stocks with solid fundamentals | P/E < 15, P/B < 2, dividend yield > 2% |
| `quality` | High-quality companies with strong returns | ROE > 15%, debt/equity < 0.5, P/E < 35 |
| `oversold` | Quality stocks that are oversold | RSI < 35, above 200 SMA, P/E < 25 |
| `technical_buy` | Technical setup for potential entry | RSI 30-45, above 200 SMA, below 50 SMA |
| `tech_momentum` | Tech sector momentum (allows high P/E) | RSI 45-75, above 50 SMA, P/E < 100 |

### 2. Custom Screening

Users can specify custom criteria:
- Technical: RSI, MACD, moving averages, volume
- Fundamental: P/E, P/B, ROE, ROA, debt/equity, growth rates
- Filters: Sector, market cap, exchange

## Workflow

### Standard Screening Workflow

1. **Parse Request:** Identify screen type or custom criteria
2. **Set Parameters:** Apply defaults or user-specified values
3. **Fetch Universe:** Get list of stocks to screen (by sector, index, or all)
4. **Apply Filters:** Filter by market cap, sector, exchange
5. **Calculate Scores:** Score each stock against criteria
6. **Rank Results:** Sort by overall score
7. **Return Top N:** Return requested number of stocks with scores

## Tool Usage Instructions

### Using the Stock Screener Script

**Script Location:** `~/.claude/skills/stock-screener/scripts/stock_screener.py`

**Basic Usage:**
```bash
# Screen for momentum stocks (default: top 5)
python3 ~/.claude/skills/stock-screener/scripts/stock_screener.py --screen momentum

# Screen with limit
python3 ~/.claude/skills/stock-screener/scripts/stock_screener.py --screen oversold --limit 10

# Screen with sector filter
python3 ~/.claude/skills/stock-screener/scripts/stock_screener.py --screen value --sector Technology --limit 5

# Screen with market cap filter
python3 ~/.claude/skills/stock-screener/scripts/stock_screener.py --screen quality --min-market-cap 10000000000

# Custom criteria
python3 ~/.claude/skills/stock-screener/scripts/stock_screener.py --custom '{"rsi_max": 30, "pe_max": 20}'
```

**Required Environment Variable:**
```bash
export FMP_API_KEY=your_api_key
```

### Output Format

The screener returns JSON with:
```json
{
    "screen_type": "momentum",
    "timestamp": "2026-01-03T10:30:00Z",
    "criteria_used": {...},
    "results": [
        {
            "rank": 1,
            "ticker": "VRT",
            "name": "Vertiv Holdings",
            "price": 175.61,
            "score": 85,
            "scores": {
                "technical": 90,
                "fundamental": 80
            },
            "metrics": {
                "rsi": 47.71,
                "macd_signal": "bullish",
                "trend": "uptrend",
                "pe_ratio": 35.5,
                "roe": 0.25
            }
        },
        ...
    ],
    "total_screened": 500,
    "matches_found": 23
}
```

### Integration with Other Skills

The stock screener is designed to work with:
- **stock-analyst:** Pass screened tickers for detailed analysis
- **newsletter-formatter:** Include screened stocks in newsletters
- **researcher:** Add context about screened stocks

**Example Pipeline:**
```
User: "Screen for momentum stocks and analyze the top 3"

1. stock-screener: Returns [VRT, ETN, PWR]
2. stock-analyst: Analyzes VRT, ETN, PWR in detail
3. Combined output: Screened picks + detailed analysis
```

## Inputs

| Parameter | Type | Description | Default |
| --------- | ---- | ----------- | ------- |
| screen | string | Predefined screen type | momentum |
| limit | int | Max stocks to return | 5 |
| sector | string | Filter by sector | None (all) |
| min_market_cap | float | Minimum market cap in USD | 1000000000 (1B) |
| custom | dict | Custom criteria (JSON) | None |
| universe | string | Stock universe (sp500, nasdaq100, all) | sp500 |

## Outputs

| Field | Type | Description |
| ----- | ---- | ----------- |
| results | list | Ranked list of matching stocks |
| screen_type | string | Screen type used |
| criteria_used | dict | Actual criteria applied |
| total_screened | int | Total stocks evaluated |
| matches_found | int | Stocks matching criteria |
| timestamp | string | When screen was run |

## Best Practices

- ✅ Use predefined screens for common use cases
- ✅ Apply sector filter to focus results
- ✅ Set reasonable market cap minimum to filter penny stocks
- ✅ Combine with stock-analyst for detailed analysis of picks
- ✅ Cache results for same-day repeated screens
- ❌ Don't screen entire market without filters (slow)
- ❌ Don't use very tight criteria (may return no results)

## Error Handling

| Error | Cause | Resolution |
| ----- | ----- | ---------- |
| No results | Criteria too restrictive | Loosen criteria or change screen type |
| API timeout | FMP API slow/down | Retry with backoff |
| Invalid sector | Typo in sector name | Use valid sector from list |
| Rate limit | Too many API calls | Wait and retry |

## Available Sectors

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

*Stock Screener Skill Version: 1.0*  
*Last Updated: January 3, 2026*


