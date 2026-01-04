#!/usr/bin/env python3
"""
Stock Valuation Analyzer
Provides valuation context including PEG ratio, sector comparisons,
and historical valuation analysis.
"""

import requests
import os
from typing import Dict, Optional

try:
    from dotenv import load_dotenv
    load_dotenv()  # Load .env file if it exists
except ImportError:
    pass  # python-dotenv not installed, fall back to environment variables, List
from datetime import datetime

class ValuationAnalyzer:
    """
    Analyzes stock valuation with context
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
    
    def calculate_peg_ratio(self, pe_ratio: float, growth_rate: float) -> Optional[float]:
        """
        Calculate PEG ratio (P/E ÷ Growth Rate)
        
        Args:
            pe_ratio: Price-to-Earnings ratio
            growth_rate: Growth rate - can be:
                - Decimal multiplier (e.g., 1.142 for 114.2% growth = 14.2% annualized)
                - Percentage (e.g., 114.2 for 114.2% growth)
                - Fraction (e.g., 0.142 for 14.2% growth)
            
        Returns:
            PEG ratio or None if invalid
        """
        if growth_rate <= 0:
            return None
        
        # Handle different growth rate formats
        # If > 1, assume it's a multiplier (e.g., 1.142 = 14.2% growth)
        # If < 1, assume it's already a fraction (e.g., 0.142 = 14.2% growth)
        # If > 10, assume it's already a percentage (e.g., 114.2 = 114.2% growth)
        
        if growth_rate > 10:
            # Already a percentage (e.g., 114.2%)
            growth_percentage = growth_rate
        elif growth_rate > 1:
            # Multiplier format (e.g., 1.142 = 14.2% growth)
            growth_percentage = (growth_rate - 1) * 100
        else:
            # Fraction format (e.g., 0.142 = 14.2% growth)
            growth_percentage = growth_rate * 100
        
        if growth_percentage == 0:
            return None
        
        peg = pe_ratio / growth_percentage
        return peg
    
    def interpret_peg_ratio(self, peg_ratio: Optional[float], growth_rate: Optional[float] = None) -> Dict[str, any]:
        """
        Interpret PEG ratio with flagging of suspicious values
        
        Args:
            peg_ratio: Calculated PEG ratio
            growth_rate: Original growth rate used (for flagging cyclical recovery)
        
        Returns:
            Dict with interpretation and assessment
        """
        if peg_ratio is None:
            return {
                "value": None,
                "value_str": "N/A",
                "interpretation": "Cannot calculate (invalid growth rate)",
                "assessment": "Unknown",
                "warning": None
            }
        
        # Flag suspiciously low PEG ratios (< 0.1) as potentially erroneous
        # This often indicates cyclical recovery from low base, not sustainable growth
        warning = None
        if peg_ratio < 0.1:
            warning = "⚠️ Suspiciously low PEG ratio - likely indicates cyclical recovery from low base, not sustainable forward growth. Consider using forward earnings estimates instead of trailing growth."
            assessment = "Potentially Misleading (Cyclical Recovery)"
            interpretation = f"PEG ratio of {peg_ratio:.2f} is suspiciously low. This likely reflects recovery from cyclical lows rather than sustainable forward growth. Forward-looking estimates should be used instead of trailing growth rates."
        elif peg_ratio < 0.5:
            assessment = "Very Undervalued"
            interpretation = "Extremely cheap relative to growth"
        elif peg_ratio < 1.0:
            assessment = "Undervalued"
            interpretation = "Cheap relative to growth rate"
        elif peg_ratio < 1.5:
            assessment = "Fairly Valued"
            interpretation = "Reasonable valuation relative to growth"
        elif peg_ratio < 2.0:
            assessment = "Overvalued"
            interpretation = "Expensive relative to growth"
        else:
            assessment = "Very Overvalued"
            interpretation = "Very expensive relative to growth"
        
        # Additional warning if growth rate is extreme (>200%)
        if growth_rate and growth_rate > 200:
            if warning:
                warning += " Additionally, extreme growth rate (>200%) suggests cyclical recovery."
            else:
                warning = "⚠️ Extreme growth rate (>200%) suggests cyclical recovery from low base, not sustainable forward growth."
        
        return {
            "value": peg_ratio,
            "value_str": f"{peg_ratio:.2f}",
            "interpretation": interpretation,
            "assessment": assessment,
            "warning": warning
        }
    
    def get_sector_pe_average(self, sector: str) -> Optional[float]:
        """
        Get sector average P/E (simplified - would need sector data)
        For now, returns default tech sector average
        """
        # Default sector averages (would ideally fetch from API)
        sector_averages = {
            "Technology": 25.0,
            "Semiconductors": 30.0,
            "Internet Content & Information": 28.0,
            "Software": 35.0,
            "Hardware": 20.0
        }
        
        return sector_averages.get(sector, 25.0)  # Default tech average
    
    def compare_to_sector(
        self,
        pe_ratio: float,
        sector: str,
        pb_ratio: Optional[float] = None,
        ps_ratio: Optional[float] = None,
        eps: Optional[float] = None
    ) -> Dict[str, any]:
        """
        Compare valuation metrics to sector averages
        
        ALGORITHMIC: Selects appropriate metric based on earnings quality
        - Uses P/E when earnings are positive and meaningful
        - Uses P/S when P/E is misleading (negative/low earnings)
        
        Returns:
            Dict with comparisons and assessments
        """
        # ALGORITHMIC: Detect if P/E is misleading
        # P/E is misleading if: (1) extremely high (>100) with negative/low earnings, OR (2) negative P/E (negative earnings)
        pe_misleading = (pe_ratio > 100 and eps is not None and (eps <= 0 or eps < 0.5)) or (pe_ratio < 0)
        
        sector_pe = self.get_sector_pe_average(sector)
        
        # ALGORITHMIC: Use P/S when P/E is misleading
        if pe_misleading and ps_ratio is not None:
            # Use P/S ratio for comparison instead
            # Default sector P/S (would ideally fetch from API)
            sector_ps = self._get_sector_ps_average(sector)
            
            ps_comparison = {
                "current": ps_ratio,
                "sector_avg": sector_ps,
                "premium_discount": ((ps_ratio / sector_ps) - 1) * 100 if sector_ps else None,
                "multiple": ps_ratio / sector_ps if sector_ps else None,
                "metric_used": "P/S Ratio (P/E misleading due to negative/low earnings)"
            }
            
            if ps_comparison["premium_discount"]:
                if ps_comparison["premium_discount"] > 50:
                    ps_assessment = "Significantly Premium"
                elif ps_comparison["premium_discount"] > 20:
                    ps_assessment = "Premium"
                elif ps_comparison["premium_discount"] > -20:
                    ps_assessment = "In-Line"
                elif ps_comparison["premium_discount"] > -50:
                    ps_assessment = "Discount"
                else:
                    ps_assessment = "Significant Discount"
            else:
                ps_assessment = "Unknown"
            
            ps_comparison["assessment"] = ps_assessment
            
            return {
                "pe_ratio": {
                    "current": pe_ratio,
                    "sector_avg": sector_pe,
                    "premium_discount": None,
                    "multiple": None,
                    "assessment": "Misleading (negative/low earnings)",
                    "note": "P/E ratio not meaningful due to negative or very low earnings"
                },
                "ps_ratio": ps_comparison,
                "sector": sector,
                "primary_metric": "ps_ratio",
                "pe_misleading": True,
                "note": "Using P/S ratio for sector comparison as P/E is misleading. Sector averages are estimates."
            }
        
        # Standard P/E comparison when earnings are meaningful
        pe_comparison = {
            "current": pe_ratio,
            "sector_avg": sector_pe,
            "premium_discount": ((pe_ratio / sector_pe) - 1) * 100 if sector_pe else None,
            "multiple": pe_ratio / sector_pe if sector_pe else None
        }
        
        if pe_comparison["premium_discount"]:
            if pe_comparison["premium_discount"] > 50:
                pe_assessment = "Significantly Premium"
            elif pe_comparison["premium_discount"] > 20:
                pe_assessment = "Premium"
            elif pe_comparison["premium_discount"] > -20:
                pe_assessment = "In-Line"
            elif pe_comparison["premium_discount"] > -50:
                pe_assessment = "Discount"
            else:
                pe_assessment = "Significant Discount"
        else:
            pe_assessment = "Unknown"
        
        pe_comparison["assessment"] = pe_assessment
        
        return {
            "pe_ratio": pe_comparison,
            "sector": sector,
            "primary_metric": "pe_ratio",
            "pe_misleading": False,
            "note": "Sector averages are estimates. Actual sector data would require additional API calls."
        }
    
    def _get_sector_ps_average(self, sector: str) -> float:
        """
        Get sector average P/S ratio (simplified - would need sector data)
        For now, returns default tech sector average
        """
        # Default sector P/S averages (would ideally fetch from API)
        sector_ps_averages = {
            "Technology": 5.0,
            "Semiconductors": 6.0,
            "Internet Content & Information": 7.0,
            "Software": 8.0,
            "Hardware": 3.0
        }
        
        return sector_ps_averages.get(sector, 5.0)  # Default tech average
    
    def analyze_valuation(
        self,
        symbol: str,
        pe_ratio: float,
        growth_rate: float,
        sector: str,
        pb_ratio: Optional[float] = None,
        ps_ratio: Optional[float] = None,
        eps: Optional[float] = None
    ) -> Dict[str, any]:
        """
        Comprehensive valuation analysis
        
        ALGORITHMIC: Detects misleading P/E and flags valuation score accordingly
        
        Returns:
            Complete valuation analysis dict
        """
        # ALGORITHMIC: Detect if P/E is misleading
        # P/E is misleading if: (1) extremely high (>100) with negative/low earnings, OR (2) negative P/E (negative earnings)
        pe_misleading = (pe_ratio > 100 and eps is not None and (eps <= 0 or eps < 0.5)) or (pe_ratio < 0)
        
        # Calculate PEG (may be misleading if P/E is misleading)
        peg_ratio = self.calculate_peg_ratio(pe_ratio, growth_rate)
        peg_interpretation = self.interpret_peg_ratio(peg_ratio, growth_rate)
        
        # Sector comparison (algorithmically selects P/S when P/E misleading)
        sector_comparison = self.compare_to_sector(pe_ratio, sector, pb_ratio, ps_ratio, eps)
        
        # Overall assessment
        # Use P/S multiple if P/E is misleading, otherwise use P/E multiple
        if pe_misleading and sector_comparison.get("ps_ratio"):
            comparison_multiple = sector_comparison["ps_ratio"].get("multiple")
        else:
            comparison_multiple = sector_comparison["pe_ratio"].get("multiple") if sector_comparison.get("pe_ratio") else None
        
        valuation_score = self._calculate_valuation_score(
            pe_ratio,
            peg_ratio,
            comparison_multiple,
            pe_misleading=pe_misleading,
            ps_ratio=ps_ratio if pe_misleading else None
        )
        
        return {
            "symbol": symbol,
            "current_valuation": {
                "pe_ratio": pe_ratio,
                "pb_ratio": pb_ratio,
                "ps_ratio": ps_ratio
            },
            "peg_ratio": {
                "value": peg_ratio,
                **peg_interpretation
            },
            "sector_comparison": sector_comparison,
            "valuation_score": valuation_score,
            "pe_misleading": pe_misleading,  # Flag for AI interpretation
            "summary": self._generate_valuation_summary(
                pe_ratio,
                peg_ratio,
                sector_comparison,
                valuation_score
            )
        }
    
    def _calculate_valuation_score(
        self,
        pe_ratio: float,
        peg_ratio: Optional[float],
        sector_multiple: Optional[float],
        pe_misleading: bool = False,
        ps_ratio: Optional[float] = None
    ) -> Dict[str, any]:
        """
        Calculate valuation score (0-10, higher = better value)
        
        ALGORITHMIC: Flags score as potentially misleading when P/E is misleading
        """
        score = 5.0  # Start neutral
        
        # ALGORITHMIC: When P/E is misleading, use P/S-based scoring
        if pe_misleading and ps_ratio is not None:
            # Score based on P/S ratio instead
            # Typical tech P/S range: 2-10, lower is better
            if ps_ratio < 2.0:
                score += 2.0
            elif ps_ratio < 4.0:
                score += 1.0
            elif ps_ratio < 6.0:
                score += 0.0
            elif ps_ratio < 8.0:
                score -= 1.0
            else:
                score -= 2.0
            
            # Sector multiple adjustment (using P/S multiple)
            if sector_multiple:
                if sector_multiple < 0.8:
                    score += 1.5
                elif sector_multiple < 1.0:
                    score += 0.5
                elif sector_multiple < 1.2:
                    score += 0.0
                elif sector_multiple < 1.5:
                    score -= 1.0
                elif sector_multiple < 2.0:
                    score -= 2.0
                else:
                    score -= 3.0
            
            # Clamp to 0-10
            score = max(0, min(10, score))
            
            return {
                "score": round(score, 1),
                "interpretation": self._interpret_valuation_score(score),
                "pe_misleading": True,
                "note": "Score based on P/S ratio as P/E is misleading due to negative/low earnings",
                "alternative_metrics": {
                    "ps_ratio": ps_ratio,
                    "note": "Consider forward P/E estimates when available"
                }
            }
        
        # Standard scoring when P/E is meaningful
        # PEG adjustment
        if peg_ratio:
            if peg_ratio < 0.5:
                score += 2.0
            elif peg_ratio < 1.0:
                score += 1.5
            elif peg_ratio < 1.5:
                score += 0.5
            elif peg_ratio < 2.0:
                score -= 1.0
            else:
                score -= 2.0
        
        # Sector multiple adjustment
        if sector_multiple:
            if sector_multiple < 0.8:
                score += 1.5
            elif sector_multiple < 1.0:
                score += 0.5
            elif sector_multiple < 1.2:
                score += 0.0
            elif sector_multiple < 1.5:
                score -= 1.0
            elif sector_multiple < 2.0:
                score -= 2.0
            else:
                score -= 3.0
        
        # Clamp to 0-10
        score = max(0, min(10, score))
        
        return {
            "score": round(score, 1),
            "interpretation": self._interpret_valuation_score(score),
            "pe_misleading": False
        }
    
    def _interpret_valuation_score(self, score: float) -> str:
        """Interpret valuation score"""
        if score >= 8.0:
            return "Excellent Value"
        elif score >= 6.5:
            return "Good Value"
        elif score >= 5.0:
            return "Fair Value"
        elif score >= 3.5:
            return "Expensive"
        else:
            return "Very Expensive"
    
    def _generate_valuation_summary(
        self,
        pe_ratio: float,
        peg_ratio: Optional[float],
        sector_comparison: Dict,
        valuation_score: Dict
    ) -> str:
        """Generate valuation summary"""
        parts = []
        
        # PEG assessment
        if peg_ratio:
            if peg_ratio < 1.0:
                parts.append(f"PEG ratio of {peg_ratio:.2f} indicates undervaluation relative to growth")
            elif peg_ratio < 1.5:
                parts.append(f"PEG ratio of {peg_ratio:.2f} suggests fair valuation")
            else:
                parts.append(f"PEG ratio of {peg_ratio:.2f} indicates overvaluation relative to growth")
        
        # Sector comparison
        if sector_comparison["pe_ratio"]["premium_discount"]:
            premium = sector_comparison["pe_ratio"]["premium_discount"]
            if premium > 20:
                parts.append(f"Trading at {premium:.1f}% premium to sector average")
            elif premium < -20:
                parts.append(f"Trading at {abs(premium):.1f}% discount to sector average")
            else:
                parts.append("Trading in-line with sector average")
        
        # Overall
        parts.append(f"Overall valuation score: {valuation_score['score']:.1f}/10 ({valuation_score['interpretation']})")
        
        return ". ".join(parts) + "."


def main():
    """Test the valuation analyzer"""
    analyzer = ValuationAnalyzer()
    
    # Test NVDA
    print("="*80)
    print("NVDA Valuation Analysis")
    print("="*80)
    
    nvda_analysis = analyzer.analyze_valuation(
        symbol="NVDA",
        pe_ratio=47.16,
        growth_rate=114.2,  # 114.2% growth (as percentage)
        sector="Semiconductors",
        pb_ratio=36.66,
        ps_ratio=22.28
    )
    
    print(f"\nP/E Ratio: {nvda_analysis['current_valuation']['pe_ratio']}")
    peg_value = nvda_analysis['peg_ratio']['value']
    if peg_value is not None and isinstance(peg_value, (int, float)):
        print(f"PEG Ratio: {peg_value:.2f} ({nvda_analysis['peg_ratio']['assessment']})")
    else:
        peg_str = nvda_analysis['peg_ratio'].get('value_str', 'N/A')
        print(f"PEG Ratio: {peg_str} ({nvda_analysis['peg_ratio']['assessment']})")
    print(f"Sector Comparison: {nvda_analysis['sector_comparison']['pe_ratio']['assessment']}")
    print(f"Valuation Score: {nvda_analysis['valuation_score']['score']}/10 ({nvda_analysis['valuation_score']['interpretation']})")
    print(f"\nSummary: {nvda_analysis['summary']}")
    
    # Test META
    print("\n" + "="*80)
    print("META Valuation Analysis")
    print("="*80)
    
    meta_analysis = analyzer.analyze_valuation(
        symbol="META",
        pe_ratio=29.32,
        growth_rate=21.9,  # 21.9% growth (as percentage)
        sector="Internet Content & Information",
        pb_ratio=8.12,
        ps_ratio=9.02
    )
    
    print(f"\nP/E Ratio: {meta_analysis['current_valuation']['pe_ratio']}")
    peg_value = meta_analysis['peg_ratio']['value']
    if peg_value is not None and isinstance(peg_value, (int, float)):
        print(f"PEG Ratio: {peg_value:.2f} ({meta_analysis['peg_ratio']['assessment']})")
    else:
        peg_str = meta_analysis['peg_ratio'].get('value_str', 'N/A')
        print(f"PEG Ratio: {peg_str} ({meta_analysis['peg_ratio']['assessment']})")
    print(f"Sector Comparison: {meta_analysis['sector_comparison']['pe_ratio']['assessment']}")
    print(f"Valuation Score: {meta_analysis['valuation_score']['score']}/10 ({meta_analysis['valuation_score']['interpretation']})")
    print(f"\nSummary: {meta_analysis['summary']}")


if __name__ == "__main__":
    main()

