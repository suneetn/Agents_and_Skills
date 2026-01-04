# Agent AI Interpretation Guide
**For:** Stock Analyst Skill - AI Interpretation Enhancement  
**Date:** 2025-12-29

---

## Overview

When orchestrating the stock analysis workflow, the agent (Claude) should generate interpretations using enhanced context that includes edge case detection. This allows AI to provide nuanced, contextual analysis rather than relying on hardcoded algorithmic rules.

---

## Enhanced Context Structure

### Valuation Context (`prepare_valuation_context`)

Now includes:
- `edge_cases`: Dict with flags for AI to interpret
  - `suspicious_peg`: PEG < 0.1 (for AI to explain why, not just flag)
  - `extreme_growth`: Net income growth > 200% (for AI to assess cyclical vs sustainable)
  - `cyclical_industry`: Industry is cyclical (semiconductors, energy, etc.)
  - `recovery_from_lows`: Price doubled from 52-week low
  - `price_appreciation_from_low`: Percentage appreciation from low
  - `near_52_week_high`: Price within 5% of 52-week high
- `revenue_growth_pct`: Percentage format for easier interpretation
- `net_income_growth_pct`: Percentage format for easier interpretation
- `current_price`, `year_low`, `year_high`: Price context

### Technical Context (`prepare_technical_context`)

Now includes:
- `edge_cases`: Dict with flags for AI to interpret
  - `rsi_near_overbought`: RSI 65-70 (for AI to provide nuanced guidance)
  - `rsi_overbought`: RSI >= 70
  - `rsi_near_oversold`: RSI 30-35
  - `strong_uptrend`: Strong uptrend flag
  - `price_near_highs`: Price within 5% of high
- `current_price`, `price_changes`: Price action context

---

## How Agent Should Generate Interpretations

### 1. Valuation Interpretation

**When generating valuation interpretation, agent should:**

1. **Check edge cases** and provide contextual explanation:
   ```python
   edge_cases = valuation_context.get('edge_cases', {})
   
   if edge_cases.get('suspicious_peg'):
       # AI explains WHY it's suspicious, not just that it is
       # Consider: cyclical recovery, forward estimates vs trailing, industry context
   
   if edge_cases.get('extreme_growth'):
       # AI assesses: cyclical recovery vs sustainable growth
       # Consider: industry cyclicality, recovery from lows, forward estimates
   
   if edge_cases.get('recovery_from_lows'):
       # AI explains: much of recovery may be priced in
       # Consider: forward-looking vs backward-looking metrics
   ```

2. **Provide nuanced interpretation** that:
   - Explains whether extreme metrics indicate cyclical recovery vs sustainable growth
   - Reconciles PEG vs P/E contradictions with context
   - Assesses whether valuation is justified given company-specific factors
   - Considers forward-looking estimates vs trailing metrics

3. **Example for MU:**
   ```
   "PEG ratio of 0.03 appears exceptionally low, but this reflects MU's recovery 
   from cyclical semiconductor downturn rather than sustainable forward growth. 
   The 897% net income growth represents recovery from depressed 2023 levels 
   when memory prices collapsed. Investors should evaluate MU based on forward 
   earnings estimates and cyclical positioning rather than trailing growth rates. 
   The stock has already appreciated 123% over the past year, suggesting much 
   of the recovery is priced in."
   ```

### 2. Technical Interpretation

**When generating technical interpretation, agent should:**

1. **Check edge cases** and provide nuanced guidance:
   ```python
   edge_cases = technical_context.get('edge_cases', {})
   
   if edge_cases.get('rsi_near_overbought'):
       # AI provides nuanced guidance:
       # - Is this concerning for entry timing?
       # - How does it interact with strong fundamentals?
       # - Entry timing vs investment decision (quality companies)
   
   if edge_cases.get('strong_uptrend') and edge_cases.get('price_near_highs'):
       # AI explains: strong momentum but extended levels
       # Consider: wait for pullback vs enter now for quality companies
   ```

2. **Provide contextual guidance** that:
   - Explains RSI levels with nuance (65-70 is near overbought, not extreme)
   - Considers fundamental strength when interpreting technicals
   - Distinguishes entry timing from investment decision
   - Provides actionable entry guidance

3. **Example for MU (RSI 68.53):**
   ```
   "RSI of 68.53 indicates the stock is approaching overbought territory 
   (70+ is typically overbought), suggesting potential for short-term pullback. 
   However, given MU's exceptional fundamental strength (8.8/10) and strong 
   uptrend, this technical condition is more relevant for entry timing than 
   investment decision. For long-term investors focused on quality companies, 
   current levels may be acceptable, though waiting for a pullback to $270-275 
   support zone would provide better risk/reward. For tactical traders, 
   consider waiting for RSI to reset below 60 or for price to pull back to 
   key support levels."
   ```

### 3. Price Target Generation

**When generating price targets, agent should:**

1. **Select methodology** based on available data:
   - Priority 1: Analyst consensus targets (if available)
   - Priority 2: P/E multiple expansion (10-30% realistic)
   - Priority 3: Technical resistance levels
   - Fallback: Conservative percentage-based (5-15%)

2. **Consider edge cases:**
   ```python
   if edge_cases.get('extreme_growth') and edge_cases.get('recovery_from_lows'):
       # DO NOT directly apply growth rate to stock price
       # Instead: Use P/E multiple expansion or analyst targets
       # Explain: Growth reflects recovery, not sustainable forward rate
   ```

3. **Generate realistic targets** with explanation:
   ```
   "Target 1: $320 (12% upside) - Based on 10% P/E multiple expansion 
   assuming stable earnings. This is conservative given MU's strong 
   fundamentals but accounts for the stock already appreciating 123% 
   from lows, suggesting much recovery is priced in."
   ```

---

## Key Principles

1. **Edge cases are flags, not rules** - AI interprets them contextually
2. **Explain WHY, not just WHAT** - Don't just flag "suspicious PEG", explain why
3. **Consider multiple factors** - Synthesize edge cases with other context
4. **Provide actionable insights** - Not just analysis, but guidance
5. **Distinguish timing from decision** - Entry timing vs investment decision

---

## Implementation

When agent orchestrates workflow:

1. **Collect enhanced context** (already done via `prepare_valuation_context`, etc.)
2. **Generate interpretations** using edge case context
3. **Inject interpretations** via `agent_interpretation_injector`
4. **Reports use** AI-generated interpretations

The enhanced context provides all necessary information for true AI generation without hardcoded rules.

---

## Example: MU Analysis

**Enhanced Context Provided:**
```python
{
    'edge_cases': {
        'suspicious_peg': True,  # 0.03
        'extreme_growth': True,   # 897%
        'cyclical_industry': True,  # Semiconductors
        'recovery_from_lows': True,  # 123% from low
        'near_52_week_high': True   # Near $290.87 high
    },
    'net_income_growth_pct': 897.6,
    'price_appreciation_from_low': 123.38
}
```

**AI Interpretation Generated:**
- Explains PEG 0.03 reflects cyclical recovery, not sustainable undervaluation
- Assesses 897% growth as recovery from depressed base, not forward rate
- Considers 123% price appreciation suggests recovery priced in
- Provides realistic price targets using P/E expansion, not growth application
- Recommends forward-looking analysis over trailing metrics

---

**Result:** Nuanced, contextual analysis that handles edge cases intelligently rather than algorithmically.



