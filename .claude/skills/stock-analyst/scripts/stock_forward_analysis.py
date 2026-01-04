#!/usr/bin/env python3
"""
Stock Forward-Looking Analysis
Provides forward-looking data including analyst estimates, earnings calendar,
and upcoming catalysts.
"""

import requests
import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class ForwardAnalysis:
    """
    Analyzes forward-looking data for stocks
    """
    
    BASE_URL = "https://financialmodelingprep.com/api/v3"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('FMP_API_KEY')
        if not self.api_key:
            raise ValueError(
                "FMP_API_KEY required. Set it in .env file or environment variable.\n"
                "Create a .env file with: FMP_API_KEY=your_key"
            )
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
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
    
    def get_analyst_estimates(self, symbol: str) -> Dict:
        """Get analyst earnings estimates"""
        try:
            data = self._make_request(f'analyst-estimates/{symbol}', {'limit': 4})
            if data and len(data) > 0:
                # Get most recent estimate
                latest = data[0]
                return {
                    'available': True,
                    'estimated_eps': latest.get('estimatedEps'),
                    'estimated_revenue': latest.get('estimatedRevenue'),
                    'estimated_revenue_low': latest.get('estimatedRevenueLow'),
                    'estimated_revenue_high': latest.get('estimatedRevenueHigh'),
                    'estimated_eps_low': latest.get('estimatedEpsLow'),
                    'estimated_eps_high': latest.get('estimatedEpsHigh'),
                    'number_of_analysts': latest.get('numberOfAnalystEstimates'),
                    'period': latest.get('date'),
                    'all_estimates': data[:4]  # Last 4 quarters
                }
            else:
                return {'available': False, 'reason': 'No estimates found'}
        except Exception as e:
            return {'available': False, 'reason': f'Error fetching estimates: {e}'}
    
    def get_earnings_calendar(self, symbol: str) -> Dict:
        """Get earnings calendar for upcoming earnings"""
        try:
            # Get earnings calendar (next 3 months)
            data = self._make_request('earning_calendar', {'from': datetime.now().strftime('%Y-%m-%d'), 'to': (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')})
            
            # Filter for our symbol
            symbol_earnings = [e for e in data if isinstance(e, dict) and e.get('symbol') == symbol]
            
            if symbol_earnings and len(symbol_earnings) > 0:
                next_earning = symbol_earnings[0]
                return {
                    'available': True,
                    'next_earnings_date': next_earning.get('date'),
                    'next_earnings_time': next_earning.get('time'),  # Before/After market
                    'estimated_eps': next_earning.get('epsEstimated'),
                    'revenue_estimated': next_earning.get('revenueEstimated'),
                    'all_upcoming': symbol_earnings[:4]  # Next 4 earnings
                }
            else:
                return {'available': False, 'reason': 'No upcoming earnings found'}
        except Exception as e:
            return {'available': False, 'reason': f'Error fetching earnings calendar: {e}'}
    
    def get_price_targets(self, symbol: str) -> Dict:
        """Get analyst price targets"""
        try:
            data = self._make_request(f'price-target/{symbol}')
            if data and len(data) > 0:
                latest = data[0]
                return {
                    'available': True,
                    'target_high': latest.get('targetHigh'),
                    'target_low': latest.get('targetLow'),
                    'target_mean': latest.get('targetMean'),
                    'target_median': latest.get('targetMedian'),
                    'number_of_analysts': latest.get('numberOfAnalysts'),
                    'current_price': latest.get('currentPrice'),
                    'upside_potential': ((latest.get('targetMean', 0) - latest.get('currentPrice', 0)) / latest.get('currentPrice', 1) * 100) if latest.get('currentPrice') else None
                }
            else:
                return {'available': False, 'reason': 'No price targets found'}
        except Exception as e:
            return {'available': False, 'reason': f'Error fetching price targets: {e}'}
    
    def identify_catalysts(self, symbol: str, profile: Dict = None) -> Dict:
        """Identify upcoming catalysts (earnings, product launches, etc.)"""
        catalysts = []
        
        # Get earnings calendar
        earnings = self.get_earnings_calendar(symbol)
        if earnings.get('available'):
            catalysts.append({
                'type': 'Earnings',
                'date': earnings.get('next_earnings_date'),
                'description': f"Q{earnings.get('next_earnings_time', 'TBD')} Earnings Report",
                'impact': 'High',
                'estimated_eps': earnings.get('estimated_eps')
            })
        
        # Get price targets for potential upgrades/downgrades
        price_targets = self.get_price_targets(symbol)
        if price_targets.get('available') and price_targets.get('upside_potential'):
            if price_targets['upside_potential'] > 20:
                catalysts.append({
                    'type': 'Analyst Coverage',
                    'description': f"Analyst consensus target suggests {price_targets['upside_potential']:.1f}% upside potential",
                    'impact': 'Medium',
                    'target_mean': price_targets.get('target_mean')
                })
        
        return {
            'catalysts': catalysts,
            'count': len(catalysts),
            'high_impact_count': len([c for c in catalysts if c.get('impact') == 'High'])
        }
    
    def analyze_forward_looking(self, symbol: str, current_price: float = None) -> Dict:
        """Comprehensive forward-looking analysis"""
        print(f"\n{'='*80}")
        print(f"FORWARD-LOOKING ANALYSIS: {symbol}")
        print(f"{'='*80}\n")
        
        # Get analyst estimates
        print("📊 ANALYST ESTIMATES")
        print("-" * 80)
        estimates = self.get_analyst_estimates(symbol)
        if estimates.get('available'):
            print(f"Next Period: {estimates.get('period', 'N/A')}")
            print(f"Estimated EPS: ${estimates.get('estimated_eps', 'N/A')}")
            if estimates.get('estimated_eps_low') and estimates.get('estimated_eps_high'):
                print(f"EPS Range: ${estimates.get('estimated_eps_low')} - ${estimates.get('estimated_eps_high')}")
            print(f"Estimated Revenue: ${estimates.get('estimated_revenue', 0)/1e9:.2f}B" if estimates.get('estimated_revenue') else "Estimated Revenue: N/A")
            print(f"Number of Analysts: {estimates.get('number_of_analysts', 'N/A')}")
        else:
            print(f"Analyst Estimates: {estimates.get('reason', 'Not available')}")
        print()
        
        # Get earnings calendar
        print("📅 EARNINGS CALENDAR")
        print("-" * 80)
        earnings = self.get_earnings_calendar(symbol)
        if earnings.get('available'):
            print(f"Next Earnings Date: {earnings.get('next_earnings_date', 'N/A')}")
            print(f"Earnings Time: {earnings.get('next_earnings_time', 'N/A')}")
            if earnings.get('estimated_eps'):
                print(f"Estimated EPS: ${earnings.get('estimated_eps', 'N/A')}")
            if earnings.get('revenue_estimated'):
                print(f"Estimated Revenue: ${earnings.get('revenue_estimated', 0)/1e9:.2f}B" if earnings.get('revenue_estimated') else "Estimated Revenue: N/A")
        else:
            print(f"Earnings Calendar: {earnings.get('reason', 'Not available')}")
        print()
        
        # Get price targets
        print("🎯 ANALYST PRICE TARGETS")
        print("-" * 80)
        price_targets = self.get_price_targets(symbol)
        if price_targets.get('available'):
            if current_price:
                print(f"Current Price: ${current_price:.2f}")
            print(f"Target Mean: ${price_targets.get('target_mean', 'N/A')}")
            print(f"Target High: ${price_targets.get('target_high', 'N/A')}")
            print(f"Target Low: ${price_targets.get('target_low', 'N/A')}")
            print(f"Target Median: ${price_targets.get('target_median', 'N/A')}")
            print(f"Number of Analysts: {price_targets.get('number_of_analysts', 'N/A')}")
            if price_targets.get('upside_potential'):
                print(f"Upside Potential: {price_targets['upside_potential']:+.1f}%")
        else:
            print(f"Price Targets: {price_targets.get('reason', 'Not available')}")
        print()
        
        # Identify catalysts
        print("🚀 UPCOMING CATALYSTS")
        print("-" * 80)
        catalysts = self.identify_catalysts(symbol)
        if catalysts['count'] > 0:
            for i, catalyst in enumerate(catalysts['catalysts'], 1):
                print(f"{i}. {catalyst['type']}: {catalyst['description']}")
                if catalyst.get('date'):
                    print(f"   Date: {catalyst['date']}")
                print(f"   Impact: {catalyst['impact']}")
        else:
            print("No major catalysts identified in next 90 days")
        print()
        
        print(f"{'='*80}")
        print(f"Analysis completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}\n")
        
        return {
            'analyst_estimates': estimates,
            'earnings_calendar': earnings,
            'price_targets': price_targets,
            'catalysts': catalysts
        }


def main():
    """Test the forward analysis"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 stock_forward_analysis.py <SYMBOL>")
        print("\nExample:")
        print("  python3 stock_forward_analysis.py NVDA")
        sys.exit(1)
    
    symbol = sys.argv[1].upper()
    
    try:
        analyzer = ForwardAnalysis()
        analyzer.analyze_forward_looking(symbol)
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

