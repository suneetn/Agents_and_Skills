---
name: analyst-light
description: Generate quick actionable trade setups with entry, target, stop loss, and mini-thesis. Use when you need fast trade ideas without full analysis depth.
version: 1.0
---

# Analyst Light

Quick actionable trade analysis for stocks. Generates entry points, price targets, stop losses, and concise investment thesis in seconds.

## When to Use This Skill

- User wants a quick trade setup for a stock
- User asks "where should I buy/sell X?"
- User wants entry, target, and stop levels
- Generating actionable content for newsletters
- Need fast analysis (5 seconds vs 30+ for full analyst)

## Core Capabilities

1. **Technical Levels**
   - Support levels (potential entries)
   - Resistance levels (potential targets)
   - ATR-based stop loss calculation
   - Trend bias (bullish/bearish/neutral)

2. **Quick Fundamental Context**
   - Mini-thesis (2-3 sentences)
   - Top risk factor
   - Growth metrics summary

3. **Trade Setup Output**
   - Entry price/zone with reasoning
   - Target price with upside %
   - Stop loss with downside %
   - Recommended timeframe

## Workflow

### Single Stock Analysis

```bash
cd ~/.claude/skills/analyst-light/scripts
export FMP_API_KEY="your_key"
python3 analyst_light.py SYMBOL
```

### Multiple Stocks (Batch)

```bash
python3 analyst_light.py AAPL MSFT GOOGL --format json
```

### Output Formats

- `--format text` (default): Human-readable summary
- `--format json`: Structured data for integration
- `--format newsletter`: Pre-formatted for email

## Tool Usage Instructions

### Script Location
`~/.claude/skills/analyst-light/scripts/analyst_light.py`

### Required Environment
```bash
export FMP_API_KEY="your_fmp_api_key"
```

### API Endpoints Used
- `/v3/quote/{symbol}` - Current price
- `/v3/historical-price-full/{symbol}` - Price history for technicals
- `/v3/profile/{symbol}` - Company info for thesis
- `/v3/financial-growth/{symbol}` - Growth metrics
- `/v3/rating/{symbol}` - FMP rating

## Output Structure

### JSON Output
```json
{
  "symbol": "MU",
  "name": "Micron Technology, Inc.",
  "price": 315.42,
  "change_percent": 10.5,
  "trade_setup": {
    "bias": "bullish",
    "entry": {
      "price": 305.0,
      "zone": [300, 310],
      "reason": "20 SMA support zone"
    },
    "target": {
      "price": 380.0,
      "upside_percent": 20.5,
      "reason": "Previous resistance + round number"
    },
    "stop": {
      "price": 280.0,
      "downside_percent": 11.2,
      "reason": "Below support, 2x ATR buffer"
    },
    "risk_reward": 1.83,
    "timeframe": "3-6 months"
  },
  "thesis": {
    "summary": "Memory leader benefiting from AI datacenter demand surge. EPS +993% YoY with expanding margins as supply tightens.",
    "top_risk": "Semiconductor cyclicality and China trade exposure",
    "catalyst": "Q1 earnings Jan 15 expected to beat"
  },
  "metrics": {
    "pe_ratio": 25.3,
    "eps_growth": 993.0,
    "revenue_growth": 45.2,
    "fmp_rating": "A+"
  }
}
```

### Text Output
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MU - Micron Technology | $315.42 (+10.5%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BIAS: 🟢 BULLISH | Rating: A+ Strong Buy

📊 TRADE SETUP
   Entry:  $300-310 (20 SMA support)
   Target: $380 (+20.5%)
   Stop:   $280 (-11.2%)
   R:R:    1.83

💡 THESIS
   Memory leader benefiting from AI datacenter demand.
   EPS +993% YoY with expanding margins.

⚠️  RISK: Semiconductor cyclicality, China exposure
⏱️  TIMEFRAME: 3-6 months
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Examples

### Quick Trade Setup
```
User: "Give me a trade setup for NVDA"
Action: Run analyst_light.py NVDA
Output: Entry/target/stop with thesis
```

### Batch for Newsletter
```
User: "Get trade setups for MU, LRCX, AMD"
Action: Run analyst_light.py MU LRCX AMD --format json
Output: JSON array of trade setups
```

### Integration with Daily Newsletter
```python
from analyst_light import AnalystLight

analyst = AnalystLight()
for stock in screened_stocks:
    setup = analyst.get_trade_setup(stock["ticker"])
    stock["trade_setup"] = setup
```

## Trigger Phrases

- "Trade setup for X"
- "Where should I buy X?"
- "Entry and target for X"
- "Quick analysis on X"
- "Actionable levels for X"

## Performance

- **Speed:** ~5 seconds per stock
- **API Calls:** 5 per stock
- **Accuracy:** Technical levels based on 60-day price history

## Limitations

- Does not include news/sentiment (use stock-screener enrichment for that)
- Technical levels are algorithmic, not pattern-based
- Thesis is template-generated from metrics, not LLM-generated
- Best for swing trading timeframes (weeks to months)

## Related Skills

- `stock-screener` - Find stocks to analyze
- `stock-analyst` - Full comprehensive analysis
- `daily-newsletter` - Orchestrates newsletter generation



