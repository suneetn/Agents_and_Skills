#!/usr/bin/env python3
"""
Stock Technical Analysis Script
Calculates technical indicators and analyzes price patterns
Works with FMP API or can use other data sources
"""

import requests
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

try:
    from dotenv import load_dotenv
    load_dotenv()  # Load .env file if it exists
except ImportError:
    pass  # python-dotenv not installed, fall back to environment variables

class TechnicalAnalyzer:
    """Technical analysis calculator for stock price data"""
    
    def __init__(self):
        """Initialize technical analyzer"""
        pass
    
    def calculate_sma(self, prices: pd.Series, period: int) -> pd.Series:
        """Calculate Simple Moving Average"""
        return prices.rolling(window=period).mean()
    
    def calculate_ema(self, prices: pd.Series, period: int) -> pd.Series:
        """Calculate Exponential Moving Average"""
        return prices.ewm(span=period, adjust=False).mean()
    
    def calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Relative Strength Index"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_macd(self, prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Calculate MACD (Moving Average Convergence Divergence)"""
        ema_fast = self.calculate_ema(prices, fast)
        ema_slow = self.calculate_ema(prices, slow)
        macd_line = ema_fast - ema_slow
        signal_line = self.calculate_ema(macd_line, signal)
        histogram = macd_line - signal_line
        return macd_line, signal_line, histogram
    
    def calculate_bollinger_bands(self, prices: pd.Series, period: int = 20, std_dev: int = 2) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Calculate Bollinger Bands"""
        sma = self.calculate_sma(prices, period)
        std = prices.rolling(window=period).std()
        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)
        return upper_band, sma, lower_band
    
    def calculate_atr(self, high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Average True Range"""
        high_low = high - low
        high_close = np.abs(high - close.shift())
        low_close = np.abs(low - close.shift())
        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = true_range.rolling(window=period).mean()
        return atr
    
    def identify_support_resistance(self, prices: pd.Series, window: int = 20) -> Tuple[List[float], List[float]]:
        """Identify support and resistance levels using local minima/maxima"""
        # Simple method: find local minima (support) and maxima (resistance)
        support_levels = []
        resistance_levels = []
        
        for i in range(window, len(prices) - window):
            local_min = prices.iloc[i-window:i+window].min()
            local_max = prices.iloc[i-window:i+window].max()
            
            if prices.iloc[i] == local_min:
                support_levels.append(prices.iloc[i])
            if prices.iloc[i] == local_max:
                resistance_levels.append(prices.iloc[i])
        
        # Remove duplicates and sort
        support_levels = sorted(set(support_levels), reverse=True)[:5]  # Top 5 support levels
        resistance_levels = sorted(set(resistance_levels))[:5]  # Top 5 resistance levels
        
        return support_levels, resistance_levels
    
    def calculate_pivot_points(self, high: pd.Series, low: pd.Series, close: pd.Series) -> Dict[str, float]:
        """Calculate pivot points for support/resistance levels"""
        # Use most recent period's high, low, close
        h = high.iloc[-1]
        l = low.iloc[-1]
        c = close.iloc[-1]
        
        # Standard pivot point calculation
        pivot = (h + l + c) / 3
        
        # Support and resistance levels
        r1 = 2 * pivot - l
        r2 = pivot + (h - l)
        r3 = h + 2 * (pivot - l)
        
        s1 = 2 * pivot - h
        s2 = pivot - (h - l)
        s3 = l - 2 * (h - pivot)
        
        return {
            'pivot': pivot,
            'resistance_1': r1,
            'resistance_2': r2,
            'resistance_3': r3,
            'support_1': s1,
            'support_2': s2,
            'support_3': s3
        }
    
    def calculate_fibonacci_levels(self, high: pd.Series, low: pd.Series) -> Dict[str, float]:
        """Calculate Fibonacci retracement levels"""
        # Use recent high and low
        recent_high = high.max()
        recent_low = low.min()
        diff = recent_high - recent_low
        
        # Fibonacci retracement levels
        fib_levels = {
            'fib_0': recent_high,
            'fib_23.6': recent_high - (diff * 0.236),
            'fib_38.2': recent_high - (diff * 0.382),
            'fib_50': recent_high - (diff * 0.5),
            'fib_61.8': recent_high - (diff * 0.618),
            'fib_78.6': recent_high - (diff * 0.786),
            'fib_100': recent_low
        }
        
        return fib_levels
    
    def analyze_volume_trends(self, volumes: pd.Series, period: int = 20) -> Dict:
        """Analyze volume trends over time"""
        if len(volumes) < period:
            return {'trend': 'Insufficient Data', 'avg_volume': None, 'current_vs_avg': None}
        
        # Calculate average volume
        avg_volume = volumes.rolling(window=period).mean().iloc[-1]
        current_volume = volumes.iloc[-1]
        
        # Volume trend (increasing/decreasing)
        recent_avg = volumes.iloc[-period:].mean()
        previous_avg = volumes.iloc[-period*2:-period].mean() if len(volumes) >= period*2 else avg_volume
        
        if recent_avg > previous_avg * 1.1:
            trend = 'Increasing'
        elif recent_avg < previous_avg * 0.9:
            trend = 'Decreasing'
        else:
            trend = 'Stable'
        
        # Current vs average
        if avg_volume > 0:
            volume_ratio = current_volume / avg_volume
            if volume_ratio > 1.5:
                volume_status = 'Very High'
            elif volume_ratio > 1.2:
                volume_status = 'High'
            elif volume_ratio > 0.8:
                volume_status = 'Normal'
            elif volume_ratio > 0.5:
                volume_status = 'Low'
            else:
                volume_status = 'Very Low'
        else:
            volume_ratio = None
            volume_status = 'Unknown'
        
        return {
            'trend': trend,
            'avg_volume': float(avg_volume) if not pd.isna(avg_volume) else None,
            'current_volume': float(current_volume),
            'current_vs_avg': volume_ratio,
            'volume_status': volume_status
        }
    
    def detect_volume_divergence(self, prices: pd.Series, volumes: pd.Series, period: int = 20) -> Dict:
        """Detect volume-price divergence"""
        if len(prices) < period * 2:
            return {'divergence': 'Insufficient Data', 'type': None}
        
        # Calculate price and volume trends
        recent_price_change = (prices.iloc[-1] - prices.iloc[-period]) / prices.iloc[-period]
        recent_volume_change = (volumes.iloc[-period:].mean() - volumes.iloc[-period*2:-period].mean()) / volumes.iloc[-period*2:-period].mean() if len(volumes) >= period*2 else 0
        
        # Detect divergence
        divergence_type = None
        if recent_price_change > 0.05 and recent_volume_change < -0.1:  # Price up, volume down
            divergence_type = 'Bearish Divergence'
        elif recent_price_change < -0.05 and recent_volume_change > 0.1:  # Price down, volume up
            divergence_type = 'Bullish Divergence'
        else:
            divergence_type = 'No Divergence'
        
        return {
            'divergence': 'Detected' if divergence_type != 'No Divergence' else 'None',
            'type': divergence_type,
            'price_change': recent_price_change,
            'volume_change': recent_volume_change
        }
    
    def volume_confirmation(self, volumes: pd.Series, signal: str, period: int = 20) -> Dict:
        """Confirm trading signals with volume analysis"""
        if len(volumes) < period:
            return {'confirmed': False, 'reason': 'Insufficient Data'}
        
        avg_volume = volumes.rolling(window=period).mean().iloc[-1]
        current_volume = volumes.iloc[-1]
        volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1.0
        
        # Volume confirmation rules
        confirmed = False
        reason = ''
        
        if signal in ['Buy', 'Strong Buy']:
            # Buy signals should have above-average volume
            if volume_ratio >= 1.2:
                confirmed = True
                reason = f'Volume confirmation: {volume_ratio:.2f}x average volume'
            else:
                confirmed = False
                reason = f'Weak volume: {volume_ratio:.2f}x average (need >1.2x)'
        elif signal in ['Sell', 'Strong Sell']:
            # Sell signals can have any volume, but high volume confirms
            if volume_ratio >= 1.2:
                confirmed = True
                reason = f'High volume confirms sell signal: {volume_ratio:.2f}x average'
            else:
                confirmed = True  # Sell signals don't require high volume
                reason = f'Normal volume: {volume_ratio:.2f}x average'
        else:  # Hold
            confirmed = True
            reason = 'Hold signal - volume analysis not critical'
        
        return {
            'confirmed': confirmed,
            'reason': reason,
            'volume_ratio': volume_ratio
        }
    
    def compare_volume_to_average(self, volumes: pd.Series, period: int = 20) -> Dict:
        """Compare current volume to average"""
        if len(volumes) < period:
            return {'comparison': 'Insufficient Data', 'ratio': None}
        
        avg_volume = volumes.rolling(window=period).mean().iloc[-1]
        current_volume = volumes.iloc[-1]
        
        if avg_volume > 0:
            ratio = current_volume / avg_volume
            if ratio > 2.0:
                status = 'Extremely High'
            elif ratio > 1.5:
                status = 'Very High'
            elif ratio > 1.2:
                status = 'High'
            elif ratio > 0.8:
                status = 'Normal'
            elif ratio > 0.5:
                status = 'Low'
            else:
                status = 'Very Low'
        else:
            ratio = None
            status = 'Unknown'
        
        return {
            'current_volume': float(current_volume),
            'avg_volume': float(avg_volume) if not pd.isna(avg_volume) else None,
            'ratio': ratio,
            'status': status
        }
    
    def analyze_trend(self, prices: pd.Series, sma_50: pd.Series, sma_200: pd.Series) -> Dict:
        """Analyze trend direction and strength"""
        current_price = prices.iloc[-1]
        sma_50_current = sma_50.iloc[-1]
        sma_200_current = sma_200.iloc[-1]
        
        # Determine trend
        if current_price > sma_50_current > sma_200_current:
            trend = "Uptrend"
            strength = "Strong"
        elif current_price > sma_50_current and sma_50_current < sma_200_current:
            trend = "Uptrend"
            strength = "Weak"
        elif current_price < sma_50_current < sma_200_current:
            trend = "Downtrend"
            strength = "Strong"
        elif current_price < sma_50_current and sma_50_current > sma_200_current:
            trend = "Downtrend"
            strength = "Weak"
        else:
            trend = "Sideways"
            strength = "Neutral"
        
        return {
            'trend': trend,
            'strength': strength,
            'price_vs_sma50': 'Above' if current_price > sma_50_current else 'Below',
            'price_vs_sma200': 'Above' if current_price > sma_200_current else 'Below',
            'sma50_vs_sma200': 'Above' if sma_50_current > sma_200_current else 'Below'
        }
    
    def get_trading_signals(self, rsi: pd.Series, macd_line: pd.Series, signal_line: pd.Series, 
                           prices: pd.Series, sma_20: pd.Series) -> Dict:
        """Generate trading signals from indicators"""
        current_rsi = rsi.iloc[-1]
        current_price = prices.iloc[-1]
        current_sma20 = sma_20.iloc[-1]
        
        signals = {
            'rsi_signal': 'Neutral',
            'macd_signal': 'Neutral',
            'trend_signal': 'Neutral',
            'overall_signal': 'Hold'
        }
        
        # RSI signals (improved interpretation)
        if current_rsi > 80:
            signals['rsi_signal'] = 'Sell (Extremely Overbought)'
        elif current_rsi > 70:
            signals['rsi_signal'] = 'Sell (Overbought)'
        elif current_rsi > 65:
            signals['rsi_signal'] = 'Caution (Approaching Overbought)'
        elif current_rsi < 20:
            signals['rsi_signal'] = 'Buy (Extremely Oversold)'
        elif current_rsi < 30:
            signals['rsi_signal'] = 'Buy (Oversold)'
        elif current_rsi < 35:
            signals['rsi_signal'] = 'Caution (Approaching Oversold)'
        else:
            signals['rsi_signal'] = 'Neutral'
        
        # MACD signals
        if macd_line.iloc[-1] > signal_line.iloc[-1] and macd_line.iloc[-2] <= signal_line.iloc[-2]:
            signals['macd_signal'] = 'Buy (Bullish Crossover)'
        elif macd_line.iloc[-1] < signal_line.iloc[-1] and macd_line.iloc[-2] >= signal_line.iloc[-2]:
            signals['macd_signal'] = 'Sell (Bearish Crossover)'
        else:
            signals['macd_signal'] = 'Neutral'
        
        # Trend signal
        if current_price > current_sma20:
            signals['trend_signal'] = 'Buy (Above SMA 20)'
        else:
            signals['trend_signal'] = 'Sell (Below SMA 20)'
        
        # Overall signal (simple majority rule)
        buy_count = sum([1 for s in [signals['rsi_signal'], signals['macd_signal'], signals['trend_signal']] if 'Buy' in s])
        sell_count = sum([1 for s in [signals['rsi_signal'], signals['macd_signal'], signals['trend_signal']] if 'Sell' in s])
        
        if buy_count >= 2:
            signals['overall_signal'] = 'Buy'
        elif sell_count >= 2:
            signals['overall_signal'] = 'Sell'
        else:
            signals['overall_signal'] = 'Hold'
        
        return signals


class FMPTechnicalAnalyzer:
    """Technical analysis using FMP API for price data"""
    
    BASE_URL = "https://financialmodelingprep.com/api/v3"
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize FMP technical analyzer"""
        self.api_key = api_key or os.getenv('FMP_API_KEY')
        if not self.api_key:
            raise ValueError(
                "API key required. Set FMP_API_KEY in .env file or environment variable.\n"
                "Get your free API key at: https://site.financialmodelingprep.com/\n"
                "Create a .env file with: FMP_API_KEY=your_key"
            )
        self.technical = TechnicalAnalyzer()
    
    def _make_request(self, endpoint: str, params: Dict = None) -> List[Dict]:
        """Make API request"""
        url = f"{self.BASE_URL}/{endpoint}"
        if params is None:
            params = {}
        params['apikey'] = self.api_key
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {e}")
    
    def get_historical_data(self, symbol: str, period: int = 365) -> pd.DataFrame:
        """Get historical price data"""
        # FMP API endpoint for historical data
        data = self._make_request(f'historical-price-full/{symbol}', {'timeseries': period})
        
        # Handle different response formats
        if isinstance(data, list) and len(data) > 0:
            if 'historical' in data[0]:
                historical = data[0]['historical']
            else:
                historical = data
        elif isinstance(data, dict) and 'historical' in data:
            historical = data['historical']
        else:
            raise Exception(f"No historical data available for {symbol}")
        
        if not historical:
            raise Exception(f"No historical data available for {symbol}")
        
        df = pd.DataFrame(historical)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date').reset_index(drop=True)
        return df
    
    def analyze_stock(self, symbol: str):
        """Perform complete technical analysis"""
        print(f"\n{'='*80}")
        print(f"TECHNICAL ANALYSIS: {symbol}")
        print(f"{'='*80}\n")
        
        # Get historical data
        print("Fetching historical price data...")
        try:
            df = self.get_historical_data(symbol)
            if df.empty:
                print("No historical data available")
                return
            
            print(f"✓ Got {len(df)} days of data")
            print(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}\n")
        except Exception as e:
            print(f"Error fetching data: {e}")
            return
        
        # Extract price series
        close_prices = df['close']
        high_prices = df['high']
        low_prices = df['low']
        volumes = df['volume']
        current_price = close_prices.iloc[-1]
        
        # Calculate indicators
        print("Calculating technical indicators...")
        
        # Moving Averages
        sma_20 = self.technical.calculate_sma(close_prices, 20)
        sma_50 = self.technical.calculate_sma(close_prices, 50)
        sma_200 = self.technical.calculate_sma(close_prices, 200)
        ema_12 = self.technical.calculate_ema(close_prices, 12)
        ema_26 = self.technical.calculate_ema(close_prices, 26)
        
        # Momentum Indicators
        rsi = self.technical.calculate_rsi(close_prices, 14)
        macd_line, signal_line, histogram = self.technical.calculate_macd(close_prices)
        
        # Volatility Indicators
        bb_upper, bb_middle, bb_lower = self.technical.calculate_bollinger_bands(close_prices)
        atr = self.technical.calculate_atr(high_prices, low_prices, close_prices)
        
        # Support/Resistance - Multiple Methods
        support_levels, resistance_levels = self.technical.identify_support_resistance(close_prices)
        pivot_points = self.technical.calculate_pivot_points(high_prices, low_prices, close_prices)
        fibonacci_levels = self.technical.calculate_fibonacci_levels(high_prices, low_prices)
        
        # Volume Analysis
        volume_trends = self.technical.analyze_volume_trends(volumes)
        volume_divergence = self.technical.detect_volume_divergence(close_prices, volumes)
        volume_comparison = self.technical.compare_volume_to_average(volumes)
        
        # Trend Analysis
        trend_analysis = self.technical.analyze_trend(close_prices, sma_50, sma_200)
        
        # Trading Signals
        trading_signals = self.technical.get_trading_signals(rsi, macd_line, signal_line, close_prices, sma_20)
        
        # Volume Confirmation for Signals
        volume_confirmation = self.technical.volume_confirmation(volumes, trading_signals['overall_signal'])
        
        # Display Results
        print("📊 CURRENT PRICE ACTION")
        print("-" * 80)
        print(f"Current Price: ${current_price:.2f}")
        print(f"Price Change (1D): {((current_price - close_prices.iloc[-2]) / close_prices.iloc[-2] * 100):+.2f}%" if len(close_prices) > 1 else "N/A")
        print(f"Price Change (1W): {((current_price - close_prices.iloc[-5]) / close_prices.iloc[-5] * 100):+.2f}%" if len(close_prices) >= 5 else "N/A")
        print(f"Price Change (1M): {((current_price - close_prices.iloc[-20]) / close_prices.iloc[-20] * 100):+.2f}%" if len(close_prices) >= 20 else "N/A")
        print(f"Price Change (1Y): {((current_price - close_prices.iloc[0]) / close_prices.iloc[0] * 100):+.2f}%")
        print()
        
        print("📈 TREND ANALYSIS")
        print("-" * 80)
        print(f"Primary Trend: {trend_analysis['trend']}")
        print(f"Trend Strength: {trend_analysis['strength']}")
        print(f"Price vs SMA 50: {trend_analysis['price_vs_sma50']}")
        print(f"Price vs SMA 200: {trend_analysis['price_vs_sma200']}")
        print(f"SMA 50 vs SMA 200: {trend_analysis['sma50_vs_sma200']}")
        print()
        
        print("📊 MOVING AVERAGES")
        print("-" * 80)
        print(f"SMA 20: ${sma_20.iloc[-1]:.2f}" if not pd.isna(sma_20.iloc[-1]) else "SMA 20: N/A")
        print(f"SMA 50: ${sma_50.iloc[-1]:.2f}" if not pd.isna(sma_50.iloc[-1]) else "SMA 50: N/A")
        print(f"SMA 200: ${sma_200.iloc[-1]:.2f}" if not pd.isna(sma_200.iloc[-1]) else "SMA 200: N/A")
        print(f"EMA 12: ${ema_12.iloc[-1]:.2f}" if not pd.isna(ema_12.iloc[-1]) else "EMA 12: N/A")
        print(f"EMA 26: ${ema_26.iloc[-1]:.2f}" if not pd.isna(ema_26.iloc[-1]) else "EMA 26: N/A")
        print()
        
        print("💹 MOMENTUM INDICATORS")
        print("-" * 80)
        current_rsi = float(rsi.iloc[-1]) if not pd.isna(rsi.iloc[-1]) else None
        rsi_status = "Overbought" if current_rsi and current_rsi > 70 else "Oversold" if current_rsi and current_rsi < 30 else "Neutral"
        print(f"RSI (14): {current_rsi:.2f} ({rsi_status})" if current_rsi else "RSI (14): N/A")
        print(f"MACD Line: {macd_line.iloc[-1]:.2f}" if not pd.isna(macd_line.iloc[-1]) else "MACD Line: N/A")
        print(f"Signal Line: {signal_line.iloc[-1]:.2f}" if not pd.isna(signal_line.iloc[-1]) else "Signal Line: N/A")
        print(f"Histogram: {histogram.iloc[-1]:.2f}" if not pd.isna(histogram.iloc[-1]) else "Histogram: N/A")
        macd_signal_str = "Bullish" if not pd.isna(macd_line.iloc[-1]) and not pd.isna(signal_line.iloc[-1]) and macd_line.iloc[-1] > signal_line.iloc[-1] else "Bearish"
        print(f"MACD Signal: {macd_signal_str}")
        print()
        
        print("📉 VOLATILITY INDICATORS")
        print("-" * 80)
        print(f"Bollinger Upper Band: ${bb_upper.iloc[-1]:.2f}" if not pd.isna(bb_upper.iloc[-1]) else "Upper Band: N/A")
        print(f"Bollinger Middle (SMA 20): ${bb_middle.iloc[-1]:.2f}" if not pd.isna(bb_middle.iloc[-1]) else "Middle: N/A")
        print(f"Bollinger Lower Band: ${bb_lower.iloc[-1]:.2f}" if not pd.isna(bb_lower.iloc[-1]) else "Lower Band: N/A")
        bb_position = "Near Upper" if not pd.isna(bb_upper.iloc[-1]) and current_price > bb_upper.iloc[-1] * 0.95 else "Near Lower" if not pd.isna(bb_lower.iloc[-1]) and current_price < bb_lower.iloc[-1] * 1.05 else "Middle"
        print(f"Price Position: {bb_position}")
        atr_value = float(atr.iloc[-1]) if not pd.isna(atr.iloc[-1]) else None
        print(f"ATR (14): ${atr_value:.2f}" if atr_value else "ATR: N/A")
        print()
        
        print("📊 VOLUME ANALYSIS")
        print("-" * 80)
        if volume_trends['avg_volume']:
            print(f"Volume Trend: {volume_trends['trend']}")
            print(f"Current Volume: {volume_trends['current_volume']:,.0f}")
            print(f"Average Volume (20-day): {volume_trends['avg_volume']:,.0f}")
            print(f"Volume Status: {volume_trends['volume_status']} ({volume_trends['current_vs_avg']:.2f}x average)" if volume_trends['current_vs_avg'] else "Volume Status: Unknown")
        else:
            print("Volume Analysis: Insufficient Data")
        print()
        
        if volume_divergence['divergence'] != 'None':
            print(f"⚠️  Volume Divergence Detected: {volume_divergence['type']}")
            print(f"   Price Change: {volume_divergence['price_change']*100:+.2f}%")
            print(f"   Volume Change: {volume_divergence['volume_change']*100:+.2f}%")
            print()
        
        print(f"Volume Confirmation: {volume_confirmation['reason']}")
        print()
        
        print("📊 SUPPORT & RESISTANCE LEVELS")
        print("-" * 80)
        print("Methodology: Multiple methods used - Local Minima/Maxima, Pivot Points, Fibonacci Retracements")
        print()
        
        print("Support Levels (Local Minima):")
        for i, level in enumerate(support_levels[:5], 1):
            print(f"  {i}. ${level:.2f}")
        print()
        
        print("Resistance Levels (Local Maxima):")
        for i, level in enumerate(resistance_levels[:5], 1):
            print(f"  {i}. ${level:.2f}")
        print()
        
        print("Pivot Points:")
        print(f"  Pivot: ${pivot_points['pivot']:.2f}")
        print(f"  Support 1: ${pivot_points['support_1']:.2f}")
        print(f"  Support 2: ${pivot_points['support_2']:.2f}")
        print(f"  Resistance 1: ${pivot_points['resistance_1']:.2f}")
        print(f"  Resistance 2: ${pivot_points['resistance_2']:.2f}")
        print()
        
        print("Fibonacci Retracement Levels:")
        print(f"  0% (High): ${fibonacci_levels['fib_0']:.2f}")
        print(f"  23.6%: ${fibonacci_levels['fib_23.6']:.2f}")
        print(f"  38.2%: ${fibonacci_levels['fib_38.2']:.2f}")
        print(f"  50%: ${fibonacci_levels['fib_50']:.2f}")
        print(f"  61.8%: ${fibonacci_levels['fib_61.8']:.2f}")
        print(f"  100% (Low): ${fibonacci_levels['fib_100']:.2f}")
        print()
        
        print("🎯 TRADING SIGNALS")
        print("-" * 80)
        print(f"RSI Signal: {trading_signals['rsi_signal']}")
        print(f"MACD Signal: {trading_signals['macd_signal']}")
        print(f"Trend Signal: {trading_signals['trend_signal']}")
        print(f"\nOverall Signal: {trading_signals['overall_signal']}")
        print()
        
        print(f"{'='*80}")
        print(f"Analysis completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}\n")
        
        # Calculate price changes
        price_changes = {}
        if len(close_prices) > 1:
            price_changes['1D'] = (current_price - close_prices.iloc[-2]) / close_prices.iloc[-2]
        if len(close_prices) >= 5:
            price_changes['1W'] = (current_price - close_prices.iloc[-5]) / close_prices.iloc[-5]
        if len(close_prices) >= 20:
            price_changes['1M'] = (current_price - close_prices.iloc[-20]) / close_prices.iloc[-20]
        price_changes['1Y'] = (current_price - close_prices.iloc[0]) / close_prices.iloc[0]
        
        # Determine price vs SMA20
        price_vs_sma20 = 'Above' if not pd.isna(sma_20.iloc[-1]) and current_price > sma_20.iloc[-1] else 'Below' if not pd.isna(sma_20.iloc[-1]) else None
        
        # Get MACD signal from trading_signals dict
        macd_signal_from_dict = trading_signals.get('macd_signal', 'Neutral')
        
        # Return structured data
        try:
            result = {
                'trend_analysis': trend_analysis,
                'trading_signals': trading_signals,
                'price_changes': price_changes,
                'support_levels': support_levels[:5],  # Top 5 support levels
                'resistance_levels': resistance_levels[:5],  # Top 5 resistance levels
                'pivot_points': pivot_points,
                'fibonacci_levels': fibonacci_levels,
                'volume_analysis': {
                    'trends': volume_trends,
                    'divergence': volume_divergence,
                    'comparison': volume_comparison,
                    'confirmation': volume_confirmation
                },
                'indicators': {
                    'rsi': current_rsi,
                    'macd_signal': macd_signal_from_dict,
                    'price_position': bb_position,
                    'atr': atr_value,
                    'price_vs_sma20': price_vs_sma20,
                    'current_price': float(current_price)
                },
                'current_price': float(current_price)
            }
            return result
        except Exception as e:
            print(f"Error creating return data: {e}")
            import traceback
            traceback.print_exc()
            return None


def main():
    """Main function"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 stock_technical_analysis.py <TICKER>")
        print("\nExample:")
        print("  python3 stock_technical_analysis.py NVDA")
        print("\nRequires FMP_API_KEY environment variable")
        sys.exit(1)
    
    ticker = sys.argv[1].upper()
    
    try:
        analyzer = FMPTechnicalAnalyzer()
        analyzer.analyze_stock(ticker)
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        print("\nSet FMP_API_KEY environment variable:")
        print("  export FMP_API_KEY=your_api_key")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

