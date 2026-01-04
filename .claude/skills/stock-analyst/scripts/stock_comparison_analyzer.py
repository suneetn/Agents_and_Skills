#!/usr/bin/env python3
"""
Stock Comparison Analyzer
Performs technical and fundamental analysis on multiple stocks and generates comparison tables
"""

import os
import sys
import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional
import json

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Add script directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

try:
    from stock_analysis_fmp import FMPStockAnalyzer
    from stock_technical_analysis import FMPTechnicalAnalyzer
except ImportError:
    # Fallback to personal directory
    personal_dir = os.path.expanduser('~/personal')
    if personal_dir not in sys.path:
        sys.path.insert(0, personal_dir)
    from stock_analysis_fmp import FMPStockAnalyzer
    from stock_technical_analysis import FMPTechnicalAnalyzer


class StockComparisonAnalyzer:
    """Analyze and compare multiple stocks"""
    
    def __init__(self):
        """Initialize analyzers"""
        self.fmp_analyzer = FMPStockAnalyzer()
        self.technical_analyzer = FMPTechnicalAnalyzer()
    
    def analyze_multiple_stocks(self, symbols: List[str], analysis_type: str = 'both') -> Dict:
        """
        Analyze multiple stocks
        
        Args:
            symbols: List of stock symbols
            analysis_type: 'fundamental', 'technical', or 'both'
        
        Returns:
            Dictionary with analysis results for each symbol
        """
        results = {}
        
        print(f"\n{'='*80}")
        print(f"ANALYZING {len(symbols)} STOCKS")
        print(f"{'='*80}\n")
        
        for idx, symbol in enumerate(symbols, 1):
            print(f"[{idx}/{len(symbols)}] Analyzing {symbol}...")
            
            try:
                symbol_data = {}
                
                if analysis_type in ['fundamental', 'both']:
                    print(f"  → Fetching fundamental data...")
                    fundamental = self.fmp_analyzer.analyze_stock(symbol)
                    symbol_data['fundamental'] = fundamental
                
                if analysis_type in ['technical', 'both']:
                    print(f"  → Fetching technical data...")
                    technical = self.technical_analyzer.analyze_stock(symbol)
                    symbol_data['technical'] = technical
                
                results[symbol] = symbol_data
                print(f"  ✓ {symbol} complete\n")
            
            except Exception as e:
                print(f"  ✗ Error analyzing {symbol}: {e}\n")
                results[symbol] = {'error': str(e)}
        
        return results
    
    def create_comparison_table(self, results: Dict, analysis_type: str = 'both') -> str:
        """
        Create markdown comparison table from results
        
        Args:
            results: Dictionary of analysis results
            analysis_type: 'fundamental', 'technical', or 'both'
        
        Returns:
            Markdown formatted comparison table
        """
        if analysis_type == 'fundamental':
            return self._create_fundamental_table(results)
        elif analysis_type == 'technical':
            return self._create_technical_table(results)
        else:
            return self._create_combined_table(results)
    
    def _create_fundamental_table(self, results: Dict) -> str:
        """Create fundamental analysis comparison table"""
        table = "## Fundamental Analysis Comparison\n\n"
        table += "| Symbol | Price | Market Cap | P/E | P/B | ROE | ROA | Debt/Equity | Revenue Growth | Profit Margin |\n"
        table += "|--------|-------|------------|-----|-----|-----|-----|-------------|----------------|---------------|\n"
        
        for symbol, data in results.items():
            if 'error' in data:
                table += f"| {symbol} | Error | - | - | - | - | - | - | - | - |\n"
                continue
            
            fundamental = data.get('fundamental', {})
            profile = fundamental.get('profile', {})
            ratios = fundamental.get('ratios', [{}])[0] if fundamental.get('ratios') else {}
            metrics = fundamental.get('key_metrics', [{}])[0] if fundamental.get('key_metrics') else {}
            
            price = profile.get('price', 'N/A')
            market_cap = profile.get('mktCap', 'N/A')
            pe = ratios.get('peRatioTTM', 'N/A')
            pb = ratios.get('priceToBookRatioTTM', 'N/A')
            roe = ratios.get('returnOnEquityTTM', 'N/A')
            roa = ratios.get('returnOnAssetsTTM', 'N/A')
            debt_equity = ratios.get('debtEquityRatioTTM', 'N/A')
            revenue_growth = metrics.get('revenueGrowth', 'N/A')
            profit_margin = ratios.get('netProfitMarginTTM', 'N/A')
            
            # Format values
            if isinstance(price, (int, float)):
                price = f"${price:.2f}"
            if isinstance(market_cap, (int, float)):
                market_cap = f"${market_cap/1e9:.2f}B" if market_cap >= 1e9 else f"${market_cap/1e6:.2f}M"
            if isinstance(pe, (int, float)):
                pe = f"{pe:.2f}"
            if isinstance(pb, (int, float)):
                pb = f"{pb:.2f}"
            if isinstance(roe, (int, float)):
                roe = f"{roe*100:.2f}%"
            if isinstance(roa, (int, float)):
                roa = f"{roa*100:.2f}%"
            if isinstance(debt_equity, (int, float)):
                debt_equity = f"{debt_equity:.2f}"
            if isinstance(revenue_growth, (int, float)):
                revenue_growth = f"{revenue_growth*100:.2f}%"
            if isinstance(profit_margin, (int, float)):
                profit_margin = f"{profit_margin*100:.2f}%"
            
            table += f"| {symbol} | {price} | {market_cap} | {pe} | {pb} | {roe} | {roa} | {debt_equity} | {revenue_growth} | {profit_margin} |\n"
        
        return table
    
    def _create_technical_table(self, results: Dict) -> str:
        """Create technical analysis comparison table"""
        table = "## Technical Analysis Comparison\n\n"
        table += "| Symbol | Price | 1D % | 1W % | 1M % | 1Y % | Trend | RSI | MACD Signal | Volume Status | Support | Resistance | Signal |\n"
        table += "|--------|-------|------|------|------|------|-------|-----|-------------|---------------|---------|------------|--------|\n"
        
        for symbol, data in results.items():
            if 'error' in data:
                table += f"| {symbol} | Error | - | - | - | - | - | - | - | - | - | - | - |\n"
                continue
            
            technical = data.get('technical', {})
            if not technical:
                table += f"| {symbol} | No Data | - | - | - | - | - | - | - | - | - | - | - |\n"
                continue
            
            indicators = technical.get('indicators', {})
            trend = technical.get('trend_analysis', {})
            signals = technical.get('trading_signals', {})
            volume = technical.get('volume_analysis', {})
            support_levels = technical.get('support_levels', [])
            resistance_levels = technical.get('resistance_levels', [])
            
            price = indicators.get('current_price', 'N/A')
            price_1d = technical.get('price_changes', {}).get('1D', None)
            price_1w = technical.get('price_changes', {}).get('1W', None)
            price_1m = technical.get('price_changes', {}).get('1M', None)
            price_1y = technical.get('price_changes', {}).get('1Y', None)
            trend_direction = trend.get('trend', 'N/A')
            rsi = indicators.get('rsi', 'N/A')
            macd_signal = indicators.get('macd_signal', 'N/A')
            volume_status = volume.get('comparison', {}).get('status', 'N/A')
            support = support_levels[0] if support_levels else 'N/A'
            resistance = resistance_levels[0] if resistance_levels else 'N/A'
            overall_signal = signals.get('overall_signal', 'N/A')
            
            # Format values
            if isinstance(price, (int, float)):
                price = f"${price:.2f}"
            if isinstance(price_1d, (int, float)):
                price_1d = f"{price_1d*100:+.2f}%"
            if isinstance(price_1w, (int, float)):
                price_1w = f"{price_1w*100:+.2f}%"
            if isinstance(price_1m, (int, float)):
                price_1m = f"{price_1m*100:+.2f}%"
            if isinstance(price_1y, (int, float)):
                price_1y = f"{price_1y*100:+.2f}%"
            if isinstance(rsi, (int, float)):
                rsi = f"{rsi:.2f}"
            if isinstance(support, (int, float)):
                support = f"${support:.2f}"
            if isinstance(resistance, (int, float)):
                resistance = f"${resistance:.2f}"
            
            table += f"| {symbol} | {price} | {price_1d or 'N/A'} | {price_1w or 'N/A'} | {price_1m or 'N/A'} | {price_1y or 'N/A'} | {trend_direction} | {rsi} | {macd_signal} | {volume_status} | {support} | {resistance} | {overall_signal} |\n"
        
        return table
    
    def _create_combined_table(self, results: Dict) -> str:
        """Create combined fundamental and technical comparison table"""
        table = "## Combined Analysis Comparison\n\n"
        table += "| Symbol | Price | Market Cap | P/E | Trend | RSI | Signal | Volume | Recommendation |\n"
        table += "|--------|-------|------------|-----|-------|-----|--------|--------|----------------|\n"
        
        for symbol, data in results.items():
            if 'error' in data:
                table += f"| {symbol} | Error | - | - | - | - | - | - | - |\n"
                continue
            
            fundamental = data.get('fundamental', {})
            technical = data.get('technical', {})
            
            # Fundamental data
            profile = fundamental.get('profile', {}) if fundamental else {}
            ratios = fundamental.get('ratios', [{}])[0] if fundamental and fundamental.get('ratios') else {}
            
            price = profile.get('price') or (technical.get('indicators', {}).get('current_price') if technical else None)
            market_cap = profile.get('mktCap', 'N/A')
            pe = ratios.get('peRatioTTM', 'N/A')
            
            # Technical data
            trend = technical.get('trend_analysis', {}) if technical else {}
            indicators = technical.get('indicators', {}) if technical else {}
            signals = technical.get('trading_signals', {}) if technical else {}
            volume = technical.get('volume_analysis', {}) if technical else {}
            
            trend_direction = trend.get('trend', 'N/A') if trend else 'N/A'
            rsi = indicators.get('rsi', 'N/A') if indicators else 'N/A'
            overall_signal = signals.get('overall_signal', 'N/A') if signals else 'N/A'
            volume_status = volume.get('comparison', {}).get('status', 'N/A') if volume else 'N/A'
            
            # Format values
            if isinstance(price, (int, float)):
                price = f"${price:.2f}"
            if isinstance(market_cap, (int, float)):
                market_cap = f"${market_cap/1e9:.2f}B" if market_cap >= 1e9 else f"${market_cap/1e6:.2f}M"
            if isinstance(pe, (int, float)):
                pe = f"{pe:.2f}"
            if isinstance(rsi, (int, float)):
                rsi = f"{rsi:.2f}"
            
            # Simple recommendation based on signal and trend
            if overall_signal == 'Buy' and trend_direction == 'Uptrend':
                recommendation = 'Strong Buy'
            elif overall_signal == 'Buy':
                recommendation = 'Buy'
            elif overall_signal == 'Sell' and trend_direction == 'Downtrend':
                recommendation = 'Strong Sell'
            elif overall_signal == 'Sell':
                recommendation = 'Sell'
            else:
                recommendation = 'Hold'
            
            table += f"| {symbol} | {price} | {market_cap} | {pe} | {trend_direction} | {rsi} | {overall_signal} | {volume_status} | {recommendation} |\n"
        
        return table
    
    def generate_comparison_report(self, symbols: List[str], analysis_type: str = 'both', output_path: Optional[str] = None) -> str:
        """
        Generate complete comparison report
        
        Args:
            symbols: List of stock symbols
            analysis_type: 'fundamental', 'technical', or 'both'
            output_path: Optional custom output path
        
        Returns:
            Path to generated report
        """
        # Analyze all stocks
        results = self.analyze_multiple_stocks(symbols, analysis_type)
        
        # Generate report
        report = f"""# Stock Comparison Analysis
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Stocks Analyzed:** {', '.join(symbols)}
**Analysis Type:** {analysis_type.title()}

---

## Executive Summary

This report compares {len(symbols)} stocks across {'fundamental and technical' if analysis_type == 'both' else analysis_type} metrics.

---

"""
        
        # Add comparison tables
        report += self.create_comparison_table(results, analysis_type)
        report += "\n\n---\n\n"
        
        # Add detailed analysis for each stock
        report += "## Detailed Analysis\n\n"
        
        for symbol in symbols:
            data = results.get(symbol, {})
            report += f"### {symbol}\n\n"
            
            if 'error' in data:
                report += f"**Error:** {data['error']}\n\n"
                continue
            
            if analysis_type in ['fundamental', 'both']:
                fundamental = data.get('fundamental', {})
                if fundamental:
                    profile = fundamental.get('profile', {})
                    report += f"**Company:** {profile.get('companyName', 'N/A')}\n"
                    report += f"**Sector:** {profile.get('sector', 'N/A')}\n"
                    report += f"**Industry:** {profile.get('industry', 'N/A')}\n\n"
            
            if analysis_type in ['technical', 'both']:
                technical = data.get('technical', {})
                if technical:
                    indicators = technical.get('indicators', {})
                    trend = technical.get('trend_analysis', {})
                    signals = technical.get('trading_signals', {})
                    
                    report += f"**Current Price:** ${indicators.get('current_price', 'N/A'):.2f}\n" if isinstance(indicators.get('current_price'), (int, float)) else f"**Current Price:** N/A\n"
                    report += f"**Trend:** {trend.get('trend', 'N/A')} ({trend.get('strength', 'N/A')})\n"
                    report += f"**RSI:** {indicators.get('rsi', 'N/A')}\n"
                    report += f"**Signal:** {signals.get('overall_signal', 'N/A')}\n\n"
            
            report += "---\n\n"
        
        # Determine output path
        if output_path is None:
            output_dir = os.path.join(os.path.expanduser('~/personal'), 'stock_analysis')
            os.makedirs(output_dir, exist_ok=True)
            
            symbols_str = '_'.join(symbols)
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            filename = f"{symbols_str}_comparison_{timestamp}.md"
            output_path = os.path.join(output_dir, filename)
        else:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save report
        with open(output_path, 'w') as f:
            f.write(report)
        
        print(f"\n{'='*80}")
        print(f"COMPARISON REPORT GENERATED")
        print(f"{'='*80}")
        print(f"📄 Report saved to: {output_path}")
        
        return output_path


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python3 stock_comparison_analyzer.py <SYMBOL1> <SYMBOL2> [SYMBOL3...] [--type fundamental|technical|both]")
        print("\nExample:")
        print("  python3 stock_comparison_analyzer.py AAPL MSFT GOOGL")
        print("  python3 stock_comparison_analyzer.py NVDA AMD --type technical")
        print("\nRequires FMP_API_KEY environment variable")
        sys.exit(1)
    
    # Parse arguments
    symbols = []
    analysis_type = 'both'
    
    for arg in sys.argv[1:]:
        if arg == '--type':
            continue
        elif arg in ['fundamental', 'technical', 'both']:
            analysis_type = arg
        else:
            symbols.append(arg.upper())
    
    if not symbols:
        print("Error: No symbols provided")
        sys.exit(1)
    
    try:
        analyzer = StockComparisonAnalyzer()
        analyzer.generate_comparison_report(symbols, analysis_type)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

