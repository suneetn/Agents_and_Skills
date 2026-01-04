#!/usr/bin/env python3
"""
Agent AI Generator
When executed by Claude agent in Cursor, the agent generates interpretations directly
This module provides structured data and prompts for the agent to process
"""

from typing import Dict, Optional


def get_valuation_interpretation_prompt(valuation_data: Dict, pe_ratio: float, sector: str,
                                       fundamental_score: Optional[float] = None,
                                       roe: Optional[float] = None,
                                       growth_rate: Optional[float] = None) -> Dict:
    """
    Get structured prompt for agent to generate valuation interpretation
    
    Returns dict with:
    - 'prompt': The prompt for the agent
    - 'context': Structured context data
    - 'requirements': What the agent should include
    """
    peg_value = valuation_data.get('peg_ratio', {}).get('value') if valuation_data else None
    sector_comparison = valuation_data.get('sector_comparison', {}) if valuation_data else {}
    valuation_score = valuation_data.get('valuation_score', {}) if valuation_data else {}
    premium = sector_comparison.get('pe_ratio', {}).get('premium_discount') if sector_comparison.get('pe_ratio') else None
    
    return {
        'type': 'valuation_interpretation',
        'context': {
            'pe_ratio': pe_ratio,
            'peg_ratio': peg_value,
            'sector': sector,
            'premium_discount': premium,
            'valuation_score': valuation_score.get('score') if valuation_score else None,
            'fundamental_score': fundamental_score,
            'roe': roe,
            'growth_rate': growth_rate
        },
        'requirements': [
            'Clearly explain what PEG ratio means and whether it suggests over/under/fair valuation',
            'Explain sector premium/discount and whether it\'s justified',
            'Reconcile any contradictions (e.g., PEG suggests undervalued but P/E is expensive)',
            'Consider fundamental strength in assessment',
            'Be concise but comprehensive',
            'Use clear, structured paragraphs (2-4 short paragraphs with breaks, NOT one massive wall of text)'
        ]
    }


def get_technical_interpretation_prompt(technical_data_dict: Dict, fundamental_score: Optional[float] = None) -> Dict:
    """Get structured prompt for agent to generate technical interpretation"""
    trend_analysis = technical_data_dict.get('trend_analysis', {})
    indicators = technical_data_dict.get('indicators', {})
    trading_signals = technical_data_dict.get('trading_signals', {})
    
    return {
        'type': 'technical_interpretation',
        'context': {
            'trend': trend_analysis.get('trend', 'N/A'),
            'trend_strength': trend_analysis.get('strength', 'N/A'),
            'price_vs_sma50': trend_analysis.get('price_vs_sma50', 'N/A'),
            'price_vs_sma200': trend_analysis.get('price_vs_sma200', 'N/A'),
            'rsi': indicators.get('rsi', 'N/A'),
            'macd_signal': trading_signals.get('macd_signal', 'N/A'),
            'overall_signal': trading_signals.get('overall_signal', 'N/A'),
            'fundamental_score': fundamental_score
        },
        'requirements': [
            'Assess trend direction and strength',
            'Interpret momentum indicators (RSI, MACD)',
            'Provide entry timing guidance',
            'Consider fundamental context when relevant',
            'Use clear, structured format (2-3 short paragraphs with breaks, NOT one dense paragraph)'
        ]
    }


def get_investment_thesis_prompt(fundamental_data: Dict, technical_data: Dict, combined_data: Dict) -> Dict:
    """Get structured prompt for agent to generate investment thesis"""
    return {
        'type': 'investment_thesis',
        'context': {
            'fundamental_score': combined_data.get('fundamental_score', 0),
            'technical_score': combined_data.get('technical_score', 0),
            'sentiment_score': combined_data.get('sentiment_score', 0),
            'alignment': combined_data.get('alignment', ''),
            'valuation_risk': combined_data.get('valuation_risk', 1.0)
        },
        'requirements': [
            'Synthesize fundamental, technical, and sentiment analysis',
            'Explain alignment or divergence between dimensions',
            'Address valuation concerns',
            'Provide clear investment rationale',
            'Be concise but comprehensive (2-3 paragraphs)',
            'Avoid repetition and create a cohesive narrative'
        ]
    }



