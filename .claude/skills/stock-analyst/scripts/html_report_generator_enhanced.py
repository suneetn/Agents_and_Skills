#!/usr/bin/env python3
"""
Enhanced HTML Report Generator for Stock Analysis
Creates beautiful HTML reports with narrative stories
Inspired by pptx skill design principles
"""

from typing import Dict, Optional
from datetime import datetime
import json


class HTMLReportGeneratorEnhanced:
    """
    Generates beautiful HTML reports from stock analysis data
    Uses design principles from pptx skill
    """
    
    def __init__(self):
        # Enhanced color palettes inspired by pptx skill
        self.color_palettes = {
            'turnaround': {
                # Inspired by "Bold Red" palette
                'primary': '#C0392B',      # Red
                'secondary': '#E74C3C',    # Bright red
                'accent': '#F39C12',       # Orange
                'success': '#27AE60',      # Green
                'text': '#2C3E50',         # Dark blue-gray
                'background': '#F4F6F6',   # Off-white
                'light': '#ECF0F1',        # Light gray
            },
            'growth': {
                # Inspired by "Classic Blue" palette
                'primary': '#1C2833',      # Deep navy
                'secondary': '#2E4053',    # Slate gray
                'accent': '#3498DB',       # Blue
                'success': '#27AE60',      # Green
                'text': '#2C3E50',
                'background': '#F4F6F6',
                'light': '#ECF0F1',
            },
            'value': {
                # Inspired by "Burgundy Luxury" palette
                'primary': '#5D1D2E',      # Burgundy
                'secondary': '#951233',    # Crimson
                'accent': '#997929',       # Gold
                'success': '#27AE60',
                'text': '#2C3E50',
                'background': '#FAF7F2',   # Cream
                'light': '#F4F6F6',
            },
            'momentum': {
                # Inspired by "Vibrant Orange" palette
                'primary': '#F96D00',      # Orange
                'secondary': '#E67E22',    # Dark orange
                'accent': '#F39C12',       # Yellow
                'success': '#27AE60',
                'text': '#222831',         # Charcoal
                'background': '#F2F2F2',    # Light gray
                'light': '#FFFFFF',
            },
            'cautious': {
                # Inspired by "Charcoal & Red" palette
                'primary': '#292929',      # Charcoal
                'secondary': '#7F8C8D',    # Dark gray
                'accent': '#95A5A6',       # Gray
                'success': '#27AE60',
                'text': '#2C3E50',
                'background': '#F8F9FA',
                'light': '#FFFFFF',
            },
        }
    
    def generate_html_report(
        self,
        symbol: str,
        narrative: Dict[str, str],
        fundamental_data: Dict,
        technical_data: Dict,
        combined_data: Dict,
        output_path: str,
        sentiment_data: Optional[Dict] = None
    ) -> str:
        """
        Generate beautiful HTML report with enhanced design
        
        Args:
            symbol: Stock symbol
            narrative: Narrative sections dict
            fundamental_data: Fundamental analysis data
            technical_data: Technical analysis data
            combined_data: Combined analysis data
            output_path: Path to save HTML file
        
        Returns:
            HTML content as string
        """
        
        framework = narrative.get('framework', 'cautious')
        colors = self.color_palettes.get(framework, self.color_palettes['cautious'])
        
        profile = fundamental_data.get('profile', {})
        company_name = profile.get('companyName', symbol)
        quote = fundamental_data.get('quote', {})
        current_price = quote.get('price', 0)
        recommendation = combined_data.get('recommendation', 'Hold')
        confidence = combined_data.get('confidence', 'Medium')
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{company_name} ({symbol}) - Stock Analysis Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Arial', 'Helvetica', sans-serif;
            line-height: 1.6;
            color: {colors['text']};
            background: {colors['background']};
            padding: 0;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 0 30px rgba(0,0,0,0.15);
        }}
        
        /* Header - Full bleed with gradient */
        .header {{
            background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%);
            color: white;
            padding: 80px 40px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        
        .header::before {{
            content: '';
            position: absolute;
            top: -50%;
            right: -10%;
            width: 500px;
            height: 500px;
            background: rgba(255,255,255,0.1);
            border-radius: 50%;
        }}
        
        .header h1 {{
            font-size: 56px;
            font-weight: bold;
            margin-bottom: 15px;
            text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
            position: relative;
            z-index: 1;
            letter-spacing: -1px;
        }}
        
        .header .symbol {{
            font-size: 28px;
            opacity: 0.95;
            margin-bottom: 25px;
            font-weight: 300;
            letter-spacing: 3px;
            position: relative;
            z-index: 1;
        }}
        
        .header .price {{
            font-size: 48px;
            font-weight: bold;
            margin-top: 25px;
            position: relative;
            z-index: 1;
        }}
        
        .header .recommendation {{
            display: inline-block;
            background: rgba(255,255,255,0.25);
            backdrop-filter: blur(10px);
            padding: 15px 40px;
            border-radius: 30px;
            margin-top: 30px;
            font-size: 22px;
            font-weight: bold;
            border: 2px solid rgba(255,255,255,0.3);
            position: relative;
            z-index: 1;
        }}
        
        /* Navigation - Edge-to-edge color band */
        .nav {{
            background: {colors['accent']};
            padding: 25px 40px;
            display: flex;
            justify-content: center;
            gap: 40px;
            flex-wrap: wrap;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .nav a {{
            color: white;
            text-decoration: none;
            font-weight: bold;
            padding: 12px 25px;
            border-radius: 8px;
            transition: all 0.3s;
            font-size: 16px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .nav a:hover {{
            background: rgba(255,255,255,0.25);
            transform: translateY(-2px);
        }}
        
        /* Content Sections - Asymmetric layouts */
        .section {{
            padding: 80px 40px;
            border-bottom: 1px solid #e0e0e0;
            position: relative;
        }}
        
        .section:last-child {{
            border-bottom: none;
        }}
        
        /* Diagonal section divider */
        .section::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: linear-gradient(90deg, {colors['primary']} 0%, {colors['accent']} 100%);
        }}
        
        .section h2 {{
            font-size: 42px;
            color: {colors['primary']};
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 4px solid {colors['accent']};
            font-weight: bold;
            letter-spacing: -1px;
        }}
        
        .section h3 {{
            font-size: 28px;
            color: {colors['secondary']};
            margin-top: 40px;
            margin-bottom: 20px;
            font-weight: 600;
        }}
        
        .narrative-text {{
            font-size: 19px;
            line-height: 1.9;
            color: {colors['text']};
            margin-bottom: 30px;
            text-align: justify;
        }}
        
        .narrative-text:first-child {{
            font-size: 22px;
            font-weight: 500;
            color: {colors['primary']};
            line-height: 1.8;
        }}
        
        /* Metrics Grid - Modular grid system */
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
            margin: 40px 0;
        }}
        
        .metric-card {{
            background: {colors['light']};
            padding: 30px;
            border-radius: 12px;
            border-left: 6px solid {colors['primary']};
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        
        .metric-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        }}
        
        .metric-card h4 {{
            color: {colors['secondary']};
            font-size: 13px;
            text-transform: uppercase;
            margin-bottom: 15px;
            letter-spacing: 1.5px;
            font-weight: 600;
        }}
        
        .metric-card .value {{
            font-size: 40px;
            font-weight: bold;
            color: {colors['primary']};
            margin-bottom: 8px;
        }}
        
        .metric-card .label {{
            font-size: 14px;
            color: #7f8c8d;
            margin-top: 8px;
        }}
        
        /* Highlight Boxes - Floating text boxes */
        .highlight-box {{
            background: linear-gradient(135deg, {colors['accent']}15 0%, {colors['primary']}15 100%);
            border-left: 6px solid {colors['accent']};
            padding: 35px;
            margin: 40px 0;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        
        .highlight-box h4 {{
            color: {colors['secondary']};
            margin-bottom: 20px;
            font-size: 24px;
            font-weight: bold;
        }}
        
        /* Two-column layout for better readability */
        .two-column {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
            margin: 40px 0;
        }}
        
        @media (max-width: 768px) {{
            .two-column {{
                grid-template-columns: 1fr;
            }}
        }}
        
        /* Lists with better styling */
        ul, ol {{
            margin-left: 40px;
            margin-bottom: 25px;
        }}
        
        li {{
            margin-bottom: 15px;
            line-height: 2;
            font-size: 18px;
        }}
        
        /* Footer */
        .footer {{
            background: {colors['text']};
            color: white;
            padding: 50px 40px;
            text-align: center;
        }}
        
        .footer p {{
            margin-bottom: 15px;
            font-size: 16px;
        }}
        
        .footer strong {{
            font-size: 20px;
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 42px;
            }}
            
            .header .price {{
                font-size: 36px;
            }}
            
            .section {{
                padding: 50px 25px;
            }}
            
            .section h2 {{
                font-size: 32px;
            }}
            
            .metrics-grid {{
                grid-template-columns: 1fr;
            }}
            
            .nav {{
                gap: 15px;
                padding: 20px 25px;
            }}
            
            .nav a {{
                padding: 10px 15px;
                font-size: 14px;
            }}
        }}
        
        /* Print styles */
        @media print {{
            .nav {{
                display: none;
            }}
            
            .section {{
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>{company_name}</h1>
            <div class="symbol">{symbol}</div>
            <div class="price">${current_price:.2f}</div>
            <div class="recommendation">{recommendation.upper()} - {confidence} Confidence</div>
        </div>
        
        <!-- Navigation -->
        <div class="nav">
            <a href="#story">The Story</a>
            <a href="#fundamentals">Fundamentals</a>
            <a href="#technicals">Technicals</a>
            <a href="#sentiment">Sentiment</a>
            <a href="#catalysts">Catalysts</a>
            <a href="#risks">Risks</a>
            <a href="#conclusion">Conclusion</a>
        </div>
        
        <!-- The Story Section -->
        <div id="story" class="section">
            <h2>The Story</h2>
            <div class="narrative-text">{narrative.get('opening_hook', '')}</div>
            <div class="narrative-text">{narrative.get('company_story', '')}</div>
        </div>
        
        <!-- Fundamentals Section -->
        <div id="fundamentals" class="section">
            <h2>Fundamental Analysis</h2>
            <div class="narrative-text">{narrative.get('fundamental_narrative', '')}</div>
            {self._generate_fundamental_metrics(fundamental_data, colors)}
        </div>
        
        <!-- Technicals Section -->
        <div id="technicals" class="section">
            <h2>Technical Analysis</h2>
            <div class="narrative-text">{narrative.get('technical_narrative', '')}</div>
            {self._generate_technical_metrics(technical_data, colors)}
        </div>
        
        <!-- Sentiment Section -->
        {self._generate_sentiment_section(sentiment_data, colors) if sentiment_data else ''}
        
        <!-- Catalysts Section -->
        <div id="catalysts" class="section">
            <h2>Key Catalysts</h2>
            <div class="narrative-text">{narrative.get('catalyst_story', '')}</div>
        </div>
        
        <!-- Risks Section -->
        <div id="risks" class="section">
            <h2>Risk Factors</h2>
            <div class="narrative-text">{narrative.get('risk_story', '')}</div>
        </div>
        
        <!-- Investment Story Section -->
        <div id="conclusion" class="section">
            <h2>Investment Thesis</h2>
            <div class="narrative-text">{narrative.get('investment_story', '')}</div>
            <div class="highlight-box">
                <h4>Conclusion</h4>
                <div class="narrative-text">{narrative.get('conclusion', '')}</div>
            </div>
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <p><strong>{company_name} ({symbol}) Stock Analysis Report</strong></p>
            <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            <p>This report is for informational purposes only and does not constitute investment advice.</p>
        </div>
    </div>
</body>
</html>"""
        
        # Save to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return html_content
    
    def _generate_fundamental_metrics(self, fundamental_data: Dict, colors: Dict) -> str:
        """Generate fundamental metrics HTML"""
        ratios = fundamental_data.get('ratios', [{}])[0]
        growth = fundamental_data.get('growth', [{}])[0]
        quote = fundamental_data.get('quote', {})
        
        roe = ratios.get('returnOnEquity', 0) * 100
        roa = ratios.get('returnOnAssets', 0) * 100
        revenue_growth = growth.get('revenueGrowth', 0) * 100
        net_income_growth = growth.get('netIncomeGrowth', 0) * 100
        pe_ratio = quote.get('pe', 0)
        
        return f"""
        <div class="metrics-grid">
            <div class="metric-card">
                <h4>Return on Equity</h4>
                <div class="value">{roe:.1f}%</div>
                <div class="label">Profitability Metric</div>
            </div>
            <div class="metric-card">
                <h4>Revenue Growth</h4>
                <div class="value">{revenue_growth:.1f}%</div>
                <div class="label">Year-over-Year</div>
            </div>
            <div class="metric-card">
                <h4>P/E Ratio</h4>
                <div class="value">{pe_ratio:.2f}</div>
                <div class="label">Valuation Metric</div>
            </div>
            <div class="metric-card">
                <h4>Net Income Growth</h4>
                <div class="value">{net_income_growth:.1f}%</div>
                <div class="label">Year-over-Year</div>
            </div>
        </div>
        """
    
    def _generate_technical_metrics(self, technical_data: Dict, colors: Dict) -> str:
        """Generate technical metrics HTML"""
        indicators = technical_data.get('indicators', {})
        trend = technical_data.get('trend', {})
        
        rsi = indicators.get('rsi', {}).get('value', 50)
        trend_direction = trend.get('direction', 'Neutral')
        
        return f"""
        <div class="metrics-grid">
            <div class="metric-card">
                <h4>RSI</h4>
                <div class="value">{rsi:.1f}</div>
                <div class="label">Momentum Indicator</div>
            </div>
            <div class="metric-card">
                <h4>Trend</h4>
                <div class="value">{trend_direction}</div>
                <div class="label">Primary Direction</div>
            </div>
        </div>
        """
    
    def _generate_sentiment_section(self, sentiment_data: Dict, colors: Dict) -> str:
        """Generate sentiment analysis section HTML"""
        if not sentiment_data:
            return ''
        
        analyst_sentiment = sentiment_data.get('analyst_sentiment', {})
        news_sentiment = sentiment_data.get('news_sentiment', {})
        combined_sentiment = sentiment_data.get('combined_sentiment', {})
        
        # Analyst data
        analyst_rating = analyst_sentiment.get('average_rating', 0)
        analyst_distribution = analyst_sentiment.get('rating_distribution', {})
        analyst_summary = analyst_sentiment.get('summary', 'N/A')
        
        # News data
        news_avg_sentiment = news_sentiment.get('average_sentiment', 0)
        positive_articles = news_sentiment.get('positive_articles', 0)
        negative_articles = news_sentiment.get('negative_articles', 0)
        neutral_articles = news_sentiment.get('neutral_articles', 0)
        total_articles = positive_articles + negative_articles + neutral_articles
        news_summary = news_sentiment.get('summary', 'N/A')
        
        # Top headlines
        top_headlines = news_sentiment.get('top_headlines', [])
        
        # Combined sentiment
        combined_score = combined_sentiment.get('combined_sentiment_score', 0)
        combined_classification = combined_sentiment.get('overall_sentiment', 'Neutral')
        
        # Determine sentiment color
        if combined_score > 0.2:
            sentiment_color = colors['success']
        elif combined_score < -0.2:
            sentiment_color = colors['primary']
        else:
            sentiment_color = colors['accent']
        
        # Build analyst distribution string
        analyst_dist_str = ', '.join([f"{k.title()}: {v}" for k, v in analyst_distribution.items()])
        
        return f"""
        <!-- Sentiment Section -->
        <div id="sentiment" class="section">
            <h2>Market Sentiment</h2>
            
            <div class="two-column">
                <!-- Analyst Sentiment -->
                <div>
                    <h3>Analyst Sentiment</h3>
                    <div class="metric-card" style="margin-bottom: 20px;">
                        <h4>Average Rating</h4>
                        <div class="value">{analyst_rating:.2f}/5.0</div>
                        <div class="label">{analyst_summary}</div>
                    </div>
                    <div class="highlight-box">
                        <h4>Rating Distribution</h4>
                        <p style="font-size: 16px; line-height: 1.8;">{analyst_dist_str}</p>
                    </div>
                </div>
                
                <!-- News Sentiment -->
                <div>
                    <h3>News Sentiment</h3>
                    <div class="metric-card" style="margin-bottom: 20px;">
                        <h4>Sentiment Score</h4>
                        <div class="value" style="color: {sentiment_color};">{news_avg_sentiment:.3f}</div>
                        <div class="label">{news_summary}</div>
                    </div>
                    <div class="highlight-box">
                        <h4>Article Breakdown</h4>
                        <p style="font-size: 16px; line-height: 1.8;">
                            <strong style="color: {colors['success']};">Positive:</strong> {positive_articles} articles<br>
                            <strong style="color: {colors['primary']};">Negative:</strong> {negative_articles} articles<br>
                            <strong style="color: {colors['accent']};">Neutral:</strong> {neutral_articles} articles<br>
                            <strong>Total:</strong> {total_articles} articles
                        </p>
                    </div>
                </div>
            </div>
            
            <!-- Combined Sentiment -->
            <div class="highlight-box" style="margin-top: 40px;">
                <h4>Overall Market Sentiment</h4>
                <div style="display: flex; align-items: center; gap: 20px; margin-top: 20px;">
                    <div style="font-size: 32px; font-weight: bold; color: {sentiment_color};">
                        {combined_classification.upper()}
                    </div>
                    <div style="font-size: 18px; color: {colors['text']};">
                        Combined Score: <strong>{combined_score:.3f}</strong>
                    </div>
                </div>
            </div>
            
            <!-- Top Headlines -->
            {self._generate_headlines_section(top_headlines, colors) if top_headlines else ''}
        </div>
        """
    
    def _generate_headlines_section(self, headlines: list, colors: Dict) -> str:
        """Generate top headlines section"""
        if not headlines:
            return ''
        
        # Separate positive and negative headlines
        positive_headlines = [h for h in headlines[:10] if h.get('sentiment', 0) > 0]
        negative_headlines = [h for h in headlines[:10] if h.get('sentiment', 0) < 0]
        
        html = '<div style="margin-top: 40px;"><h3>Recent Headlines</h3>'
        
        if positive_headlines:
            html += '<div style="margin-top: 20px;"><h4 style="color: ' + colors['success'] + '; margin-bottom: 15px;">Top Positive Headlines</h4><ul style="list-style: none; padding-left: 0;">'
            for headline in positive_headlines[:5]:
                title = headline.get('title', 'N/A')
                url = headline.get('url', '#')
                date = headline.get('publishedDate', '')
                html += f'<li style="margin-bottom: 15px; padding-left: 20px; border-left: 3px solid {colors["success"]};">'
                html += f'<a href="{url}" target="_blank" style="color: {colors["text"]}; text-decoration: none; font-weight: 500;">{title}</a>'
                if date:
                    html += f'<span style="color: #7f8c8d; font-size: 14px; margin-left: 10px;">({date})</span>'
                html += '</li>'
            html += '</ul></div>'
        
        if negative_headlines:
            html += '<div style="margin-top: 20px;"><h4 style="color: ' + colors['primary'] + '; margin-bottom: 15px;">Top Negative Headlines</h4><ul style="list-style: none; padding-left: 0;">'
            for headline in negative_headlines[:3]:
                title = headline.get('title', 'N/A')
                url = headline.get('url', '#')
                date = headline.get('publishedDate', '')
                html += f'<li style="margin-bottom: 15px; padding-left: 20px; border-left: 3px solid {colors["primary"]};">'
                html += f'<a href="{url}" target="_blank" style="color: {colors["text"]}; text-decoration: none; font-weight: 500;">{title}</a>'
                if date:
                    html += f'<span style="color: #7f8c8d; font-size: 14px; margin-left: 10px;">({date})</span>'
                html += '</li>'
            html += '</ul></div>'
        
        html += '</div>'
        return html

