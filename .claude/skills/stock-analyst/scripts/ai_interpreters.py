#!/usr/bin/env python3
"""
AI Interpretation Functions
Provides intelligent interpretation of fundamental, technical, and valuation metrics
"""

from typing import Dict, List
import re


def call_ai_for_interpretation(prompt: str, context: Dict) -> str:
    """
    Generate interpretation using rule-based logic.
    In Cursor/Claude environment, this provides actual interpretations rather than placeholders.
    """
    # Extract key information from prompt
    prompt_lower = prompt.lower()
    
    # ROE interpretation
    if "return on equity" in prompt_lower or "roe" in prompt_lower:
        # Extract ROE value from prompt (capture negative sign)
        roe_match = re.search(r'(-?\d+\.?\d*)%', prompt)
        if roe_match:
            roe_pct = float(roe_match.group(1))
            roe = roe_pct / 100
            if roe < 0:
                return f"Negative profitability (ROE: {roe_pct:.1f}%) - Company is losing money, indicating significant operational challenges or restructuring. This is a major red flag requiring immediate attention."
            elif roe > 0.5:
                return f"Exceptional profitability (ROE: {roe_pct:.1f}%) - Well above industry average, indicates highly efficient use of shareholder equity and strong competitive advantages."
            elif roe > 0.25:
                return f"Strong profitability (ROE: {roe_pct:.1f}%) - Above average, indicates good efficiency and effective capital allocation."
            elif roe > 0.15:
                return f"Moderate profitability (ROE: {roe_pct:.1f}%) - In-line with industry average, indicates acceptable efficiency."
            else:
                return f"Weak profitability (ROE: {roe_pct:.1f}%) - Below average, indicates efficiency concerns and potential operational challenges."
    
    # ROA interpretation
    if "return on assets" in prompt_lower or "roa" in prompt_lower:
        roa_match = re.search(r'(-?\d+\.?\d*)%', prompt)  # Capture negative sign
        if roa_match:
            roa_pct = float(roa_match.group(1))
            roa = roa_pct / 100
            if roa < 0:
                return f"Negative asset efficiency (ROA: {roa_pct:.1f}%) - Company is losing money on assets, indicating severe operational challenges or restructuring. This is a critical concern."
            elif roa > 0.2:
                return f"Excellent asset efficiency (ROA: {roa_pct:.1f}%) - Company generates strong returns on assets, indicating effective asset utilization and operational excellence."
            elif roa > 0.1:
                return f"Good asset efficiency (ROA: {roa_pct:.1f}%) - Reasonable asset utilization, indicates solid operational performance."
            else:
                return f"Moderate asset efficiency (ROA: {roa_pct:.1f}%) - Room for improvement in asset utilization and operational efficiency."
    
    # Debt-to-Equity interpretation
    if "debt-to-equity" in prompt_lower or "debt" in prompt_lower:
        debt_match = re.search(r'(\d+\.?\d*)', prompt)
        if debt_match:
            debt_equity = float(debt_match.group(1))
            if debt_equity < 0.5:
                return f"Low debt (Debt-to-Equity: {debt_equity:.2f}) - Conservative balance sheet with minimal financial risk, providing flexibility for growth opportunities."
            elif debt_equity < 1.0:
                return f"Moderate debt (Debt-to-Equity: {debt_equity:.2f}) - Reasonable leverage levels, manageable financial risk with balanced capital structure."
            else:
                return f"High debt (Debt-to-Equity: {debt_equity:.2f}) - Elevated leverage increases financial risk and reduces financial flexibility."
    
    # Current Ratio interpretation
    if "current ratio" in prompt_lower or "liquidity" in prompt_lower:
        cr_match = re.search(r'(\d+\.?\d*)', prompt)
        if cr_match:
            current_ratio = float(cr_match.group(1))
            if current_ratio > 2.0:
                return f"Excellent liquidity (Current Ratio: {current_ratio:.2f}) - Strong ability to meet short-term obligations, indicates robust financial health."
            elif current_ratio > 1.0:
                return f"Adequate liquidity (Current Ratio: {current_ratio:.2f}) - Sufficient short-term coverage, indicates healthy working capital management."
            else:
                return f"Tight liquidity (Current Ratio: {current_ratio:.2f}) - May face short-term cash flow challenges, requires monitoring of working capital."
    
    # Net Income Growth interpretation (check BEFORE revenue growth to avoid false matches)
    if "net income growth" in prompt_lower or "profit growth" in prompt_lower:
        growth_match = re.search(r'(-?\d+\.?\d*)%', prompt)  # Capture negative sign
        if growth_match:
            ni_pct = float(growth_match.group(1))
            # Try to extract revenue growth for margin comparison
            rev_match = re.search(r'revenue growth.*?(\d+\.?\d*)%', prompt_lower)
            rev_pct = None
            if rev_match:
                rev_pct = float(rev_match.group(1))
            
            margin_note = ""
            if rev_pct:
                if ni_pct > rev_pct:
                    margin_note = f" Net income growing faster than revenue ({ni_pct:.1f}% vs {rev_pct:.1f}%) indicates margin expansion."
                elif ni_pct < rev_pct:
                    margin_note = f" Net income growth ({ni_pct:.1f}%) lags revenue growth ({rev_pct:.1f}%), suggesting margin pressure."
            
            # Handle negative growth first
            if ni_pct < -100:
                return f"Severe profit decline ({ni_pct:.1f}% YoY) - Massive losses indicate fundamental business challenges, potential restructuring, or cyclical downturn. This is a critical red flag requiring immediate investigation.{margin_note}"
            elif ni_pct < 0:
                return f"Negative profit growth ({ni_pct:.1f}% YoY) - Declining earnings is a significant concern requiring immediate attention to operational efficiency and cost management.{margin_note}"
            elif ni_pct > 30:
                return f"Exceptional profit growth ({ni_pct:.1f}% YoY) - Outstanding bottom-line expansion indicates strong operational efficiency, margin expansion, or favorable cost management.{margin_note}"
            elif ni_pct > 15:
                return f"Strong profit growth ({ni_pct:.1f}% YoY) - Healthy earnings expansion above average, indicates improving profitability trends.{margin_note}"
            elif ni_pct > 5:
                return f"Moderate profit growth ({ni_pct:.1f}% YoY) - Steady earnings growth indicates stable profitability.{margin_note}"
            else:
                return f"Weak profit growth ({ni_pct:.1f}% YoY) - Minimal earnings expansion may indicate margin pressure or operational challenges.{margin_note}"
    
    # Revenue Growth interpretation (check AFTER net income to avoid false matches)
    if "revenue growth" in prompt_lower:
        growth_match = re.search(r'(-?\d+\.?\d*)%', prompt)  # Capture negative sign
        if growth_match:
            rev_pct = float(growth_match.group(1))
            if rev_pct > 20:
                return f"Exceptional revenue growth ({rev_pct:.1f}% YoY) - Strong top-line expansion indicates market share gains, successful product launches, or strong demand trends."
            elif rev_pct > 10:
                return f"Strong revenue growth ({rev_pct:.1f}% YoY) - Healthy expansion above industry average, indicates solid business momentum."
            elif rev_pct > 5:
                return f"Moderate revenue growth ({rev_pct:.1f}% YoY) - Steady expansion in-line with market growth, indicates stable business performance."
            elif rev_pct > 0:
                return f"Slow revenue growth ({rev_pct:.1f}% YoY) - Minimal expansion may indicate market saturation or competitive pressures."
            else:
                return f"Negative revenue growth ({rev_pct:.1f}% YoY) - Declining sales is a concerning trend that requires investigation into market dynamics or operational issues."
    
    # Default: return meaningful interpretation based on prompt
    return f"Analysis indicates: {prompt[:150]}..."


def interpret_fundamental_metrics(ratios: List[Dict], growth: List[Dict], quote: Dict) -> Dict[str, str]:
    """
    AI interpretation of fundamental metrics using LLM.
    Generates contextual, nuanced interpretations rather than rule-based thresholds.
    """
    interpretations = {}
    
    # Prepare context for AI
    context = {
        'ratios': ratios[0] if ratios else {},
        'growth': growth[0] if growth else {},
        'quote': quote
    }
    
    # Use AI to interpret each metric with context
    if ratios and len(ratios) > 0:
        ratio = ratios[0]
        roe = ratio.get('returnOnEquity', 0)
        roa = ratio.get('returnOnAssets', 0)
        debt_equity = ratio.get('debtEquityRatio', 0)
        current_ratio = ratio.get('currentRatio', 0)
        
        # AI interpretation for ROE
        roe_prompt = f"Interpret this Return on Equity (ROE) of {roe*100:.1f}% for a stock. Provide context about what this means relative to industry standards, what it indicates about profitability, and what investors should know. Be specific and actionable."
        interpretations['roe'] = call_ai_for_interpretation(roe_prompt, context)
        
        # AI interpretation for ROA
        roa_prompt = f"Interpret this Return on Assets (ROA) of {roa*100:.1f}% for a stock. Explain what this indicates about asset efficiency and how it compares to typical company performance."
        interpretations['roa'] = call_ai_for_interpretation(roa_prompt, context)
        
        # AI interpretation for Debt-to-Equity
        debt_prompt = f"Interpret this Debt-to-Equity ratio of {debt_equity:.2f} for a stock. Explain what this means for financial risk, balance sheet strength, and investor considerations."
        interpretations['debt'] = call_ai_for_interpretation(debt_prompt, context)
        
        # AI interpretation for Current Ratio
        liquidity_prompt = f"Interpret this Current Ratio of {current_ratio:.2f} for a stock. Explain what this indicates about liquidity, short-term financial health, and ability to meet obligations."
        interpretations['liquidity'] = call_ai_for_interpretation(liquidity_prompt, context)
    
    if growth and len(growth) > 0:
        g = growth[0]
        rev_growth = g.get('revenueGrowth', 0)
        ni_growth = g.get('netIncomeGrowth', 0)
        
        # Convert to percentages
        if rev_growth > 1:
            rev_pct = (rev_growth - 1) * 100
        else:
            rev_pct = rev_growth * 100
        
        if ni_growth > 1:
            ni_pct = (ni_growth - 1) * 100
        else:
            ni_pct = ni_growth * 100
        
        # AI interpretation for Revenue Growth
        rev_prompt = f"Interpret this revenue growth of {rev_pct:.1f}% YoY for a stock. Explain what this indicates about business expansion, market position, and growth trajectory. Provide context relative to industry norms."
        interpretations['revenue_growth'] = call_ai_for_interpretation(rev_prompt, context)
        
        # AI interpretation for Net Income Growth
        ni_prompt = f"Interpret this net income growth of {ni_pct:.1f}% YoY for a stock. Explain what this indicates about profitability trends, operational efficiency, and earnings quality. Compare to revenue growth to assess margin trends."
        interpretations['profit_growth'] = call_ai_for_interpretation(ni_prompt, context)
    
    # Check if interpretations are placeholders and use rule-based fallback
    placeholder_check = any('[AI-Generated Interpretation:' in str(v) for v in interpretations.values())
    
    if placeholder_check and ratios and len(ratios) > 0:
        # Use rule-based interpretations as fallback
        ratio = ratios[0]
        roe = ratio.get('returnOnEquity', 0)
        roa = ratio.get('returnOnAssets', 0)
        debt_equity = ratio.get('debtEquityRatio', 0)
        current_ratio = ratio.get('currentRatio', 0)
        
        # ROE interpretation
        if '[AI-Generated Interpretation:' in str(interpretations.get('roe', '')):
            if roe > 0.5:
                interpretations['roe'] = f"Exceptional profitability (ROE: {roe*100:.1f}%) - Well above industry average, indicates highly efficient use of shareholder equity"
            elif roe > 0.25:
                interpretations['roe'] = f"Strong profitability (ROE: {roe*100:.1f}%) - Above average, indicates good efficiency"
            elif roe > 0.15:
                interpretations['roe'] = f"Moderate profitability (ROE: {roe*100:.1f}%) - In-line with industry average"
            else:
                interpretations['roe'] = f"Weak profitability (ROE: {roe*100:.1f}%) - Below average, indicates efficiency concerns"
        
        # ROA interpretation
        if '[AI-Generated Interpretation:' in str(interpretations.get('roa', '')):
            if roa > 0.2:
                interpretations['roa'] = f"Excellent asset efficiency (ROA: {roa*100:.1f}%) - Company generates strong returns on assets"
            elif roa > 0.1:
                interpretations['roa'] = f"Good asset efficiency (ROA: {roa*100:.1f}%) - Reasonable asset utilization"
            else:
                interpretations['roa'] = f"Moderate asset efficiency (ROA: {roa*100:.1f}%) - Room for improvement"
        
        # Debt interpretation
        if '[AI-Generated Interpretation:' in str(interpretations.get('debt', '')):
            if debt_equity < 0.5:
                interpretations['debt'] = f"Low debt (Debt-to-Equity: {debt_equity:.2f}) - Conservative balance sheet, minimal financial risk"
            elif debt_equity < 1.0:
                interpretations['debt'] = f"Moderate debt (Debt-to-Equity: {debt_equity:.2f}) - Reasonable leverage, manageable risk"
            else:
                interpretations['debt'] = f"High debt (Debt-to-Equity: {debt_equity:.2f}) - Elevated leverage, higher financial risk"
        
        # Liquidity interpretation
        if '[AI-Generated Interpretation:' in str(interpretations.get('liquidity', '')):
            if current_ratio > 2.0:
                interpretations['liquidity'] = f"Excellent liquidity (Current Ratio: {current_ratio:.2f}) - Strong ability to meet short-term obligations"
            elif current_ratio > 1.0:
                interpretations['liquidity'] = f"Adequate liquidity (Current Ratio: {current_ratio:.2f}) - Sufficient short-term coverage"
            else:
                interpretations['liquidity'] = f"Tight liquidity (Current Ratio: {current_ratio:.2f}) - May face short-term cash flow challenges"
    
    if placeholder_check and growth and len(growth) > 0:
        g = growth[0]
        rev_growth = g.get('revenueGrowth', 0)
        ni_growth = g.get('netIncomeGrowth', 0)
        
        # Revenue growth interpretation
        if rev_growth > 1:
            rev_pct = (rev_growth - 1) * 100
        else:
            rev_pct = rev_growth * 100
        
        if '[AI-Generated Interpretation:' in str(interpretations.get('revenue_growth', '')):
            if rev_pct > 20:
                interpretations['revenue_growth'] = f"Exceptional revenue growth ({rev_pct:.1f}% YoY) - Strong top-line expansion, indicates market share gains or new product success"
            elif rev_pct > 10:
                interpretations['revenue_growth'] = f"Strong revenue growth ({rev_pct:.1f}% YoY) - Healthy expansion, above industry average"
            elif rev_pct > 5:
                interpretations['revenue_growth'] = f"Moderate revenue growth ({rev_pct:.1f}% YoY) - Steady expansion, in-line with market"
            elif rev_pct > 0:
                interpretations['revenue_growth'] = f"Slow revenue growth ({rev_pct:.1f}% YoY) - Minimal expansion, may indicate market saturation"
            else:
                interpretations['revenue_growth'] = f"Negative revenue growth ({rev_pct:.1f}% YoY) - Declining sales, concerning trend"
        
        # Net income growth interpretation
        if ni_growth > 1:
            ni_pct = (ni_growth - 1) * 100
        else:
            ni_pct = ni_growth * 100
        
        if '[AI-Generated Interpretation:' in str(interpretations.get('profit_growth', '')):
            if ni_pct > 30:
                interpretations['profit_growth'] = f"Exceptional profit growth ({ni_pct:.1f}% YoY) - Outstanding bottom-line expansion, indicates strong operational efficiency or margin expansion"
            elif ni_pct > 15:
                interpretations['profit_growth'] = f"Strong profit growth ({ni_pct:.1f}% YoY) - Healthy earnings expansion, above average"
            elif ni_pct > 5:
                interpretations['profit_growth'] = f"Moderate profit growth ({ni_pct:.1f}% YoY) - Steady earnings growth"
            else:
                interpretations['profit_growth'] = f"Weak profit growth ({ni_pct:.1f}% YoY) - Minimal earnings expansion, may indicate margin pressure"
    
    return interpretations


def interpret_technical_indicators(technical_data: Dict) -> Dict[str, str]:
    """AI interpretation of technical indicators"""
    interpretations = {}
    
    # This would parse the technical analyzer output
    # For now, return structured interpretation framework
    interpretations['trend'] = "Analyze trend strength and direction"
    interpretations['momentum'] = "Interpret RSI and MACD signals"
    interpretations['volatility'] = "Assess Bollinger Bands and ATR"
    interpretations['support_resistance'] = "Explain key price levels"
    
    return interpretations


def interpret_valuation(valuation_data: Dict, pe_ratio: float, sector: str,
                       fundamental_score: float = None, roe: float = None,
                       growth_rate: float = None, eps: float = None) -> str:
    """
    AI interpretation of valuation metrics WITH context about fundamental strength.
    
    When executed by Claude agent in Cursor:
    - The agent generates interpretation directly (no API calls needed)
    - Agent can inject interpretation via agent_interpretation_injector
    
    When executed standalone:
    - Falls back to rule-based logic
    """
    # Try to get agent-generated interpretation first
    try:
        from agent_interpretation_injector import get_agent_interpretation, generate_valuation_key
        # Try to get symbol from context if available
        symbol = valuation_data.get('symbol', 'UNKNOWN') if isinstance(valuation_data, dict) else 'UNKNOWN'
        # If symbol is UNKNOWN, try to extract from profile if available
        if symbol == 'UNKNOWN' and isinstance(valuation_data, dict):
            profile = valuation_data.get('profile', {})
            if profile:
                symbol = profile.get('symbol', 'UNKNOWN')
        key = generate_valuation_key(symbol, pe_ratio)
        agent_interpretation = get_agent_interpretation(key)
        if agent_interpretation and not agent_interpretation.startswith('[AGENT GENERATES'):
            # Only return if it's actual generated text, not a placeholder
            return agent_interpretation
    except Exception:
        pass
    
    # Try API-based AI generation
    try:
        from ai_llm_generator import get_ai_generator
        ai_gen = get_ai_generator()
        if ai_gen.enabled:
            return ai_gen.generate_valuation_interpretation(
                valuation_data, pe_ratio, sector, fundamental_score, roe, growth_rate
            )
    except Exception as e:
        print(f"⚠️  AI valuation interpretation unavailable: {e}. Using rule-based logic.")
    
    # Fallback to rule-based logic
    if not valuation_data:
        return "Valuation analysis unavailable"
    
    peg_value = valuation_data.get('peg_ratio', {}).get('value')
    sector_comparison = valuation_data.get('sector_comparison', {})
    valuation_score = valuation_data.get('valuation_score', {})
    
    interpretation_parts = []
    
    # Handle extremely high P/E edge case (likely due to negative/low earnings)
    if pe_ratio and pe_ratio > 100:
        # Check if this is likely due to negative/low earnings
        # Get EPS from quote if available in context
        eps_context = None
        if isinstance(valuation_data, dict):
            # Try to get EPS from various sources
            quote_data = valuation_data.get('quote') if isinstance(valuation_data.get('quote'), dict) else None
            if quote_data:
                eps_context = quote_data.get('eps')
        
        # Use passed EPS or try to get from context
        eps_to_use = eps if eps is not None else eps_context
        
        if eps_to_use is not None and (eps_to_use <= 0 or eps_to_use < 0.5):
            interpretation_parts.append(
                f"⚠️ P/E ratio of {pe_ratio:.1f} is extremely high, but this is likely misleading due to negative or very low earnings "
                f"(EPS: ${eps_to_use:.2f}). High P/E ratios (>100) often indicate companies with losses or minimal profits, "
                f"not premium valuations. Investors should focus on forward earnings estimates, cash flow metrics, or revenue-based "
                f"valuations rather than P/E ratios when earnings are negative or near zero."
            )
        else:
            interpretation_parts.append(
                f"⚠️ P/E ratio of {pe_ratio:.1f} is extremely high (>100), which typically indicates either: "
                f"(1) Very low or negative earnings making P/E ratio misleading, or (2) Exceptional growth expectations. "
                f"Investors should verify earnings quality and consider forward-looking estimates rather than trailing P/E."
            )
    
    # PEG interpretation - handle type conversion
    if peg_value is not None:
        try:
            if isinstance(peg_value, str):
                # Skip if it's "N/A" or similar
                if peg_value.lower() in ['n/a', 'na', 'none', '']:
                    peg_value = None
                else:
                    peg_value = float(peg_value)
        except (ValueError, TypeError):
            peg_value = None
    
    if peg_value is not None and isinstance(peg_value, (int, float)):
        if peg_value < 0.5:
            interpretation_parts.append(f"PEG ratio of {peg_value:.2f} indicates the stock is significantly undervalued relative to its earnings growth rate. This suggests exceptional value opportunity.")
        elif peg_value < 1.0:
            interpretation_parts.append(f"PEG ratio of {peg_value:.2f} indicates the stock is undervalued relative to growth. The P/E multiple is justified by strong earnings growth.")
        elif peg_value < 1.5:
            interpretation_parts.append(f"PEG ratio of {peg_value:.2f} suggests fair valuation relative to growth. The stock trades at reasonable multiples given its growth rate.")
        elif peg_value < 2.0:
            interpretation_parts.append(f"PEG ratio of {peg_value:.2f} indicates overvaluation relative to growth. The P/E multiple may be stretched given the earnings growth rate.")
        else:
            interpretation_parts.append(f"PEG ratio of {peg_value:.2f} indicates significant overvaluation. The stock trades at premium multiples that may not be sustainable.")
    
    # Sector comparison interpretation with fundamental context
    # Store premium for later use in reconciliation
    premium = None
    if sector_comparison.get('pe_ratio', {}).get('premium_discount'):
        premium = sector_comparison['pe_ratio']['premium_discount']
        if premium > 50:
            interpretation_parts.append(f"Trading at {premium:.1f}% premium to sector average - Significant premium that requires exceptional performance to justify.")
        elif premium > 20:
            if fundamental_score and fundamental_score >= 7.0:
                interpretation_parts.append(
                    f"Trading at {premium:.1f}% premium to sector average. This premium is justified "
                    f"by superior fundamentals (score: {fundamental_score:.1f}/10)"
                )
                if roe:
                    interpretation_parts.append(f", including strong profitability (ROE: {roe*100:.1f}%)")
                if growth_rate:
                    interpretation_parts.append(f" and consistent growth ({growth_rate*100:.1f}% YoY)")
                interpretation_parts.append(
                    ". For quality companies, premium valuations can be sustained if fundamentals remain strong."
                )
            else:
                interpretation_parts.append(f"Trading at {premium:.1f}% premium to sector average - Premium valuation justified by superior fundamentals or growth prospects.")
        elif premium > -20:
            interpretation_parts.append(f"Trading in-line with sector average - Fair valuation relative to peers.")
        else:
            interpretation_parts.append(f"Trading at {abs(premium):.1f}% discount to sector average - Potentially undervalued relative to peers.")
    
    # Valuation score interpretation with reconciliation and fundamental context
    # Consolidate to avoid repetition - build one comprehensive interpretation
    if valuation_score.get('score'):
        score = valuation_score['score']
        peg_overvalued = peg_value is not None and isinstance(peg_value, (int, float)) and peg_value > 1.5
        has_strong_fundamentals = fundamental_score and fundamental_score >= 7.0
        
        # Build consolidated interpretation to avoid repetition
        if peg_overvalued and has_strong_fundamentals and premium and premium > 20:
            # Case: PEG suggests overvaluation but strong fundamentals justify premium
            consolidated = f"Valuation reconciliation: PEG ratio of {peg_value:.2f} suggests overvaluation relative to growth (PEG > 1.5), and the stock trades at a {premium:.1f}% premium to sector average. "
            consolidated += f"However, this premium is justified by exceptional fundamentals (score: {fundamental_score:.1f}/10)"
            if roe:
                consolidated += f", including strong profitability (ROE: {roe*100:.1f}%)"
            if growth_rate:
                consolidated += f" and consistent growth ({growth_rate*100:.1f}% YoY)"
            consolidated += f". The valuation score of {score:.1f}/10 reflects high absolute P/E multiples, but for quality companies with sustainable competitive advantages, premium valuations can be justified if fundamentals remain strong. "
            consolidated += f"Investors should monitor whether earnings growth continues to support the premium valuation."
            interpretation_parts.append(consolidated)
        elif peg_overvalued and score < 5.0:
            # Case: Both PEG and P/E suggest expensive, need clear reconciliation
            if premium and premium > 20:
                reconciliation = f"Valuation assessment: PEG ratio of {peg_value:.2f} indicates overvaluation relative to earnings growth (PEG > 1.5), and the stock trades at a {premium:.1f}% premium to sector average. "
            else:
                reconciliation = f"Valuation assessment: PEG ratio of {peg_value:.2f} indicates overvaluation relative to earnings growth (PEG > 1.5). "
            reconciliation += f"The valuation score of {score:.1f}/10 confirms high absolute P/E multiples. "
            if has_strong_fundamentals:
                reconciliation += f"While fundamentals are strong (score: {fundamental_score:.1f}/10), the combination of high PEG and premium P/E suggests limited upside unless growth accelerates significantly or the company demonstrates exceptional competitive advantages that justify the premium."
            else:
                reconciliation += f"This combination suggests limited upside unless growth accelerates significantly or the company demonstrates exceptional competitive advantages."
            interpretation_parts.append(reconciliation)
        elif score >= 8:
            interpretation_parts.append(f"Overall valuation score of {score:.1f}/10 indicates excellent value opportunity.")
        elif score >= 6:
            interpretation_parts.append(f"Overall valuation score of {score:.1f}/10 indicates reasonable valuation.")
        elif score >= 4:
            if has_strong_fundamentals:
                interpretation_parts.append(
                    f"Overall valuation score of {score:.1f}/10 indicates expensive valuation. However, "
                    f"strong fundamentals (score: {fundamental_score:.1f}/10) suggest the premium may be "
                    f"justified by exceptional competitive position and execution."
                )
            else:
                interpretation_parts.append(f"Overall valuation score of {score:.1f}/10 indicates expensive valuation.")
        else:
            if has_strong_fundamentals:
                interpretation_parts.append(
                    f"Overall valuation score of {score:.1f}/10 indicates very expensive valuation. However, "
                    f"strong fundamentals (score: {fundamental_score:.1f}/10) suggest the premium may be "
                    f"justified by exceptional competitive position and execution."
                )
            else:
                interpretation_parts.append(f"Overall valuation score of {score:.1f}/10 indicates very expensive valuation with limited upside potential.")
        
        # Additional reconciliation only if not already covered above
        if not (peg_overvalued and has_strong_fundamentals):
            # Reconcile PEG vs P/E valuation contradiction
            if peg_value is not None and isinstance(peg_value, (int, float)):
                if peg_value < 1.0 and score < 6.0:
                    # PEG suggests fair/undervalued but P/E is expensive
                    pe_ratio_val = valuation_data.get('pe_ratio', pe_ratio) if valuation_data else pe_ratio
                    sector_avg_val = sector_comparison.get('pe_ratio', {}).get('sector_avg', 25.0) if sector_comparison.get('pe_ratio') else 25.0
                    interpretation_parts.append(f"Valuation reconciliation: PEG ratio of {peg_value:.2f} suggests the stock is undervalued relative to its earnings growth rate (PEG < 1.0 indicates growth-adjusted value). However, the valuation score of {score:.1f}/10 reflects that absolute P/E ratios ({pe_ratio_val:.1f}) are elevated relative to sector average ({sector_avg_val:.1f}). This means: (1) The company's strong earnings growth justifies current multiples on a growth-adjusted basis, but (2) absolute P/E levels are high and require continued exceptional growth to sustain. For investors, this suggests the stock may be fairly valued IF growth continues at current rates, but vulnerable if growth slows.")
                elif peg_value > 1.5 and score < 5.0:
                    # Both PEG and P/E suggest expensive
                    interpretation_parts.append(f"Both PEG ratio ({peg_value:.2f}) and absolute P/E levels indicate expensive valuation. PEG > 1.5 suggests overvaluation relative to growth, while the valuation score of {score:.1f}/10 confirms high absolute multiples. This combination suggests limited upside unless growth accelerates significantly or the company demonstrates exceptional competitive advantages.")
                elif peg_value < 1.5 and score >= 6.0:
                    # PEG reasonable and P/E reasonable
                    interpretation_parts.append(f"Valuation appears reasonable: PEG ratio of {peg_value:.2f} suggests fair growth-adjusted valuation, and the valuation score of {score:.1f}/10 indicates reasonable absolute P/E levels. This combination suggests the stock is fairly valued relative to both growth prospects and absolute earnings multiples.")
                elif peg_value > 1.5 and score >= 6.0:
                    # PEG expensive but P/E reasonable
                    interpretation_parts.append(f"Valuation perspective: PEG ratio of {peg_value:.2f} suggests premium relative to growth, but the valuation score of {score:.1f}/10 indicates reasonable absolute P/E levels. This suggests the stock trades at fair absolute multiples, but growth expectations embedded in the price are high. Monitor whether actual growth meets or exceeds these expectations.")
    
    return " ".join(interpretation_parts) if interpretation_parts else "Valuation analysis complete."


def interpret_technical_analysis(technical_data_dict: Dict, fundamental_score: float = None) -> str:
    """
    AI interpretation of technical indicators with context
    """
    # Try to get agent-generated interpretation first
    try:
        from agent_interpretation_injector import get_agent_interpretation, generate_technical_key
        # Try to get symbol from context if available
        symbol = technical_data_dict.get('symbol', 'UNKNOWN') if isinstance(technical_data_dict, dict) else 'UNKNOWN'
        key = generate_technical_key(symbol)
        agent_interpretation = get_agent_interpretation(key)
        if agent_interpretation:
            return agent_interpretation
    except Exception:
        pass
    
    # Try API-based AI generation
    try:
        from ai_llm_generator import get_ai_generator
        ai_gen = get_ai_generator()
        if ai_gen.enabled:
            return ai_gen.generate_technical_interpretation(technical_data_dict, fundamental_score)
    except Exception as e:
        print(f"⚠️  AI technical interpretation unavailable: {e}. Using rule-based logic.")
    
    # Fallback to rule-based logic
    trend_analysis = technical_data_dict.get('trend_analysis', {})
    indicators = technical_data_dict.get('indicators', {})
    trading_signals = technical_data_dict.get('trading_signals', {})
    
    interpretation_parts = []
    
    # Trend interpretation
    trend = trend_analysis.get('trend', '')
    price_vs_sma200 = trend_analysis.get('price_vs_sma200', '')
    
    if trend == 'Downtrend' and price_vs_sma200 == 'Above':
        interpretation_parts.append(
            "Short-term downtrend within longer-term uptrend. Price remains above SMA 200, "
            "indicating the primary trend is still intact. The current weakness appears to be "
            "a pullback within a larger uptrend, which can present entry opportunities for "
            "long-term investors."
        )
    elif trend == 'Uptrend':
        interpretation_parts.append(
            "Strong uptrend with price above key moving averages. Momentum is positive, "
            "indicating continued strength. However, consider entry timing to avoid buying "
            "at extended levels."
        )
    elif trend == 'Downtrend':
        interpretation_parts.append(
            "Downtrend in progress with price below key moving averages. This suggests "
            "negative momentum and potential for further weakness. Wait for trend reversal "
            "signals before considering entry."
        )
    elif trend == 'Sideways':
        interpretation_parts.append(
            "Sideways consolidation pattern. Price is range-bound, indicating indecision "
            "between buyers and sellers. Look for breakout above resistance or breakdown "
            "below support for directional clarity."
        )
    
    # RSI interpretation
    rsi = indicators.get('rsi')
    if rsi is not None:
        if 30 < rsi < 50:
            interpretation_parts.append(
                f"RSI at {rsi:.1f} is in neutral territory, indicating neither overbought nor "
                f"oversold conditions. This suggests the stock is not at extreme levels and "
                f"has room to move in either direction. For entry timing, this neutral RSI "
                f"combined with strong fundamentals suggests potential for upward movement."
            )
        elif rsi > 70:
            interpretation_parts.append(
                f"RSI at {rsi:.1f} indicates overbought conditions. While this suggests "
                f"potential for short-term pullback, strong fundamentals may support the "
                f"current level. Consider waiting for pullback to enter."
            )
        elif rsi < 30:
            interpretation_parts.append(
                f"RSI at {rsi:.1f} indicates oversold conditions, suggesting potential for "
                f"bounce. This may present entry opportunity, especially if fundamentals "
                f"remain strong."
            )
    
    # MACD interpretation
    macd_signal = trading_signals.get('macd_signal', '')
    if macd_signal == 'Bullish':
        interpretation_parts.append(
            "MACD shows bullish signal, indicating positive momentum. This supports the "
            "case for upward price movement, especially when combined with strong fundamentals."
        )
    elif macd_signal == 'Bearish':
        interpretation_parts.append(
            "MACD shows bearish signal, indicating negative momentum. However, this may be "
            "short-term noise if fundamentals remain strong. Monitor for confirmation."
        )
    elif macd_signal == 'Neutral':
        interpretation_parts.append(
            "MACD is neutral, indicating lack of clear momentum direction. This suggests "
            "consolidation or indecision in the market."
        )
    
    # Context with fundamentals
    if fundamental_score and fundamental_score >= 7.0:
        interpretation_parts.append(
            f"Given strong fundamentals (score: {fundamental_score:.1f}/10), short-term technical "
            f"weakness may present buying opportunities for long-term investors. Technical "
            f"indicators are more relevant for entry timing than investment decision for "
            f"quality companies."
        )
    elif fundamental_score and fundamental_score < 5.0:
        interpretation_parts.append(
            f"With weak fundamentals (score: {fundamental_score:.1f}/10), technical indicators "
            f"become more critical. Wait for both technical and fundamental improvement before "
            f"considering entry."
        )
    
    return " ".join(interpretation_parts) if interpretation_parts else "Technical analysis complete."


def synthesize_investment_thesis(fundamental_data: Dict, technical_data: Dict, combined_data: Dict) -> str:
    """
    Synthesize investment thesis combining fundamental, technical, and sentiment analysis.
    Generates actual content rather than placeholder text.
    
    Uses live AI generator with contradiction handling when available.
    """
    # Try live AI generator first (handles contradictions)
    try:
        from agent_ai_generator_live import generate_thesis_interpretation_live
        # Try to get symbol from context if available
        symbol = fundamental_data.get('profile', {}).get('symbol', 'UNKNOWN') if isinstance(fundamental_data, dict) else 'UNKNOWN'
        if symbol == 'UNKNOWN':
            symbol = technical_data.get('symbol', 'UNKNOWN') if isinstance(technical_data, dict) else 'UNKNOWN'
        if symbol != 'UNKNOWN':
            live_thesis = generate_thesis_interpretation_live(symbol, fundamental_data, technical_data, combined_data)
            # Check if it's a placeholder or actual content
            if live_thesis and '[AGENT GENERATES' not in live_thesis:
                return live_thesis
    except Exception as e:
        pass  # Fall through to other methods
    
    # Try to get agent-generated interpretation from cache
    try:
        from agent_interpretation_injector import get_agent_interpretation, generate_thesis_key
        # Try to get symbol from context if available
        symbol = fundamental_data.get('profile', {}).get('symbol', 'UNKNOWN') if isinstance(fundamental_data, dict) else 'UNKNOWN'
        if symbol == 'UNKNOWN':
            symbol = technical_data.get('symbol', 'UNKNOWN') if isinstance(technical_data, dict) else 'UNKNOWN'
        key = generate_thesis_key(symbol)
        agent_interpretation = get_agent_interpretation(key)
        if agent_interpretation:
            return agent_interpretation
    except Exception:
        pass
    
    # Try API-based AI generation
    try:
        from ai_llm_generator import get_ai_generator
        ai_gen = get_ai_generator()
        if ai_gen.enabled:
            return ai_gen.generate_investment_thesis(fundamental_data, technical_data, combined_data)
    except Exception as e:
        print(f"⚠️  AI investment thesis unavailable: {e}. Using rule-based logic.")
    
    # Fallback to rule-based logic
    fundamental_score = combined_data.get('fundamental_score', 0)
    technical_score = combined_data.get('technical_score', 0)
    sentiment_score = combined_data.get('sentiment_score', 0)
    sentiment_classification = combined_data.get('sentiment_classification', 'Neutral')
    alignment = combined_data.get('alignment', '')
    valuation_risk = combined_data.get('valuation_risk', 1.0)
    fundamental_details = combined_data.get('fundamental_score_details', {})
    technical_details = combined_data.get('technical_score_details', {})
    
    thesis_parts = []
    
    # Fundamental analysis summary
    if fundamental_score >= 8.0:
        thesis_parts.append(f"The stock demonstrates exceptional fundamental strength (score: {fundamental_score}/10), with strong profitability, growth, and financial health metrics.")
    elif fundamental_score >= 6.0:
        thesis_parts.append(f"The stock shows solid fundamentals (score: {fundamental_score}/10), with reasonable profitability and growth characteristics.")
    else:
        thesis_parts.append(f"Fundamental analysis reveals concerns (score: {fundamental_score}/10), with below-average metrics indicating potential operational or financial challenges.")
    
    # Technical analysis summary
    if technical_score >= 7.0:
        thesis_parts.append(f"Technical indicators suggest strong momentum (score: {technical_score}/10), with favorable trend alignment and positive price action.")
    elif technical_score >= 5.0:
        thesis_parts.append(f"Technical setup is moderate (score: {technical_score}/10), with mixed signals requiring careful monitoring.")
    else:
        thesis_parts.append(f"Technical indicators show weakness (score: {technical_score}/10), with concerning trend and momentum patterns.")
    
    # Alignment analysis
    if "Strong Alignment" in alignment:
        thesis_parts.append(f"The analysis shows strong alignment across fundamental, technical, and sentiment dimensions, providing confidence in the investment thesis.")
    elif "Divergence" in alignment:
        thesis_parts.append(f"However, there is divergence between different analysis dimensions, requiring careful consideration of conflicting signals.")
    
    # Valuation context
    if valuation_risk > 1.5:
        thesis_parts.append(f"The stock trades at a significant premium ({valuation_risk:.2f}x sector average), requiring continued exceptional performance to justify current valuation levels.")
    elif valuation_risk > 1.2:
        thesis_parts.append(f"Valuation is elevated ({valuation_risk:.2f}x sector average), but may be justified by strong fundamentals and growth prospects.")
    else:
        thesis_parts.append(f"Valuation appears reasonable ({valuation_risk:.2f}x sector average), providing attractive risk-adjusted opportunity.")
    
    # Sentiment context
    if sentiment_classification == 'Bullish':
        thesis_parts.append(f"Market sentiment is bullish (score: {sentiment_score:.3f}), supporting positive outlook.")
    elif sentiment_classification == 'Bearish':
        thesis_parts.append(f"Market sentiment is bearish (score: {sentiment_score:.3f}), which may weigh on near-term performance.")
    
    # Risk considerations
    if fundamental_score < 6.0 or technical_score < 5.0:
        thesis_parts.append("Key risks include fundamental weakness or technical deterioration that could impact investment returns.")
    
    # Combine into cohesive thesis
    thesis = " ".join(thesis_parts)
    
    # Ensure minimum length and quality
    if len(thesis) < 200:
        thesis += " Overall, the investment opportunity requires careful evaluation of both strengths and risks before making investment decisions."
    
    return thesis

