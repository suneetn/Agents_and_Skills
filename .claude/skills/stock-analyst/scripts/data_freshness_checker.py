#!/usr/bin/env python3
"""
Data Freshness Checker
Checks if financial data is recent enough for accurate analysis
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple


def check_data_freshness(fundamental_data: Dict) -> Dict[str, any]:
    """
    Check freshness of fundamental data
    
    Args:
        fundamental_data: Dictionary containing profile, ratios, income, growth data
        
    Returns:
        Dict with freshness status, warnings, and data periods
    """
    current_date = datetime.now()
    warnings = []
    data_periods = {}
    is_stale = False
    
    # Check income statement date
    income = fundamental_data.get('income', [])
    if income and len(income) > 0:
        income_date_str = income[0].get('date') or income[0].get('calendarDate')
        if income_date_str:
            try:
                income_date = datetime.strptime(income_date_str[:10], '%Y-%m-%d')
                days_old = (current_date - income_date).days
                data_periods['income'] = {
                    'date': income_date_str[:10],
                    'days_old': days_old,
                    'period': 'annual' if 'annual' in str(income_date_str).lower() else 'quarterly'
                }
                
                if days_old > 90:
                    is_stale = True
                    warnings.append(f"Income statement data is {days_old} days old (as of {income_date_str[:10]})")
            except (ValueError, TypeError):
                pass
    
    # Check ratios date
    ratios = fundamental_data.get('ratios', [])
    if ratios and len(ratios) > 0:
        ratio_date_str = ratios[0].get('date') or ratios[0].get('calendarDate')
        if ratio_date_str:
            try:
                ratio_date = datetime.strptime(ratio_date_str[:10], '%Y-%m-%d')
                days_old = (current_date - ratio_date).days
                data_periods['ratios'] = {
                    'date': ratio_date_str[:10],
                    'days_old': days_old,
                    'period': 'annual' if 'annual' in str(ratio_date_str).lower() else 'quarterly'
                }
                
                if days_old > 90:
                    is_stale = True
                    if not any('ratios' in w for w in warnings):
                        warnings.append(f"Ratios data is {days_old} days old (as of {ratio_date_str[:10]})")
            except (ValueError, TypeError):
                pass
    
    # Check growth data date
    growth = fundamental_data.get('growth', [])
    if growth and len(growth) > 0:
        growth_date_str = growth[0].get('date') or growth[0].get('calendarDate')
        if growth_date_str:
            try:
                growth_date = datetime.strptime(growth_date_str[:10], '%Y-%m-%d')
                days_old = (current_date - growth_date).days
                data_periods['growth'] = {
                    'date': growth_date_str[:10],
                    'days_old': days_old,
                    'period': 'annual' if 'annual' in str(growth_date_str).lower() else 'quarterly'
                }
                
                if days_old > 90:
                    is_stale = True
                    if not any('growth' in w for w in warnings):
                        warnings.append(f"Growth data is {days_old} days old (as of {growth_date_str[:10]})")
            except (ValueError, TypeError):
                pass
    
    # Determine primary data period
    primary_period = 'unknown'
    if data_periods:
        periods = [d.get('period') for d in data_periods.values() if d.get('period')]
        if periods:
            # Prefer quarterly if available
            if 'quarterly' in periods:
                primary_period = 'quarterly'
            else:
                primary_period = periods[0]
    
    # Get most recent date
    most_recent_date = None
    most_recent_days = None
    if data_periods:
        dates = [(d.get('date'), d.get('days_old')) for d in data_periods.values() if d.get('date')]
        if dates:
            most_recent = min(dates, key=lambda x: x[1] if x[1] else 999)
            most_recent_date = most_recent[0]
            most_recent_days = most_recent[1]
    
    return {
        'is_stale': is_stale,
        'warnings': warnings,
        'data_periods': data_periods,
        'primary_period': primary_period,
        'most_recent_date': most_recent_date,
        'most_recent_days_old': most_recent_days,
        'status': 'stale' if is_stale else 'fresh' if most_recent_days and most_recent_days <= 30 else 'moderate'
    }


def get_data_freshness_summary(freshness_data: Dict) -> str:
    """
    Generate human-readable freshness summary
    
    Args:
        freshness_data: Output from check_data_freshness()
        
    Returns:
        Formatted summary string
    """
    if not freshness_data.get('most_recent_date'):
        return "⚠️ Data freshness could not be determined"
    
    days_old = freshness_data.get('most_recent_days_old', 0)
    most_recent_date = freshness_data.get('most_recent_date')
    primary_period = freshness_data.get('primary_period', 'unknown')
    
    if days_old > 90:
        return f"⚠️ **STALE DATA WARNING:** Most recent data is {days_old} days old (as of {most_recent_date}). Analysis may not reflect recent developments. Consider using more recent quarterly data if available."
    elif days_old > 60:
        return f"⚠️ **MODERATE FRESHNESS:** Most recent data is {days_old} days old (as of {most_recent_date}). Consider verifying with latest quarterly data."
    elif days_old > 30:
        return f"✓ Data is {days_old} days old (as of {most_recent_date}). {primary_period.capitalize()} data."
    else:
        return f"✓ Data is fresh ({days_old} days old, as of {most_recent_date}). {primary_period.capitalize()} data."


def prioritize_quarterly_data(fundamental_data: Dict) -> Dict:
    """
    Attempt to fetch quarterly data if annual data is stale
    
    Note: This is a placeholder - actual implementation would need to
    modify the data fetching logic in workflow_steps.py
    
    Args:
        fundamental_data: Current fundamental data
        
    Returns:
        Updated fundamental_data with quarterly data if available
    """
    # This would need to be implemented by modifying workflow_steps.py
    # to fetch quarterly data when annual data is stale
    return fundamental_data



