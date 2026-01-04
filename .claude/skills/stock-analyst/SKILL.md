---
name: stock-analyst
description: Use this skill when analyzing stocks, performing fundamental analysis, conducting technical analysis, evaluating investments, comparing stocks, screening securities, or generating investment recommendations. This includes analyzing company financials, ratios, growth metrics, price patterns, technical indicators, trends, valuation metrics, risk assessment, and sentiment analysis. Invoke when users mention stock tickers, fundamental analysis, technical analysis, investment research, stock screening, financial ratios, technical indicators, or investment recommendations.
---

# Stock Analyst Skill

This skill enables Claude to perform comprehensive stock analysis combining fundamental analysis (company financials, ratios, growth) with technical analysis (price patterns, indicators, trends) to provide complete investment insights. **The workflow includes AI interpretation** of all metrics, contextual explanations, and narrative synthesis to deliver actionable investment recommendations.

## When to Use This Skill

Use this skill when:
- User asks to analyze a stock ticker (e.g., "Analyze NVDA", "Do analysis on AAPL")
- User requests fundamental analysis of a stock
- User requests technical analysis of a stock
- User wants combined fundamental + technical analysis
- User asks for investment recommendation on a stock
- User wants to compare stocks using both fundamental and technical metrics
- User wants to analyze multiple stocks at once (batch analysis)
- User wants to benchmark a stock against competitors
- User requests stock screening based on financial metrics or technical patterns

**Examples:**
- "Analyze NVDA"
- "Do fundamental analysis on Apple"
- "What's the technical analysis for Microsoft?"
- "Give me a complete analysis of TSLA including fundamentals and technicals"
- "Compare AAPL vs MSFT using fundamental and technical analysis"
- "Analyze these 5 stocks: UNH CI HUM CNC MOH"
- "Compare the top datacenter stocks"
- "Benchmark PLTR against its top 5 competitors"
- "Screen for stocks with P/E < 20 and RSI < 30"

## Core Capabilities

### 1. Fundamental Analysis (Using FMP API)

**Capability:** Analyze company financials, ratios, growth metrics, and valuation

**Data Sources:**
- **Primary:** Financial Modeling Prep (FMP) API
**Script Location:** `~/.claude/skills/stock-analyst/scripts/stock_analysis_fmp.py` (preferred) or `~/.claude/skills/stock-analyst/scripts/stock_analysis_fmp.py` (fallback)
- **Supporting Scripts:** `stock_valuation_analyzer.py` for PEG ratio and sector comparison
- **API Key:** Required via `FMP_API_KEY` environment variable

**Process:**
1. Initialize FMP Client using `stock_analysis_fmp.py`
2. Fetch company profile, current quote, financial ratios
3. Fetch key metrics, financial statements, growth metrics
4. Analyze financial health, valuation, and growth prospects
5. Use `stock_valuation_analyzer.py` for PEG ratio calculation and sector comparison

**Output:** Comprehensive fundamental analysis summary

### 2. Technical Analysis

**Capability:** Analyze price patterns, trends, and technical indicators

**Data Sources:**
- **Primary:** FMP API for historical price data
- **Script Location:** `~/.claude/skills/stock-analyst/scripts/stock_technical_analysis.py`
- **Alternative:** Browser tools to access Yahoo Finance, TradingView

**Process:**
1. Fetch historical price data (1 year minimum)
2. Calculate moving averages (SMA 20/50/200, EMA 12/26)
3. Calculate momentum indicators (RSI, MACD)
4. Calculate volatility indicators (Bollinger Bands, ATR)
5. Analyze volume trends
6. Identify support/resistance levels
7. Detect chart patterns
8. Generate trading signals

**Output:** Comprehensive technical analysis summary

### 3. Combined Analysis

**Capability:** Synthesize fundamental and technical analysis

**Process:**
1. Compare fundamental strength with technical setup
2. Identify alignment or divergence
3. Assess overall investment thesis
4. Determine risk/reward ratio
5. Set price targets
6. Formulate recommendation

**Output:** Combined analysis and investment recommendation

### 4. Multi-Stock Comparison

**Capability:** Analyze and compare multiple stocks side-by-side with comparison tables

**Script Location:** `~/.claude/skills/stock-analyst/scripts/stock_comparison_analyzer.py`

**Usage:**
```bash
# Compare multiple stocks with both fundamental and technical analysis
python3 ~/.claude/skills/stock-analyst/scripts/stock_comparison_analyzer.py AAPL MSFT GOOGL --type both

# Technical analysis comparison only
python3 ~/.claude/skills/stock-analyst/scripts/stock_comparison_analyzer.py UNH CI HUM CNC MOH --type technical

# Fundamental analysis comparison only
python3 ~/.claude/skills/stock-analyst/scripts/stock_comparison_analyzer.py NVDA AMD INTC --type fundamental
```

**Options:**
- `--type fundamental` - Run fundamental analysis only on all stocks
- `--type technical` - Run technical analysis only on all stocks
- `--type both` - Run both analyses (default)

**Process:**
1. Accept multiple stock symbols as arguments
2. Run fundamental and/or technical analysis on each stock
3. Aggregate results into comparison data structures
4. Generate side-by-side comparison tables
5. Provide summary with signals and recommendations for each stock
6. Save comparison report to file

**Output:**
- Comparison table with key metrics for all stocks
- Individual analysis summaries for each stock
- Trading signals and recommendations
- Report saved to `~/personal/stock_analysis/{TICKERS}_comparison_{timestamp}.md`

**Trigger Phrases:**
- "Compare AAPL, MSFT, and GOOGL"
- "Analyze these stocks together: UNH CI HUM"
- "Benchmark PLTR against its competitors"
- "Side-by-side comparison of healthcare stocks"
- "Which is better: NVDA or AMD?" (2-stock comparison)

## Workflow

### Standard Stock Analysis Workflow (Enhanced with AI Interpretation)

1. **Initialize:** Set up FMP API connection
2. **Fundamental Analysis:** Fetch and analyze financial data **with AI interpretation**
3. **Technical Analysis:** Calculate indicators and analyze price patterns **with AI interpretation**
4. **Sentiment Analysis:** Analyze analyst recommendations and news sentiment (Step 3.5)
5. **Combined Analysis:** Synthesize insights **with AI synthesis** including sentiment
6. **Report Generation:** Create comprehensive analysis report **with AI interpretation** of all metrics

## Tool Usage Instructions

### Using Stock Analysis Scripts

**Scripts Location:** Scripts are located in `~/.claude/skills/stock-analyst/scripts/` directory:
- `stock_analysis_fmp.py` - Fundamental analysis using FMP API
- `stock_technical_analysis.py` - Technical analysis with indicators
- `stock_comparison_analyzer.py` - Multi-stock comparison and batch analysis
- `stock_recommendation_engine.py` - Consistent recommendation scoring system
- `stock_valuation_analyzer.py` - Valuation context (PEG ratio, sector comparison)

**Note:** If scripts don't exist at `~/.claude/skills/stock-analyst/scripts/`, they may also be available at `~/personal/`. Check both locations.

**Fundamental Analysis:**
```bash
# Preferred: Use script from skill directory
python3 ~/.claude/skills/stock-analyst/scripts/stock_analysis_fmp.py NVDA

# Fallback: Use script from personal directory  
python3 ~/.claude/skills/stock-analyst/scripts/stock_analysis_fmp.py NVDA
```

**Technical Analysis:**
```bash
# Preferred: Use script from skill directory
python3 ~/.claude/skills/stock-analyst/scripts/stock_technical_analysis.py NVDA

# Fallback: Use script from personal directory
python3 ~/.claude/skills/stock-analyst/scripts/stock_technical_analysis.py NVDA
```

**Both scripts require `FMP_API_KEY` environment variable.**

**Multi-Stock Comparison:**
```bash
# Compare multiple stocks (generates comparison table and report)
python3 ~/.claude/skills/stock-analyst/scripts/stock_comparison_analyzer.py AAPL MSFT GOOGL AMZN --type both

# Example output location: ~/personal/stock_analysis/AAPL_MSFT_GOOGL_AMZN_comparison_2026-01-03_12-30-45.md
```

**Alternative: Import as Python Module**

If running as part of a Python script, you can import the classes directly:

```python
import sys
import os

# Add script directory to path
script_dir = os.path.expanduser('~/.claude/skills/stock-analyst/scripts')
if os.path.exists(script_dir):
    sys.path.insert(0, script_dir)
    from stock_analysis_fmp import FMPStockAnalyzer
    from stock_technical_analysis import FMPTechnicalAnalyzer, TechnicalAnalyzer
    from stock_recommendation_engine import StockRecommendationEngine
    from stock_valuation_analyzer import ValuationAnalyzer
    
    # Use the classes
    analyzer = FMPStockAnalyzer()
    analyzer.analyze_stock('NVDA')
```

## Output Format

Generate comprehensive reports including:
- Executive Summary with Investment Thesis
- Fundamental Analysis (financials, ratios, growth) **with AI interpretation**
- Technical Analysis (indicators, trends, signals) **with AI interpretation**
- Sentiment Analysis (analyst recommendations + news sentiment)
- Combined Assessment **with AI synthesis**
- Investment Recommendation **with actionable entry/exit strategies**
- Risk Factors **with contextual assessment**
- Price Targets based on technical and fundamental analysis

**AI Interpretation Features:**
- Contextual explanations for all financial ratios (what they mean, industry comparison)
- Narrative synthesis of growth metrics and trends
- Investment thesis development combining all analysis dimensions
- Actionable recommendations with entry/exit strategies
- Risk assessment with mitigation strategies

**Report Location:**

*Single Stock Analysis:*
Reports are automatically saved to `~/personal/stock_analysis/[SYMBOL]/[TIMESTAMP]_comprehensive_analysis.md`
where `[SYMBOL]` is the ticker symbol and `[TIMESTAMP]` is in `YYYY-MM-DD_HH-MM-SS` format.

*Multi-Stock Comparison:*
Comparison reports are saved to `~/personal/stock_analysis/[TICKERS]_comparison_[TIMESTAMP].md`
where `[TICKERS]` is the list of symbols joined by underscores (e.g., `AAPL_MSFT_GOOGL_comparison_2026-01-03_12-30-45.md`).

Each analysis is preserved with a unique timestamp, allowing you to track changes and improvements over time.

## Examples

**Single Stock:**
- "Analyze NVDA" → Complete fundamental + technical analysis
- "Do fundamental analysis on Apple" → Fundamental analysis only
- "Technical analysis for Microsoft" → Technical analysis only

**Multi-Stock Comparison:**
- "Compare AAPL vs MSFT" → Side-by-side comparison of 2 stocks
- "Analyze UNH, CI, HUM, CNC, MOH" → Comparison of 5 healthcare stocks
- "Compare the top 5 tech stocks" → Multi-stock comparison with research
- "Benchmark PLTR against competitors" → Stock + competitor comparison
- "Which is better: NVDA or AMD?" → Head-to-head comparison

## Best Practices

- ✅ Always verify API key before starting
- ✅ Use latest available data
- ✅ Calculate multiple indicators for confirmation
- ✅ Combine fundamental and technical for comprehensive view
- ✅ Set clear price targets and risk levels
- ✅ Cite data sources and dates

---

*Stock Analyst Skill Version: 1.0*

## Code Implementation Strategy

The skill works in two ways:
1. **Using Existing Scripts (Preferred):** Use scripts from `~/.claude/skills/stock-analyst/scripts/`
2. **Writing Code JIT:** If scripts don't exist, implement on-the-fly

See `./reference/code-implementation.md` for detailed code examples and implementation patterns.

---

## Enhanced Features

See `./reference/enhanced-features.md` for comprehensive documentation on:
- Phase 1 enhancements (volume analysis, support/resistance, valuation context)
- Phase 2 enhancements (forward-looking analysis, risk quantification, unified workflow)
- Usage examples and output organization
- Version history and changelog

---

*Stock Analyst Skill Version: 3.1 (Multi-Stock Comparison)*  
*Last Updated: January 3, 2026*

## Supporting Documentation

- `./reference/code-implementation.md` - Code examples and JIT implementation patterns
- `./reference/enhanced-features.md` - Enhanced features, usage examples, and version history
