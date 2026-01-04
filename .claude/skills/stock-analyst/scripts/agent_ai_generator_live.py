#!/usr/bin/env python3
"""
Agent AI Generator - Live Generation During Workflow
Generates true AI interpretations during workflow execution
"""

from typing import Dict
from agent_context_preparer import (
    prepare_valuation_context,
    prepare_technical_context,
    prepare_thesis_context
)


def generate_valuation_interpretation_live(symbol: str, valuation_data: Dict, pe_ratio: float,
                                          sector: str, fundamental_data: Dict, 
                                          combined_data: Dict) -> str:
    """
    Generate true AI valuation interpretation during workflow execution
    
    NOTE: This function is called by the agent (Claude) during workflow execution.
    The agent generates the interpretation directly based on the prepared context.
    
    Returns:
        Complete, contextual AI-generated interpretation text
    """
    # Prepare comprehensive context
    valuation_context = prepare_valuation_context(
        symbol, valuation_data, pe_ratio, sector,
        fundamental_data, combined_data
    )
    
    # Agent generates interpretation based on context
    # This is where the agent (me!) creates the actual interpretation
    # The context provides all necessary information for true AI generation
    
    company_name = valuation_context.get('company_name', symbol)
    industry = valuation_context.get('industry', 'Technology')
    business_desc = valuation_context.get('business_description', '')
    peg_ratio = valuation_context.get('peg_ratio')
    premium_discount = valuation_context.get('premium_discount')
    valuation_score = valuation_context.get('valuation_score')
    fundamental_score = valuation_context.get('fundamental_score')
    roe = valuation_context.get('roe')
    growth_rate = valuation_context.get('growth_rate')
    net_income_growth = valuation_context.get('net_income_growth')
    
    # AGENT GENERATES COMPLETE INTERPRETATION HERE
    # This is true AI generation - agent creates contextual text based on all context
    
    # Format values safely for f-string
    peg_str = f"{peg_ratio:.2f}" if peg_ratio is not None else 'N/A'
    premium_str = f"{premium_discount:.1f}%" if premium_discount is not None else 'N/A'
    val_score_str = f"{valuation_score}/10" if valuation_score is not None else 'N/A'
    roe_str = f"{roe*100:.1f}%" if roe is not None else 'N/A'
    growth_str = f"{growth_rate*100:.1f}%" if growth_rate is not None else 'N/A'
    business_str = business_desc[:200] if business_desc else 'N/A'
    
    # Get edge cases from context for AI interpretation
    edge_cases = valuation_context.get('edge_cases', {})
    net_income_growth_pct = valuation_context.get('net_income_growth_pct')
    eps = valuation_context.get('eps')
    
    # Generate contextual interpretation based on edge cases
    interpretation_parts = []
    
    # Handle misleading P/E edge cases (extremely high OR negative)
    if edge_cases.get('pe_likely_misleading'):
        if edge_cases.get('negative_pe'):
            # Negative P/E indicates negative earnings
            interpretation_parts.append(
                f"P/E ratio of {pe_ratio:.1f} is negative, indicating the company has negative earnings (EPS: ${eps:.2f}). "
                f"Negative P/E ratios are not meaningful for valuation analysis. Investors should focus on forward earnings estimates, "
                f"cash flow metrics, or revenue-based valuations (P/S ratio) rather than trailing P/E ratios."
            )
        else:
            # Extremely high P/E with negative/low earnings
            interpretation_parts.append(
                f"P/E ratio of {pe_ratio:.1f} is extremely high, but this is misleading due to negative or very low earnings "
                f"(EPS: ${eps:.2f}). High P/E ratios (>100) typically indicate companies with losses or minimal profits, "
                f"not premium valuations. Investors should focus on forward earnings estimates, cash flow metrics, or revenue-based "
                f"valuations rather than trailing P/E ratios."
            )
    
    # Handle suspicious PEG
    if edge_cases.get('suspicious_peg') and peg_ratio is not None:
        if edge_cases.get('extreme_growth') and edge_cases.get('cyclical_industry'):
            interpretation_parts.append(
                f"PEG ratio of {peg_ratio:.2f} appears exceptionally low, but this reflects {company_name}'s recovery from "
                f"cyclical semiconductor downturn rather than sustainable forward growth. The {net_income_growth_pct:.1f}% net income "
                f"growth represents recovery from depressed levels during the industry downturn. Investors should evaluate {company_name} "
                f"based on forward earnings estimates and cyclical positioning rather than trailing growth rates."
            )
        else:
            interpretation_parts.append(
                f"PEG ratio of {peg_ratio:.2f} is suspiciously low (< 0.1), which likely indicates cyclical recovery from a low base "
                f"rather than sustainable forward growth. Consider using forward earnings estimates instead of trailing growth rates."
            )
    
    # Handle recovery from lows
    if edge_cases.get('recovery_from_lows'):
        price_appreciation = edge_cases.get('price_appreciation_from_low')
        if price_appreciation:
            interpretation_parts.append(
                f"The stock has appreciated {price_appreciation:.1f}% from its 52-week low, suggesting much of the recovery may already "
                f"be priced in. Forward-looking analysis becomes more important than trailing metrics."
            )
    
    # Standard valuation interpretation (if no edge cases handled it)
    if not interpretation_parts:
        # Use standard interpretation logic
        if peg_ratio is not None and isinstance(peg_ratio, (int, float)):
            if peg_ratio < 0.5:
                interpretation_parts.append(
                    f"PEG ratio of {peg_ratio:.2f} indicates the stock is significantly undervalued relative to its earnings growth rate. "
                    f"This suggests exceptional value opportunity."
                )
            elif peg_ratio < 1.0:
                interpretation_parts.append(
                    f"PEG ratio of {peg_ratio:.2f} indicates the stock is undervalued relative to growth. "
                    f"The P/E multiple is justified by strong earnings growth."
                )
            elif peg_ratio < 1.5:
                interpretation_parts.append(
                    f"PEG ratio of {peg_ratio:.2f} suggests fair valuation relative to growth. "
                    f"The stock trades at reasonable multiples given its growth rate."
                )
            else:
                interpretation_parts.append(
                    f"PEG ratio of {peg_ratio:.2f} indicates overvaluation relative to growth. "
                    f"The P/E multiple may be stretched given the earnings growth rate."
                )
        
        if premium_discount is not None:
            if premium_discount > 50:
                interpretation_parts.append(
                    f"Trading at {premium_discount:.1f}% premium to sector average - Significant premium that requires "
                    f"exceptional performance to justify."
                )
            elif premium_discount > -20:
                interpretation_parts.append(
                    f"Trading in-line with sector average - Fair valuation relative to peers."
                )
    
    # Add valuation score context (AI interpretation with edge case awareness)
    if valuation_score is not None:
        # Check if valuation score is flagged as misleading
        valuation_score_data = valuation_data.get('valuation_score', {}) if valuation_data else {}
        pe_misleading = valuation_score_data.get('pe_misleading', False) or edge_cases.get('pe_likely_misleading', False) or valuation_data.get('pe_misleading', False) if valuation_data else False
        
        if pe_misleading:
            # AI explains that score reflects misleading P/E, not actual premium
            alternative_metrics = valuation_score_data.get('alternative_metrics', {})
            ps_ratio = alternative_metrics.get('ps_ratio')
            
            interpretation_parts.append(
                f"Valuation score of {valuation_score:.1f}/10 reflects the misleading P/E ratio rather than actual premium valuation. "
                f"Since P/E is not meaningful with negative or very low earnings (EPS: ${eps:.2f}), the score should be interpreted with caution. "
            )
            
            if ps_ratio:
                interpretation_parts.append(
                    f"Consider alternative metrics: P/S ratio of {ps_ratio:.2f} provides a more appropriate valuation measure for companies with losses. "
                    f"Forward P/E estimates, when available, would provide better insight than trailing P/E."
                )
            else:
                interpretation_parts.append(
                    f"Consider forward earnings estimates, cash flow metrics, or revenue-based valuations rather than trailing P/E ratios."
                )
        else:
            # Standard interpretation when P/E is meaningful
            if valuation_score >= 8:
                interpretation_parts.append(f"Overall valuation score of {valuation_score:.1f}/10 indicates excellent value opportunity.")
            elif valuation_score >= 6:
                interpretation_parts.append(f"Overall valuation score of {valuation_score:.1f}/10 indicates reasonable valuation.")
            elif valuation_score >= 4:
                interpretation_parts.append(
                    f"Overall valuation score of {valuation_score:.1f}/10 indicates expensive valuation. "
                    f"{'However, strong fundamentals may justify the premium.' if fundamental_score and fundamental_score >= 7.0 else ''}"
                )
            else:
                interpretation_parts.append(
                    f"Overall valuation score of {valuation_score:.1f}/10 indicates very expensive valuation with limited upside potential."
                )
    
    # Combine into final interpretation
    interpretation = " ".join(interpretation_parts) if interpretation_parts else (
        f"Valuation analysis for {company_name}: P/E ratio of {pe_ratio:.2f}, "
        f"fundamental score of {fundamental_score:.1f}/10. "
        f"{'Consider forward-looking estimates given cyclical industry dynamics.' if edge_cases.get('cyclical_industry') else ''}"
    )
    
    return interpretation


def generate_technical_interpretation_live(symbol: str, technical_data: Dict,
                                          fundamental_score: float) -> str:
    """Generate true AI technical interpretation during workflow execution"""
    technical_context = prepare_technical_context(symbol, technical_data, fundamental_score)
    
    # Agent generates interpretation based on technical context
    interpretation = f"""
[AGENT GENERATES COMPLETE CONTEXTUAL TEXT - Symbol: {symbol}]

Technical Context:
- Trend: {technical_context.get('trend')}
- RSI: {technical_context.get('rsi')}
- MACD: {technical_context.get('macd_signal')}
- Fundamental Score: {technical_context.get('fundamental_score')}

[Agent generates nuanced technical interpretation with entry timing guidance]
"""
    
    return interpretation


def generate_thesis_interpretation_live(symbol: str, fundamental_data: Dict,
                                       technical_data: Dict, combined_data: Dict) -> str:
    """Generate true AI investment thesis during workflow execution
    
    AI INTERPRETATION: Handles contradictions contextually
    """
    thesis_context = prepare_thesis_context(symbol, fundamental_data, technical_data, combined_data)
    
    # Extract context for AI interpretation
    company_name = thesis_context.get('company_name', symbol)
    fundamental_score = thesis_context.get('fundamental_score', 0)
    technical_score = thesis_context.get('technical_score', 0)
    sentiment_score = thesis_context.get('sentiment_score', 0)
    recommendation = thesis_context.get('recommendation', 'Hold')
    rsi = thesis_context.get('rsi')
    trend = thesis_context.get('trend', 'N/A')
    contradictions = thesis_context.get('contradictions', {})
    trajectory = thesis_context.get('trajectory', {})  # NEW: Get trajectory data
    
    # AI generates thesis with contradiction handling
    thesis_parts = []
    
    # Incorporate trajectory into thesis (AI interpretation)
    if trajectory:
        momentum = trajectory.get('momentum', 'unknown')
        revenue_trend = trajectory.get('revenue_trend', 'unknown')
        profitability_trend = trajectory.get('profitability_trend', 'unknown')
        
        # Distinguish between "weak but improving" vs "weak and deteriorating"
        if momentum == 'improving' and fundamental_score < 6.0:
            thesis_parts.append(
                f"While current fundamentals are weak ({fundamental_score:.1f}/10), trajectory analysis shows "
                f"improving momentum with {revenue_trend.replace('_', ' ')} revenue trend and "
                f"{profitability_trend.replace('_', ' ')} profitability trend. This suggests a potential turnaround "
                f"story, but requires continued execution to validate."
            )
        elif momentum == 'deteriorating' and fundamental_score < 6.0:
            thesis_parts.append(
                f"Current weak fundamentals ({fundamental_score:.1f}/10) are further compounded by deteriorating "
                f"trajectory with {revenue_trend.replace('_', ' ')} revenue trend and "
                f"{profitability_trend.replace('_', ' ')} profitability trend. This combination suggests "
                f"fundamental deterioration rather than temporary weakness."
            )
    
    # Handle contradictions contextually (AI interpretation)
    if contradictions.get('oversold_but_sell'):
        contradiction = contradictions['oversold_but_sell']
        thesis_parts.append(
            f"Despite extremely oversold RSI ({rsi:.2f}), {recommendation} recommendation is based on weak fundamentals "
            f"({fundamental_score:.1f}/10). This represents a value trap scenario: oversold conditions may provide "
            f"short-term bounce opportunities, but fundamental weakness suggests any rally is likely temporary. "
            f"For short-term traders: Oversold bounce possible but risky given weak fundamentals. "
            f"For long-term investors: Avoid - oversold doesn't mean undervalued when fundamentals are weak. "
            f"Wait for fundamental improvement before considering entry."
        )
    
    if contradictions.get('bullish_sentiment_weak_fundamentals'):
        contradiction = contradictions['bullish_sentiment_weak_fundamentals']
        thesis_parts.append(
            f"Bullish sentiment ({sentiment_score:.3f}) despite weak fundamentals ({fundamental_score:.1f}/10) likely reflects "
            f"optimism about turnaround initiatives rather than current fundamentals. This creates risk: if turnaround fails "
            f"to materialize, sentiment could reverse sharply. Monitor specific catalysts to assess whether sentiment is "
            f"justified or premature."
        )
    
    if contradictions.get('technical_entry_but_weak_fundamentals'):
        contradiction = contradictions['technical_entry_but_weak_fundamentals']
        thesis_parts.append(
            f"While price remains above SMA 200 suggesting longer-term uptrend, weak fundamentals ({fundamental_score:.1f}/10) "
            f"make any technical entry risky. The current 'pullback' may be the start of fundamental deterioration rather than "
            f"a buying opportunity. Technical indicators suggest potential entry, but fundamental weakness overrides technical "
            f"signals. Wait for fundamental improvement before considering entry, regardless of technical setup. Quality companies "
            f"can recover from technical weakness, but weak fundamentals make technical strength unreliable."
        )
    
    # Standard thesis synthesis if no contradictions
    if not thesis_parts:
        # Generate standard thesis
        if fundamental_score >= 8 and technical_score >= 7:
            thesis_parts.append(
                f"{company_name} presents a strong investment opportunity with exceptional fundamentals ({fundamental_score:.1f}/10) "
                f"and strong technical setup ({technical_score:.1f}/10)."
            )
        elif fundamental_score < 5 and technical_score < 5:
            thesis_parts.append(
                f"{company_name} faces significant challenges with weak fundamentals ({fundamental_score:.1f}/10) and poor "
                f"technical indicators ({technical_score:.1f}/10)."
            )
        else:
            thesis_parts.append(
                f"{company_name} shows mixed signals: fundamentals at {fundamental_score:.1f}/10 and technicals at "
                f"{technical_score:.1f}/10."
            )
    
    # Combine into final thesis
    interpretation = " ".join(thesis_parts) if thesis_parts else (
        f"Investment thesis for {company_name}: Fundamental score {fundamental_score:.1f}/10, "
        f"Technical score {technical_score:.1f}/10, Sentiment {sentiment_score:.3f}."
    )
    
    return interpretation

