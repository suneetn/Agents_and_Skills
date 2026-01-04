#!/usr/bin/env python3
"""
AI Direct Generator Module
Uses the executing agent (Claude in Cursor) as the LLM for interpretations
Instead of API calls, generates prompts that the agent can fulfill directly
"""

import os
from typing import Dict, Optional
import json


def is_cursor_environment() -> bool:
    """Check if running in Cursor/Claude environment"""
    # Check for Cursor-specific environment variables
    cursor_vars = ['CURSOR', 'CURSOR_AGENT', 'CLAUDE_IN_CURSOR']
    if any(os.getenv(var) for var in cursor_vars):
        return True
    
    # Check if we're being called from Cursor workflow
    # In Cursor, the agent can generate directly
    return False


class DirectAIGenerator:
    """
    Direct AI Generator - Uses the executing agent (Claude) for interpretations
    Instead of API calls, this generates structured prompts that the agent processes
    """
    
    def __init__(self):
        """Initialize direct AI generator"""
        self.enabled = True  # Always enabled when agent is executing
        self.use_agent = True  # Use agent directly
    
    def generate_valuation_interpretation(self, valuation_data: Dict, pe_ratio: float, sector: str,
                                          fundamental_score: Optional[float] = None,
                                          roe: Optional[float] = None,
                                          growth_rate: Optional[float] = None) -> str:
        """
        Generate valuation interpretation using the executing agent
        
        This function is designed to be called by the agent (Claude) directly,
        so the agent can generate the interpretation in real-time.
        """
        # Build context for agent
        peg_value = valuation_data.get('peg_ratio', {}).get('value') if valuation_data else None
        sector_comparison = valuation_data.get('sector_comparison', {}) if valuation_data else {}
        valuation_score = valuation_data.get('valuation_score', {}) if valuation_data else {}
        premium = sector_comparison.get('pe_ratio', {}).get('premium_discount') if sector_comparison.get('pe_ratio') else None
        
        # Format values for agent
        peg_str = f"{peg_value:.2f}" if peg_value else "N/A"
        premium_str = f"{premium:.1f}% premium" if premium else "N/A"
        valuation_score_val = valuation_score.get('score') if valuation_score else None
        valuation_score_str = f"{valuation_score_val}/10" if valuation_score_val is not None else "N/A"
        fundamental_score_str = f"{fundamental_score:.1f}/10" if fundamental_score else "N/A"
        roe_str = f"{roe*100:.1f}%" if roe else "N/A"
        growth_rate_str = f"{growth_rate*100:.1f}% YoY" if growth_rate else "N/A"
        
        # Generate interpretation prompt for agent
        # The agent (Claude) will process this and generate the interpretation
        interpretation_prompt = f"""As a financial analyst, provide a clear, structured valuation interpretation for this stock:

Valuation Metrics:
- P/E Ratio: {pe_ratio:.2f}
- PEG Ratio: {peg_str}
- Sector: {sector}
- Premium/Discount to Sector: {premium_str}
- Valuation Score: {valuation_score_str}
- Fundamental Score: {fundamental_score_str}
- ROE: {roe_str}
- Growth Rate: {growth_rate_str}

Requirements:
1. Clearly explain what PEG ratio means and whether it suggests over/under/fair valuation
2. Explain sector premium/discount and whether it's justified
3. Reconcile any contradictions (e.g., PEG suggests undervalued but P/E is expensive)
4. Consider fundamental strength in your assessment
5. Be concise but comprehensive
6. Use clear, structured paragraphs (2-4 short paragraphs with breaks between concepts, NOT one massive wall of text)

Generate the interpretation now:"""
        
        # Return prompt - agent will generate interpretation
        # In practice, this would be processed by the agent directly
        return interpretation_prompt
    
    def generate_technical_interpretation(self, technical_data_dict: Dict, fundamental_score: Optional[float] = None) -> str:
        """Generate technical interpretation using the executing agent"""
        trend_analysis = technical_data_dict.get('trend_analysis', {})
        indicators = technical_data_dict.get('indicators', {})
        trading_signals = technical_data_dict.get('trading_signals', {})
        
        fundamental_score_str = f"{fundamental_score:.1f}/10" if fundamental_score else "N/A"
        
        interpretation_prompt = f"""As a technical analyst, provide a clear, actionable technical analysis interpretation:

Technical Data:
Trend:
- Primary Trend: {trend_analysis.get('trend', 'N/A')}
- Trend Strength: {trend_analysis.get('strength', 'N/A')}
- Price vs SMA 50: {trend_analysis.get('price_vs_sma50', 'N/A')}
- Price vs SMA 200: {trend_analysis.get('price_vs_sma200', 'N/A')}

Momentum:
- RSI (14): {indicators.get('rsi', 'N/A')}
- MACD Signal: {trading_signals.get('macd_signal', 'N/A')}

Trading Signals:
- Overall Signal: {trading_signals.get('overall_signal', 'N/A')}

Fundamental Context: {fundamental_score_str}

Requirements:
1. Assess trend direction and strength
2. Interpret momentum indicators (RSI, MACD)
3. Provide entry timing guidance
4. Consider fundamental context when relevant
5. Use clear, structured format (2-3 short paragraphs with breaks, NOT one dense paragraph)

Generate the interpretation now:"""
        
        return interpretation_prompt
    
    def generate_investment_thesis(self, fundamental_data: Dict, technical_data: Dict, combined_data: Dict) -> str:
        """Generate investment thesis using the executing agent"""
        fundamental_score = combined_data.get('fundamental_score', 0)
        technical_score = combined_data.get('technical_score', 0)
        sentiment_score = combined_data.get('sentiment_score', 0)
        alignment = combined_data.get('alignment', '')
        valuation_risk = combined_data.get('valuation_risk', 1.0)
        
        interpretation_prompt = f"""As a senior investment analyst, synthesize a comprehensive investment thesis:

Analysis Summary:
- Fundamental Score: {fundamental_score:.1f}/10
- Technical Score: {technical_score:.1f}/10
- Sentiment Score: {sentiment_score:.3f}
- Analysis Alignment: {alignment}
- Valuation Risk: {valuation_risk:.2f}x sector average

Requirements:
1. Synthesize fundamental, technical, and sentiment analysis
2. Explain alignment or divergence between dimensions
3. Address valuation concerns
4. Provide clear investment rationale
5. Be concise but comprehensive (2-3 paragraphs)
6. Avoid repetition and create a cohesive narrative

Generate the investment thesis now:"""
        
        return interpretation_prompt


# For agent-based generation, we need a different approach
# The agent can call these functions and generate interpretations directly
def generate_interpretation_via_agent(prompt: str, context: Dict) -> str:
    """
    This function is called by the agent to generate interpretations directly
    The agent (Claude) processes the prompt and returns the interpretation
    """
    # This is a placeholder - the actual generation happens when the agent
    # processes this during workflow execution
    return f"[AGENT_GENERATED: {prompt}]"


# Global instance
_direct_ai_generator = None

def get_direct_ai_generator() -> DirectAIGenerator:
    """Get or create global direct AI generator instance"""
    global _direct_ai_generator
    if _direct_ai_generator is None:
        _direct_ai_generator = DirectAIGenerator()
    return _direct_ai_generator



