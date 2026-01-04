#!/usr/bin/env python3
"""
Narrative Context Preparer
Prepares comprehensive context for AI narrative generation
Similar to agent_context_preparer.py but for narrative stories
"""

from typing import Dict, Optional


def prepare_narrative_context(
    symbol: str,
    fundamental_data: Dict,
    technical_data: Dict,
    sentiment_data: Dict,
    combined_data: Dict,
    sec_guidance: Optional[Dict] = None,
    trajectory_data: Optional[Dict] = None
) -> Dict:
    """
    Prepare comprehensive context for narrative generation
    
    Returns:
        Dict with all context needed for compelling narrative generation
    """
    
    profile = fundamental_data.get('profile', {})
    quote = fundamental_data.get('quote', {})
    ratios = fundamental_data.get('ratios', [{}])[0]
    growth = fundamental_data.get('growth', [{}])[0]
    income = fundamental_data.get('income', [{}])[0]
    
    # Company context
    company_name = profile.get('companyName', symbol)
    sector = profile.get('sector', '')
    industry = profile.get('industry', '')
    description = profile.get('description', '')
    
    # Market context
    current_price = quote.get('price', 0)
    market_cap = quote.get('marketCap', 0)
    pe_ratio = quote.get('pe', 0)
    eps = quote.get('eps', 0)
    year_high = quote.get('yearHigh', 0)
    year_low = quote.get('yearLow', 0)
    
    # Fundamental metrics
    roe = ratios.get('returnOnEquity', 0)
    roa = ratios.get('returnOnAssets', 0)
    debt_to_equity = ratios.get('debtEquityRatio', 0)
    current_ratio = ratios.get('currentRatio', 0)
    
    # Growth metrics
    revenue_growth = growth.get('revenueGrowth', 0)
    net_income_growth = growth.get('netIncomeGrowth', 0)
    eps_growth = growth.get('epsGrowth', 0)
    
    # Financials
    revenue = income.get('revenue', 0)
    net_income = income.get('netIncome', 0)
    operating_income = income.get('operatingIncome', 0)
    
    # Technical context
    trend = technical_data.get('trend', {})
    indicators = technical_data.get('indicators', {})
    signals = technical_data.get('signals', {})
    
    trend_direction = trend.get('direction', 'Neutral')
    trend_strength = trend.get('strength', 'Moderate')
    rsi = indicators.get('rsi', {}).get('value', 50)
    macd_signal = signals.get('macd', 'Neutral')
    
    # Sentiment context
    sentiment_score = combined_data.get('sentiment_score', 0)
    sentiment_classification = combined_data.get('sentiment_classification', 'Neutral')
    analyst_sentiment = sentiment_data.get('analyst_sentiment', {})
    news_sentiment = sentiment_data.get('news_sentiment', {})
    
    # Combined analysis
    fundamental_score = combined_data.get('fundamental_score', 0)
    technical_score = combined_data.get('technical_score', 0)
    recommendation = combined_data.get('recommendation', 'Hold')
    confidence = combined_data.get('confidence', 'Medium')
    investment_thesis = combined_data.get('investment_thesis', '')
    
    # Trajectory context
    trajectory_momentum = trajectory_data.get('momentum', 'stable') if trajectory_data else 'stable'
    revenue_trend = trajectory_data.get('revenue_trend', 'stable') if trajectory_data else 'stable'
    profitability_trend = trajectory_data.get('profitability_trend', 'stable') if trajectory_data else 'stable'
    
    # SEC guidance context
    sec_strategic_initiatives = []
    sec_market_outlook = []
    sec_management_tone = 'neutral'
    sec_confidence_level = 'medium'
    profitability_timeline = None
    
    if sec_guidance and sec_guidance.get('available'):
        guidance = sec_guidance.get('guidance', {})
        sec_strategic_initiatives = guidance.get('strategic_initiatives', [])
        sec_market_outlook = guidance.get('market_outlook', [])
        sec_management_tone = guidance.get('management_tone', 'neutral')
        sec_confidence_level = guidance.get('confidence_level', 'medium')
        profitability_timeline = guidance.get('profitability_timeline')
    
    # Determine narrative framework
    framework = _determine_narrative_framework(
        fundamental_score,
        technical_score,
        trajectory_momentum,
        revenue_growth,
        roe
    )
    
    return {
        # Company
        'symbol': symbol,
        'company_name': company_name,
        'sector': sector,
        'industry': industry,
        'description': description,
        
        # Market
        'current_price': current_price,
        'market_cap': market_cap,
        'pe_ratio': pe_ratio,
        'eps': eps,
        'year_high': year_high,
        'year_low': year_low,
        'price_appreciation_from_low': ((current_price - year_low) / year_low * 100) if year_low > 0 else 0,
        
        # Fundamentals
        'roe': roe,
        'roa': roa,
        'debt_to_equity': debt_to_equity,
        'current_ratio': current_ratio,
        'revenue': revenue,
        'net_income': net_income,
        'operating_income': operating_income,
        
        # Growth
        'revenue_growth': revenue_growth,
        'net_income_growth': net_income_growth,
        'eps_growth': eps_growth,
        
        # Technicals
        'trend_direction': trend_direction,
        'trend_strength': trend_strength,
        'rsi': rsi,
        'macd_signal': macd_signal,
        
        # Sentiment
        'sentiment_score': sentiment_score,
        'sentiment_classification': sentiment_classification,
        'analyst_sentiment': analyst_sentiment,
        'news_sentiment': news_sentiment,
        
        # Combined
        'fundamental_score': fundamental_score,
        'technical_score': technical_score,
        'recommendation': recommendation,
        'confidence': confidence,
        'investment_thesis': investment_thesis,
        
        # Trajectory
        'trajectory_momentum': trajectory_momentum,
        'revenue_trend': revenue_trend,
        'profitability_trend': profitability_trend,
        
        # SEC Guidance
        'sec_strategic_initiatives': sec_strategic_initiatives,
        'sec_market_outlook': sec_market_outlook,
        'sec_management_tone': sec_management_tone,
        'sec_confidence_level': sec_confidence_level,
        'profitability_timeline': profitability_timeline,
        
        # Framework
        'framework': framework,
    }


def _determine_narrative_framework(
    fundamental_score: float,
    technical_score: float,
    trajectory_momentum: str,
    revenue_growth: float,
    roe: float
) -> str:
    """Determine narrative framework"""
    
    # Turnaround: Weak fundamentals but improving trajectory
    if fundamental_score < 6 and trajectory_momentum == 'improving':
        return 'turnaround'
    
    # Growth: Strong fundamentals and growth
    if fundamental_score >= 7 and revenue_growth > 0.15:
        return 'growth'
    
    # Value: Strong fundamentals, reasonable metrics
    if fundamental_score >= 7 and roe > 0.1:
        return 'value'
    
    # Momentum: Strong technicals
    if technical_score >= 7:
        return 'momentum'
    
    # Cautious: Mixed signals
    return 'cautious'



