#!/usr/bin/env python3
"""
Technical Scoring Algorithm
Calculates technical strength score (0-10) based on technical indicators
"""

from typing import Dict, Optional


class TechnicalScorer:
    """
    Calculates technical strength score from technical analysis data
    Score components:
    - Trend (30%): Trend direction and strength
    - Momentum (30%): RSI, MACD signals
    - Price Action (25%): Price performance vs moving averages, price changes
    - Volatility/Support (15%): Bollinger bands position, support/resistance proximity
    """
    
    def __init__(self):
        self.weights = {
            'trend': 0.30,
            'momentum': 0.30,
            'price_action': 0.25,
            'volatility': 0.15
        }
    
    def calculate_trend_score(self, trend_analysis: Dict) -> float:
        """
        Calculate trend score (0-10) based on trend direction and strength
        
        Args:
            trend_analysis: Dict with 'trend', 'strength', 'price_vs_sma50', etc.
        
        Returns:
            Score from 0-10
        """
        if not trend_analysis:
            return 5.0  # Neutral if no data
        
        trend = trend_analysis.get('trend', 'Sideways')
        strength = trend_analysis.get('strength', 'Neutral')
        price_vs_sma50 = trend_analysis.get('price_vs_sma50', 'Below')
        price_vs_sma200 = trend_analysis.get('price_vs_sma200', 'Below')
        sma50_vs_sma200 = trend_analysis.get('sma50_vs_sma200', 'Below')
        
        score = 5.0  # Start neutral
        
        # Trend direction (0-5 points)
        if trend == 'Uptrend':
            score += 2.5
        elif trend == 'Downtrend':
            score -= 2.5
        
        # Trend strength (0-2.5 points)
        if strength == 'Strong':
            if trend == 'Uptrend':
                score += 2.5
            elif trend == 'Downtrend':
                score -= 2.5
        elif strength == 'Weak':
            if trend == 'Uptrend':
                score += 1.0
            elif trend == 'Downtrend':
                score -= 1.0
        
        # Moving average alignment (0-2.5 points)
        # Bullish: Price > SMA50 > SMA200
        if price_vs_sma50 == 'Above' and price_vs_sma200 == 'Above' and sma50_vs_sma200 == 'Above':
            score += 2.5
        # Bearish: Price < SMA50 < SMA200
        elif price_vs_sma50 == 'Below' and price_vs_sma200 == 'Below' and sma50_vs_sma200 == 'Below':
            score -= 2.5
        # Mixed signals
        elif price_vs_sma50 == 'Above' and price_vs_sma200 == 'Above':
            score += 1.0
        elif price_vs_sma50 == 'Below' and price_vs_sma200 == 'Below':
            score -= 1.0
        
        return max(0.0, min(10.0, score))
    
    def calculate_momentum_score(self, rsi: Optional[float], macd_signal: str, rsi_signal: str) -> float:
        """
        Calculate momentum score (0-10) based on RSI and MACD
        
        Args:
            rsi: Current RSI value (0-100)
            macd_signal: MACD signal ('Bullish', 'Bearish', 'Neutral')
            rsi_signal: RSI signal string
        
        Returns:
            Score from 0-10
        """
        score = 5.0  # Start neutral
        
        # RSI scoring (0-5 points)
        if rsi is not None:
            if rsi < 30:
                score += 2.5  # Oversold - bullish potential
            elif rsi > 70:
                score -= 2.5  # Overbought - bearish potential
            elif 40 <= rsi <= 60:
                score += 1.0  # Healthy neutral zone
            elif 30 <= rsi < 40:
                score += 1.5  # Slightly oversold
            elif 60 < rsi <= 70:
                score -= 1.5  # Slightly overbought
        
        # MACD signal (0-3 points)
        if 'Bullish' in macd_signal or 'Buy' in macd_signal:
            score += 3.0
        elif 'Bearish' in macd_signal or 'Sell' in macd_signal:
            score -= 3.0
        
        # RSI signal confirmation (0-2 points)
        if 'Buy' in rsi_signal or 'Oversold' in rsi_signal:
            score += 2.0
        elif 'Sell' in rsi_signal or 'Overbought' in rsi_signal:
            score -= 2.0
        
        return max(0.0, min(10.0, score))
    
    def calculate_price_action_score(
        self, 
        price_changes: Dict,
        price_vs_sma20: Optional[str],
        price_vs_sma50: Optional[str]
    ) -> float:
        """
        Calculate price action score (0-10) based on price performance
        
        Args:
            price_changes: Dict with '1D', '1W', '1M', '1Y' changes
            price_vs_sma20: 'Above' or 'Below'
            price_vs_sma50: 'Above' or 'Below'
        
        Returns:
            Score from 0-10
        """
        score = 5.0  # Start neutral
        
        # Price changes (0-5 points)
        # Weight: 1Y (40%), 1M (30%), 1W (20%), 1D (10%)
        change_1y = price_changes.get('1Y', 0)
        change_1m = price_changes.get('1M', 0)
        change_1w = price_changes.get('1W', 0)
        change_1d = price_changes.get('1D', 0)
        
        # 1Y change (0-2 points)
        if change_1y > 0.20:  # >20%
            score += 2.0
        elif change_1y > 0.10:  # 10-20%
            score += 1.0
        elif change_1y < -0.20:  # <-20%
            score -= 2.0
        elif change_1y < -0.10:  # -10% to -20%
            score -= 1.0
        
        # 1M change (0-1.5 points)
        if change_1m > 0.10:  # >10%
            score += 1.5
        elif change_1m > 0.05:  # 5-10%
            score += 0.75
        elif change_1m < -0.10:  # <-10%
            score -= 1.5
        elif change_1m < -0.05:  # -5% to -10%
            score -= 0.75
        
        # 1W change (0-1 point)
        if change_1w > 0.05:  # >5%
            score += 1.0
        elif change_1w < -0.05:  # <-5%
            score -= 1.0
        
        # 1D change (0-0.5 points) - less weight
        if change_1d > 0.02:  # >2%
            score += 0.5
        elif change_1d < -0.02:  # <-2%
            score -= 0.5
        
        # Moving average position (0-2 points)
        if price_vs_sma20 == 'Above' and price_vs_sma50 == 'Above':
            score += 2.0
        elif price_vs_sma20 == 'Below' and price_vs_sma50 == 'Below':
            score -= 2.0
        elif price_vs_sma20 == 'Above':
            score += 1.0
        elif price_vs_sma20 == 'Below':
            score -= 1.0
        
        return max(0.0, min(10.0, score))
    
    def calculate_volatility_score(
        self,
        price_position: Optional[str],
        atr: Optional[float],
        current_price: Optional[float]
    ) -> float:
        """
        Calculate volatility/support score (0-10)
        
        Args:
            price_position: Position relative to Bollinger Bands ('Near Upper', 'Near Lower', 'Middle')
            atr: Average True Range value
            current_price: Current stock price
        
        Returns:
            Score from 0-10
        """
        score = 5.0  # Start neutral
        
        # Bollinger Bands position (0-3 points)
        if price_position == 'Near Upper':
            score -= 1.5  # Potentially overbought
        elif price_position == 'Near Lower':
            score += 1.5  # Potentially oversold
        elif price_position == 'Middle':
            score += 0.5  # Healthy middle range
        
        # ATR-based volatility assessment (0-2 points)
        # Lower ATR relative to price = less volatility = better (for stability)
        if atr is not None and current_price is not None and current_price > 0:
            atr_pct = (atr / current_price) * 100
            if atr_pct < 2.0:  # Low volatility (<2% of price)
                score += 1.0
            elif atr_pct > 5.0:  # High volatility (>5% of price)
                score -= 1.0
        
        return max(0.0, min(10.0, score))
    
    def calculate_technical_score(
        self,
        trend_analysis: Dict,
        trading_signals: Dict,
        price_changes: Dict,
        indicators: Dict,
        current_price: Optional[float] = None
    ) -> Dict:
        """
        Calculate overall technical score from all components
        
        Args:
            trend_analysis: Trend analysis dict
            trading_signals: Trading signals dict with RSI, MACD signals
            price_changes: Price change percentages
            indicators: Dict with RSI value, Bollinger bands position, ATR
            current_price: Current stock price (for ATR calculation)
        
        Returns:
            Dict with component scores and overall score
        """
        # Extract values
        rsi = indicators.get('rsi')
        macd_signal = trading_signals.get('macd_signal', 'Neutral')
        rsi_signal = trading_signals.get('rsi_signal', 'Neutral')
        price_position = indicators.get('price_position')
        atr = indicators.get('atr')
        price_vs_sma20 = indicators.get('price_vs_sma20')
        price_vs_sma50 = trend_analysis.get('price_vs_sma50')
        
        # Calculate component scores
        trend_score = self.calculate_trend_score(trend_analysis)
        momentum_score = self.calculate_momentum_score(rsi, macd_signal, rsi_signal)
        price_action_score = self.calculate_price_action_score(
            price_changes, price_vs_sma20, price_vs_sma50
        )
        volatility_score = self.calculate_volatility_score(
            price_position, atr, current_price
        )
        
        # Weighted average
        overall_score = (
            trend_score * self.weights['trend'] +
            momentum_score * self.weights['momentum'] +
            price_action_score * self.weights['price_action'] +
            volatility_score * self.weights['volatility']
        )
        
        return {
            'overall_score': round(overall_score, 1),
            'trend_score': round(trend_score, 1),
            'momentum_score': round(momentum_score, 1),
            'price_action_score': round(price_action_score, 1),
            'volatility_score': round(volatility_score, 1)
        }
    
    def get_technical_strength_label(self, score: float) -> str:
        """Get label for technical score"""
        if score >= 8.0:
            return "Excellent"
        elif score >= 6.0:
            return "Good"
        elif score >= 4.0:
            return "Moderate"
        else:
            return "Poor"


if __name__ == '__main__':
    # Example Usage (requires dummy data or technical analysis data)
    print("TechnicalScorer script - for module import. No direct execution example.")

