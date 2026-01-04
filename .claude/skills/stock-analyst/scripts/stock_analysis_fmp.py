#!/usr/bin/env python3
"""
Stock Fundamental Analysis using Financial Modeling Prep (FMP) API
https://site.financialmodelingprep.com/developer/docs/
"""

import requests
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

try:
    from dotenv import load_dotenv
    load_dotenv()  # Load .env file if it exists
except ImportError:
    pass  # python-dotenv not installed, fall back to environment variables

class FMPStockAnalyzer:
    """Financial Modeling Prep API client for stock analysis"""
    
    BASE_URL = "https://financialmodelingprep.com/api/v3"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize FMP client
        
        Args:
            api_key: FMP API key. If not provided, will try to get from FMP_API_KEY env variable
        """
        self.api_key = api_key or os.getenv('FMP_API_KEY')
        if not self.api_key:
            raise ValueError(
                "API key required. Set FMP_API_KEY in .env file, environment variable, or pass as argument.\n"
                "Get your free API key at: https://site.financialmodelingprep.com/\n"
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
    
    def get_profile(self, symbol: str) -> Dict:
        """Get company profile"""
        data = self._make_request(f'profile/{symbol}', {})
        return data[0] if data else {}
    
    def get_quote(self, symbol: str) -> Dict:
        """Get current stock quote"""
        data = self._make_request(f'quote/{symbol}', {})
        return data[0] if data else {}
    
    def get_income_statement(self, symbol: str, period: str = 'annual', limit: int = 5) -> List[Dict]:
        """Get income statements"""
        params = {'period': period, 'limit': limit}
        return self._make_request(f'income-statement/{symbol}', params)
    
    def get_balance_sheet(self, symbol: str, period: str = 'annual', limit: int = 5) -> List[Dict]:
        """Get balance sheets"""
        params = {'period': period, 'limit': limit}
        return self._make_request(f'balance-sheet-statement/{symbol}', params)
    
    def get_cash_flow(self, symbol: str, period: str = 'annual', limit: int = 5) -> List[Dict]:
        """Get cash flow statements"""
        params = {'period': period, 'limit': limit}
        return self._make_request(f'cash-flow-statement/{symbol}', params)
    
    def get_ratios(self, symbol: str, period: str = 'annual', limit: int = 5) -> List[Dict]:
        """Get financial ratios"""
        params = {'period': period, 'limit': limit}
        return self._make_request(f'ratios/{symbol}', params)
    
    def get_key_metrics(self, symbol: str, period: str = 'annual', limit: int = 5) -> List[Dict]:
        """Get key financial metrics"""
        params = {'period': period, 'limit': limit}
        return self._make_request(f'key-metrics/{symbol}', params)
    
    def get_financial_growth(self, symbol: str, period: str = 'annual', limit: int = 5) -> List[Dict]:
        """Get financial growth metrics"""
        params = {'period': period, 'limit': limit}
        return self._make_request(f'financial-growth/{symbol}', params)
    
    def get_dcf(self, symbol: str, period: str = 'annual', limit: int = 5) -> List[Dict]:
        """Get discounted cash flow valuation"""
        params = {'symbol': symbol, 'period': period, 'limit': limit}
        return self._make_request('discounted-cash-flow', params)
    
    def get_enterprise_value(self, symbol: str, period: str = 'annual', limit: int = 5) -> List[Dict]:
        """Get enterprise value"""
        params = {'symbol': symbol, 'period': period, 'limit': limit}
        return self._make_request('enterprise-values', params)
    
    def analyze_stock(self, symbol: str):
        """Perform comprehensive fundamental analysis"""
        print(f"\n{'='*80}")
        print(f"FUNDAMENTAL ANALYSIS: {symbol}")
        print(f"{'='*80}\n")
        
        # Get basic info
        print("📊 COMPANY INFORMATION")
        print("-" * 80)
        try:
            profile = self.get_profile(symbol)
            if profile:
                print(f"Company Name: {profile.get('companyName', 'N/A')}")
                print(f"Symbol: {profile.get('symbol', 'N/A')}")
                print(f"Exchange: {profile.get('exchangeShortName', 'N/A')}")
                print(f"Sector: {profile.get('sector', 'N/A')}")
                print(f"Industry: {profile.get('industry', 'N/A')}")
                print(f"Website: {profile.get('website', 'N/A')}")
                print(f"Description: {profile.get('description', 'N/A')[:200]}...")
                print()
            else:
                print("Could not fetch company profile")
        except Exception as e:
            print(f"Error fetching profile: {e}\n")
        
        # Get current quote
        print("💰 CURRENT MARKET DATA")
        print("-" * 80)
        try:
            quote = self.get_quote(symbol)
            if quote:
                print(f"Current Price: ${quote.get('price', 'N/A')}")
                print(f"Previous Close: ${quote.get('previousClose', 'N/A')}")
                print(f"Market Cap: ${quote.get('marketCap', 0)/1e9:.2f}B" if quote.get('marketCap') else "Market Cap: N/A")
                print(f"Volume: {quote.get('volume', 0):,}" if quote.get('volume') else "Volume: N/A")
                print(f"52 Week High: ${quote.get('yearHigh', 'N/A')}")
                print(f"52 Week Low: ${quote.get('yearLow', 'N/A')}")
                print(f"PE Ratio: {quote.get('pe', 'N/A')}")
                print(f"EPS: ${quote.get('eps', 'N/A')}")
                print()
            else:
                print("Could not fetch quote data")
        except Exception as e:
            print(f"Error fetching quote: {e}\n")
        
        # Get financial ratios
        print("📈 FINANCIAL RATIOS")
        print("-" * 80)
        try:
            ratios = self.get_ratios(symbol, limit=1)
            if ratios and len(ratios) > 0:
                ratio = ratios[0]
                print(f"Current Ratio: {ratio.get('currentRatio', 'N/A')}")
                print(f"Quick Ratio: {ratio.get('quickRatio', 'N/A')}")
                print(f"Debt to Equity: {ratio.get('debtEquityRatio', 'N/A')}")
                print(f"Return on Equity: {ratio.get('returnOnEquity', 'N/A')}")
                print(f"Return on Assets: {ratio.get('returnOnAssets', 'N/A')}")
                print(f"Price to Book: {ratio.get('priceToBookRatio', 'N/A')}")
                print(f"Price to Sales: {ratio.get('priceToSalesRatio', 'N/A')}")
                print(f"PEG Ratio: {ratio.get('pegRatio', 'N/A')}")
                print()
            else:
                print("Could not fetch ratios")
        except Exception as e:
            print(f"Error fetching ratios: {e}\n")
        
        # Get key metrics
        print("💵 KEY FINANCIAL METRICS")
        print("-" * 80)
        try:
            metrics = self.get_key_metrics(symbol, limit=1)
            if metrics and len(metrics) > 0:
                metric = metrics[0]
                print(f"Revenue Per Share: ${metric.get('revenuePerShare', 'N/A')}")
                print(f"Net Income Per Share: ${metric.get('netIncomePerShare', 'N/A')}")
                print(f"Operating Cash Flow Per Share: ${metric.get('operatingCashFlowPerShare', 'N/A')}")
                print(f"Free Cash Flow Per Share: ${metric.get('freeCashFlowPerShare', 'N/A')}")
                print(f"EV/EBITDA: {metric.get('enterpriseValueOverEBITDA', 'N/A')}")
                print(f"EV/Revenue: {metric.get('enterpriseValueOverRevenue', 'N/A')}")
                print()
            else:
                print("Could not fetch key metrics")
        except Exception as e:
            print(f"Error fetching key metrics: {e}\n")
        
        # Get latest income statement
        print("📋 LATEST INCOME STATEMENT")
        print("-" * 80)
        try:
            income_statements = self.get_income_statement(symbol, limit=1)
            if income_statements and len(income_statements) > 0:
                income = income_statements[0]
                print(f"Period: {income.get('date', 'N/A')}")
                print(f"Revenue: ${income.get('revenue', 0)/1e9:.2f}B" if income.get('revenue') else "Revenue: N/A")
                print(f"Gross Profit: ${income.get('grossProfit', 0)/1e9:.2f}B" if income.get('grossProfit') else "Gross Profit: N/A")
                print(f"Operating Income: ${income.get('operatingIncome', 0)/1e9:.2f}B" if income.get('operatingIncome') else "Operating Income: N/A")
                print(f"Net Income: ${income.get('netIncome', 0)/1e9:.2f}B" if income.get('netIncome') else "Net Income: N/A")
                print(f"EPS: ${income.get('eps', 'N/A')}")
                print()
            else:
                print("Could not fetch income statement")
        except Exception as e:
            print(f"Error fetching income statement: {e}\n")
        
        # Get financial growth
        print("📊 FINANCIAL GROWTH")
        print("-" * 80)
        try:
            growth = self.get_financial_growth(symbol, limit=1)
            if growth and len(growth) > 0:
                g = growth[0]
                print(f"Revenue Growth: {g.get('revenueGrowth', 'N/A')}")
                print(f"Net Income Growth: {g.get('netIncomeGrowth', 'N/A')}")
                print(f"EPS Growth: {g.get('epsGrowth', 'N/A')}")
                print(f"Operating Cash Flow Growth: {g.get('operatingCashFlowGrowth', 'N/A')}")
                print()
            else:
                print("Could not fetch growth metrics")
        except Exception as e:
            print(f"Error fetching growth: {e}\n")
        
        print(f"{'='*80}")
        print(f"Analysis completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}\n")


def main():
    """Main function"""
    import sys
    
    # Get API key from environment variable first, then command line
    api_key = os.getenv('FMP_API_KEY')
    
    # Get ticker symbol (first arg if no API key in env, or second arg if API key provided)
    ticker = "NVDA"  # Default
    if len(sys.argv) > 1:
        # If API key not in env and first arg looks like API key (long string), use it
        if not api_key and len(sys.argv[1]) > 20:
            api_key = sys.argv[1]
            if len(sys.argv) > 2:
                ticker = sys.argv[2].upper()
        else:
            # First arg is ticker
            ticker = sys.argv[1].upper()
    
    try:
        analyzer = FMPStockAnalyzer(api_key)
        analyzer.analyze_stock(ticker)
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        print("\nUsage:")
        print("  python3 stock_analysis_fmp.py [API_KEY] [TICKER]")
        print("\nOr set environment variable:")
        print("  export FMP_API_KEY=your_api_key")
        print("  python3 stock_analysis_fmp.py [TICKER]")
        print("\nGet your free API key at: https://site.financialmodelingprep.com/")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

