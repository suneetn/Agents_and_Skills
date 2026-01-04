#!/usr/bin/env python3
"""
Stock Screener
Screens stocks based on technical and fundamental criteria using FMP API.
Returns ranked list of stocks matching specified criteria.
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import Dict, List, Optional, Any
import time

# Add script directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

try:
    import requests
except ImportError:
    print("Error: requests library required. Install with: pip install requests")
    sys.exit(1)

from screen_definitions import SCREEN_DEFINITIONS, get_screen_criteria, is_growth_screen, use_full_rating


class StockScreener:
    """Screen stocks based on technical and fundamental criteria."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize screener with FMP API key."""
        self.api_key = api_key or os.environ.get('FMP_API_KEY')
        if not self.api_key:
            raise ValueError("FMP_API_KEY environment variable required")
        self.base_url = "https://financialmodelingprep.com/api/v3"
        self.cache = {}
        self.cache_duration = 300  # 5 minutes
        self.api_calls = 0  # Track API calls for performance monitoring
        self.start_time = None
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Any:
        """Make API request with error handling."""
        url = f"{self.base_url}/{endpoint}"
        params = params or {}
        params['apikey'] = self.api_key
        self.api_calls += 1  # Track API calls
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            print(f"Warning: API timeout for {endpoint}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Warning: API error for {endpoint}: {e}")
            return None
    
    def get_fmp_screener_results(
        self,
        sector: Optional[str] = None,
        min_market_cap: float = 1_000_000_000,
        limit: int = 100,
        exchange: str = None
    ) -> List[Dict]:
        """
        Use FMP's native stock-screener endpoint for server-side filtering.
        Much faster than client-side filtering.
        """
        params = {
            'marketCapMoreThan': int(min_market_cap),
            'isActivelyTrading': 'true',
            'isEtf': 'false',
            'isFund': 'false',
            'country': 'US',
            'limit': limit
        }
        
        if sector:
            params['sector'] = sector
        
        if exchange:
            params['exchange'] = exchange
        
        data = self._make_request("stock-screener", params)
        
        # Filter out non-US exchanges (like .BA Buenos Aires)
        if data:
            data = [
                item for item in data 
                if item.get('exchangeShortName') in ['NYSE', 'NASDAQ', 'AMEX', None]
                and '.' not in item.get('symbol', '')  # Filter symbols with dots (foreign)
            ]
        
        return data if data else []
    
    def get_stock_rating(self, symbol: str) -> Optional[Dict]:
        """Get FMP's calculated rating for a stock."""
        data = self._make_request(f"rating/{symbol}")
        if data and len(data) > 0:
            return data[0]
        return None
    
    def get_bulk_ratings(self, symbols: List[str]) -> Dict[str, Dict]:
        """Get ratings for multiple symbols (individual calls, but only for top N)."""
        ratings = {}
        for symbol in symbols:
            rating = self.get_stock_rating(symbol)
            if rating:
                ratings[symbol] = rating
        return ratings
    
    def get_growth_data(self, symbol: str) -> Optional[Dict]:
        """Get growth metrics for a stock."""
        data = self._make_request(f"financial-growth/{symbol}", {"limit": 1})
        if data and len(data) > 0:
            return data[0]
        return None
    
    def get_bulk_growth_data(self, symbols: List[str]) -> Dict[str, Dict]:
        """Get growth data for multiple symbols."""
        growth_data = {}
        for symbol in symbols:
            data = self.get_growth_data(symbol)
            if data:
                growth_data[symbol] = data
        return growth_data
    
    # ==================== RESEARCH ENDPOINTS ====================
    
    def get_stock_news(self, symbol: str, limit: int = 5) -> List[Dict]:
        """Get recent news for a stock."""
        data = self._make_request("stock_news", {"tickers": symbol, "limit": limit})
        if data:
            from datetime import datetime as dt
            results = []
            for item in data[:limit]:
                raw_date = item.get("publishedDate", "")[:10] if item.get("publishedDate") else ""
                # Format date as "Jan 3" style
                try:
                    parsed = dt.strptime(raw_date, "%Y-%m-%d")
                    formatted_date = parsed.strftime("%b %d")  # e.g., "Jan 03"
                except:
                    formatted_date = raw_date
                
                results.append({
                    "title": item.get("title", ""),
                    "source": item.get("site", ""),
                    "date": formatted_date,
                    "url": item.get("url", ""),
                    "summary": item.get("text", "")[:200] + "..." if item.get("text") else ""
                })
            return results
        return []
    
    def get_earnings_calendar(self, symbol: str) -> Optional[Dict]:
        """Get upcoming earnings date for a stock."""
        data = self._make_request(f"earning_calendar", {"symbol": symbol})
        if data and len(data) > 0:
            # Find the next upcoming earnings
            from datetime import datetime as dt
            today = dt.now().date()
            
            # Sort by date and find next upcoming
            upcoming = []
            for item in data:
                try:
                    raw_date = item.get("date", "")
                    if not raw_date:
                        continue
                    earnings_date = dt.strptime(raw_date, "%Y-%m-%d").date()
                    if earnings_date >= today:
                        upcoming.append((earnings_date, item))
                except:
                    continue
            
            if upcoming:
                # Sort by date and take earliest
                upcoming.sort(key=lambda x: x[0])
                earnings_date, item = upcoming[0]
                raw_date = item.get("date", "")
                days_until = (earnings_date - today).days
                
                # Format date as human-readable
                if days_until == 0:
                    formatted_date = "Today"
                elif days_until == 1:
                    formatted_date = "Tomorrow"
                elif days_until <= 7:
                    formatted_date = f"In {days_until} days"
                elif days_until <= 30:
                    formatted_date = earnings_date.strftime("%b %d")  # e.g., "Jan 15"
                else:
                    formatted_date = earnings_date.strftime("%b %d")  # e.g., "Feb 20"
                
                return {
                    "date": formatted_date,
                    "raw_date": raw_date,
                    "days_until": days_until,
                    "eps_estimate": item.get("epsEstimated"),
                    "revenue_estimate": item.get("revenueEstimated"),
                    "time": item.get("time", "")
                }
        
        # No upcoming earnings found
        return {"date": "Not scheduled", "raw_date": None, "days_until": None}
    
    def get_analyst_actions(self, symbol: str, limit: int = 5) -> List[Dict]:
        """Get recent analyst upgrades/downgrades."""
        data = self._make_request(f"upgrades-downgrades", {"symbol": symbol})
        if data:
            return [
                {
                    "date": item.get("publishedDate", "")[:10] if item.get("publishedDate") else "",
                    "firm": item.get("gradingCompany", ""),
                    "action": item.get("action", ""),  # upgrade, downgrade, maintain
                    "from_grade": item.get("previousGrade", ""),
                    "to_grade": item.get("newGrade", ""),
                    "price_target": item.get("priceTarget")
                }
                for item in data[:limit]
            ]
        return []
    
    def get_analyst_estimates(self, symbol: str) -> Optional[Dict]:
        """Get analyst consensus estimates."""
        data = self._make_request(f"analyst-estimates/{symbol}", {"limit": 1})
        if data and len(data) > 0:
            item = data[0]
            return {
                "date": item.get("date"),
                "avg_eps_estimate": item.get("estimatedEpsAvg"),
                "avg_revenue_estimate": item.get("estimatedRevenueAvg"),
                "num_analysts_eps": item.get("numberAnalystsEstimatedEps"),
                "num_analysts_revenue": item.get("numberAnalystEstimatedRevenue")
            }
        return None
    
    def enrich_with_research(self, stocks: List[Dict]) -> List[Dict]:
        """
        Enrich stock data with research information.
        
        Adds:
        - Recent news headlines
        - Upcoming earnings date
        - Recent analyst actions
        
        Args:
            stocks: List of stock dicts with 'ticker' key
            
        Returns:
            Same list with 'research' key added to each stock
        """
        for stock in stocks:
            symbol = stock.get('ticker')
            if not symbol:
                continue
            
            research = {}
            
            # Get news
            news = self.get_stock_news(symbol, limit=2)
            if news:
                research['news'] = news
            
            # Get earnings calendar
            earnings = self.get_earnings_calendar(symbol)
            if earnings:
                research['earnings'] = earnings
            
            # Get analyst actions
            analyst_actions = self.get_analyst_actions(symbol, limit=3)
            if analyst_actions:
                # Summarize: count upgrades vs downgrades in last 30 days
                upgrades = sum(1 for a in analyst_actions if 'upgrade' in a.get('action', '').lower())
                downgrades = sum(1 for a in analyst_actions if 'downgrade' in a.get('action', '').lower())
                research['analyst_actions'] = {
                    'recent': analyst_actions[:2],  # Last 2 actions
                    'upgrades_30d': upgrades,
                    'downgrades_30d': downgrades,
                    'net_sentiment': upgrades - downgrades
                }
            
            stock['research'] = research
        
        return stocks
    
    def calculate_growth_adjusted_rating(
        self, 
        rating: Dict, 
        growth: Optional[Dict], 
        use_full: bool = False
    ) -> Dict:
        """
        Calculate growth-adjusted FMP rating.
        
        For growth/momentum screens: Exclude P/E and P/B penalties
        For value screens: Use full rating
        
        Args:
            rating: FMP rating data
            growth: Growth data (optional)
            use_full: Whether to use full rating (for value screens)
        
        Returns:
            Adjusted rating dict with score and grade
        """
        if use_full:
            # Value screen: use full rating as-is
            return {
                'grade': rating.get('rating', 'N/A'),
                'score': rating.get('ratingScore', 3),
                'recommendation': rating.get('ratingRecommendation', 'N/A'),
                'details': {
                    'dcf': rating.get('ratingDetailsDCFScore'),
                    'roe': rating.get('ratingDetailsROEScore'),
                    'roa': rating.get('ratingDetailsROAScore'),
                    'de': rating.get('ratingDetailsDEScore'),
                    'pe': rating.get('ratingDetailsPEScore'),
                    'pb': rating.get('ratingDetailsPBScore'),
                },
                'adjusted': False
            }
        
        # Growth/momentum screen: exclude P/E and P/B, calculate adjusted score
        roe_score = rating.get('ratingDetailsROEScore', 3)
        roa_score = rating.get('ratingDetailsROAScore', 3)
        de_score = rating.get('ratingDetailsDEScore', 3)
        dcf_score = rating.get('ratingDetailsDCFScore', 3)
        
        # Calculate adjusted score (only using quality metrics)
        quality_scores = [roe_score, roa_score, de_score]
        adjusted_score = sum(quality_scores) / len(quality_scores)
        
        # If we have growth data, boost the score
        growth_boost = 0
        peg_ratio = None
        
        if growth:
            revenue_growth = growth.get('revenueGrowth', 0)
            eps_growth = growth.get('epsgrowth', 0)
            
            # Boost for high growth
            if revenue_growth > 0.30:  # >30% revenue growth
                growth_boost += 0.5
            elif revenue_growth > 0.20:  # >20%
                growth_boost += 0.3
            elif revenue_growth > 0.10:  # >10%
                growth_boost += 0.1
            
            if eps_growth > 0.50:  # >50% EPS growth
                growth_boost += 0.5
            elif eps_growth > 0.25:  # >25%
                growth_boost += 0.3
            elif eps_growth > 0.10:  # >10%
                growth_boost += 0.1
            
            # Calculate PEG if possible
            pe_score = rating.get('ratingDetailsPEScore', 3)
            if eps_growth > 0 and pe_score:
                # Rough PEG estimate
                peg_ratio = round((6 - pe_score) * 20 / (eps_growth * 100), 2)
        
        # Apply boost (max 1 point)
        final_score = min(5, adjusted_score + growth_boost)
        
        # Convert score to grade
        if final_score >= 4.5:
            grade = 'A+'
            rec = 'Strong Buy'
        elif final_score >= 4:
            grade = 'A'
            rec = 'Buy'
        elif final_score >= 3.5:
            grade = 'A-'
            rec = 'Buy'
        elif final_score >= 3:
            grade = 'B+'
            rec = 'Neutral'
        elif final_score >= 2.5:
            grade = 'B'
            rec = 'Neutral'
        elif final_score >= 2:
            grade = 'B-'
            rec = 'Neutral'
        else:
            grade = 'C'
            rec = 'Sell'
        
        return {
            'grade': grade,
            'score': round(final_score, 1),
            'recommendation': rec,
            'details': {
                'roe': roe_score,
                'roa': roa_score,
                'de': de_score,
                'dcf': dcf_score,
                'pe': '(excluded)',
                'pb': '(excluded)',
            },
            'growth_boost': round(growth_boost, 2),
            'peg_ratio': peg_ratio,
            'adjusted': True
        }
    
    def screen_stocks_v2(
        self,
        screen_type: str = "momentum",
        limit: int = 5,
        sector: Optional[str] = None,
        min_market_cap: float = 1_000_000_000,
        enrich_with_ratings: bool = True,
        enrich_with_research: bool = False
    ) -> Dict:
        """
        Optimized V2 screener using FMP's native endpoints.
        
        Flow:
        1. Use /stock-screener for initial server-side filtering
        2. Get bulk quotes for technical data
        3. Score and rank
        4. Enrich top N with ratings (optional)
        5. Enrich with research data (optional)
        
        Args:
            screen_type: Predefined screen type
            limit: Max stocks to return
            sector: Filter by sector
            min_market_cap: Minimum market cap
            enrich_with_ratings: Whether to fetch FMP ratings for top results
            enrich_with_research: Whether to add news, earnings, analyst actions
        
        Returns:
            Dict with results, performance metrics, and API call count
        """
        self.api_calls = 0
        self.start_time = time.time()
        
        print(f"\n{'='*60}")
        print(f"STOCK SCREENER V2 - {screen_type.upper()}")
        print(f"{'='*60}\n")
        
        # Get criteria
        criteria = get_screen_criteria(screen_type)
        
        print(f"Screen type: {screen_type}")
        print(f"Sector filter: {sector or 'All'}")
        print(f"Min market cap: ${min_market_cap:,.0f}")
        print(f"Limit: {limit}")
        print(f"Enrich with ratings: {enrich_with_ratings}")
        print()
        
        # Step 1: Use FMP's stock-screener for initial filtering (1 API call)
        print("Step 1: Server-side filtering via /stock-screener...")
        screener_results = self.get_fmp_screener_results(
            sector=sector,
            min_market_cap=min_market_cap,
            limit=200  # Get more candidates for scoring
        )
        print(f"  → Got {len(screener_results)} candidates (1 API call)")
        
        if not screener_results:
            return self._build_empty_result(screen_type, criteria, sector, min_market_cap)
        
        # Extract symbols
        symbols = [s['symbol'] for s in screener_results]
        
        # Step 2: Get bulk quotes for technical data
        print("Step 2: Fetching bulk quotes for technical data...")
        quotes = self.get_bulk_quotes(symbols)
        print(f"  → Got quotes for {len(quotes)} stocks ({self.api_calls} total API calls)")
        
        # Step 3: Score and rank
        print("Step 3: Scoring stocks...")
        results = []
        
        for item in screener_results:
            symbol = item['symbol']
            quote = quotes.get(symbol, {})
            
            if not quote:
                continue
            
            # Build stock data combining screener + quote data
            stock_data = {
                'symbol': symbol,
                'name': item.get('companyName', symbol),
                'price': quote.get('price', item.get('price', 0)),
                'change_percent': quote.get('changesPercentage', 0),
                'market_cap': item.get('marketCap', 0),
                'sector': item.get('sector', 'Unknown'),
                'industry': item.get('industry', 'Unknown'),
                'beta': item.get('beta'),
                'volume': quote.get('volume', item.get('volume', 0)),
                'avg_volume': quote.get('avgVolume', 1),
                'pe_ratio': quote.get('pe'),
                'price_avg_50': quote.get('priceAvg50'),
                'price_avg_200': quote.get('priceAvg200'),
            }
            
            # Calculate score
            scores = self.calculate_score_fast(stock_data, criteria)
            
            if scores['passed']:
                results.append({
                    'ticker': symbol,
                    'name': stock_data['name'],
                    'price': stock_data['price'],
                    'change_percent': stock_data['change_percent'],
                    'market_cap': stock_data['market_cap'],
                    'sector': stock_data['sector'],
                    'industry': stock_data['industry'],
                    'score': scores['overall'],
                    'scores': {
                        'technical': scores['technical'],
                        'fundamental': scores['fundamental']
                    },
                    'metrics': {
                        'pe_ratio': stock_data.get('pe_ratio'),
                        'beta': stock_data.get('beta'),
                        'price_vs_50sma': round((stock_data['price'] / stock_data['price_avg_50'] - 1) * 100, 2) if stock_data.get('price_avg_50') else None,
                        'price_vs_200sma': round((stock_data['price'] / stock_data['price_avg_200'] - 1) * 100, 2) if stock_data.get('price_avg_200') else None,
                    }
                })
        
        # Sort by score
        results.sort(key=lambda x: x['score'], reverse=True)
        top_results = results[:limit]
        
        print(f"  → {len(results)} stocks passed filters, returning top {len(top_results)}")
        
        # Step 4: Enrich top results with FMP ratings (optional)
        if enrich_with_ratings and top_results:
            use_full = use_full_rating(screen_type)
            is_growth = is_growth_screen(screen_type)
            
            mode_str = "full" if use_full else "growth-adjusted (excluding P/E, P/B)"
            print(f"Step 4: Enriching top {len(top_results)} with FMP ratings ({mode_str})...")
            
            top_symbols = [r['ticker'] for r in top_results]
            ratings = self.get_bulk_ratings(top_symbols)
            
            # For growth screens, also fetch growth data
            growth_data = {}
            if is_growth or not use_full:
                print(f"  → Fetching growth data for adjustment...")
                growth_data = self.get_bulk_growth_data(top_symbols)
            
            for result in top_results:
                rating = ratings.get(result['ticker'])
                growth = growth_data.get(result['ticker'])
                
                if rating:
                    # Calculate adjusted rating
                    adjusted_rating = self.calculate_growth_adjusted_rating(
                        rating, growth, use_full=use_full
                    )
                    result['fmp_rating'] = adjusted_rating
                    
                    # Add growth metrics if available
                    if growth:
                        result['growth'] = {
                            'revenue_growth': round(growth.get('revenueGrowth', 0) * 100, 1),
                            'eps_growth': round(growth.get('epsgrowth', 0) * 100, 1),
                            'net_income_growth': round(growth.get('netIncomeGrowth', 0) * 100, 1),
                        }
                    
                    # Boost score based on adjusted FMP rating
                    rating_boost = (adjusted_rating['score'] - 3) * 5  # -10 to +10
                    result['score'] = round(result['score'] + rating_boost, 1)
                    result['score_with_rating'] = result['score']
            
            # Re-sort after rating boost
            top_results.sort(key=lambda x: x['score'], reverse=True)
            print(f"  → Added ratings ({self.api_calls} total API calls)")
        
        # Step 5: Enrich with research (optional)
        if enrich_with_research and top_results:
            print(f"Step 5: Enriching with research data (news, earnings, analyst actions)...")
            top_results = self.enrich_with_research(top_results)
            print(f"  → Added research data ({self.api_calls} total API calls)")
        
        # Add rank
        for i, result in enumerate(top_results):
            result['rank'] = i + 1
        
        # Calculate performance
        elapsed = time.time() - self.start_time
        
        # Print results
        print(f"\n{'='*60}")
        print(f"RESULTS: Top {len(top_results)} {screen_type.upper()} Stocks")
        print(f"{'='*60}\n")
        
        for result in top_results:
            rating_str = ""
            if 'fmp_rating' in result:
                fmp = result['fmp_rating']
                adj_str = " (adj)" if fmp.get('adjusted') else ""
                rating_str = f" | FMP: {fmp['grade']}{adj_str} ({fmp['recommendation']})"
            
            print(f"#{result['rank']} {result['ticker']} - {result['name']}")
            print(f"   Price: ${result['price']:.2f} ({result['change_percent']:+.2f}%)")
            print(f"   Score: {result['score']:.1f}{rating_str}")
            
            # Show growth metrics if available
            if 'growth' in result:
                g = result['growth']
                print(f"   Growth: Rev {g['revenue_growth']:+.1f}% | EPS {g['eps_growth']:+.1f}%")
            
            if result['metrics'].get('pe_ratio'):
                print(f"   P/E: {result['metrics']['pe_ratio']:.1f}")
            if result['metrics'].get('price_vs_50sma'):
                print(f"   vs 50 SMA: {result['metrics']['price_vs_50sma']:+.1f}%")
            print()
        
        # Performance summary
        print(f"{'='*60}")
        print("PERFORMANCE METRICS")
        print(f"{'='*60}")
        print(f"Total API calls: {self.api_calls}")
        print(f"Total time: {elapsed:.2f} seconds")
        print(f"Stocks screened: {len(screener_results)}")
        print(f"Matches found: {len(results)}")
        print(f"Returned: {len(top_results)}")
        
        # Build output
        output = {
            'screen_type': screen_type,
            'timestamp': datetime.now().isoformat(),
            'criteria_used': criteria,
            'filters': {
                'sector': sector,
                'min_market_cap': min_market_cap,
            },
            'results': top_results,
            'total_screened': len(screener_results),
            'matches_found': len(results),
            'tickers': [r['ticker'] for r in top_results],
            'performance': {
                'api_calls': self.api_calls,
                'elapsed_seconds': round(elapsed, 2),
                'with_ratings': enrich_with_ratings
            }
        }
        
        return output
    
    def _build_empty_result(self, screen_type, criteria, sector, min_market_cap):
        """Build empty result when no stocks found."""
        return {
            'screen_type': screen_type,
            'timestamp': datetime.now().isoformat(),
            'criteria_used': criteria,
            'filters': {'sector': sector, 'min_market_cap': min_market_cap},
            'results': [],
            'total_screened': 0,
            'matches_found': 0,
            'tickers': [],
            'performance': {'api_calls': self.api_calls, 'elapsed_seconds': 0}
        }
    
    def get_stock_universe(self, universe: str = "sp500") -> List[str]:
        """Get list of stocks to screen."""
        cache_key = f"universe_{universe}"
        
        if universe == "sp500":
            data = self._make_request("sp500_constituent")
        elif universe == "nasdaq100":
            data = self._make_request("nasdaq_constituent")
        elif universe == "dowjones":
            data = self._make_request("dowjones_constituent")
        else:
            # Default to S&P 500
            data = self._make_request("sp500_constituent")
        
        if data:
            return [item['symbol'] for item in data]
        return []
    
    def get_bulk_quotes(self, symbols: List[str]) -> Dict[str, Dict]:
        """Get quotes for multiple symbols in one call."""
        # FMP allows comma-separated symbols
        batch_size = 50
        all_quotes = {}
        
        for i in range(0, len(symbols), batch_size):
            batch = symbols[i:i + batch_size]
            symbols_str = ",".join(batch)
            data = self._make_request(f"quote/{symbols_str}")
            if data:
                for quote in data:
                    all_quotes[quote['symbol']] = quote
        
        return all_quotes
    
    def screen_stocks_fast(
        self,
        screen_type: str = "momentum",
        limit: int = 5,
        sector: Optional[str] = None,
        min_market_cap: float = 1_000_000_000,
        universe: str = "sp500",
        custom_criteria: Optional[Dict] = None
    ) -> Dict:
        """
        Fast screening using bulk quote endpoint.
        Uses fewer API calls by fetching quotes in batches.
        """
        print(f"\n{'='*60}")
        print(f"STOCK SCREENER (FAST) - {screen_type.upper()}")
        print(f"{'='*60}\n")
        
        # Get criteria
        if custom_criteria:
            criteria = custom_criteria
            screen_type = "custom"
        else:
            criteria = get_screen_criteria(screen_type)
        
        print(f"Screen type: {screen_type}")
        print(f"Universe: {universe}")
        print(f"Sector filter: {sector or 'All'}")
        print(f"Min market cap: ${min_market_cap:,.0f}")
        print(f"Limit: {limit}")
        print()
        
        # Get stock universe
        print("Fetching stock universe...")
        symbols = self.get_stock_universe(universe)
        print(f"Found {len(symbols)} stocks in universe")
        
        # Get bulk quotes (much faster)
        print("Fetching bulk quotes...")
        quotes = self.get_bulk_quotes(symbols)
        print(f"Got quotes for {len(quotes)} stocks")
        
        # Screen based on available quote data
        results = []
        screened = 0
        
        print("\nScoring stocks...")
        for symbol, quote in quotes.items():
            screened += 1
            
            # Apply basic filters
            market_cap = quote.get('marketCap', 0)
            if market_cap < min_market_cap:
                continue
            
            stock_sector = quote.get('sector', 'Unknown')
            if sector and stock_sector.lower() != sector.lower():
                continue
            
            # Build stock data from quote
            stock_data = {
                'symbol': symbol,
                'name': quote.get('name', symbol),
                'price': quote.get('price', 0),
                'change_percent': quote.get('changesPercentage', 0),
                'market_cap': market_cap,
                'sector': stock_sector,
                'pe_ratio': quote.get('pe'),
                'eps': quote.get('eps'),
                'price_avg_50': quote.get('priceAvg50'),
                'price_avg_200': quote.get('priceAvg200'),
                'volume': quote.get('volume', 0),
                'avg_volume': quote.get('avgVolume', 1),
                '52_week_high': quote.get('yearHigh'),
                '52_week_low': quote.get('yearLow'),
                # These won't be available in bulk quote, use None
                'rsi': None,
                'roe': None,
                'debt_to_equity': None,
            }
            
            # Calculate score with available data
            scores = self.calculate_score_fast(stock_data, criteria)
            
            if scores['passed']:
                results.append({
                    'ticker': symbol,
                    'name': stock_data['name'],
                    'price': stock_data['price'],
                    'change_percent': stock_data['change_percent'],
                    'market_cap': stock_data['market_cap'],
                    'sector': stock_data['sector'],
                    'score': scores['overall'],
                    'scores': {
                        'technical': scores['technical'],
                        'fundamental': scores['fundamental']
                    },
                    'metrics': {
                        'pe_ratio': stock_data.get('pe_ratio'),
                        'price_vs_50sma': round((stock_data['price'] / stock_data['price_avg_50'] - 1) * 100, 2) if stock_data.get('price_avg_50') else None,
                        'price_vs_200sma': round((stock_data['price'] / stock_data['price_avg_200'] - 1) * 100, 2) if stock_data.get('price_avg_200') else None,
                        'change_1d': stock_data['change_percent'],
                    }
                })
        
        # Sort by score and limit
        results.sort(key=lambda x: x['score'], reverse=True)
        top_results = results[:limit]
        
        # Add rank
        for i, result in enumerate(top_results):
            result['rank'] = i + 1
        
        # Print results
        print(f"\n{'='*60}")
        print(f"RESULTS: Top {len(top_results)} {screen_type.upper()} Stocks")
        print(f"{'='*60}\n")
        
        for result in top_results:
            print(f"#{result['rank']} {result['ticker']} - {result['name']}")
            print(f"   Price: ${result['price']:.2f} ({result['change_percent']:+.2f}%)")
            print(f"   Score: {result['score']:.1f} (Tech: {result['scores']['technical']:.1f}, Fund: {result['scores']['fundamental']:.1f})")
            if result['metrics'].get('pe_ratio'):
                print(f"   P/E: {result['metrics']['pe_ratio']:.1f}")
            if result['metrics'].get('price_vs_50sma'):
                print(f"   vs 50 SMA: {result['metrics']['price_vs_50sma']:+.1f}%")
            print()
        
        # Build output
        output = {
            'screen_type': screen_type,
            'timestamp': datetime.now().isoformat(),
            'criteria_used': criteria,
            'filters': {
                'sector': sector,
                'min_market_cap': min_market_cap,
                'universe': universe
            },
            'results': top_results,
            'total_screened': screened,
            'matches_found': len(results),
            'tickers': [r['ticker'] for r in top_results]
        }
        
        print(f"Total screened: {screened}")
        print(f"Matches found: {len(results)}")
        print(f"Returned: {len(top_results)}")
        
        return output
    
    def calculate_score_fast(self, stock_data: Dict, criteria: Dict) -> Dict:
        """Calculate score using only quote data (faster, less precise)."""
        technical_score = 0
        fundamental_score = 0
        technical_checks = 0
        fundamental_checks = 0
        passed_filters = True
        
        # Moving average scoring
        if stock_data.get('price') and stock_data.get('price_avg_50'):
            technical_checks += 1
            pct_from_50 = (stock_data['price'] - stock_data['price_avg_50']) / stock_data['price_avg_50']
            
            if criteria.get('above_sma_50', False):
                if stock_data['price'] > stock_data['price_avg_50']:
                    technical_score += 80 + min(20, pct_from_50 * 100)
                else:
                    passed_filters = False
            elif criteria.get('below_sma_50', False):
                if stock_data['price'] < stock_data['price_avg_50']:
                    technical_score += 80 + min(20, abs(pct_from_50) * 100)
                else:
                    passed_filters = False
            else:
                # For momentum, being above is good
                if pct_from_50 > 0:
                    technical_score += 50 + min(50, pct_from_50 * 200)
                else:
                    technical_score += max(0, 50 + pct_from_50 * 100)
        
        if stock_data.get('price') and stock_data.get('price_avg_200'):
            technical_checks += 1
            pct_from_200 = (stock_data['price'] - stock_data['price_avg_200']) / stock_data['price_avg_200']
            
            if criteria.get('above_sma_200', False):
                if stock_data['price'] > stock_data['price_avg_200']:
                    technical_score += 100
                else:
                    passed_filters = False
            else:
                if pct_from_200 > 0:
                    technical_score += 50 + min(50, pct_from_200 * 100)
                else:
                    technical_score += max(0, 50 + pct_from_200 * 50)
        
        # Momentum from daily change
        if stock_data.get('change_percent') is not None:
            technical_checks += 1
            change = stock_data['change_percent']
            # For momentum, positive change is good
            if change > 0:
                technical_score += min(100, 50 + change * 10)
            else:
                technical_score += max(0, 50 + change * 5)
        
        # Volume scoring
        if stock_data.get('volume') and stock_data.get('avg_volume'):
            technical_checks += 1
            vol_ratio = stock_data['volume'] / max(stock_data['avg_volume'], 1)
            technical_score += min(100, vol_ratio * 50)
        
        # P/E scoring
        if stock_data.get('pe_ratio') is not None:
            pe = stock_data['pe_ratio']
            if pe > 0:
                fundamental_checks += 1
                if 'pe_max' in criteria:
                    if pe <= criteria['pe_max']:
                        fundamental_score += max(0, (criteria['pe_max'] - pe) / criteria['pe_max'] * 100)
                    else:
                        passed_filters = False
                else:
                    if pe < 30:
                        fundamental_score += max(0, (30 - pe) / 30 * 100)
                    else:
                        fundamental_score += 30
        
        # Calculate final scores
        tech_final = technical_score / max(technical_checks, 1)
        fund_final = fundamental_score / max(fundamental_checks, 1) if fundamental_checks > 0 else 50
        
        tech_weight = criteria.get('technical_weight', 0.5)
        fund_weight = 1 - tech_weight
        
        overall_score = (tech_final * tech_weight) + (fund_final * fund_weight)
        
        return {
            'passed': passed_filters,
            'overall': round(overall_score, 1),
            'technical': round(tech_final, 1),
            'fundamental': round(fund_final, 1)
        }
    
    def get_stock_data(self, symbol: str) -> Optional[Dict]:
        """Get combined fundamental and technical data for a stock."""
        # Check cache
        cache_key = f"stock_{symbol}"
        if cache_key in self.cache:
            cached_time, cached_data = self.cache[cache_key]
            if time.time() - cached_time < self.cache_duration:
                return cached_data
        
        # Fetch quote data
        quote_data = self._make_request(f"quote/{symbol}")
        if not quote_data or len(quote_data) == 0:
            return None
        quote = quote_data[0]
        
        # Fetch key metrics
        metrics_data = self._make_request(f"key-metrics-ttm/{symbol}")
        metrics = metrics_data[0] if metrics_data and len(metrics_data) > 0 else {}
        
        # Fetch ratios
        ratios_data = self._make_request(f"ratios-ttm/{symbol}")
        ratios = ratios_data[0] if ratios_data and len(ratios_data) > 0 else {}
        
        # Fetch technical indicators (RSI)
        rsi_data = self._make_request(f"technical_indicator/daily/{symbol}", 
                                       {"type": "rsi", "period": 14})
        rsi = rsi_data[0]['rsi'] if rsi_data and len(rsi_data) > 0 else None
        
        # Combine data
        stock_data = {
            'symbol': symbol,
            'name': quote.get('name', symbol),
            'price': quote.get('price', 0),
            'change_percent': quote.get('changesPercentage', 0),
            'market_cap': quote.get('marketCap', 0),
            'volume': quote.get('volume', 0),
            'avg_volume': quote.get('avgVolume', 0),
            'pe_ratio': quote.get('pe', None),
            'eps': quote.get('eps', None),
            'sector': quote.get('sector', 'Unknown'),
            
            # Technical
            'rsi': rsi,
            'price_avg_50': quote.get('priceAvg50', None),
            'price_avg_200': quote.get('priceAvg200', None),
            '52_week_high': quote.get('yearHigh', None),
            '52_week_low': quote.get('yearLow', None),
            
            # Fundamental from ratios
            'roe': ratios.get('returnOnEquityTTM', None),
            'roa': ratios.get('returnOnAssetsTTM', None),
            'debt_to_equity': ratios.get('debtEquityRatioTTM', None),
            'current_ratio': ratios.get('currentRatioTTM', None),
            'price_to_book': ratios.get('priceToBookRatioTTM', None),
            'dividend_yield': ratios.get('dividendYieldTTM', None),
            
            # Growth from metrics
            'revenue_growth': metrics.get('revenuePerShareTTM', None),
            'fcf_per_share': metrics.get('freeCashFlowPerShareTTM', None),
        }
        
        # Cache the data
        self.cache[cache_key] = (time.time(), stock_data)
        
        return stock_data
    
    def calculate_score(self, stock_data: Dict, criteria: Dict) -> Dict:
        """Calculate how well a stock matches the criteria."""
        technical_score = 0
        fundamental_score = 0
        technical_checks = 0
        fundamental_checks = 0
        passed_filters = True
        
        # RSI scoring
        if stock_data.get('rsi') is not None:
            rsi = stock_data['rsi']
            if 'rsi_min' in criteria and 'rsi_max' in criteria:
                technical_checks += 1
                if criteria['rsi_min'] <= rsi <= criteria['rsi_max']:
                    # Score based on how centered in range
                    mid = (criteria['rsi_min'] + criteria['rsi_max']) / 2
                    range_size = criteria['rsi_max'] - criteria['rsi_min']
                    distance = abs(rsi - mid) / (range_size / 2)
                    technical_score += (1 - distance) * 100
                else:
                    passed_filters = False
            elif 'rsi_max' in criteria:
                technical_checks += 1
                if rsi <= criteria['rsi_max']:
                    # Lower is better for oversold
                    technical_score += max(0, (criteria['rsi_max'] - rsi) / criteria['rsi_max'] * 100)
                else:
                    passed_filters = False
        
        # Moving average scoring (price vs 50/200 SMA)
        if stock_data.get('price') and stock_data.get('price_avg_50'):
            technical_checks += 1
            if criteria.get('above_sma_50', False):
                if stock_data['price'] > stock_data['price_avg_50']:
                    technical_score += 100
                else:
                    passed_filters = False
            elif criteria.get('below_sma_50', False):
                if stock_data['price'] < stock_data['price_avg_50']:
                    technical_score += 100
                else:
                    passed_filters = False
            else:
                # Neutral - just score based on position
                pct_from_50 = (stock_data['price'] - stock_data['price_avg_50']) / stock_data['price_avg_50']
                technical_score += 50 + (pct_from_50 * 100)
        
        if stock_data.get('price') and stock_data.get('price_avg_200'):
            technical_checks += 1
            if criteria.get('above_sma_200', False):
                if stock_data['price'] > stock_data['price_avg_200']:
                    technical_score += 100
                else:
                    passed_filters = False
        
        # Volume scoring
        if stock_data.get('volume') and stock_data.get('avg_volume'):
            technical_checks += 1
            vol_ratio = stock_data['volume'] / stock_data['avg_volume']
            if criteria.get('volume_surge', False) and vol_ratio > 1.5:
                technical_score += 100
            elif vol_ratio > 0.5:  # At least some activity
                technical_score += min(100, vol_ratio * 50)
        
        # P/E scoring
        if stock_data.get('pe_ratio') is not None:
            pe = stock_data['pe_ratio']
            if pe > 0:  # Positive earnings
                fundamental_checks += 1
                if 'pe_max' in criteria:
                    if pe <= criteria['pe_max']:
                        fundamental_score += max(0, (criteria['pe_max'] - pe) / criteria['pe_max'] * 100)
                    else:
                        passed_filters = False
                else:
                    # General scoring - moderate P/E is good
                    if pe < 30:
                        fundamental_score += max(0, (30 - pe) / 30 * 100)
        
        # ROE scoring
        if stock_data.get('roe') is not None:
            roe = stock_data['roe']
            fundamental_checks += 1
            if 'roe_min' in criteria:
                if roe >= criteria['roe_min']:
                    fundamental_score += min(100, roe / criteria['roe_min'] * 50)
                else:
                    passed_filters = False
            else:
                # Higher ROE is better
                fundamental_score += min(100, roe * 200)
        
        # Debt to Equity scoring
        if stock_data.get('debt_to_equity') is not None:
            de = stock_data['debt_to_equity']
            fundamental_checks += 1
            if 'debt_equity_max' in criteria:
                if de <= criteria['debt_equity_max']:
                    fundamental_score += max(0, (criteria['debt_equity_max'] - de) / criteria['debt_equity_max'] * 100)
                else:
                    passed_filters = False
            elif de < 1.0:  # Low debt is generally good
                fundamental_score += (1 - de) * 100
        
        # Price to Book scoring
        if stock_data.get('price_to_book') is not None:
            pb = stock_data['price_to_book']
            if pb > 0:
                fundamental_checks += 1
                if 'pb_max' in criteria and pb <= criteria['pb_max']:
                    fundamental_score += max(0, (criteria['pb_max'] - pb) / criteria['pb_max'] * 100)
        
        # Dividend yield scoring (for value screens)
        if criteria.get('dividend_yield_min') and stock_data.get('dividend_yield'):
            fundamental_checks += 1
            if stock_data['dividend_yield'] >= criteria['dividend_yield_min']:
                fundamental_score += 100
            else:
                passed_filters = False
        
        # Calculate final scores
        tech_final = technical_score / technical_checks if technical_checks > 0 else 50
        fund_final = fundamental_score / fundamental_checks if fundamental_checks > 0 else 50
        
        # Weight technical vs fundamental based on screen type
        tech_weight = criteria.get('technical_weight', 0.5)
        fund_weight = 1 - tech_weight
        
        overall_score = (tech_final * tech_weight) + (fund_final * fund_weight)
        
        return {
            'passed': passed_filters,
            'overall': round(overall_score, 1),
            'technical': round(tech_final, 1),
            'fundamental': round(fund_final, 1)
        }
    
    def screen_stocks(
        self,
        screen_type: str = "momentum",
        limit: int = 5,
        sector: Optional[str] = None,
        min_market_cap: float = 1_000_000_000,
        universe: str = "sp500",
        custom_criteria: Optional[Dict] = None
    ) -> Dict:
        """
        Screen stocks based on criteria.
        
        Args:
            screen_type: Predefined screen (momentum, oversold, value, quality, technical_buy)
            limit: Maximum stocks to return
            sector: Filter by sector
            min_market_cap: Minimum market cap in USD
            universe: Stock universe to screen (sp500, nasdaq100, all)
            custom_criteria: Custom criteria dict (overrides screen_type)
        
        Returns:
            Dict with results, metadata, and scores
        """
        print(f"\n{'='*60}")
        print(f"STOCK SCREENER - {screen_type.upper()}")
        print(f"{'='*60}\n")
        
        # Get criteria
        if custom_criteria:
            criteria = custom_criteria
            screen_type = "custom"
        else:
            criteria = get_screen_criteria(screen_type)
        
        print(f"Screen type: {screen_type}")
        print(f"Universe: {universe}")
        print(f"Sector filter: {sector or 'All'}")
        print(f"Min market cap: ${min_market_cap:,.0f}")
        print(f"Limit: {limit}")
        print()
        
        # Get stock universe
        print("Fetching stock universe...")
        symbols = self.get_stock_universe(universe)
        print(f"Found {len(symbols)} stocks in universe")
        
        # Screen stocks
        results = []
        screened = 0
        
        print("\nScreening stocks...")
        for i, symbol in enumerate(symbols):
            if (i + 1) % 50 == 0:
                print(f"  Progress: {i + 1}/{len(symbols)}")
            
            try:
                stock_data = self.get_stock_data(symbol)
                if not stock_data:
                    continue
                
                screened += 1
                
                # Apply filters
                if min_market_cap and stock_data.get('market_cap', 0) < min_market_cap:
                    continue
                
                if sector and stock_data.get('sector', '').lower() != sector.lower():
                    continue
                
                # Calculate score
                scores = self.calculate_score(stock_data, criteria)
                
                if scores['passed']:
                    results.append({
                        'ticker': symbol,
                        'name': stock_data['name'],
                        'price': stock_data['price'],
                        'change_percent': stock_data['change_percent'],
                        'market_cap': stock_data['market_cap'],
                        'sector': stock_data['sector'],
                        'score': scores['overall'],
                        'scores': {
                            'technical': scores['technical'],
                            'fundamental': scores['fundamental']
                        },
                        'metrics': {
                            'rsi': stock_data.get('rsi'),
                            'pe_ratio': stock_data.get('pe_ratio'),
                            'roe': stock_data.get('roe'),
                            'debt_to_equity': stock_data.get('debt_to_equity'),
                            'price_vs_50sma': round((stock_data['price'] / stock_data['price_avg_50'] - 1) * 100, 2) if stock_data.get('price_avg_50') else None,
                            'price_vs_200sma': round((stock_data['price'] / stock_data['price_avg_200'] - 1) * 100, 2) if stock_data.get('price_avg_200') else None,
                        }
                    })
                    
            except Exception as e:
                print(f"  Warning: Error processing {symbol}: {e}")
                continue
        
        # Sort by score and limit
        results.sort(key=lambda x: x['score'], reverse=True)
        top_results = results[:limit]
        
        # Add rank
        for i, result in enumerate(top_results):
            result['rank'] = i + 1
        
        # Print results
        print(f"\n{'='*60}")
        print(f"RESULTS: Top {len(top_results)} {screen_type.upper()} Stocks")
        print(f"{'='*60}\n")
        
        for result in top_results:
            print(f"#{result['rank']} {result['ticker']} - {result['name']}")
            print(f"   Price: ${result['price']:.2f} ({result['change_percent']:+.2f}%)")
            print(f"   Score: {result['score']:.1f} (Tech: {result['scores']['technical']:.1f}, Fund: {result['scores']['fundamental']:.1f})")
            if result['metrics'].get('rsi'):
                print(f"   RSI: {result['metrics']['rsi']:.1f}")
            if result['metrics'].get('pe_ratio'):
                print(f"   P/E: {result['metrics']['pe_ratio']:.1f}")
            print()
        
        # Build output
        output = {
            'screen_type': screen_type,
            'timestamp': datetime.now().isoformat(),
            'criteria_used': criteria,
            'filters': {
                'sector': sector,
                'min_market_cap': min_market_cap,
                'universe': universe
            },
            'results': top_results,
            'total_screened': screened,
            'matches_found': len(results),
            'tickers': [r['ticker'] for r in top_results]
        }
        
        print(f"Total screened: {screened}")
        print(f"Matches found: {len(results)}")
        print(f"Returned: {len(top_results)}")
        
        return output


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description='Screen stocks based on criteria')
    parser.add_argument('--screen', type=str, default='momentum',
                        choices=['momentum', 'oversold', 'value', 'quality', 'technical_buy', 'growth'],
                        help='Predefined screen type')
    parser.add_argument('--limit', type=int, default=5,
                        help='Max stocks to return')
    parser.add_argument('--sector', type=str, default=None,
                        help='Filter by sector')
    parser.add_argument('--min-market-cap', type=float, default=1_000_000_000,
                        help='Minimum market cap in USD')
    parser.add_argument('--universe', type=str, default='sp500',
                        choices=['sp500', 'nasdaq100', 'dowjones'],
                        help='Stock universe to screen (for v1 mode)')
    parser.add_argument('--custom', type=str, default=None,
                        help='Custom criteria as JSON string')
    parser.add_argument('--output', type=str, default=None,
                        help='Output file path (JSON)')
    parser.add_argument('--no-ratings', action='store_true',
                        help='Skip FMP ratings enrichment (faster)')
    parser.add_argument('--research', action='store_true',
                        help='Include research data (news, earnings, analyst actions)')
    parser.add_argument('--v1', action='store_true',
                        help='Use V1 screener (slower, uses S&P 500 list)')
    parser.add_argument('--compare', action='store_true',
                        help='Compare V1 vs V2 performance')
    parser.add_argument('--test-all-screens', action='store_true',
                        help='Test all predefined screens')
    
    args = parser.parse_args()
    
    try:
        screener = StockScreener()
        
        if args.test_all_screens:
            print("Testing all predefined screens (V2 mode)...\n")
            for screen_type in SCREEN_DEFINITIONS.keys():
                print(f"\n{'#'*60}")
                print(f"Testing: {screen_type}")
                print(f"{'#'*60}")
                result = screener.screen_stocks_v2(
                    screen_type=screen_type,
                    limit=3,
                    enrich_with_ratings=True
                )
                print(f"Found {len(result['results'])} stocks\n")
            return
        
        if args.compare:
            # Compare V1 vs V2 performance
            print("="*70)
            print("PERFORMANCE COMPARISON: V1 vs V2")
            print("="*70)
            
            # V1 (fast mode without ratings)
            print("\n--- V1 (Bulk quotes from S&P 500 list) ---")
            screener.api_calls = 0
            start = time.time()
            result_v1 = screener.screen_stocks_fast(
                screen_type=args.screen,
                limit=args.limit,
                sector=args.sector,
                min_market_cap=args.min_market_cap,
                universe=args.universe
            )
            v1_time = time.time() - start
            v1_calls = screener.api_calls
            
            # V2 without ratings
            print("\n--- V2 (FMP Screener, no ratings) ---")
            result_v2_no_rating = screener.screen_stocks_v2(
                screen_type=args.screen,
                limit=args.limit,
                sector=args.sector,
                min_market_cap=args.min_market_cap,
                enrich_with_ratings=False
            )
            
            # V2 with ratings
            print("\n--- V2 (FMP Screener + Ratings) ---")
            result_v2_rating = screener.screen_stocks_v2(
                screen_type=args.screen,
                limit=args.limit,
                sector=args.sector,
                min_market_cap=args.min_market_cap,
                enrich_with_ratings=True
            )
            
            # Summary
            print("\n" + "="*70)
            print("COMPARISON SUMMARY")
            print("="*70)
            print(f"{'Method':<30} {'API Calls':<12} {'Time (s)':<12} {'Results':<10}")
            print("-"*70)
            print(f"{'V1 (Bulk S&P 500)':<30} {v1_calls:<12} {v1_time:<12.2f} {len(result_v1['results']):<10}")
            print(f"{'V2 (FMP Screener, no ratings)':<30} {result_v2_no_rating['performance']['api_calls']:<12} {result_v2_no_rating['performance']['elapsed_seconds']:<12.2f} {len(result_v2_no_rating['results']):<10}")
            print(f"{'V2 (FMP Screener + Ratings)':<30} {result_v2_rating['performance']['api_calls']:<12} {result_v2_rating['performance']['elapsed_seconds']:<12.2f} {len(result_v2_rating['results']):<10}")
            print("-"*70)
            
            # Show top picks from each
            print("\nTop Picks Comparison:")
            print(f"V1: {', '.join(result_v1['tickers'])}")
            print(f"V2 (no ratings): {', '.join(result_v2_no_rating['tickers'])}")
            print(f"V2 (+ ratings): {', '.join(result_v2_rating['tickers'])}")
            return
        
        # Default: Use V2 screener
        if args.v1:
            result = screener.screen_stocks_fast(
                screen_type=args.screen,
                limit=args.limit,
                sector=args.sector,
                min_market_cap=args.min_market_cap,
                universe=args.universe
            )
        else:
            result = screener.screen_stocks_v2(
                screen_type=args.screen,
                limit=args.limit,
                sector=args.sector,
                min_market_cap=args.min_market_cap,
                enrich_with_ratings=not args.no_ratings,
                enrich_with_research=args.research
            )
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\nResults saved to: {args.output}")
        
        # Print tickers for easy copy
        print(f"\nTickers: {', '.join(result['tickers'])}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

