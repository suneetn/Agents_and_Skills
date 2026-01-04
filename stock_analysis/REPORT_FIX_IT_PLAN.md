# Report Generation Fix-It Plan

**Based on:** TSM Report Critique  
**Target File:** `stock_analyst_workflow_enhanced.py` (step5_report_generation function)  
**Date:** December 28, 2025

---

## Overview

This plan addresses 10 critical issues identified in the report critique, organized by priority and implementation complexity.

---

## Priority 1: Critical Fixes (Must Fix Immediately)

### Issue 1.1: Replace Placeholder Text with Actual AI Interpretations

**Problem:** Lines 863-903 show placeholder text `[AI-Generated Interpretation: ...]` instead of actual interpretations.

**Root Cause:** The `interpretations` dict from `fundamental_data` is empty or not being populated correctly.

**Current Code Location:**
- `step5_report_generation()` lines 863-903
- `interpret_fundamental_metrics()` function (lines 99-239) - generates interpretations but may not be called

**Fix Steps:**

1. **Verify interpretations are generated:**
   ```python
   # In step2_fundamental_analysis(), ensure interpretations are added:
   interpretations = interpret_fundamental_metrics(ratios, growth, quote)
   fundamental_data['interpretations'] = interpretations
   ```

2. **Update report generation to use actual interpretations:**
   ```python
   # Lines 863-903: Replace placeholder checks with actual content
   if 'roe' in interpretations and interpretations['roe']:
       report_content += f"  *{interpretations['roe']}*\n"
   else:
       # Generate on-the-fly if missing
       roe_interpretation = generate_roe_interpretation(roe)
       report_content += f"  *{roe_interpretation}*\n"
   ```

3. **Create fallback interpretation generator:**
   ```python
   def generate_quick_interpretation(metric_name, value, context):
       """Generate interpretation if not available from AI"""
       # Rule-based fallback interpretations
       # This ensures report always has content
   ```

**Files to Modify:**
- `stock_analyst_workflow_enhanced.py` - step2_fundamental_analysis(), step5_report_generation()

**Estimated Effort:** 2-3 hours

---

### Issue 1.2: Include Complete Technical Analysis Section

**Problem:** Lines 924-938 reference "comprehensive technical analysis output above" but no technical data is included.

**Root Cause:** Technical data is available in `technical_data['data']` but not being extracted and formatted for the report.

**Current Code Location:**
- `step5_report_generation()` lines 924-938

**Fix Steps:**

1. **Extract technical data from technical_data dict:**
   ```python
   technical_data_dict = technical_data.get('data', {})
   if technical_data_dict:
       trend_analysis = technical_data_dict.get('trend_analysis', {})
       trading_signals = technical_data_dict.get('trading_signals', {})
       price_changes = technical_data_dict.get('price_changes', {})
       indicators = technical_data_dict.get('indicators', {})
       current_price = technical_data_dict.get('current_price')
   ```

2. **Build comprehensive technical section:**
   ```python
   report_content += """
   ## Technical Analysis
   
   ### Current Price Action
   """
   if price_changes:
       report_content += f"- **Current Price:** ${current_price:.2f}\n"
       report_content += f"- **Price Change (1D):** {price_changes.get('1D', 0)*100:+.2f}%\n"
       report_content += f"- **Price Change (1W):** {price_changes.get('1W', 0)*100:+.2f}%\n"
       report_content += f"- **Price Change (1M):** {price_changes.get('1M', 0)*100:+.2f}%\n"
       report_content += f"- **Price Change (1Y):** {price_changes.get('1Y', 0)*100:+.2f}%\n"
   
   # Add trend analysis, moving averages, momentum indicators, etc.
   ```

3. **Include technical score breakdown:**
   ```python
   technical_score_details = combined_data.get('technical_score_details')
   if technical_score_details:
       report_content += f"""
   ### Technical Score Breakdown
   - **Overall:** {technical_score_details['overall_score']}/10
   - **Trend:** {technical_score_details['trend_score']}/10
   - **Momentum:** {technical_score_details['momentum_score']}/10
   - **Price Action:** {technical_score_details['price_action_score']}/10
   - **Volatility:** {technical_score_details['volatility_score']}/10
   """
   ```

**Files to Modify:**
- `stock_analyst_workflow_enhanced.py` - step5_report_generation()

**Estimated Effort:** 3-4 hours

---

### Issue 1.3: Generate Actual Investment Thesis

**Problem:** Lines 1000-1002 show placeholder text instead of actual investment thesis.

**Root Cause:** `combined_data.get('investment_thesis')` returns placeholder text from `synthesize_investment_thesis()` function.

**Current Code Location:**
- `step4_combined_analysis()` - calls `synthesize_investment_thesis()` (lines 678-732)
- `synthesize_investment_thesis()` function generates prompt but doesn't call LLM

**Fix Steps:**

1. **Update synthesize_investment_thesis() to generate actual content:**
   ```python
   def synthesize_investment_thesis(symbol, fundamental_score, technical_score, 
                                     sentiment_score, fundamental_details, 
                                     technical_details, valuation_risk):
       """Generate actual investment thesis using AI"""
       
       # Build comprehensive prompt
       prompt = f"""
       Based on the following analysis, provide a comprehensive investment thesis for {symbol}:
       
       Fundamental Score: {fundamental_score}/10
       - Profitability: {fundamental_details.get('profitability_score')}/10
       - Growth: {fundamental_details.get('growth_score')}/10
       - Financial Health: {fundamental_details.get('financial_health_score')}/10
       - Valuation: {fundamental_details.get('valuation_score')}/10
       
       Technical Score: {technical_score}/10
       - Trend: {technical_details.get('trend_score')}/10
       - Momentum: {technical_details.get('momentum_score')}/10
       
       Sentiment: {sentiment_score} ({sentiment_classification})
       Valuation Risk: {valuation_risk}x sector
       
       Provide a 3-4 paragraph investment thesis that:
       1. Synthesizes the fundamental, technical, and sentiment analysis
       2. Explains the investment opportunity or concerns
       3. Addresses key risks and catalysts
       4. Provides clear rationale for the recommendation
       """
       
       # Call AI to generate thesis (using Claude API or similar)
       thesis = generate_ai_content(prompt)
       return thesis
   ```

2. **Alternative: Use rule-based synthesis if AI unavailable:**
   ```python
   def synthesize_investment_thesis_rule_based(...):
       """Rule-based investment thesis generation"""
       thesis_parts = []
       
       # Fundamental analysis summary
       if fundamental_score >= 8:
           thesis_parts.append(f"{symbol} demonstrates exceptional fundamental strength...")
       elif fundamental_score >= 6:
           thesis_parts.append(f"{symbol} shows solid fundamentals...")
       
       # Technical analysis summary
       if technical_score >= 7:
           thesis_parts.append("Technical indicators suggest strong momentum...")
       
       # Valuation context
       if valuation_risk > 1.5:
           thesis_parts.append("However, premium valuation requires continued strong performance...")
       
       # Risk factors
       thesis_parts.append("Key risks include...")
       
       return " ".join(thesis_parts)
   ```

**Files to Modify:**
- `stock_analyst_workflow_enhanced.py` - synthesize_investment_thesis(), step4_combined_analysis()

**Estimated Effort:** 4-5 hours (with AI integration) or 2-3 hours (rule-based)

---

## Priority 2: Important Fixes (Should Fix Soon)

### Issue 2.1: Resolve Valuation Contradiction

**Problem:** Line 921 says PEG indicates "undervalued" but valuation score suggests "expensive" without explanation.

**Root Cause:** `interpret_valuation()` function doesn't reconcile PEG vs. overall valuation score.

**Current Code Location:**
- `step5_report_generation()` line 921
- `interpret_valuation()` function (lines 254-442)

**Fix Steps:**

1. **Update interpret_valuation() to provide reconciliation:**
   ```python
   def interpret_valuation(valuation_data, pe_ratio, sector):
       """Interpret valuation with reconciliation of metrics"""
       
       peg_value = valuation_data.get('peg_ratio', {}).get('value')
       valuation_score = valuation_data.get('valuation_score', {}).get('score', 5.0)
       sector_premium = valuation_data.get('sector_comparison', {}).get('pe_ratio', {}).get('premium_discount', 0)
       
       interpretation = []
       
       # PEG interpretation
       if peg_value and isinstance(peg_value, (int, float)):
           if peg_value < 1.0:
               interpretation.append(f"PEG ratio of {peg_value:.2f} suggests the stock is undervalued relative to its earnings growth rate.")
           elif peg_value < 1.5:
               interpretation.append(f"PEG ratio of {peg_value:.2f} indicates fair valuation relative to growth.")
           else:
               interpretation.append(f"PEG ratio of {peg_value:.2f} suggests overvaluation relative to growth.")
       
       # Overall valuation score interpretation
       if valuation_score < 4.0:
           interpretation.append(f"However, the overall valuation score of {valuation_score}/10 indicates expensive valuation.")
       elif valuation_score < 6.0:
           interpretation.append(f"The overall valuation score of {valuation_score}/10 suggests fair to expensive valuation.")
       else:
           interpretation.append(f"The overall valuation score of {valuation_score}/10 indicates reasonable valuation.")
       
       # Reconciliation
       if peg_value and isinstance(peg_value, (int, float)) and peg_value < 1.0 and valuation_score < 5.0:
           interpretation.append("This apparent contradiction can be explained: While PEG suggests growth-adjusted value, the absolute P/E ratio and sector premium indicate the stock trades at premium multiples. The PEG undervaluation reflects strong earnings growth expectations, but current valuation levels require continued exceptional performance to justify.")
       
       return " ".join(interpretation)
   ```

**Files to Modify:**
- `stock_analyst_workflow_enhanced.py` - interpret_valuation()

**Estimated Effort:** 1-2 hours

---

### Issue 2.2: Add Fundamental Score Breakdown

**Problem:** Report shows overall fundamental score but not component breakdown.

**Root Cause:** `combined_data` contains `fundamental_score_details` but it's not included in report.

**Current Code Location:**
- `step5_report_generation()` lines 992-998

**Fix Steps:**

1. **Add fundamental score breakdown section:**
   ```python
   # After line 998, add:
   fundamental_score_details = combined_data.get('fundamental_score_details')
   if fundamental_score_details:
       report_content += f"""
   ### Fundamental Score Breakdown
   
   - **Overall Score:** {fundamental_score_details['overall_score']}/10 ({fundamental_scorer.get_fundamental_strength_label(fundamental_score_details['overall_score'])})
   - **Profitability:** {fundamental_score_details['profitability_score']}/10
     - Based on ROE, ROA, and profit margins
   - **Growth:** {fundamental_score_details['growth_score']}/10
     - Based on revenue and earnings growth rates
   - **Financial Health:** {fundamental_score_details['financial_health_score']}/10
     - Based on debt levels, liquidity, and cash flow
   - **Valuation:** {fundamental_score_details['valuation_score']}/10
     - Based on P/E, PEG, and sector comparison
   """
   ```

**Files to Modify:**
- `stock_analyst_workflow_enhanced.py` - step5_report_generation()

**Estimated Effort:** 30 minutes

---

### Issue 2.3: Include Detailed Risk Factors

**Problem:** Risk Factors section is generic and doesn't include stock-specific risks.

**Root Cause:** `generate_actionable_recommendation()` function doesn't generate stock-specific risks.

**Current Code Location:**
- `step5_report_generation()` lines 1027-1040
- `generate_actionable_recommendation()` function (needs to be found/created)

**Fix Steps:**

1. **Create stock-specific risk generator:**
   ```python
   def generate_stock_specific_risks(symbol, profile, fundamental_data, technical_data, combined_data):
       """Generate stock-specific risk factors"""
       
       risks = []
       sector = profile.get('sector', '')
       industry = profile.get('industry', '')
       
       # Sector-specific risks
       if sector == 'Technology' and 'Semiconductor' in industry:
           risks.append("**Geopolitical Risks:** Semiconductor companies face risks from trade tensions and geopolitical conflicts, particularly for companies with operations in Taiwan or China.")
           risks.append("**Cyclical Industry:** Semiconductor industry is cyclical and subject to demand fluctuations.")
       
       if 'Taiwan' in profile.get('companyName', '') or symbol == 'TSM':
           risks.append("**Taiwan-China Relations:** Geopolitical tensions between Taiwan and China pose significant risks to operations and supply chains.")
       
       # Valuation risks
       valuation_risk = combined_data.get('valuation_risk', 1.0)
       if valuation_risk > 1.5:
           risks.append(f"**Valuation Risk:** Trading at {valuation_risk:.2f}x sector average requires continued exceptional performance to justify premium.")
       
       # Technical risks
       technical_score = combined_data.get('technical_score', 5.0)
       if technical_score < 5.0:
           risks.append("**Technical Weakness:** Weak technical indicators suggest potential downside risk.")
       
       # Fundamental risks
       fundamental_score = combined_data.get('fundamental_score', 5.0)
       if fundamental_score < 6.0:
           risks.append("**Fundamental Concerns:** Below-average fundamental metrics indicate potential operational or financial challenges.")
       
       # Customer concentration (if available)
       # Add logic to check for customer concentration risks
       
       return risks
   ```

2. **Update risk factors section:**
   ```python
   risks = generate_stock_specific_risks(symbol, profile, fundamental_data, technical_data, combined_data)
   if risks:
       report_content += "\n".join([f"- {risk}\n" for risk in risks])
   ```

**Files to Modify:**
- `stock_analyst_workflow_enhanced.py` - step5_report_generation(), new function

**Estimated Effort:** 2-3 hours

---

## Priority 3: Enhancement Fixes (Nice to Have)

### Issue 3.1: Improve Price Targets with Technical/Fundamental Basis

**Problem:** Price targets are generic percentages without technical/fundamental basis.

**Root Cause:** `generate_actionable_recommendation()` function uses generic percentage-based targets.

**Fix Steps:**

1. **Extract actual technical resistance levels:**
   ```python
   def generate_price_targets(technical_data, quote, fundamental_score, valuation_risk):
       """Generate price targets based on technical and fundamental analysis"""
       
       current_price = quote.get('price', 0)
       technical_data_dict = technical_data.get('data', {})
       
       targets = []
       
       # Technical resistance levels
       if technical_data_dict:
           # Get resistance levels from technical analysis
           # Use actual resistance levels as targets
       
       # Fundamental targets based on P/E expansion
       if fundamental_score >= 8.0:
           # Calculate target based on earnings growth and P/E expansion
           # Target P/E = current P/E * (1 + earnings_growth_rate)
       
       return targets
   ```

**Files to Modify:**
- `stock_analyst_workflow_enhanced.py` - generate_actionable_recommendation() or new function

**Estimated Effort:** 2-3 hours

---

### Issue 3.2: Enhance Entry/Exit Strategies with Actual Technical Levels

**Problem:** Entry/exit strategies don't reference actual support/resistance levels.

**Fix Steps:**

1. **Extract support/resistance from technical data:**
   ```python
   def generate_entry_exit_strategy(technical_data, quote, combined_data):
       """Generate entry/exit strategy based on actual technical levels"""
       
       technical_data_dict = technical_data.get('data', {})
       current_price = quote.get('price', 0)
       
       # Get actual support levels
       # Get actual resistance levels
       # Generate strategies based on these levels
   ```

**Files to Modify:**
- `stock_analyst_workflow_enhanced.py` - generate_actionable_recommendation()

**Estimated Effort:** 2 hours

---

### Issue 3.3: Add Sector/Peer Comparison

**Problem:** Report doesn't compare stock to peers or sector.

**Fix Steps:**

1. **Add peer comparison function:**
   ```python
   def generate_peer_comparison(symbol, sector, quote, ratios):
       """Generate peer comparison section"""
       # Use FMP API to get sector/peer data
       # Compare key metrics
   ```

**Files to Modify:**
- `stock_analyst_workflow_enhanced.py` - step5_report_generation(), new function
- May need to add FMP API calls for sector/peer data

**Estimated Effort:** 3-4 hours

---

### Issue 3.4: Expand Sentiment Interpretation

**Problem:** Sentiment section lacks interpretation and key themes.

**Fix Steps:**

1. **Extract key themes from news articles:**
   ```python
   def extract_sentiment_themes(sentiment_data):
       """Extract key themes from news sentiment"""
       # Analyze news articles for common themes
       # Provide interpretation
   ```

**Files to Modify:**
- `stock_analyst_workflow_enhanced.py` - step5_report_generation()

**Estimated Effort:** 2-3 hours

---

## Implementation Plan

### Phase 1: Critical Fixes (Week 1)
- [ ] Issue 1.1: Replace placeholder text
- [ ] Issue 1.2: Include complete technical analysis
- [ ] Issue 1.3: Generate actual investment thesis

**Timeline:** 3-4 days  
**Testing:** Test with 2-3 stocks to verify fixes

### Phase 2: Important Fixes (Week 2)
- [ ] Issue 2.1: Resolve valuation contradiction
- [ ] Issue 2.2: Add fundamental score breakdown
- [ ] Issue 2.3: Include detailed risk factors

**Timeline:** 2-3 days  
**Testing:** Test with same stocks + 2 new stocks

### Phase 3: Enhancements (Week 3-4)
- [ ] Issue 3.1: Improve price targets
- [ ] Issue 3.2: Enhance entry/exit strategies
- [ ] Issue 3.3: Add sector/peer comparison
- [ ] Issue 3.4: Expand sentiment interpretation

**Timeline:** 1-2 weeks  
**Testing:** Comprehensive testing with multiple stocks

---

## Testing Strategy

### Unit Tests
- Test each fix independently
- Verify data extraction from technical_data
- Verify interpretation generation

### Integration Tests
- Run full analysis on test stocks (TSM, NVDA, AAPL)
- Compare before/after reports
- Verify all sections are populated

### Validation Tests
- Check for placeholder text (should be zero)
- Verify technical data completeness
- Validate investment thesis quality
- Check risk factors are stock-specific

---

## Success Criteria

### Phase 1 Complete When:
- ✅ Zero placeholder text in reports
- ✅ Complete technical analysis section with all indicators
- ✅ Actual investment thesis (not placeholder)

### Phase 2 Complete When:
- ✅ Valuation contradiction explained
- ✅ Fundamental score breakdown included
- ✅ Stock-specific risk factors included

### Phase 3 Complete When:
- ✅ Price targets based on technical/fundamental analysis
- ✅ Entry/exit strategies reference actual levels
- ✅ Peer comparison section included
- ✅ Sentiment interpretation expanded

---

## Files to Modify

1. **Primary File:**
   - `~/.claude/skills/stock-analyst/scripts/stock_analyst_workflow_enhanced.py`
   - Also update: `~/personal/stock_analyst_workflow_enhanced.py`

2. **Supporting Functions:**
   - `interpret_fundamental_metrics()` - ensure returns actual interpretations
   - `interpret_valuation()` - add reconciliation logic
   - `synthesize_investment_thesis()` - generate actual content
   - `generate_actionable_recommendation()` - improve with actual levels
   - New functions: `generate_stock_specific_risks()`, `generate_price_targets()`, etc.

---

## Estimated Total Effort

- **Phase 1 (Critical):** 9-12 hours
- **Phase 2 (Important):** 4-6 hours
- **Phase 3 (Enhancements):** 9-12 hours

**Total:** 22-30 hours

---

## Notes

- Start with Phase 1 fixes as they are critical for report quality
- Test each phase before moving to next
- Consider creating a test report generator to validate fixes
- May need to add AI integration for investment thesis generation (or use rule-based fallback)




