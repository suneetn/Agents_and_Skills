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
    
    Args:
        symbol: Stock symbol
        valuation_data: Valuation analysis data
        pe_ratio: Current P/E ratio
        sector: Sector name
        fundamental_data: Fundamental analysis data
        combined_data: Combined analysis results
        
    Returns:
        Dict with comprehensive context for agent to generate interpretation
    """
    profile = fundamental_data.get('profile', {})
    quote = fundamental_data.get('quote', {})
    ratios = fundamental_data.get('ratios', [])
    growth = fundamental_data.get('growth', [])
    
    peg_value = valuation_data.get('peg_ratio', {}).get('value') if valuation_data else None
    sector_comparison = valuation_data.get('sector_comparison', {}) if valuation_data else {}
    valuation_score = valuation_data.get('valuation_score', {}) if valuation_data else {}
    premium = sector_comparison.get('pe_ratio', {}).get('premium_discount') if sector_comparison.get('pe_ratio') else None
    
    # Extract key metrics
    roe = ratios[0].get('returnOnEquity') if ratios and len(ratios) > 0 else None
    growth_rate = growth[0].get('revenueGrowth') if growth and len(growth) > 0 else None
    net_income_growth = growth[0].get('netIncomeGrowth') if growth and len(growth) > 0 else None
    profit_margin = ratios[0].get('netProfitMargin') if ratios and len(ratios) > 0 else None
    debt_to_equity = ratios[0].get('debtEquityRatio') if ratios and len(ratios) > 0 else None
    
    # Get business description (truncate for context)
    business_description = profile.get('description', '')
    if business_description and len(business_description) > 500:
        business_description = business_description[:500] + "..."
    
    # Calculate growth percentages for edge case detection
    revenue_growth_pct = None
    net_income_growth_pct = None
    if growth_rate:
        if growth_rate > 1:
            revenue_growth_pct = (growth_rate - 1) * 100
        else:
            revenue_growth_pct = growth_rate * 100
    if net_income_growth:
        if net_income_growth > 1:
            net_income_growth_pct = (net_income_growth - 1) * 100
        else:
            net_income_growth_pct = net_income_growth * 100
    
    # Detect edge cases for AI interpretation (not algorithmic rules)
    current_price = quote.get('price', 0) if quote else 0
    year_low = quote.get('yearLow', 0) if quote else 0
    year_high = quote.get('yearHigh', 0) if quote else 0
    
    # Cyclical industries (for context, not hardcoded rules)
    cyclical_industries = ['Semiconductors', 'Energy', 'Materials', 'Basic Materials', 
                          'Oil & Gas', 'Metals & Mining']
    is_cyclical_industry = sector in cyclical_industries or any(
        ind in profile.get('industry', '') for ind in ['Semiconductor', 'Memory', 'Energy', 'Mining']
    )
    
    # Recovery indicators (for context)
    recovery_from_lows = False
    if year_low and current_price and year_low > 0:
        price_appreciation = (current_price / year_low - 1) * 100
        recovery_from_lows = price_appreciation > 100  # More than doubled from low
    
    # Check for extremely high P/E (likely due to negative/low earnings) OR negative P/E
    eps = quote.get('eps', 0) if quote else 0
    extremely_high_pe = pe_ratio > 100 if pe_ratio else False
    negative_pe = pe_ratio < 0 if pe_ratio else False
    negative_or_low_earnings = eps is not None and (eps <= 0 or eps < 0.5)
    
    # Edge case flags (for AI to interpret, not algorithmic rules)
    edge_cases = {
        'suspicious_peg': peg_value is not None and isinstance(peg_value, (int, float)) and peg_value < 0.1,
        'extreme_growth': net_income_growth_pct is not None and net_income_growth_pct > 200,
        'cyclical_industry': is_cyclical_industry,
        'recovery_from_lows': recovery_from_lows,
        'price_appreciation_from_low': price_appreciation if year_low and current_price else None,
        'near_52_week_high': year_high and current_price and (current_price / year_high) > 0.95 if year_high else False,
        'extremely_high_pe': extremely_high_pe,
        'negative_pe': negative_pe,  # NEW: Flag negative P/E
        'negative_or_low_earnings': negative_or_low_earnings,
        'pe_likely_misleading': (extremely_high_pe and negative_or_low_earnings) or negative_pe  # Updated: Include negative P/E
    }
    
    return {
        'symbol': symbol,
        'company_name': profile.get('companyName', ''),
        'sector': sector,
        'industry': profile.get('industry', ''),
        'business_description': business_description,
        'pe_ratio': pe_ratio,
        'peg_ratio': peg_value,
        'premium_discount': premium,
        'valuation_score': valuation_score.get('score') if valuation_score else None,
        'fundamental_score': combined_data.get('fundamental_score') if combined_data else None,
        'roe': roe,
        'growth_rate': growth_rate,
        'revenue_growth_pct': revenue_growth_pct,
        'net_income_growth': net_income_growth,
        'net_income_growth_pct': net_income_growth_pct,
        'market_cap': quote.get('marketCap') if quote else None,
        'current_price': current_price,
        'year_low': year_low,
        'year_high': year_high,
        'eps': eps,
        'edge_cases': edge_cases,  # For AI to interpret contextually
        'key_metrics': {
            'profit_margin': profit_margin,
            'debt_to_equity': debt_to_equity,
        }
    }


def prepare_technical_context(symbol: str, technical_data: Dict, 
                             fundamental_score: Optional[float]) -> Dict:
    """
    Prepares comprehensive context for technical interpretation
    
    Args:
        symbol: Stock symbol
        technical_data: Technical analysis data
        fundamental_score: Fundamental score for context
        
    Returns:
        Dict with comprehensive context for agent to generate technical interpretation
    """
    technical_data_dict = technical_data.get('data', {}) if technical_data else {}
    trend_analysis = technical_data_dict.get('trend_analysis', {})
    indicators = technical_data_dict.get('indicators', {})
    trading_signals = technical_data_dict.get('trading_signals', {})
    
    rsi = indicators.get('rsi', None)
    current_price = technical_data_dict.get('current_price')
    price_changes = technical_data_dict.get('price_changes', {})
    
    # Edge case flags for AI interpretation (not hardcoded rules)
    technical_edge_cases = {
        'rsi_near_overbought': rsi is not None and 65 <= rsi < 70,
        'rsi_overbought': rsi is not None and rsi >= 70,
        'rsi_near_oversold': rsi is not None and 30 < rsi <= 35,
        'strong_uptrend': trend_analysis.get('trend') == 'Uptrend' and trend_analysis.get('strength') == 'Strong',
        'price_near_highs': current_price and technical_data_dict.get('year_high') and (
            current_price / technical_data_dict.get('year_high', 1)) > 0.95 if technical_data_dict.get('year_high') else False
    }
    
    return {
        'symbol': symbol,
        'trend': trend_analysis.get('trend', 'N/A'),
        'trend_strength': trend_analysis.get('strength', 'N/A'),
        'price_vs_sma50': trend_analysis.get('price_vs_sma50', 'N/A'),
        'price_vs_sma200': trend_analysis.get('price_vs_sma200', 'N/A'),
        'rsi': rsi,
        'macd_signal': trading_signals.get('macd_signal', 'N/A'),
        'overall_signal': trading_signals.get('overall_signal', 'N/A'),
        'fundamental_score': fundamental_score,
        'current_price': current_price,
        'price_changes': price_changes,
        'edge_cases': technical_edge_cases  # For AI to interpret contextually
    }


def prepare_thesis_context(symbol: str, fundamental_data: Dict, technical_data: Dict,
                          combined_data: Dict) -> Dict:
    """
    Prepares comprehensive context for investment thesis
    
    Args:
        symbol: Stock symbol
        fundamental_data: Fundamental analysis data
        technical_data: Technical analysis data
        combined_data: Combined analysis results
        
    Returns:
        Dict with comprehensive context for agent to generate investment thesis
    """
    profile = fundamental_data.get('profile', {})
    
    # Extract scores and recommendation for contradiction detection
    fundamental_score = combined_data.get('fundamental_score', 0)
    technical_score = combined_data.get('technical_score', 0)
    sentiment_score = combined_data.get('sentiment_score', 0)
    recommendation = combined_data.get('recommendation', 'Hold')
    
    # Extract trajectory data
    trajectory_data = fundamental_data.get('trajectory', {})
    
    # Extract technical data for contradiction detection
    technical_data_dict = technical_data.get('data', {}) if technical_data else {}
    indicators = technical_data_dict.get('indicators', {})
    rsi = indicators.get('rsi', None)
    trend_analysis = technical_data_dict.get('trend_analysis', {})
    trend = trend_analysis.get('trend', 'N/A')
    price_vs_sma200 = trend_analysis.get('price_vs_sma200', 'N/A')
    
    # ALGORITHMIC: Detect contradictions
    contradictions = {}
    
    # Contradiction 1: RSI oversold but SELL recommendation
    rsi_oversold = rsi is not None and rsi < 30
    recommendation_sell = recommendation == 'Sell'
    fundamentals_weak = fundamental_score < 5.0
    
    if rsi_oversold and recommendation_sell and fundamentals_weak:
        contradictions['oversold_but_sell'] = {
            'type': 'value_trap',
            'rsi': rsi,
            'fundamental_score': fundamental_score,
            'description': 'Extremely oversold RSI but SELL recommendation due to weak fundamentals'
        }
    
    # Contradiction 2: Bullish sentiment but weak fundamentals
    sentiment_bullish = sentiment_score > 0.1
    if sentiment_bullish and fundamentals_weak:
        contradictions['bullish_sentiment_weak_fundamentals'] = {
            'type': 'sentiment_fundamental_divergence',
            'sentiment_score': sentiment_score,
            'fundamental_score': fundamental_score,
            'description': 'Bullish sentiment despite weak fundamentals'
        }
    
    # Contradiction 3: Technical entry signal but weak fundamentals
    trend_positive = trend == 'Uptrend' and price_vs_sma200 == 'Above'
    technical_suggests_entry = rsi_oversold or (trend_positive and technical_score >= 6.0)
    
    if trend_positive and fundamentals_weak and technical_suggests_entry:
        contradictions['technical_entry_but_weak_fundamentals'] = {
            'type': 'technical_fundamental_divergence',
            'trend': trend,
            'fundamental_score': fundamental_score,
            'technical_score': technical_score,
            'description': 'Technical indicators suggest entry but fundamentals are weak'
        }
    
    return {
        'symbol': symbol,
        'company_name': profile.get('companyName', ''),
        'sector': profile.get('sector', 'Technology'),
        'industry': profile.get('industry', ''),
        'fundamental_score': fundamental_score,
        'technical_score': technical_score,
        'sentiment_score': sentiment_score,
        'alignment': combined_data.get('alignment', ''),
        'valuation_risk': combined_data.get('valuation_risk', 1.0),
        'recommendation': recommendation,
        'rsi': rsi,
        'trend': trend,
        'trajectory': trajectory_data,  # NEW: Add trajectory data
        'contradictions': contradictions  # For AI to interpret contextually
    }

