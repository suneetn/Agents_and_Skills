#!/usr/bin/env python3
"""
AI LLM Generator Module
Provides actual AI/LLM-powered interpretation using Claude API
"""

import os
from typing import Dict, List, Optional
import json

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    print("⚠️  Anthropic SDK not installed. Install with: pip install anthropic")


class AIGenerator:
    """AI-powered text generation using Claude API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize AI generator with API key"""
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key and ANTHROPIC_AVAILABLE:
            # Try to get from common locations
            try:
                from dotenv import load_dotenv
                load_dotenv()
                self.api_key = os.getenv('ANTHROPIC_API_KEY')
            except ImportError:
                pass
        
        if ANTHROPIC_AVAILABLE and self.api_key:
            self.client = anthropic.Anthropic(api_key=self.api_key)
            self.enabled = True
        else:
            self.client = None
            self.enabled = False
            if not ANTHROPIC_AVAILABLE:
                print("⚠️  Anthropic SDK not available. Using fallback rule-based logic.")
            elif not self.api_key:
                print("⚠️  ANTHROPIC_API_KEY not found. Using fallback rule-based logic.")
    
    def generate_interpretation(self, prompt: str, context: Dict, max_tokens: int = 200) -> str:
        """
        Generate interpretation using Claude API
        
        Args:
            prompt: The interpretation prompt/question
            context: Contextual data (metrics, scores, etc.)
            max_tokens: Maximum tokens for response
            
        Returns:
            Generated interpretation text
        """
        if not self.enabled:
            # Fallback to rule-based logic
            from ai_interpreters import call_ai_for_interpretation
            return call_ai_for_interpretation(prompt, context)
        
        try:
            # Build context string from context dict
            context_str = self._build_context_string(context)
            
            # Create system prompt
            system_prompt = """You are a financial analyst providing clear, concise, and actionable interpretations of stock metrics. 
Your interpretations should be:
- Professional and accurate
- Contextual (consider the full picture, not just isolated metrics)
- Actionable (help investors understand what the data means)
- Concise (avoid unnecessary verbosity)
- Avoid repetition

Format your response as a single, well-structured paragraph or bullet points if appropriate."""
            
            # Create user message
            user_message = f"""Context:
{context_str}

Question/Prompt: {prompt}

Provide a clear, contextual interpretation that helps investors understand what this metric means in the context of the company's overall financial health and investment potential."""
            
            # Call Claude API
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=max_tokens,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )
            
            # Extract response text
            response_text = message.content[0].text if message.content else ""
            return response_text.strip()
            
        except Exception as e:
            print(f"⚠️  AI generation error: {e}. Falling back to rule-based logic.")
            # Fallback to rule-based logic
            from ai_interpreters import call_ai_for_interpretation
            return call_ai_for_interpretation(prompt, context)
    
    def generate_valuation_interpretation(self, valuation_data: Dict, pe_ratio: float, sector: str,
                                          fundamental_score: Optional[float] = None,
                                          roe: Optional[float] = None,
                                          growth_rate: Optional[float] = None) -> str:
        """
        Generate comprehensive valuation interpretation using AI
        
        Args:
            valuation_data: Valuation analysis data (PEG, sector comparison, etc.)
            pe_ratio: Current P/E ratio
            sector: Sector name
            fundamental_score: Overall fundamental score
            roe: Return on equity
            growth_rate: Revenue growth rate
            
        Returns:
            Comprehensive valuation interpretation
        """
        if not self.enabled:
            # Fallback to rule-based logic
            from ai_interpreters import interpret_valuation
            return interpret_valuation(valuation_data, pe_ratio, sector, fundamental_score, roe, growth_rate)
        
        try:
            # Build context
            peg_value = valuation_data.get('peg_ratio', {}).get('value') if valuation_data else None
            sector_comparison = valuation_data.get('sector_comparison', {}) if valuation_data else {}
            valuation_score = valuation_data.get('valuation_score', {}) if valuation_data else {}
            premium = sector_comparison.get('pe_ratio', {}).get('premium_discount') if sector_comparison.get('pe_ratio') else None
            
            context = {
                'pe_ratio': pe_ratio,
                'peg_ratio': peg_value,
                'sector': sector,
                'fundamental_score': fundamental_score,
                'roe': roe,
                'growth_rate': growth_rate,
                'premium_discount': premium,
                'valuation_score': valuation_score.get('score') if valuation_score else None
            }
            
            system_prompt = """You are a financial analyst providing valuation analysis. Your interpretation should:
1. Clearly explain what PEG ratio means and whether it suggests over/under/fair valuation
2. Explain sector premium/discount and whether it's justified
3. Reconcile any contradictions (e.g., PEG suggests undervalued but P/E is expensive)
4. Consider fundamental strength in your assessment
5. Be concise but comprehensive
6. Use clear, structured paragraphs (not one massive wall of text)

Format as 2-4 short paragraphs with clear breaks between concepts."""
            
            # Build user message with proper formatting (avoid nested f-strings)
            premium_str = f"{premium:.1f}% premium" if premium else "N/A"
            valuation_score_val = context['valuation_score']
            valuation_score_str = f"{valuation_score_val}/10" if valuation_score_val is not None else "N/A"
            fundamental_score_str = f"{fundamental_score:.1f}/10" if fundamental_score else "N/A"
            roe_str = f"{roe*100:.1f}%" if roe else "N/A"
            growth_rate_str = f"{growth_rate*100:.1f}% YoY" if growth_rate else "N/A"
            peg_str = f"{peg_value:.2f}" if peg_value else "N/A"
            
            user_message = f"""Analyze the valuation for this stock:

- P/E Ratio: {pe_ratio:.2f}
- PEG Ratio: {peg_str}
- Sector: {sector}
- Premium/Discount to Sector: {premium_str}
- Valuation Score: {valuation_score_str}
- Fundamental Score: {fundamental_score_str}
- ROE: {roe_str}
- Growth Rate: {growth_rate_str}

Provide a clear, structured valuation interpretation that reconciles all these factors and helps investors understand whether the stock is fairly valued, overvalued, or undervalued."""
            
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=400,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )
            
            response_text = message.content[0].text if message.content else ""
            return response_text.strip()
            
        except Exception as e:
            print(f"⚠️  AI valuation interpretation error: {e}. Falling back to rule-based logic.")
            from ai_interpreters import interpret_valuation
            return interpret_valuation(valuation_data, pe_ratio, sector, fundamental_score, roe, growth_rate)
    
    def generate_technical_interpretation(self, technical_data_dict: Dict, fundamental_score: Optional[float] = None) -> str:
        """
        Generate technical analysis interpretation using AI
        
        Args:
            technical_data_dict: Technical analysis data
            fundamental_score: Fundamental score for context
            
        Returns:
            Technical interpretation
        """
        if not self.enabled:
            from ai_interpreters import interpret_technical_analysis
            return interpret_technical_analysis(technical_data_dict, fundamental_score)
        
        try:
            trend_analysis = technical_data_dict.get('trend_analysis', {})
            indicators = technical_data_dict.get('indicators', {})
            trading_signals = technical_data_dict.get('trading_signals', {})
            
            system_prompt = """You are a technical analyst providing clear, actionable technical analysis. Your interpretation should:
1. Assess trend direction and strength
2. Interpret momentum indicators (RSI, MACD)
3. Provide entry timing guidance
4. Consider fundamental context when relevant
5. Use clear, structured format (not one dense paragraph)

Format as 2-3 short paragraphs with clear breaks."""
            
            user_message = f"""Analyze the technical indicators:

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

Fundamental Context: {f"{fundamental_score:.1f}/10" if fundamental_score else "N/A"}

Provide a clear technical interpretation that helps investors understand entry timing and technical setup."""
            
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=300,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )
            
            response_text = message.content[0].text if message.content else ""
            return response_text.strip()
            
        except Exception as e:
            print(f"⚠️  AI technical interpretation error: {e}. Falling back to rule-based logic.")
            from ai_interpreters import interpret_technical_analysis
            return interpret_technical_analysis(technical_data_dict, fundamental_score)
    
    def generate_investment_thesis(self, fundamental_data: Dict, technical_data: Dict, combined_data: Dict) -> str:
        """
        Generate investment thesis using AI
        
        Args:
            fundamental_data: Fundamental analysis data
            technical_data: Technical analysis data
            combined_data: Combined analysis results
            
        Returns:
            Investment thesis
        """
        if not self.enabled:
            from ai_interpreters import synthesize_investment_thesis
            return synthesize_investment_thesis(fundamental_data, technical_data, combined_data)
        
        try:
            fundamental_score = combined_data.get('fundamental_score', 0)
            technical_score = combined_data.get('technical_score', 0)
            sentiment_score = combined_data.get('sentiment_score', 0)
            alignment = combined_data.get('alignment', '')
            valuation_risk = combined_data.get('valuation_risk', 1.0)
            
            system_prompt = """You are a senior investment analyst synthesizing a comprehensive investment thesis. Your thesis should:
1. Synthesize fundamental, technical, and sentiment analysis
2. Explain alignment or divergence between dimensions
3. Address valuation concerns
4. Provide clear investment rationale
5. Be concise but comprehensive (2-3 paragraphs)

Avoid repetition and create a cohesive narrative."""
            
            user_message = f"""Synthesize an investment thesis based on:

Fundamental Score: {fundamental_score:.1f}/10
Technical Score: {technical_score:.1f}/10
Sentiment Score: {sentiment_score:.3f}
Analysis Alignment: {alignment}
Valuation Risk: {valuation_risk:.2f}x sector average

Create a cohesive investment thesis that synthesizes these factors into a clear narrative about the investment opportunity."""
            
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=400,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )
            
            response_text = message.content[0].text if message.content else ""
            return response_text.strip()
            
        except Exception as e:
            print(f"⚠️  AI investment thesis error: {e}. Falling back to rule-based logic.")
            from ai_interpreters import synthesize_investment_thesis
            return synthesize_investment_thesis(fundamental_data, technical_data, combined_data)
    
    def _build_context_string(self, context: Dict) -> str:
        """Build context string from context dictionary"""
        parts = []
        for key, value in context.items():
            if value is not None:
                if isinstance(value, float):
                    parts.append(f"{key}: {value:.2f}")
                elif isinstance(value, (int, str)):
                    parts.append(f"{key}: {value}")
                elif isinstance(value, dict):
                    parts.append(f"{key}: {json.dumps(value, indent=2)}")
        return "\n".join(parts)


# Global instance
_ai_generator = None

def get_ai_generator() -> AIGenerator:
    """Get or create global AI generator instance"""
    global _ai_generator
    if _ai_generator is None:
        _ai_generator = AIGenerator()
    return _ai_generator

