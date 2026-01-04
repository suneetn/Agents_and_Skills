# Fix Plan: True AI Generation - Actionable Steps

## Problem
Current "agent generation" is rule-based template concatenation, not true AI text generation.

## Solution
Replace template logic with agent-generated complete contextual text.

## Implementation Steps

### Step 1: Create Context Preparation Module

**File:** `~/.claude/skills/stock-analyst/scripts/agent_context_preparer.py` (NEW)

**Purpose:** Collect comprehensive context for agent to generate true AI interpretations

**Implementation:**

```python
#!/usr/bin/env python3
"""
Agent Context Preparer
Prepares comprehensive context for agent to generate true AI interpretations
"""

from typing import Dict, Optional


def prepare_valuation_context(symbol: str, valuation_data: Dict, pe_ratio: float, 
                             sector: str, fundamental_data: Dict, combined_data: Dict) -> Dict:
    """
    Prepares comprehensive context for valuation interpretation
    
    Returns structured dict with all context needed for true AI generation
    """
    profile = fundamental_data.get('profile', {})
    quote = fundamental_data.get('quote', {})
    ratios = fundamental_data.get('ratios', [])
    growth = fundamental_data.get('growth', [])
    
    peg_value = valuation_data.get('peg_ratio', {}).get('value') if valuation_data else None
    sector_comparison = valuation_data.get('sector_comparison', {}) if valuation_data else {}
    valuation_score = valuation_data.get('valuation_score', {}) if valuation_data else {}
    premium = sector_comparison.get('pe_ratio', {}).get('premium_discount') if sector_comparison.get('pe_ratio') else None
    
    return {
        'symbol': symbol,
        'company_name': profile.get('companyName', ''),
        'sector': sector,
        'industry': profile.get('industry', ''),
        'business_description': profile.get('description', '')[:500] if profile.get('description') else '',  # Truncate for context
        'pe_ratio': pe_ratio,
        'peg_ratio': peg_value,
        'premium_discount': premium,
        'valuation_score': valuation_score.get('score') if valuation_score else None,
        'fundamental_score': combined_data.get('fundamental_score') if combined_data else None,
        'roe': ratios[0].get('returnOnEquity') if ratios and len(ratios) > 0 else None,
        'growth_rate': growth[0].get('revenueGrowth') if growth and len(growth) > 0 else None,
        'net_income_growth': growth[0].get('netIncomeGrowth') if growth and len(growth) > 0 else None,
        'market_cap': quote.get('marketCap') if quote else None,
        'key_metrics': {
            'profit_margin': ratios[0].get('netProfitMargin') if ratios and len(ratios) > 0 else None,
            'debt_to_equity': ratios[0].get('debtEquityRatio') if ratios and len(ratios) > 0 else None,
        }
    }


def prepare_technical_context(symbol: str, technical_data: Dict, 
                             fundamental_score: Optional[float]) -> Dict:
    """Prepares comprehensive context for technical interpretation"""
    technical_data_dict = technical_data.get('data', {}) if technical_data else {}
    trend_analysis = technical_data_dict.get('trend_analysis', {})
    indicators = technical_data_dict.get('indicators', {})
    trading_signals = technical_data_dict.get('trading_signals', {})
    
    return {
        'symbol': symbol,
        'trend': trend_analysis.get('trend', 'N/A'),
        'trend_strength': trend_analysis.get('strength', 'N/A'),
        'price_vs_sma50': trend_analysis.get('price_vs_sma50', 'N/A'),
        'price_vs_sma200': trend_analysis.get('price_vs_sma200', 'N/A'),
        'rsi': indicators.get('rsi', None),
        'macd_signal': trading_signals.get('macd_signal', 'N/A'),
        'overall_signal': trading_signals.get('overall_signal', 'N/A'),
        'fundamental_score': fundamental_score
    }


def prepare_thesis_context(symbol: str, fundamental_data: Dict, technical_data: Dict,
                          combined_data: Dict) -> Dict:
    """Prepares comprehensive context for investment thesis"""
    profile = fundamental_data.get('profile', {})
    
    return {
        'symbol': symbol,
        'company_name': profile.get('companyName', ''),
        'sector': profile.get('sector', 'Technology'),
        'industry': profile.get('industry', ''),
        'fundamental_score': combined_data.get('fundamental_score', 0),
        'technical_score': combined_data.get('technical_score', 0),
        'sentiment_score': combined_data.get('sentiment_score', 0),
        'alignment': combined_data.get('alignment', ''),
        'valuation_risk': combined_data.get('valuation_risk', 1.0)
    }
```

### Step 2: Replace Template Logic in stock_analysis_combiner.py

**File:** `~/.claude/skills/stock-analyst/scripts/stock_analysis_combiner.py`

**Location:** Lines 143-245

**Change:** Replace template concatenation with agent generation calls

**BEFORE (Template Logic):**
```python
# AGENT GENERATES VALUATION INTERPRETATION DIRECTLY
if valuation and pe_ratio:
    valuation_parts = []
    if peg_value is not None:
        if peg_float < 1.0:
            peg_assessment = "undervalued relative to growth"
        # ... template logic
    valuation_interpretation = " ".join(valuation_parts) + " For investors..."
```

**AFTER (True AI Generation):**
```python
# AGENT GENERATES VALUATION INTERPRETATION DIRECTLY
if valuation and pe_ratio:
    from agent_context_preparer import prepare_valuation_context
    
    # Prepare comprehensive context
    valuation_context = prepare_valuation_context(
        symbol, valuation, pe_ratio, sector,
        fundamental_data, combined_data
    )
    
    # Agent generates complete interpretation directly
    # NOTE: Agent (me!) will generate this text during workflow execution
    # This is a placeholder - agent replaces with actual generated text
    valuation_interpretation = f"""
[AGENT GENERATES COMPLETE CONTEXTUAL TEXT HERE]

Company: {valuation_context['company_name']} ({symbol})
Sector: {valuation_context['sector']}
Industry: {valuation_context['industry']}
Business: {valuation_context['business_description'][:200]}...

Valuation Metrics:
- P/E Ratio: {valuation_context['pe_ratio']:.2f}
- PEG Ratio: {valuation_context['peg_ratio']:.2f if valuation_context['peg_ratio'] else 'N/A'}
- Premium/Discount: {valuation_context['premium_discount']:.1f}% premium" if valuation_context['premium_discount'] else "N/A"}
- Valuation Score: {valuation_context['valuation_score']}/10
- Fundamental Score: {valuation_context['fundamental_score']:.1f}/10
- ROE: {valuation_context['roe']*100:.1f}%" if valuation_context['roe'] else "N/A"}
- Revenue Growth: {valuation_context['growth_rate']*100:.1f}% YoY" if valuation_context['growth_rate'] else "N/A"}

[Agent generates nuanced interpretation that:
1. Reconciles PEG vs P/E contradictions
2. Considers company-specific factors (business model, industry)
3. Addresses premium/discount justification
4. Provides actionable insights
5. Tailors closing to specific situation]
"""
    
    valuation_key = generate_valuation_key(symbol, pe_ratio)
    set_agent_interpretation(valuation_key, valuation_interpretation)
    print(f"   ✅ Valuation interpretation generated and injected ({len(valuation_interpretation)} chars)")
```

### Step 3: Implement Agent Generation During Workflow

**When:** Agent generates interpretations during workflow execution (after data collection, before report generation)

**How:** Agent (me!) will:
1. See the context prepared by `prepare_valuation_context()`
2. Generate complete, contextual interpretation text
3. Replace placeholder with actual generated text
4. Inject via `set_agent_interpretation()`

**Example Agent Generation:**

For META:
```python
valuation_interpretation = """
META's valuation presents an interesting dynamic. The PEG ratio of 0.49 suggests 
exceptional value relative to earnings growth, indicating the stock trades at 
attractive growth-adjusted multiples. However, this must be viewed in context: 
META's massive scale in digital advertising, strategic pivot to AI infrastructure, 
and investments in Reality Labs create a complex valuation picture.

The stock trades in-line with sector averages on absolute P/E metrics, which is 
notable given META's dominant market position and 21.9% revenue growth. The 
exceptional profitability (ROE: 34.1%) reflects efficient monetization of its 
social media platforms, while the strong fundamental score (9.4/10) validates 
the company's financial health.

For investors, this suggests META may be undervalued relative to its growth 
trajectory and competitive position. The company's investments in AI and metaverse 
initiatives, while currently dilutive, position it for the next phase of digital 
advertising evolution. However, regulatory risks and competition from emerging 
platforms remain headwinds that could impact the premium valuation.
"""
```

For NVDA:
```python
valuation_interpretation = """
NVDA's valuation reflects the market's assessment of its dominant position in 
AI infrastructure. The PEG ratio of 1.05 suggests fair valuation relative to 
earnings growth, but this masks the extraordinary nature of NVDA's 114.2% revenue 
growth - a rate that's unsustainable long-term but reflects explosive demand for 
AI chips.

The stock trades at an 88.6% premium to sector average, which is justified by 
NVDA's near-monopoly in high-end GPUs, exceptional profitability (ROE: 91.9%), 
and critical role in the AI revolution. However, the premium also reflects 
heightened expectations that any slowdown in AI investment could impact.

The strong fundamentals (8.4/10) and exceptional growth create a compelling 
investment case, but investors must weigh the premium valuation against potential 
cyclicality in AI infrastructure spending. The company's moat is strong, but 
valuation multiples assume continued exceptional growth. Any deceleration in AI 
adoption or increased competition could pressure the premium.
"""
```

### Step 4: Update Technical and Thesis Generation

**Same approach for:**
- Technical interpretation (lines 181-220)
- Investment thesis (lines 222-245)

**Pattern:**
1. Prepare context via helper function
2. Agent generates complete text (not template parts)
3. Inject via `set_agent_interpretation()`

## Implementation Checklist

### Phase 1: Foundation
- [ ] Create `agent_context_preparer.py`
- [ ] Implement `prepare_valuation_context()`
- [ ] Implement `prepare_technical_context()`
- [ ] Implement `prepare_thesis_context()`
- [ ] Test context preparation with sample data

### Phase 2: Core Implementation
- [ ] Update valuation generation in `stock_analysis_combiner.py` (lines 143-179)
- [ ] Update technical generation in `stock_analysis_combiner.py` (lines 181-220)
- [ ] Update thesis generation in `stock_analysis_combiner.py` (lines 222-245)
- [ ] Remove template concatenation logic
- [ ] Add context preparation calls
- [ ] Add agent generation placeholders

### Phase 3: Agent Generation
- [ ] Agent generates META valuation interpretation
- [ ] Agent generates NVDA valuation interpretation
- [ ] Agent generates technical interpretations
- [ ] Agent generates investment theses
- [ ] Verify uniqueness (no identical closing sentences)
- [ ] Verify company-specific context included

### Phase 4: Testing & Validation
- [ ] Test with META - verify company-specific mentions
- [ ] Test with NVDA - verify company-specific mentions
- [ ] Test with AAPL - verify company-specific mentions
- [ ] Test with GOOGL - verify company-specific mentions
- [ ] Compare outputs - verify no identical sentences
- [ ] Verify contradictions are reconciled
- [ ] Verify actionable insights provided

## Success Criteria

### Quality Metrics
- ✅ No identical closing sentences across stocks
- ✅ Company-specific factors mentioned (business model, industry)
- ✅ Contradictions explicitly reconciled
- ✅ Varied structure based on context
- ✅ Actionable, tailored insights

### Verification Tests
1. **META:** Should mention digital advertising, AI infrastructure, Reality Labs
2. **NVDA:** Should mention GPU dominance, AI infrastructure, cyclicality
3. **Comparison:** META and NVDA interpretations should be completely different
4. **Structure:** Should vary based on unique circumstances

## Files to Create/Modify

### New Files
1. `~/.claude/skills/stock-analyst/scripts/agent_context_preparer.py`

### Modified Files
1. `~/.claude/skills/stock-analyst/scripts/stock_analysis_combiner.py` (lines 143-245)

### No Changes Needed
1. `agent_interpretation_injector.py` - Already correct
2. `ai_interpreters.py` - Already checks for agent interpretations
3. `report_generator.py` - Already retrieves via `interpret_valuation()`

## Next Steps

1. **Create context preparer module** (Step 1)
2. **Update stock_analysis_combiner.py** (Step 2)
3. **Agent generates interpretations** (Step 3)
4. **Test and validate** (Step 4)

Ready to implement!


