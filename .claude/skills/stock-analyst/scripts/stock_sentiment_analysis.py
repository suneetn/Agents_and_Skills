#!/usr/bin/env python3
"""
Stock Sentiment Analysis using Financial Modeling Prep (FMP) API
Analyzes analyst recommendations and news sentiment
"""

import requests
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import Counter
import re

try:
    from dotenv import load_dotenv
    load_dotenv()  # Load .env file if it exists
except ImportError:
    pass  # python-dotenv not installed, fall back to environment variables

try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    VADER_AVAILABLE = True
except ImportError:
    VADER_AVAILABLE = False
    print("⚠️  vaderSentiment not installed. Install with: pip install vaderSentiment")
    print("   Falling back to simple keyword-based sentiment analysis")


class SentimentAnalyzer:
    """Simple sentiment analyzer using keyword matching"""
    
    POSITIVE_WORDS = [
        'bullish', 'buy', 'strong', 'growth', 'positive', 'outperform', 'upgrade',
        'gain', 'rise', 'surge', 'rally', 'breakthrough', 'success', 'profit',
        'beat', 'exceed', 'outperform', 'optimistic', 'favorable', 'momentum'
    ]
    
    NEGATIVE_WORDS = [
        'bearish', 'sell', 'weak', 'decline', 'negative', 'underperform', 'downgrade',
        'loss', 'fall', 'drop', 'crash', 'concern', 'risk', 'miss', 'disappoint',
        'underperform', 'pessimistic', 'unfavorable', 'volatility', 'uncertainty'
    ]
    
    def analyze_text(self, text: str) -> Dict:
        """Analyze sentiment of text using keyword matching"""
        if not text:
            return {'compound': 0.0, 'positive': 0.0, 'negative': 0.0, 'neutral': 1.0}
        
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        positive_count = sum(1 for word in words if word in self.POSITIVE_WORDS)
        negative_count = sum(1 for word in words if word in self.NEGATIVE_WORDS)
        total_words = len(words)
        
        if total_words == 0:
            return {'compound': 0.0, 'positive': 0.0, 'negative': 0.0, 'neutral': 1.0}
        
        positive_score = positive_count / total_words
        negative_score = negative_count / total_words
        compound = (positive_score - negative_score) * 0.5  # Scale down
        
        return {
            'compound': compound,
            'positive': positive_score,
            'negative': negative_score,
            'neutral': 1.0 - (positive_score + negative_score)
        }


class FMPSentimentAnalyzer:
    """Sentiment analysis using FMP API for analyst recommendations and news"""
    
    BASE_URL = "https://financialmodelingprep.com/api/v3"
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize FMP sentiment analyzer"""
        self.api_key = api_key or os.getenv('FMP_API_KEY')
        if not self.api_key:
            raise ValueError(
                "API key required. Set FMP_API_KEY in .env file or environment variable.\n"
                "Get your free API key at: https://site.financialmodelingprep.com/\n"
                "Create a .env file with: FMP_API_KEY=your_key"
            )
        
        # Initialize sentiment analyzer
        if VADER_AVAILABLE:
            self.sentiment_analyzer = SentimentIntensityAnalyzer()
        else:
            self.sentiment_analyzer = SentimentAnalyzer()
    
    def _make_request(self, endpoint: str, params: Dict = None) -> List[Dict]:
        """Make API request"""
        url = f"{self.BASE_URL}/{endpoint}"
        if params is None:
            params = {}
        params['apikey'] = self.api_key
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data if isinstance(data, list) else []
        except requests.exceptions.RequestException as e:
            print(f"⚠️  API request failed for {endpoint}: {e}")
            return []
    
    def get_analyst_recommendations(self, symbol: str, limit: int = 10) -> List[Dict]:
        """Get analyst recommendations/ratings"""
        # Try different endpoint formats
        endpoints = [
            f'grade/{symbol}',
            f'analyst-estimates/{symbol}',
            f'rating/{symbol}'
        ]
        
        for endpoint in endpoints:
            data = self._make_request(endpoint, {'limit': limit})
            if data:
                return data
        
        return []
    
    def get_stock_news(self, symbol: str, limit: int = 20) -> List[Dict]:
        """Get recent news articles for stock"""
        # Try different endpoint formats
        endpoints = [
            f'stock_news?tickers={symbol}',
            f'news/{symbol}',
            f'stock-news/{symbol}'
        ]
        
        for endpoint in endpoints:
            data = self._make_request(endpoint, {'limit': limit})
            if data:
                return data
        
        return []
    
    def analyze_analyst_sentiment(self, recommendations: List[Dict]) -> Dict:
        """Analyze sentiment from analyst recommendations"""
        if not recommendations:
            return {
                'average_rating': None,
                'rating_distribution': {},
                'sentiment_score': 0.0,
                'recommendation_summary': 'No analyst recommendations available'
            }
        
        # Map ratings to scores (common formats)
        rating_map = {
            'strong buy': 5, 'buy': 4, 'hold': 3, 'sell': 2, 'strong sell': 1,
            'outperform': 4, 'market perform': 3, 'underperform': 2,
            'overweight': 4, 'equal weight': 3, 'underweight': 2,
            'positive': 4, 'neutral': 3, 'negative': 2
        }
        
        ratings = []
        rating_counts = Counter()
        
        for rec in recommendations:
            # Try different field names for rating
            rating = None
            # Check newGrade first (most recent), then previousGrade, then other fields
            for field in ['newGrade', 'previousGrade', 'rating', 'recommendation', 'grade', 'ratingRecommendation']:
                if field in rec and rec[field]:
                    rating = str(rec[field]).lower().strip()
                    # Skip if it's empty or "none"
                    if rating and rating != 'none' and rating != 'n/a':
                        break
            
            if rating:
                rating_counts[rating] += 1
                # Map to score
                score = rating_map.get(rating, 3)  # Default to neutral
                ratings.append(score)
        
        if ratings:
            avg_rating = sum(ratings) / len(ratings)
            # Normalize to -1 to 1 scale (1-5 -> -1 to 1)
            sentiment_score = ((avg_rating - 3) / 2) * 0.8  # Scale to -0.8 to 0.8
        else:
            avg_rating = None
            sentiment_score = 0.0
        
        # Determine recommendation summary
        if avg_rating:
            if avg_rating >= 4.0:
                summary = 'Strongly Bullish - Analysts overwhelmingly recommend Buy'
            elif avg_rating >= 3.5:
                summary = 'Bullish - Analysts lean towards Buy'
            elif avg_rating >= 2.5:
                summary = 'Neutral - Mixed analyst opinions'
            elif avg_rating >= 2.0:
                summary = 'Bearish - Analysts lean towards Sell'
            else:
                summary = 'Strongly Bearish - Analysts recommend Sell'
        else:
            summary = 'No clear analyst consensus available'
        
        return {
            'average_rating': avg_rating,
            'rating_distribution': dict(rating_counts),
            'sentiment_score': sentiment_score,
            'recommendation_summary': summary,
            'total_recommendations': len(recommendations),
            'raw_recommendations': recommendations[:10]  # Include raw data for display
        }
    
    def analyze_news_sentiment(self, news_articles: List[Dict]) -> Dict:
        """Analyze sentiment from news articles"""
        if not news_articles:
            return {
                'average_sentiment': 0.0,
                'positive_count': 0,
                'negative_count': 0,
                'neutral_count': 0,
                'sentiment_score': 0.0,
                'news_summary': 'No recent news articles available'
            }
        
        sentiments = []
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        positive_articles_list = []
        negative_articles_list = []
        neutral_articles_list = []
        
        for article in news_articles:
            # Combine title and text for analysis
            text = ""
            if 'title' in article:
                text += article['title'] + " "
            if 'text' in article:
                text += article['text']
            elif 'content' in article:
                text += article['content']
            elif 'description' in article:
                text += article['description']
            
            if text:
                if VADER_AVAILABLE:
                    sentiment = self.sentiment_analyzer.polarity_scores(text)
                    compound = sentiment.get('compound', 0.0)
                else:
                    sentiment = self.sentiment_analyzer.analyze_text(text)
                    compound = sentiment.get('compound', 0.0)
                sentiments.append(compound)
                
                # Store article with sentiment for categorization
                article_with_sentiment = article.copy()
                article_with_sentiment['sentiment'] = compound
                
                if compound > 0.1:
                    positive_count += 1
                    positive_articles_list.append(article_with_sentiment)
                elif compound < -0.1:
                    negative_count += 1
                    negative_articles_list.append(article_with_sentiment)
                else:
                    neutral_count += 1
                    neutral_articles_list.append(article_with_sentiment)
        
        if sentiments:
            avg_sentiment = sum(sentiments) / len(sentiments)
        else:
            avg_sentiment = 0.0
        
        # Determine news summary
        if avg_sentiment > 0.2:
            summary = f'Positive News Sentiment - {positive_count} positive articles out of {len(news_articles)}'
        elif avg_sentiment < -0.2:
            summary = f'Negative News Sentiment - {negative_count} negative articles out of {len(news_articles)}'
        else:
            summary = f'Neutral News Sentiment - Mixed coverage with {neutral_count} neutral articles'
        
        return {
            'average_sentiment': avg_sentiment,
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count': neutral_count,
            'sentiment_score': avg_sentiment,
            'news_summary': summary,
            'total_articles': len(news_articles),
            'positive_articles': positive_articles_list[:5],  # Top 5 positive articles
            'negative_articles': negative_articles_list[:5],  # Top 5 negative articles
            'neutral_articles': neutral_articles_list[:3]     # Top 3 neutral articles
        }
    
    def analyze_stock_sentiment(self, symbol: str) -> Dict:
        """Perform comprehensive sentiment analysis"""
        print(f"\n{'='*80}")
        print(f"SENTIMENT ANALYSIS: {symbol}")
        print(f"{'='*80}\n")
        
        # Fetch data
        print("📊 Fetching analyst recommendations...")
        recommendations = self.get_analyst_recommendations(symbol)
        print(f"   Found {len(recommendations)} recommendations")
        
        print("\n📰 Fetching recent news articles...")
        news_articles = self.get_stock_news(symbol)
        print(f"   Found {len(news_articles)} news articles")
        
        # Analyze sentiment
        print("\n" + "-"*80)
        print("ANALYST SENTIMENT")
        print("-"*80)
        
        analyst_sentiment = self.analyze_analyst_sentiment(recommendations)
        
        if analyst_sentiment['average_rating']:
            print(f"Average Rating: {analyst_sentiment['average_rating']:.2f}/5.0")
            print(f"Rating Distribution: {analyst_sentiment['rating_distribution']}")
        print(f"Sentiment Score: {analyst_sentiment['sentiment_score']:.3f}")
        print(f"Summary: {analyst_sentiment['recommendation_summary']}")
        
        print("\n" + "-"*80)
        print("NEWS SENTIMENT")
        print("-"*80)
        
        news_sentiment = self.analyze_news_sentiment(news_articles)
        
        print(f"Average Sentiment: {news_sentiment['average_sentiment']:.3f}")
        print(f"Positive Articles: {news_sentiment['positive_count']}")
        print(f"Negative Articles: {news_sentiment['negative_count']}")
        print(f"Neutral Articles: {news_sentiment['neutral_count']}")
        print(f"Summary: {news_sentiment['news_summary']}")
        
        # Combined sentiment
        print("\n" + "-"*80)
        print("COMBINED SENTIMENT")
        print("-"*80)
        
        # Weight analyst sentiment more heavily (60%) than news (40%)
        analyst_weight = 0.6
        news_weight = 0.4
        
        combined_score = (
            analyst_sentiment['sentiment_score'] * analyst_weight +
            news_sentiment['sentiment_score'] * news_weight
        )
        
        if combined_score > 0.3:
            overall_sentiment = 'Strongly Bullish'
        elif combined_score > 0.1:
            overall_sentiment = 'Bullish'
        elif combined_score > -0.1:
            overall_sentiment = 'Neutral'
        elif combined_score > -0.3:
            overall_sentiment = 'Bearish'
        else:
            overall_sentiment = 'Strongly Bearish'
        
        print(f"Combined Sentiment Score: {combined_score:.3f}")
        print(f"Overall Sentiment: {overall_sentiment}")
        
        return {
            'symbol': symbol,
            'analyst_sentiment': analyst_sentiment,
            'news_sentiment': news_sentiment,
            'combined_sentiment': {
                'score': combined_score,
                'sentiment': overall_sentiment,
                'analyst_weight': analyst_weight,
                'news_weight': news_weight
            },
            'recommendations': recommendations[:5],  # Top 5
            'recent_news': news_articles[:5]  # Top 5
        }


if __name__ == "__main__":
    import sys
    
    symbol = sys.argv[1].upper() if len(sys.argv) > 1 else "AAPL"
    
    try:
        analyzer = FMPSentimentAnalyzer()
        result = analyzer.analyze_stock_sentiment(symbol)
        
        print("\n" + "="*80)
        print("✅ SENTIMENT ANALYSIS COMPLETE")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

