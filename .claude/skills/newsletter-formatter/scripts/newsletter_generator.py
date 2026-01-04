#!/usr/bin/env python3
"""
Newsletter Generator
Generates HTML email newsletters from stock data
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

# Add parent dir for imports
sys.path.insert(0, str(Path(__file__).parent))

from jinja2 import Environment, FileSystemLoader, select_autoescape
from sparkline_generator import SparklineGenerator, get_trend_indicator

# Get template directory
TEMPLATE_DIR = Path(__file__).parent.parent / 'templates'


class NewsletterGenerator:
    """Generates HTML email newsletters from stock data"""
    
    def __init__(self, template_dir: Optional[Path] = None):
        """
        Initialize newsletter generator
        
        Args:
            template_dir: Path to template directory
        """
        self.template_dir = template_dir or TEMPLATE_DIR
        
        # Setup Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Add custom filters
        self.env.filters['format_currency'] = self._format_currency
        self.env.filters['format_percent'] = self._format_percent
        self.env.filters['trend_color'] = self._trend_color
        
        # Sparkline generator
        self.sparkline_gen = SparklineGenerator(width=80, height=24)
        
    def generate(
        self,
        data: Dict[str, Any],
        template_name: str = 'stock-picks.html',
        include_charts: bool = True,
        include_details: bool = True
    ) -> Dict[str, str]:
        """
        Generate newsletter HTML from data
        
        Args:
            data: Newsletter data dictionary
            template_name: Template file name
            include_charts: Generate sparkline charts
            include_details: Include detailed analysis section
            
        Returns:
            Dictionary with 'html', 'text', and 'subject' keys
        """
        # Enrich data with sparklines if requested
        if include_charts and 'stocks' in data:
            data = self._add_sparklines(data)
        
        # Add metadata
        data['include_details'] = include_details
        data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        # Load and render template
        template = self.env.get_template(template_name)
        html = template.render(**data)
        
        # Generate plain text version
        text = self._generate_plain_text(data)
        
        # Generate subject line
        subject = self._generate_subject(data)
        
        return {
            'html': html,
            'text': text,
            'subject': subject
        }
    
    def _add_sparklines(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Add sparkline images to stock data"""
        for stock in data.get('stocks', []):
            if 'price_history' in stock and stock['price_history']:
                stock['sparkline'] = self.sparkline_gen.generate(
                    stock['price_history'],
                    show_trend=True
                )
                trend_emoji, trend_color = get_trend_indicator(stock['price_history'])
                stock['trend_emoji'] = trend_emoji
                stock['trend_color'] = trend_color
        return data
    
    def _generate_plain_text(self, data: Dict[str, Any]) -> str:
        """Generate plain text version of newsletter"""
        lines = []
        
        # Header
        title = data.get('title', 'Daily Stock Picks')
        date = data.get('date', datetime.now().strftime('%B %d, %Y'))
        lines.append(f"{'='*50}")
        lines.append(title.upper())
        lines.append(date)
        lines.append(f"{'='*50}")
        lines.append("")
        
        # Market summary
        if 'market_summary' in data:
            lines.append("MARKET SUMMARY")
            lines.append("-" * 30)
            lines.append(data['market_summary'])
            lines.append("")
        
        # Stock picks
        lines.append("TODAY'S TOP PICKS")
        lines.append("-" * 30)
        
        for stock in data.get('stocks', []):
            change = stock.get('change_percent', 0)
            change_str = f"+{change:.1f}%" if change >= 0 else f"{change:.1f}%"
            
            lines.append(f"#{stock['rank']} {stock['ticker']} - {stock.get('name', '')}")
            lines.append(f"   Price: ${stock['price']:.2f} ({change_str})")
            
            if stock.get('fmp_rating'):
                lines.append(f"   Rating: {stock['fmp_rating']['grade']} ({stock['fmp_rating']['recommendation']})")
            
            if stock.get('growth'):
                rev = stock['growth'].get('revenue_growth', 0)
                eps = stock['growth'].get('eps_growth', 0)
                lines.append(f"   Growth: Rev {rev:+.0f}% | EPS {eps:+.0f}%")
            
            lines.append(f"   Score: {stock.get('score', 0):.0f}/100")
            lines.append("")
        
        # Footer
        lines.append("-" * 50)
        lines.append(data.get('footer_text', 'This is not financial advice.'))
        
        return "\n".join(lines)
    
    def _generate_subject(self, data: Dict[str, Any]) -> str:
        """Generate email subject line"""
        date = data.get('date', datetime.now().strftime('%b %d'))
        
        # Get top stock
        top_stock = data.get('stocks', [{}])[0]
        top_ticker = top_stock.get('ticker', 'Stocks')
        
        screen_type = data.get('screen_type', 'Momentum')
        
        return f"📈 {screen_type} Picks: {top_ticker} leads | {date}"
    
    @staticmethod
    def _format_currency(value: float) -> str:
        """Format number as currency"""
        return f"${value:,.2f}"
    
    @staticmethod
    def _format_percent(value: float, show_sign: bool = True) -> str:
        """Format number as percentage"""
        if show_sign:
            return f"{value:+.1f}%"
        return f"{value:.1f}%"
    
    @staticmethod
    def _trend_color(value: float) -> str:
        """Get color based on trend"""
        return '#38a169' if value >= 0 else '#e53e3e'
    
    def save(
        self,
        result: Dict[str, str],
        output_dir: Path,
        filename_prefix: str = 'newsletter'
    ) -> Dict[str, Path]:
        """
        Save generated newsletter to files
        
        Args:
            result: Generation result dictionary
            output_dir: Output directory
            filename_prefix: Prefix for output files
            
        Returns:
            Dictionary with file paths
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        paths = {}
        
        # Save HTML
        html_path = output_dir / f"{filename_prefix}_{timestamp}.html"
        with open(html_path, 'w') as f:
            f.write(result['html'])
        paths['html'] = html_path
        
        # Save plain text
        text_path = output_dir / f"{filename_prefix}_{timestamp}.txt"
        with open(text_path, 'w') as f:
            f.write(result['text'])
        paths['text'] = text_path
        
        return paths


def create_sample_data() -> Dict[str, Any]:
    """Create sample data for testing"""
    return {
        "title": "QuantHub Daily",
        "subtitle": "AI-Powered Stock Picks",
        "date": datetime.now().strftime("%B %d, %Y"),
        "edition": 42,
        "screen_type": "Momentum",
        "total_screened": "500+",
        "market_summary": "Markets rallied on Thursday with the S&P 500 gaining 1.2%. Tech stocks led the advance as investors rotated into growth names. The Nasdaq hit new all-time highs while value sectors lagged.",
        "stocks": [
            {
                "rank": 1,
                "ticker": "PLTR",
                "name": "Palantir Technologies",
                "price": 167.86,
                "change_percent": 2.5,
                "score": 92.0,
                "fmp_rating": {
                    "grade": "A+",
                    "recommendation": "Strong Buy",
                    "adjusted": True
                },
                "growth": {
                    "revenue_growth": 28.8,
                    "eps_growth": 114.9
                },
                "metrics": {
                    "pe_ratio": 390,
                    "price_vs_50sma": 15.2
                },
                "price_history": [145, 150, 148, 155, 160, 158, 165, 168]
            },
            {
                "rank": 2,
                "ticker": "NVDA",
                "name": "NVIDIA Corporation",
                "price": 188.85,
                "change_percent": 1.8,
                "score": 89.0,
                "fmp_rating": {
                    "grade": "A+",
                    "recommendation": "Strong Buy",
                    "adjusted": True
                },
                "growth": {
                    "revenue_growth": 114.2,
                    "eps_growth": 145.5
                },
                "metrics": {
                    "pe_ratio": 47,
                    "price_vs_50sma": 8.5
                },
                "price_history": [170, 175, 172, 180, 183, 185, 187, 189]
            },
            {
                "rank": 3,
                "ticker": "META",
                "name": "Meta Platforms Inc",
                "price": 612.50,
                "change_percent": 0.9,
                "score": 85.0,
                "fmp_rating": {
                    "grade": "A",
                    "recommendation": "Buy",
                    "adjusted": True
                },
                "growth": {
                    "revenue_growth": 22.5,
                    "eps_growth": 35.2
                },
                "metrics": {
                    "pe_ratio": 28,
                    "price_vs_50sma": 5.2
                },
                "price_history": [580, 590, 585, 600, 605, 608, 610, 613]
            },
            {
                "rank": 4,
                "ticker": "CRWD",
                "name": "CrowdStrike Holdings",
                "price": 368.20,
                "change_percent": 3.2,
                "score": 82.0,
                "fmp_rating": {
                    "grade": "A-",
                    "recommendation": "Buy",
                    "adjusted": True
                },
                "growth": {
                    "revenue_growth": 33.1,
                    "eps_growth": 45.8
                },
                "metrics": {
                    "pe_ratio": 95,
                    "price_vs_50sma": 12.1
                },
                "price_history": [340, 345, 350, 355, 360, 358, 365, 368]
            },
            {
                "rank": 5,
                "ticker": "PANW",
                "name": "Palo Alto Networks",
                "price": 195.80,
                "change_percent": 1.5,
                "score": 78.0,
                "fmp_rating": {
                    "grade": "B+",
                    "recommendation": "Buy",
                    "adjusted": True
                },
                "growth": {
                    "revenue_growth": 15.8,
                    "eps_growth": 28.3
                },
                "metrics": {
                    "pe_ratio": 52,
                    "price_vs_50sma": 6.8
                },
                "price_history": [185, 188, 186, 190, 192, 193, 194, 196]
            }
        ],
        "footer_text": "This newsletter is for informational purposes only and does not constitute financial advice. Past performance does not guarantee future results. Always do your own research before making investment decisions."
    }


def main():
    parser = argparse.ArgumentParser(description='Generate stock newsletter')
    parser.add_argument('--data', type=str, help='Path to JSON data file')
    parser.add_argument('--sample', action='store_true', help='Use sample data')
    parser.add_argument('--output', type=str, default='newsletter.html', 
                       help='Output HTML file path')
    parser.add_argument('--no-charts', action='store_true', help='Disable sparkline charts')
    parser.add_argument('--no-details', action='store_true', help='Disable detailed analysis')
    parser.add_argument('--template', type=str, default='stock-picks.html',
                       help='Template to use')
    
    args = parser.parse_args()
    
    # Load data
    if args.sample:
        data = create_sample_data()
        print("📝 Using sample data...")
    elif args.data:
        with open(args.data, 'r') as f:
            data = json.load(f)
        print(f"📂 Loaded data from {args.data}")
    else:
        print("❌ Error: Please provide --data or --sample")
        sys.exit(1)
    
    # Generate newsletter
    generator = NewsletterGenerator()
    
    print(f"🎨 Generating newsletter with template: {args.template}")
    result = generator.generate(
        data,
        template_name=args.template,
        include_charts=not args.no_charts,
        include_details=not args.no_details
    )
    
    # Save HTML
    with open(args.output, 'w') as f:
        f.write(result['html'])
    print(f"✅ Saved HTML to: {args.output}")
    
    # Save text version
    text_output = args.output.replace('.html', '.txt')
    with open(text_output, 'w') as f:
        f.write(result['text'])
    print(f"✅ Saved text to: {text_output}")
    
    # Print subject
    print(f"📧 Subject: {result['subject']}")
    
    print("\n🎉 Newsletter generated successfully!")


if __name__ == '__main__':
    main()



