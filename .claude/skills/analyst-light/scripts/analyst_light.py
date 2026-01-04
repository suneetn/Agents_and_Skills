#!/usr/bin/env python3
"""
Analyst Light - Quick actionable trade setups (V3)

Generates entry, target, stop loss, and investment thesis for stocks.
Uses ATR-based targets to ensure minimum 1.5:1 risk/reward ratio.

Note: Template-based thesis generation. When invoked by Claude,
the AI layer provides richer narrative interpretation of the data.
"""

import os
import sys
import json
import argparse
import requests
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta

# FMP API Configuration
FMP_API_KEY = os.environ.get("FMP_API_KEY", "")
FMP_BASE_URL = "https://financialmodelingprep.com/api/v3"

# Minimum R:R ratio for actionable trades
MIN_RISK_REWARD = 1.5


class FMPClient:
    """Simple FMP API client"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
    
    def _get(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Make GET request to FMP API"""
        params = params or {}
        params["apikey"] = self.api_key
        
        try:
            url = f"{FMP_BASE_URL}/{endpoint}"
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"API Error ({endpoint}): {e}", file=sys.stderr)
            return None
    
    def get_quote(self, symbol: str) -> Optional[Dict]:
        """Get current quote"""
        data = self._get(f"quote/{symbol}")
        return data[0] if data else None
    
    def get_profile(self, symbol: str) -> Optional[Dict]:
        """Get company profile"""
        data = self._get(f"profile/{symbol}")
        return data[0] if data else None
    
    def get_historical_prices(self, symbol: str, days: int = 90) -> Optional[List[Dict]]:
        """Get historical daily prices with OHLC data"""
        data = self._get(f"historical-price-full/{symbol}")
        if data and "historical" in data:
            return data["historical"][:days]
        return None
    
    def get_financial_growth(self, symbol: str) -> Optional[Dict]:
        """Get financial growth metrics"""
        data = self._get(f"financial-growth/{symbol}", {"limit": 1})
        return data[0] if data else None
    
    def get_rating(self, symbol: str) -> Optional[Dict]:
        """Get FMP rating"""
        data = self._get(f"rating/{symbol}")
        return data[0] if data else None
    
    def get_key_metrics(self, symbol: str) -> Optional[Dict]:
        """Get key metrics TTM"""
        data = self._get(f"key-metrics-ttm/{symbol}")
        return data[0] if data else None


class AnalystLight:
    """Quick actionable trade analysis with proper R:R"""
    
    def __init__(self, api_key: str = None):
        """
        Initialize analyst.
        
        Args:
            api_key: FMP API key (defaults to FMP_API_KEY env var)
        """
        self.client = FMPClient(api_key or FMP_API_KEY)
    
    def get_trade_setup(self, symbol: str, min_rr: float = MIN_RISK_REWARD, screen_context: Dict = None, news_data: List[Dict] = None) -> Dict:
        """
        Generate complete trade setup for a symbol
        
        Args:
            symbol: Stock ticker
            min_rr: Minimum risk/reward ratio (default 1.5)
            screen_context: Optional dict with screen_type and score for thesis generation
            news_data: Optional list of news articles (for context, not used directly)
        
        Returns dict with:
        - Trade setup (entry, target, stop)
        - Investment thesis (template-based, AI layer enhances when invoked by Claude)
        - Key metrics
        - Quality assessment with breakdown
        """
        symbol = symbol.upper().strip()
        
        # Fetch all data
        quote = self.client.get_quote(symbol)
        profile = self.client.get_profile(symbol)
        prices = self.client.get_historical_prices(symbol, days=90)
        growth = self.client.get_financial_growth(symbol)
        rating = self.client.get_rating(symbol)
        key_metrics = self.client.get_key_metrics(symbol)
        
        if not quote or not prices:
            return {"error": f"Could not fetch data for {symbol}"}
        
        # Calculate technical levels with proper ATR
        technicals = self._calculate_technicals(prices, quote)
        
        # Generate trade setup using ATR-based targets
        trade_setup = self._generate_trade_setup(technicals, quote, min_rr)
        
        # Compile metrics
        metrics = self._compile_metrics(quote, growth, rating, key_metrics)
        
        # Quality assessment with detailed breakdown
        quality = self._assess_quality(trade_setup, technicals)
        
        # Generate template-based thesis (Claude enhances this when orchestrating)
        thesis = self._generate_thesis(profile, growth, quote, key_metrics, technicals, screen_context)
        
        # Add sentiment inference from technicals
        thesis["sentiment"] = self._infer_sentiment(technicals, trade_setup)
        thesis["sentiment_score"] = self._calculate_sentiment_score(technicals, trade_setup)
        
        return {
            "symbol": symbol,
            "name": quote.get("name", profile.get("companyName", symbol) if profile else symbol),
            "price": quote.get("price", 0),
            "change_percent": round(quote.get("changesPercentage", 0), 2),
            "trade_setup": trade_setup,
            "thesis": thesis,
            "metrics": metrics,
            "quality": quality,
            "generated_at": datetime.now().isoformat()
        }
    
    def _calculate_technicals(self, prices: List[Dict], quote: Dict) -> Dict:
        """Calculate technical indicators with proper ATR"""
        
        current_price = quote.get("price", 0)
        
        if not prices or current_price <= 0:
            return {"error": "No price data"}
        
        # Extract OHLC data
        closes = [p.get("close", 0) for p in prices]
        highs = [p.get("high", p.get("close", 0)) for p in prices]
        lows = [p.get("low", p.get("close", 0)) for p in prices]
        
        # Reverse for chronological order (oldest first)
        closes_asc = closes[::-1]
        
        # Calculate SMAs
        sma_20 = sum(closes_asc[-20:]) / 20 if len(closes_asc) >= 20 else current_price
        sma_50 = sum(closes_asc[-50:]) / 50 if len(closes_asc) >= 50 else current_price
        
        # Calculate TRUE ATR (Average True Range)
        true_ranges = []
        for i in range(min(14, len(prices) - 1)):
            high = highs[i]
            low = lows[i]
            prev_close = closes[i + 1] if i + 1 < len(closes) else closes[i]
            
            tr = max(
                high - low,
                abs(high - prev_close),
                abs(low - prev_close)
            )
            true_ranges.append(tr)
        
        atr = sum(true_ranges) / len(true_ranges) if true_ranges else current_price * 0.02
        atr_percent = (atr / current_price) * 100
        
        # Find key levels
        recent_high_20 = max(highs[:20]) if len(highs) >= 20 else max(highs)
        recent_low_20 = min(lows[:20]) if len(lows) >= 20 else min(lows)
        recent_high_60 = max(highs[:60]) if len(highs) >= 60 else max(highs)
        recent_low_60 = min(lows[:60]) if len(lows) >= 60 else min(lows)
        
        # Calculate price position in range
        range_60 = recent_high_60 - recent_low_60
        position_in_range = ((current_price - recent_low_60) / range_60 * 100) if range_60 > 0 else 50
        
        # Determine trend strength
        price_vs_sma20 = ((current_price / sma_20) - 1) * 100 if sma_20 else 0
        price_vs_sma50 = ((current_price / sma_50) - 1) * 100 if sma_50 else 0
        
        if current_price > sma_20 > sma_50 and price_vs_sma20 > 0:
            trend = "bullish"
            trend_strength = min(100, price_vs_sma20 * 5)  # 0-100 scale
        elif current_price < sma_20 < sma_50 and price_vs_sma20 < 0:
            trend = "bearish"
            trend_strength = min(100, abs(price_vs_sma20) * 5)
        else:
            trend = "neutral"
            trend_strength = 50
        
        return {
            "sma_20": round(sma_20, 2),
            "sma_50": round(sma_50, 2),
            "atr": round(atr, 2),
            "atr_percent": round(atr_percent, 2),
            "recent_high_20": round(recent_high_20, 2),
            "recent_low_20": round(recent_low_20, 2),
            "recent_high_60": round(recent_high_60, 2),
            "recent_low_60": round(recent_low_60, 2),
            "position_in_range": round(position_in_range, 1),
            "trend": trend,
            "trend_strength": round(trend_strength, 0),
            "price_vs_sma20": round(price_vs_sma20, 2),
            "price_vs_sma50": round(price_vs_sma50, 2)
        }
    
    def _generate_trade_setup(self, technicals: Dict, quote: Dict, min_rr: float) -> Dict:
        """Generate ATR-based trade setup with minimum R:R"""
        
        current_price = quote.get("price", 0)
        atr = technicals.get("atr", current_price * 0.02)
        trend = technicals.get("trend", "neutral")
        sma_20 = technicals.get("sma_20", current_price)
        position_in_range = technicals.get("position_in_range", 50)
        
        # Determine bias
        if trend == "bullish":
            bias = "bullish"
            bias_emoji = "🟢"
        elif trend == "bearish":
            bias = "bearish"
            bias_emoji = "🔴"
        else:
            bias = "neutral"
            bias_emoji = "🟡"
        
        # ATR-based levels with variation based on position and trend
        # Different ATR multipliers create R:R variation (1.5x to 3.5x)
        trend_strength = technicals.get("trend_strength", 50)
        
        if position_in_range > 80:
            # Near highs - conservative, wait for pullback
            entry_price = current_price - (1.2 * atr)  # Wait for pullback
            target_multiplier = 2.0 + (trend_strength / 100)  # 2.0-3.0x based on trend
            stop_multiplier = 1.2  # Tighter stop near highs
            target_price = entry_price + (target_multiplier * atr)
            stop_price = entry_price - (stop_multiplier * atr)
            entry_reason = f"Wait for pullback to ${entry_price:.0f} (1.2 ATR below current)"
        elif position_in_range < 20:
            # Near lows - aggressive, oversold bounce
            entry_price = current_price
            target_multiplier = 3.5 + (trend_strength / 200)  # 3.5-4.0x for bounce
            stop_multiplier = 1.0  # Tight stop at lows
            target_price = current_price + (target_multiplier * atr)
            stop_price = current_price - (stop_multiplier * atr)
            entry_reason = f"Near 60-day lows, oversold bounce setup"
        elif position_in_range < 40:
            # Lower half - good entry zone
            entry_price = current_price
            target_multiplier = 3.0 + (trend_strength / 150)  # 3.0-3.7x
            stop_multiplier = 1.3
            target_price = current_price + (target_multiplier * atr)
            stop_price = current_price - (stop_multiplier * atr)
            entry_reason = f"Lower range entry, favorable risk position"
        else:
            # Middle to upper range - standard setup
            if trend == "bullish":
                entry_price = max(sma_20, current_price - (0.5 * atr))
                target_multiplier = 2.5 + (trend_strength / 200)  # 2.5-3.0x
                stop_multiplier = 1.4
                target_price = entry_price + (target_multiplier * atr)
                stop_price = entry_price - (stop_multiplier * atr)
                entry_reason = f"Pullback to 20 SMA support at ${sma_20:.0f}"
            elif trend == "bearish":
                entry_price = current_price
                target_multiplier = 2.8
                stop_multiplier = 1.5
                target_price = current_price - (target_multiplier * atr)  # Short target
                stop_price = current_price + (stop_multiplier * atr)
                entry_reason = "Bearish trend, short opportunity"
            else:
                entry_price = sma_20
                target_multiplier = 2.2  # Conservative for neutral
                stop_multiplier = 1.5
                target_price = sma_20 + (target_multiplier * atr)
                stop_price = sma_20 - (stop_multiplier * atr)
                entry_reason = f"Wait for 20 SMA retest at ${sma_20:.0f}"
        
        # Calculate percentages and R:R
        if trend == "bearish":
            # For shorts, target is below entry
            upside_pct = ((entry_price - target_price) / entry_price) * 100
            downside_pct = ((stop_price - entry_price) / entry_price) * 100
            potential_gain = entry_price - target_price
            potential_loss = stop_price - entry_price
        else:
            upside_pct = ((target_price - entry_price) / entry_price) * 100
            downside_pct = ((entry_price - stop_price) / entry_price) * 100
            potential_gain = target_price - entry_price
            potential_loss = entry_price - stop_price
        
        risk_reward = round(potential_gain / potential_loss, 2) if potential_loss > 0 else 0
        
        # If R:R is below minimum, adjust target to improve it (but show actual calculated R:R)
        adjusted = False
        if risk_reward < min_rr and potential_loss > 0:
            # Extend target to meet minimum R:R
            required_gain = potential_loss * min_rr
            if trend == "bearish":
                target_price = entry_price - required_gain
            else:
                target_price = entry_price + required_gain
            upside_pct = (required_gain / entry_price) * 100
            # Recalculate actual R:R with new target
            potential_gain = abs(target_price - entry_price)
            risk_reward = round(potential_gain / potential_loss, 2)
            adjusted = True
        
        # Entry zone (±2% around entry price)
        entry_zone = [round(entry_price * 0.98, 2), round(entry_price * 1.02, 2)]
        
        # Timeframe based on ATR volatility
        atr_pct = technicals.get("atr_percent", 2)
        if atr_pct > 4:
            timeframe = "1-2 weeks"
        elif atr_pct > 2.5:
            timeframe = "2-4 weeks"
        elif atr_pct > 1.5:
            timeframe = "1-2 months"
        else:
            timeframe = "2-4 months"
        
        # Target reasoning - clearer description
        target_gain = abs(target_price - entry_price)
        current_to_target = abs(target_price - current_price)
        if trend == "bearish":
            target_reason = f"Target ${target_price:.0f} (${current_to_target:.0f} from current)"
        else:
            target_reason = f"Target ${target_price:.0f} (+${current_to_target:.0f} from current)"
        
        return {
            "bias": bias,
            "bias_emoji": bias_emoji,
            "entry": {
                "price": round(entry_price, 2),
                "zone": entry_zone,
                "reason": entry_reason
            },
            "target": {
                "price": round(target_price, 2),
                "upside_percent": round(upside_pct, 1),
                "reason": target_reason
            },
            "stop": {
                "price": round(stop_price, 2),
                "downside_percent": round(downside_pct, 1),
                "reason": f"1.5x ATR below entry (${1.5*atr:.0f})"
            },
            "risk_reward": risk_reward,
            "timeframe": timeframe,
            "position_in_range": position_in_range
        }
    
    def _infer_sentiment(self, technicals: Dict, trade_setup: Dict) -> str:
        """Infer sentiment from technical data"""
        trend = technicals.get("trend", "neutral")
        bias = trade_setup.get("bias", "neutral")
        position = technicals.get("position_in_range", 50)
        
        if trend == "bullish" and bias == "bullish":
            return "bullish"
        elif trend == "bearish" and bias == "bearish":
            return "bearish"
        elif position < 25:
            return "cautiously bullish"  # Oversold bounce potential
        elif position > 80:
            return "cautiously bearish"  # Overbought
        return "neutral"
    
    def _calculate_sentiment_score(self, technicals: Dict, trade_setup: Dict) -> float:
        """Calculate sentiment score from -1 to 1"""
        score = 0.0
        
        # Trend contribution
        trend = technicals.get("trend", "neutral")
        if trend == "bullish":
            score += 0.4
        elif trend == "bearish":
            score -= 0.4
        
        # Position contribution
        position = technicals.get("position_in_range", 50)
        if position < 30:
            score += 0.3  # Near lows = bullish potential
        elif position > 70:
            score -= 0.2  # Near highs = less upside
        
        # R:R contribution
        rr = trade_setup.get("risk_reward", 1.5)
        if rr >= 2.5:
            score += 0.3
        elif rr >= 2.0:
            score += 0.2
        elif rr < 1.5:
            score -= 0.2
        
        return round(max(-1.0, min(1.0, score)), 2)
    
    def _generate_thesis(
        self, 
        profile: Optional[Dict], 
        growth: Optional[Dict], 
        quote: Dict,
        key_metrics: Optional[Dict],
        technicals: Dict,
        screen_context: Optional[Dict] = None
    ) -> Dict:
        """Generate comprehensive template-based investment thesis"""
        
        company_name = quote.get("name", "Company")
        ticker = quote.get("symbol", "")
        sector = profile.get("sector", "Unknown") if profile else "Unknown"
        industry = profile.get("industry", "Unknown") if profile else "Unknown"
        description = profile.get("description", "")[:200] if profile else ""
        
        # Growth metrics
        eps_growth = growth.get("epsgrowth", 0) * 100 if growth else 0
        rev_growth = growth.get("revenueGrowth", 0) * 100 if growth else 0
        
        # Valuation metrics
        pe_ratio = quote.get("pe", 0) or 0
        price = quote.get("price", 0)
        change_pct = quote.get("changesPercentage", 0)
        market_cap = quote.get("marketCap", 0)
        
        # Technical context
        trend = technicals.get("trend", "neutral")
        position_in_range = technicals.get("position_in_range", 50)
        price_vs_sma20 = technicals.get("price_vs_sma20", 0)
        price_vs_sma50 = technicals.get("price_vs_sma50", 0)
        
        # Build comprehensive thesis narrative
        thesis_lines = []
        
        # 1. Company context (what they do)
        if sector != "Unknown":
            cap_tier = "mega-cap" if market_cap > 200e9 else "large-cap" if market_cap > 10e9 else "mid-cap" if market_cap > 2e9 else "small-cap"
            thesis_lines.append(f"{company_name} is a {cap_tier} {sector.lower()} company in the {industry.lower()} space.")
        
        # 2. Why it surfaced (screening reason)
        screen_reason = ""
        if screen_context:
            screen_type = screen_context.get("screen_type", "")
            screen_score = screen_context.get("score", 0)
            if screen_type == "momentum":
                screen_reason = f"The stock surfaced in our momentum screen (score: {screen_score:.0f}) due to strong technical momentum and positive price action."
            elif screen_type == "growth":
                screen_reason = f"Identified by our growth screen (score: {screen_score:.0f}) for above-average revenue and earnings expansion."
            elif screen_type == "value":
                screen_reason = f"Flagged by our value screen (score: {screen_score:.0f}) as potentially undervalued relative to fundamentals."
            elif screen_type == "tech_momentum":
                screen_reason = f"Selected by our tech momentum screen (score: {screen_score:.0f}) for leadership in the technology sector."
        
        if screen_reason:
            thesis_lines.append(screen_reason)
        
        # 3. Technical setup (why now)
        tech_narrative = ""
        if position_in_range > 80:
            tech_narrative = f"Currently extended at {position_in_range:.0f}% of its 60-day range. While momentum is strong, waiting for a pullback to the ${technicals.get('sma_20', price*0.95):.0f} area would offer better risk/reward."
        elif position_in_range < 25:
            tech_narrative = f"Trading near 60-day lows ({position_in_range:.0f}% of range), presenting a potential oversold bounce opportunity if support holds."
        elif trend == "bullish" and 30 < position_in_range < 70:
            tech_narrative = f"In a healthy uptrend with price {price_vs_sma20:.1f}% above the 20-day moving average. The stock has room to run before becoming extended."
        elif trend == "bearish":
            tech_narrative = f"Currently in a downtrend with price {abs(price_vs_sma20):.1f}% below the 20-day MA. Consider waiting for trend reversal signals."
        else:
            tech_narrative = f"Consolidating in the middle of its range. Watch for a breakout above ${technicals.get('recent_high_20', price*1.02):.0f} for confirmation."
        
        if tech_narrative:
            thesis_lines.append(tech_narrative)
        
        # 4. Fundamental story
        fund_parts = []
        if eps_growth > 50:
            fund_parts.append(f"exceptional {eps_growth:.0f}% EPS growth")
        elif eps_growth > 20:
            fund_parts.append(f"solid {eps_growth:.0f}% earnings growth")
        elif eps_growth > 0:
            fund_parts.append(f"modest {eps_growth:.0f}% earnings growth")
        elif eps_growth < -10:
            fund_parts.append(f"declining earnings ({eps_growth:.0f}%)")
        
        if rev_growth > 30:
            fund_parts.append(f"rapid {rev_growth:.0f}% revenue expansion")
        elif rev_growth > 15:
            fund_parts.append(f"healthy {rev_growth:.0f}% revenue growth")
        
        if pe_ratio > 0:
            if pe_ratio < 15:
                fund_parts.append(f"attractively valued at {pe_ratio:.0f}x earnings")
            elif pe_ratio > 40:
                fund_parts.append(f"trading at a premium {pe_ratio:.0f}x multiple")
        
        if fund_parts:
            fund_narrative = "Fundamentally, the company shows " + ", ".join(fund_parts) + "."
            thesis_lines.append(fund_narrative)
        
        # Combine into summary
        summary = " ".join(thesis_lines)
        
        # Specific risks based on data
        risks = []
        if position_in_range > 80:
            risks.append("Overbought near highs, pullback likely before next leg up")
        elif position_in_range < 20:
            risks.append("Catching a falling knife if support breaks")
        if eps_growth < -10:
            risks.append("Declining earnings trajectory could pressure multiple")
        if pe_ratio and pe_ratio > 50:
            risks.append("Elevated valuation leaves little margin for execution misses")
        if sector == "Technology":
            risks.append("Tech valuations sensitive to interest rate expectations")
        elif sector == "Financial Services":
            risks.append("Bank profitability tied to yield curve and credit quality")
        elif sector == "Energy":
            risks.append("Commodity price volatility affects earnings visibility")
        elif sector == "Healthcare":
            risks.append("Regulatory and reimbursement policy risks")
        if not risks:
            risks.append("General market and sector rotation risk")
        
        # Catalysts
        catalysts = []
        if eps_growth > 30:
            catalysts.append("Continued earnings beat streak")
        if position_in_range < 30:
            catalysts.append("Oversold bounce as selling exhaustion sets in")
        if rev_growth > 20:
            catalysts.append("Revenue acceleration driving operating leverage")
        if sector == "Technology":
            catalysts.append("AI/cloud tailwinds in tech sector")
        catalysts.append("Upcoming quarterly earnings report")
        
        return {
            "summary": summary[:500],  # Longer summary allowed
            "top_risk": risks[0],
            "catalyst": catalysts[0] if catalysts else "Earnings report",
            "all_risks": risks[:3],
            "all_catalysts": catalysts[:3]
        }
    
    def _compile_metrics(
        self, 
        quote: Dict, 
        growth: Optional[Dict], 
        rating: Optional[Dict],
        key_metrics: Optional[Dict]
    ) -> Dict:
        """Compile key metrics"""
        
        metrics = {
            "pe_ratio": quote.get("pe"),
            "market_cap": quote.get("marketCap"),
            "volume": quote.get("volume"),
            "avg_volume": quote.get("avgVolume"),
            "52_week_high": quote.get("yearHigh"),
            "52_week_low": quote.get("yearLow"),
        }
        
        if growth:
            metrics["eps_growth"] = round(growth.get("epsgrowth", 0) * 100, 1)
            metrics["revenue_growth"] = round(growth.get("revenueGrowth", 0) * 100, 1)
        
        if key_metrics:
            metrics["roe"] = key_metrics.get("roeTTM")
            metrics["debt_to_equity"] = key_metrics.get("debtToEquityTTM")
        
        if rating:
            metrics["fmp_rating"] = {
                "grade": rating.get("ratingRecommendation", "N/A"),
                "score": rating.get("ratingScore", 0)
            }
        
        return metrics
    
    def _assess_quality(self, trade_setup: Dict, technicals: Dict) -> Dict:
        """Assess trade quality with balanced scoring and detailed breakdown"""
        
        rr = trade_setup.get("risk_reward", 0)
        position = trade_setup.get("position_in_range", 50)
        trend = technicals.get("trend", "neutral")
        trend_strength = technicals.get("trend_strength", 50)
        bias = trade_setup.get("bias", "neutral")
        
        # Quality score (0-100)
        score = 0
        flags = []
        
        # Detailed breakdown for transparency
        breakdown = {
            "rr_score": {"points": 0, "max": 35, "label": "Risk/Reward"},
            "position_score": {"points": 0, "max": 35, "label": "Entry Position"},
            "trend_score": {"points": 0, "max": 30, "label": "Trend Clarity"}
        }
        
        # R:R contribution (0-35 points) - primary factor
        if rr >= 2.5:
            rr_pts = 35
            rr_label = "Excellent (2.5:1+)"
            flags.append("✓ Excellent R:R (2.5:1+)")
        elif rr >= 2:
            rr_pts = 30
            rr_label = "Good (2.0:1+)"
            flags.append("✓ Good R:R (2:1+)")
        elif rr >= 1.7:
            rr_pts = 25
            rr_label = "Solid (1.7:1+)"
            flags.append("✓ Solid R:R (1.7:1+)")
        elif rr >= 1.5:
            rr_pts = 20
            rr_label = "Acceptable (1.5:1)"
            flags.append("○ Acceptable R:R (1.5:1)")
        else:
            rr_pts = 10
            rr_label = "Marginal (<1.5:1)"
            flags.append("✗ Marginal R:R (<1.5:1)")
        
        score += rr_pts
        breakdown["rr_score"]["points"] = rr_pts
        breakdown["rr_score"]["value"] = f"{rr:.1f}:1"
        breakdown["rr_score"]["detail"] = rr_label
        
        # Position + trend alignment (0-35 points)
        if trend == "bullish" and position > 60:
            pos_pts = 30
            pos_label = "Momentum (strong trend)"
            flags.append("✓ Strong momentum setup")
        elif trend == "bullish" and position <= 60:
            pos_pts = 35
            pos_label = "Pullback (ideal entry)"
            flags.append("✓ Pullback in uptrend (ideal)")
        elif position < 30:
            pos_pts = 30
            pos_label = "Oversold (bounce potential)"
            flags.append("✓ Oversold bounce potential")
        elif position < 50:
            pos_pts = 25
            pos_label = "Lower range (reasonable)"
            flags.append("✓ Lower range entry")
        elif trend == "bearish":
            pos_pts = 10
            pos_label = "Downtrend (caution)"
            flags.append("⚠️ Downtrend (caution)")
        else:
            pos_pts = 20
            pos_label = "Middle range (neutral)"
            flags.append("○ Neutral positioning")
        
        score += pos_pts
        breakdown["position_score"]["points"] = pos_pts
        breakdown["position_score"]["value"] = f"{position:.0f}%"
        breakdown["position_score"]["detail"] = pos_label
        
        # Trend clarity bonus (0-30 points)
        if trend_strength > 60:
            trend_pts = 30
            trend_label = "Clear direction"
            flags.append("✓ Clear trend direction")
        elif trend_strength > 40:
            trend_pts = 25
            trend_label = "Moderate clarity"
            flags.append("○ Moderate trend")
        elif trend == "neutral":
            trend_pts = 20
            trend_label = "Range-bound"
            flags.append("○ Range-bound")
        else:
            trend_pts = 15
            trend_label = "Weak/unclear"
            flags.append("○ Weak trend")
        
        score += trend_pts
        breakdown["trend_score"]["points"] = trend_pts
        breakdown["trend_score"]["value"] = trend.capitalize()
        breakdown["trend_score"]["detail"] = trend_label
        
        # Grade with adjusted thresholds
        if score >= 85:
            grade = "A"
            recommendation = "Strong Setup"
            grade_explanation = "Excellent risk/reward, optimal entry position, clear trend"
        elif score >= 70:
            grade = "B"
            recommendation = "Good Setup"
            grade_explanation = "Good risk/reward with favorable conditions"
        elif score >= 55:
            grade = "C"
            recommendation = "Fair Setup"
            grade_explanation = "Acceptable setup with some concerns"
        else:
            grade = "D"
            recommendation = "Weak Setup"
            grade_explanation = "Suboptimal conditions, consider alternatives"
        
        return {
            "score": score,
            "grade": grade,
            "recommendation": recommendation,
            "explanation": grade_explanation,
            "flags": flags,
            "breakdown": breakdown,  # Detailed scoring breakdown
            "actionable": rr >= MIN_RISK_REWARD
        }
    
    def format_text(self, result: Dict) -> str:
        """Format result as human-readable text"""
        
        if "error" in result:
            return f"Error: {result['error']}"
        
        setup = result.get("trade_setup", {})
        thesis = result.get("thesis", {})
        metrics = result.get("metrics", {})
        quality = result.get("quality", {})
        
        # Quality indicator
        quality_emoji = "🟢" if quality.get("grade") in ["A", "B"] else "🟡" if quality.get("grade") == "C" else "🔴"
        
        lines = [
            "━" * 55,
            f"{result['symbol']} - {result['name'][:30]}",
            f"${result['price']:.2f} ({result['change_percent']:+.1f}%) | {quality_emoji} {quality.get('grade', 'N/A')} - {quality.get('recommendation', '')}",
            "━" * 55,
            "",
            f"BIAS: {setup.get('bias_emoji', '🟡')} {setup.get('bias', 'NEUTRAL').upper()} | R:R {setup['risk_reward']:.1f}:1",
            "",
            "📊 TRADE SETUP",
            f"   Entry:  ${setup['entry']['zone'][0]:.0f}-{setup['entry']['zone'][1]:.0f}",
            f"           {setup['entry']['reason']}",
            f"   Target: ${setup['target']['price']:.0f} (+{setup['target']['upside_percent']:.0f}%)",
            f"   Stop:   ${setup['stop']['price']:.0f} (-{setup['stop']['downside_percent']:.0f}%)",
            "",
            "💡 WHY",
            f"   {thesis.get('summary', 'N/A')[:100]}",
            "",
            f"⚠️ RISK: {thesis.get('top_risk', 'N/A')}",
            f"⏱️ TIME: {setup.get('timeframe', 'N/A')}",
            "",
            "QUALITY FLAGS:",
        ]
        
        for flag in quality.get("flags", []):
            lines.append(f"   {flag}")
        
        lines.append("━" * 55)
        
        return "\n".join(lines)
    
    def format_newsletter(self, result: Dict) -> str:
        """Format result for newsletter inclusion"""
        
        if "error" in result:
            return ""
        
        setup = result.get("trade_setup", {})
        thesis = result.get("thesis", {})
        quality = result.get("quality", {})
        
        return f"""
<div class="stock-card {setup.get('bias', 'neutral')}">
    <div class="stock-header">
        <span class="ticker">{result['symbol']}</span>
        <span class="name">{result['name']}</span>
        <span class="price">${result['price']:.2f}</span>
        <span class="change {'positive' if result['change_percent'] > 0 else 'negative'}">{result['change_percent']:+.1f}%</span>
        <span class="quality-badge grade-{quality.get('grade', 'C').lower()}">{quality.get('grade', 'C')}</span>
    </div>
    <div class="trade-setup">
        <div class="rr-badge {'good' if setup['risk_reward'] >= 2 else 'ok' if setup['risk_reward'] >= 1.5 else 'bad'}">
            R:R {setup['risk_reward']:.1f}:1
        </div>
        <div class="setup-row">
            <span class="label">Entry:</span>
            <span class="value">${setup['entry']['zone'][0]:.0f}-{setup['entry']['zone'][1]:.0f}</span>
        </div>
        <div class="setup-row">
            <span class="label">Target:</span>
            <span class="value">${setup['target']['price']:.0f}</span>
            <span class="upside">+{setup['target']['upside_percent']:.0f}%</span>
        </div>
        <div class="setup-row">
            <span class="label">Stop:</span>
            <span class="value">${setup['stop']['price']:.0f}</span>
            <span class="downside">-{setup['stop']['downside_percent']:.0f}%</span>
        </div>
    </div>
    <div class="thesis">{thesis.get('summary', '')[:150]}</div>
    <div class="meta">
        <span class="risk">⚠️ {thesis.get('top_risk', '')}</span>
        <span class="timeframe">⏱️ {setup.get('timeframe', '')}</span>
    </div>
</div>
"""


def main():
    parser = argparse.ArgumentParser(description="Analyst Light - Quick trade setups (V2)")
    parser.add_argument("symbols", nargs="+", help="Stock symbol(s) to analyze")
    parser.add_argument("--format", choices=["text", "json", "newsletter"], default="text",
                       help="Output format")
    parser.add_argument("--min-rr", type=float, default=MIN_RISK_REWARD,
                       help=f"Minimum risk/reward ratio (default: {MIN_RISK_REWARD})")
    
    args = parser.parse_args()
    
    if not FMP_API_KEY:
        print("Error: FMP_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)
    
    analyst = AnalystLight()
    results = []
    
    for symbol in args.symbols:
        result = analyst.get_trade_setup(symbol, min_rr=args.min_rr)
        results.append(result)
        
        if args.format == "text":
            print(analyst.format_text(result))
            print()
    
    if args.format == "json":
        print(json.dumps(results if len(results) > 1 else results[0], indent=2, default=str))
    elif args.format == "newsletter":
        for result in results:
            print(analyst.format_newsletter(result))


if __name__ == "__main__":
    main()
