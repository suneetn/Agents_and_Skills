#!/usr/bin/env python3
"""
HTML Report Generator for Stock Analysis
Creates beautiful HTML reports with narrative stories
Inspired by pptx skill design principles
"""

from typing import Dict, Optional
from datetime import datetime
import json


class HTMLReportGenerator:
    """
    Generates beautiful HTML reports from stock analysis data
    """
    
    def __init__(self):
        self.color_palettes = {
            'turnaround': {
                'primary': '#E74C3C',      # Red
                'secondary': '#C0392B',    # Dark red
                'accent': '#F39C12',       # Orange
                'text': '#2C3E50',         # Dark blue-gray
                'background': '#ECF0F1',   # Light gray
                'success': '#27AE60',      # Green
            },
            'growth': {
                'primary': '#3498DB',       # Blue
                'secondary': '#2980B9',    # Dark blue
                'accent': '#1ABC9C',       # Teal
                'text': '#2C3E50',
                'background': '#F8F9FA',
                'success': '#27AE60',
            },
            'value': {
                'primary': '#9B59B6',      # Purple
                'secondary': '#8E44AD',    # Dark purple
                'accent': '#E67E22',       # Orange
                'text': '#2C3E50',
                'background': '#F8F9FA',
                'success': '#27AE60',
            },
            'momentum': {
                'primary': '#E67E22',      # Orange
                'secondary': '#D35400',    # Dark orange
                'accent': '#F39C12',       # Yellow
                'text': '#2C3E50',
                'background': '#FEF9E7',
                'success': '#27AE60',
            },
            'cautious': {
                'primary': '#95A5A6',      # Gray
                'secondary': '#7F8C8D',    # Dark gray
                'accent': '#34495E',       # Dark blue-gray
                'text': '#2C3E50',
                'background': '#F8F9FA',
                'success': '#27AE60',
            },
        }
    
    def generate_html_report(
        self,
        symbol: str,
        narrative: Dict[str, str],
        fundamental_data: Dict,
        technical_data: Dict,
        combined_data: Dict,
        output_path: str
    ) -> str:
        """
        Generate beautiful HTML report
        
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
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        
        /* Header */
        .header {{
            background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%);
            color: white;
            padding: 60px 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 48px;
            font-weight: bold;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}
        
        .header .symbol {{
            font-size: 24px;
            opacity: 0.9;
            margin-bottom: 20px;
        }}
        
        .header .price {{
            font-size: 36px;
            font-weight: bold;
            margin-top: 20px;
        }}
        
        .header .recommendation {{
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 10px 30px;
            border-radius: 25px;
            margin-top: 20px;
            font-size: 20px;
            font-weight: bold;
        }}
        
        /* Navigation */
        .nav {{
            background: {colors['accent']};
            padding: 20px 40px;
            display: flex;
            justify-content: center;
            gap: 30px;
            flex-wrap: wrap;
        }}
        
        .nav a {{
            color: white;
            text-decoration: none;
            font-weight: bold;
            padding: 10px 20px;
            border-radius: 5px;
            transition: background 0.3s;
        }}
        
        .nav a:hover {{
            background: rgba(255,255,255,0.2);
        }}
        
        /* Content Sections */
        .section {{
            padding: 60px 40px;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .section:last-child {{
            border-bottom: none;
        }}
        
        .section h2 {{
            font-size: 36px;
            color: {colors['primary']};
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 3px solid {colors['accent']};
        }}
        
        .section h3 {{
            font-size: 24px;
            color: {colors['secondary']};
            margin-top: 30px;
            margin-bottom: 15px;
        }}
        
        .narrative-text {{
            font-size: 18px;
            line-height: 1.8;
            color: {colors['text']};
            margin-bottom: 25px;
            text-align: justify;
        }}
        
        .narrative-text:first-child {{
            font-size: 20px;
            font-weight: 500;
            color: {colors['primary']};
        }}
        
        /* Metrics Grid */
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        
        .metric-card {{
            background: {colors['background']};
            padding: 25px;
            border-radius: 10px;
            border-left: 4px solid {colors['primary']};
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        
        .metric-card h4 {{
            color: {colors['secondary']};
            font-size: 14px;
            text-transform: uppercase;
            margin-bottom: 10px;
            letter-spacing: 1px;
        }}
        
        .metric-card .value {{
            font-size: 32px;
            font-weight: bold;
            color: {colors['primary']};
        }}
        
        .metric-card .label {{
            font-size: 14px;
            color: #7f8c8d;
            margin-top: 5px;
        }}
        
        /* Highlights */
        .highlight-box {{
            background: linear-gradient(135deg, {colors['accent']}15 0%, {colors['primary']}15 100%);
            border-left: 4px solid {colors['accent']};
            padding: 25px;
            margin: 30px 0;
            border-radius: 5px;
        }}
        
        .highlight-box h4 {{
            color: {colors['secondary']};
            margin-bottom: 15px;
            font-size: 20px;
        }}
        
        /* Lists */
        ul, ol {{
            margin-left: 30px;
            margin-bottom: 20px;
        }}
        
        li {{
            margin-bottom: 10px;
            line-height: 1.8;
        }}
        
        /* Footer */
        .footer {{
            background: {colors['text']};
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .footer p {{
            margin-bottom: 10px;
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 36px;
            }}
            
            .section {{
                padding: 40px 20px;
            }}
            
            .metrics-grid {{
                grid-template-columns: 1fr;
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



