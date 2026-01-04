#!/usr/bin/env python3
"""
Fundamental Scoring Algorithm
Calculates fundamental strength score (0-10) based on actual financial metrics
"""

from typing import Dict, List, Optional
import math

class FundamentalScorer:
    """
    Calculates fundamental strength score from actual financial data
    Score components:
    - Profitability (30%): ROE, ROA, profit margins
    - Growth (30%): Revenue growth, earnings growth
    - Financial Health (20%): Debt levels, liquidity, cash flow
    - Valuation (20%): P/E relative to growth, sector comparison
    """
    
    def __init__(self):
        self.weights = {
            'profitability': 0.30,
            'growth': 0.30,
            'financial_health': 0.20,
            'valuation': 0.20
        }
    
    def calculate_profitability_score(self, ratios: List[Dict], income: List[Dict]) -> float:
        """
        Calculate profitability score (0-10) based on ROE, ROA, and margins
        
        Args:
            ratios: Financial ratios data
            income: Income statement data
        
        Returns:
            Score from 0-10
        """
        if not ratios or len(ratios) == 0:
            return 5.0  # Neutral if no data
        
        ratio = ratios[0]
        roe = ratio.get('returnOnEquity', 0)
        roa = ratio.get('returnOnAssets', 0)
        
        # Get profit margin from income statement
        profit_margin = 0.0
        if income and len(income) > 0:
            revenue = income[0].get('revenue', 0)
            net_income = income[0].get('netIncome', 0)
            if revenue > 0:
                profit_margin = net_income / revenue
        
        # Score ROE (0-4 points)
        # Excellent: >25%, Good: 15-25%, Moderate: 10-15%, Poor: <10%
        roe_score = 0.0
        if roe > 0.25:
            roe_score = 4.0
        elif roe > 0.15:
            roe_score = 3.0
        elif roe > 0.10:
            roe_score = 2.0
        elif roe > 0.05:
            roe_score = 1.0
        else:
            roe_score = 0.0
        
        # Score ROA (0-3 points)
        # Excellent: >15%, Good: 10-15%, Moderate: 5-10%, Poor: <5%
        roa_score = 0.0
        if roa > 0.15:
            roa_score = 3.0
        elif roa > 0.10:
            roa_score = 2.0
        elif roa > 0.05:
            roa_score = 1.0
        else:
            roa_score = 0.0
        
        # Score Profit Margin (0-3 points)
        # Excellent: >20%, Good: 10-20%, Moderate: 5-10%, Poor: <5%
        margin_score = 0.0
        if profit_margin > 0.20:
            margin_score = 3.0
        elif profit_margin > 0.10:
            margin_score = 2.0
        elif profit_margin > 0.05:
            margin_score = 1.0
        else:
            margin_score = 0.0
        
        # Normalize to 0-10 scale
        total_score = roe_score + roa_score + margin_score
        normalized_score = (total_score / 10.0) * 10.0
        
        return min(10.0, max(0.0, normalized_score))
    
    def calculate_growth_score(self, growth: List[Dict]) -> float:
        """
        Calculate growth score (0-10) based on revenue and earnings growth
        
        Args:
            growth: Financial growth data
        
        Returns:
            Score from 0-10
        """
        if not growth or len(growth) == 0:
            return 5.0  # Neutral if no data
        
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
        
        # Score Revenue Growth (0-5 points)
        # Excellent: >20%, Good: 10-20%, Moderate: 5-10%, Slow: 0-5%, Negative: <0%
        rev_score = 0.0
        if rev_pct > 20:
            rev_score = 5.0
        elif rev_pct > 10:
            rev_score = 4.0
        elif rev_pct > 5:
            rev_score = 3.0
        elif rev_pct > 0:
            rev_score = 2.0
        elif rev_pct > -5:
            rev_score = 1.0
        else:
            rev_score = 0.0
        
        # Score Net Income Growth (0-5 points)
        # Excellent: >30%, Good: 15-30%, Moderate: 5-15%, Slow: 0-5%, Negative: <0%
        ni_score = 0.0
        if ni_pct > 30:
            ni_score = 5.0
        elif ni_pct > 15:
            ni_score = 4.0
        elif ni_pct > 5:
            ni_score = 3.0
        elif ni_pct > 0:
            ni_score = 2.0
        elif ni_pct > -10:
            ni_score = 1.0
        else:
            ni_score = 0.0
        
        # Normalize to 0-10 scale
        total_score = rev_score + ni_score
        normalized_score = (total_score / 10.0) * 10.0
        
        return min(10.0, max(0.0, normalized_score))
    
    def calculate_financial_health_score(self, ratios: List[Dict]) -> float:
        """
        Calculate financial health score (0-10) based on debt, liquidity, and cash flow
        
        Args:
            ratios: Financial ratios data
        
        Returns:
            Score from 0-10
        """
        if not ratios or len(ratios) == 0:
            return 5.0  # Neutral if no data
        
        ratio = ratios[0]
        debt_equity = ratio.get('debtEquityRatio', 0)
        current_ratio = ratio.get('currentRatio', 0)
        
        # Score Debt-to-Equity (0-5 points)
        # Excellent: <0.3, Good: 0.3-0.5, Moderate: 0.5-1.0, High: >1.0
        debt_score = 0.0
        if debt_equity < 0.3:
            debt_score = 5.0
        elif debt_equity < 0.5:
            debt_score = 4.0
        elif debt_equity < 1.0:
            debt_score = 3.0
        elif debt_equity < 1.5:
            debt_score = 2.0
        else:
            debt_score = 1.0
        
        # Score Current Ratio (0-5 points)
        # Excellent: >2.0, Good: 1.5-2.0, Moderate: 1.0-1.5, Poor: <1.0
        liquidity_score = 0.0
        if current_ratio > 2.0:
            liquidity_score = 5.0
        elif current_ratio > 1.5:
            liquidity_score = 4.0
        elif current_ratio > 1.0:
            liquidity_score = 3.0
        elif current_ratio > 0.8:
            liquidity_score = 2.0
        else:
            liquidity_score = 1.0
        
        # Normalize to 0-10 scale
        total_score = debt_score + liquidity_score
        normalized_score = (total_score / 10.0) * 10.0
        
        return min(10.0, max(0.0, normalized_score))
    
    def calculate_valuation_score(self, pe_ratio: float, peg_ratio: Optional[float], 
                                  sector_premium: float, valuation_score: Optional[float]) -> float:
        """
        Calculate valuation score (0-10) - higher score = better value
        
        Args:
            pe_ratio: P/E ratio
            peg_ratio: PEG ratio (optional)
            sector_premium: Premium to sector average (as multiplier, e.g., 1.5 = 50% premium)
            valuation_score: Pre-calculated valuation score (optional)
        
        Returns:
            Score from 0-10 (inverted - lower valuation = higher score)
        """
        # If we have a pre-calculated valuation score, use it (inverted)
        if valuation_score is not None:
            # Valuation score is typically 0-10 where higher = better value
            # But for fundamental score, we want lower valuation = higher score
            # So we'll use it as-is since it's already oriented correctly
            return valuation_score
        
        # Calculate from components
        score = 5.0  # Start neutral
        
        # Adjust for PEG ratio if available
        if peg_ratio is not None and isinstance(peg_ratio, (int, float)):
            if peg_ratio < 0.5:
                score += 2.0  # Excellent value
            elif peg_ratio < 1.0:
                score += 1.0  # Good value
            elif peg_ratio < 1.5:
                score += 0.0  # Fair
            elif peg_ratio < 2.0:
                score -= 1.0  # Expensive
            else:
                score -= 2.0  # Very expensive
        
        # Adjust for sector premium
        if sector_premium > 2.0:  # >100% premium
            score -= 3.0
        elif sector_premium > 1.5:  # >50% premium
            score -= 2.0
        elif sector_premium > 1.2:  # >20% premium
            score -= 1.0
        elif sector_premium < 0.8:  # >20% discount
            score += 1.0
        elif sector_premium < 0.6:  # >40% discount
            score += 2.0
        
        # Adjust for P/E ratio (if extremely high)
        if pe_ratio > 100:
            score -= 2.0
        elif pe_ratio > 50:
            score -= 1.0
        elif pe_ratio > 30:
            score -= 0.5
        
        return min(10.0, max(0.0, score))
    
    def calculate_fundamental_score(self, ratios: List[Dict], growth: List[Dict], 
                                   income: List[Dict], pe_ratio: float,
                                   peg_ratio: Optional[float] = None,
                                   sector_premium: float = 1.0,
                                   valuation_score: Optional[float] = None) -> Dict:
        """
        Calculate overall fundamental score from all components
        
        Returns:
            Dict with component scores and overall score
        """
        profitability_score = self.calculate_profitability_score(ratios, income)
        growth_score = self.calculate_growth_score(growth)
        health_score = self.calculate_financial_health_score(ratios)
        valuation_score_calc = self.calculate_valuation_score(
            pe_ratio, peg_ratio, sector_premium, valuation_score
        )
        
        # Weighted average
        overall_score = (
            profitability_score * self.weights['profitability'] +
            growth_score * self.weights['growth'] +
            health_score * self.weights['financial_health'] +
            valuation_score_calc * self.weights['valuation']
        )
        
        return {
            'overall_score': round(overall_score, 2),
            'profitability_score': round(profitability_score, 2),
            'growth_score': round(growth_score, 2),
            'financial_health_score': round(health_score, 2),
            'valuation_score': round(valuation_score_calc, 2),
            'components': {
                'profitability': {
                    'score': profitability_score,
                    'weight': self.weights['profitability']
                },
                'growth': {
                    'score': growth_score,
                    'weight': self.weights['growth']
                },
                'financial_health': {
                    'score': health_score,
                    'weight': self.weights['financial_health']
                },
                'valuation': {
                    'score': valuation_score_calc,
                    'weight': self.weights['valuation']
                }
            }
        }
    
    def get_fundamental_strength_label(self, score: float) -> str:
        """Get human-readable label for fundamental score"""
        if score >= 8.0:
            return "Exceptional"
        elif score >= 7.0:
            return "Strong"
        elif score >= 6.0:
            return "Good"
        elif score >= 5.0:
            return "Moderate"
        elif score >= 4.0:
            return "Weak"
        else:
            return "Poor"

