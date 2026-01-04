#!/usr/bin/env python3
"""
Trajectory Analyzer
Analyzes improvement/deterioration trends by comparing recent quarters
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime


def analyze_trajectory(fundamental_data: Dict) -> Dict[str, any]:
    """
    Analyze trajectory by comparing recent quarters
    
    Args:
        fundamental_data: Dictionary containing income, ratios, growth data
        
    Returns:
        Dict with trajectory analysis including trends and momentum
    """
    trajectory = {
        'revenue_trend': 'unknown',
        'profitability_trend': 'unknown',
        'margin_trend': 'unknown',
        'momentum': 'unknown',
        'trajectory_score': None,
        'quarters_compared': [],
        'key_improvements': [],
        'key_deteriorations': []
    }
    
    # Get multiple quarters for comparison (if available)
    income = fundamental_data.get('income', [])
    growth = fundamental_data.get('growth', [])
    ratios = fundamental_data.get('ratios', [])
    
    # Try to get multiple quarters (up to 4)
    # Note: This would need to be enhanced to fetch multiple periods
    if income and len(income) > 0:
        current_income = income[0]
        current_revenue = current_income.get('revenue')
        current_net_income = current_income.get('netIncome')
        current_date = current_income.get('date') or current_income.get('calendarDate')
        
        if current_date:
            trajectory['quarters_compared'].append({
                'date': current_date[:10] if isinstance(current_date, str) else str(current_date),
                'revenue': current_revenue,
                'net_income': current_net_income
            })
    
    # Analyze growth trends
    if growth and len(growth) > 0:
        current_growth = growth[0]
        revenue_growth = current_growth.get('revenueGrowth')
        net_income_growth = current_growth.get('netIncomeGrowth')
        
        # Determine revenue trend
        if revenue_growth is not None:
            if isinstance(revenue_growth, (int, float)):
                if revenue_growth > 1:
                    revenue_growth_pct = (revenue_growth - 1) * 100
                else:
                    revenue_growth_pct = revenue_growth * 100
                
                if revenue_growth_pct > 10:
                    trajectory['revenue_trend'] = 'strong_growth'
                elif revenue_growth_pct > 0:
                    trajectory['revenue_trend'] = 'growing'
                elif revenue_growth_pct > -10:
                    trajectory['revenue_trend'] = 'declining'
                else:
                    trajectory['revenue_trend'] = 'sharp_decline'
        
        # Determine profitability trend
        if net_income_growth is not None:
            if isinstance(net_income_growth, (int, float)):
                if net_income_growth > 1:
                    ni_growth_pct = (net_income_growth - 1) * 100
                else:
                    ni_growth_pct = net_income_growth * 100
                
                # Check if improving from losses
                if ni_growth_pct > 50 and current_income and current_income.get('netIncome', 0) < 0:
                    trajectory['profitability_trend'] = 'improving_from_losses'
                    trajectory['key_improvements'].append('Net income improving from losses')
                elif ni_growth_pct > 20:
                    trajectory['profitability_trend'] = 'strong_growth'
                elif ni_growth_pct > 0:
                    trajectory['profitability_trend'] = 'growing'
                elif ni_growth_pct > -20:
                    trajectory['profitability_trend'] = 'declining'
                else:
                    trajectory['profitability_trend'] = 'sharp_decline'
                    trajectory['key_deteriorations'].append('Net income declining significantly')
    
    # Analyze margin trends from ratios
    if ratios and len(ratios) > 0:
        current_ratios = ratios[0]
        profit_margin = current_ratios.get('netProfitMargin')
        
        if profit_margin is not None:
            if profit_margin > 0.1:
                trajectory['margin_trend'] = 'healthy'
            elif profit_margin > 0:
                trajectory['margin_trend'] = 'low_but_positive'
            elif profit_margin > -0.1:
                trajectory['margin_trend'] = 'narrow_losses'
            else:
                trajectory['margin_trend'] = 'significant_losses'
    
    # Determine overall momentum
    improvements = len(trajectory['key_improvements'])
    deteriorations = len(trajectory['key_deteriorations'])
    
    if trajectory['revenue_trend'] in ['strong_growth', 'growing'] and \
       trajectory['profitability_trend'] in ['improving_from_losses', 'strong_growth', 'growing']:
        trajectory['momentum'] = 'improving'
    elif trajectory['revenue_trend'] in ['declining', 'sharp_decline'] and \
         trajectory['profitability_trend'] in ['declining', 'sharp_decline']:
        trajectory['momentum'] = 'deteriorating'
    elif improvements > deteriorations:
        trajectory['momentum'] = 'improving'
    elif deteriorations > improvements:
        trajectory['momentum'] = 'deteriorating'
    else:
        trajectory['momentum'] = 'stable'
    
    # Calculate trajectory score (0-10, higher = better trajectory)
    score = 5.0  # Start neutral
    
    if trajectory['momentum'] == 'improving':
        score += 2.0
    elif trajectory['momentum'] == 'deteriorating':
        score -= 2.0
    
    if trajectory['revenue_trend'] == 'strong_growth':
        score += 1.5
    elif trajectory['revenue_trend'] == 'growing':
        score += 0.5
    elif trajectory['revenue_trend'] == 'declining':
        score -= 0.5
    elif trajectory['revenue_trend'] == 'sharp_decline':
        score -= 1.5
    
    if trajectory['profitability_trend'] == 'improving_from_losses':
        score += 1.0  # Positive signal for turnaround
    elif trajectory['profitability_trend'] == 'strong_growth':
        score += 1.5
    elif trajectory['profitability_trend'] == 'growing':
        score += 0.5
    elif trajectory['profitability_trend'] == 'declining':
        score -= 0.5
    elif trajectory['profitability_trend'] == 'sharp_decline':
        score -= 1.5
    
    trajectory['trajectory_score'] = max(0, min(10, round(score, 1)))
    
    return trajectory


def get_trajectory_summary(trajectory: Dict) -> str:
    """
    Generate human-readable trajectory summary
    
    Args:
        trajectory: Output from analyze_trajectory()
        
    Returns:
        Formatted summary string
    """
    momentum = trajectory.get('momentum', 'unknown')
    revenue_trend = trajectory.get('revenue_trend', 'unknown')
    profitability_trend = trajectory.get('profitability_trend', 'unknown')
    trajectory_score = trajectory.get('trajectory_score')
    
    summary_parts = []
    
    if momentum == 'improving':
        summary_parts.append("**Improving Trajectory:** Company shows positive momentum with improving fundamentals.")
    elif momentum == 'deteriorating':
        summary_parts.append("**Deteriorating Trajectory:** Company shows negative momentum with declining fundamentals.")
    elif momentum == 'stable':
        summary_parts.append("**Stable Trajectory:** Company shows stable fundamentals without significant changes.")
    else:
        summary_parts.append("**Trajectory:** Unable to determine clear trend from available data.")
    
    # Add trend details
    if revenue_trend == 'strong_growth':
        summary_parts.append("Revenue is growing strongly.")
    elif revenue_trend == 'growing':
        summary_parts.append("Revenue is growing.")
    elif revenue_trend == 'declining':
        summary_parts.append("Revenue is declining.")
    elif revenue_trend == 'sharp_decline':
        summary_parts.append("Revenue is declining sharply.")
    
    if profitability_trend == 'improving_from_losses':
        summary_parts.append("Profitability is improving from losses (turnaround signal).")
    elif profitability_trend == 'strong_growth':
        summary_parts.append("Profitability is growing strongly.")
    elif profitability_trend == 'growing':
        summary_parts.append("Profitability is growing.")
    elif profitability_trend == 'declining':
        summary_parts.append("Profitability is declining.")
    elif profitability_trend == 'sharp_decline':
        summary_parts.append("Profitability is declining sharply.")
    
    # Add improvements/deteriorations
    improvements = trajectory.get('key_improvements', [])
    deteriorations = trajectory.get('key_deteriorations', [])
    
    if improvements:
        summary_parts.append(f"Key improvements: {', '.join(improvements)}")
    if deteriorations:
        summary_parts.append(f"Key concerns: {', '.join(deteriorations)}")
    
    if trajectory_score is not None:
        summary_parts.append(f"Trajectory score: {trajectory_score}/10")
    
    return ". ".join(summary_parts) + "."
