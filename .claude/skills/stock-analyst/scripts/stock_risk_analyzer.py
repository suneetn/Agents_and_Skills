#!/usr/bin/env python3
"""
Stock Risk Analyzer
Quantifies risks using probability × impact matrix and provides risk mitigation strategies.
"""

from typing import Dict, List, Optional, Tuple
from enum import Enum
from datetime import datetime

class RiskLevel(Enum):
    VERY_LOW = "Very Low"
    LOW = "Low"
    MEDIUM = "Medium"
    MEDIUM_HIGH = "Medium-High"
    HIGH = "High"
    VERY_HIGH = "Very High"

class ProbabilityLevel(Enum):
    VERY_LOW = "Very Low"
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    VERY_HIGH = "Very High"

class ImpactLevel(Enum):
    VERY_LOW = "Very Low"
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    VERY_HIGH = "Very High"

class RiskAnalyzer:
    """
    Analyzes and quantifies stock risks
    """
    
    def __init__(self):
        """Initialize risk analyzer"""
        pass
    
    def quantify_risk(self, probability: ProbabilityLevel, impact: ImpactLevel) -> Dict:
        """
        Quantify risk using probability × impact matrix
        
        Returns:
            Dict with risk score, level, and assessment
        """
        # Map to numeric values
        prob_values = {
            ProbabilityLevel.VERY_LOW: 1,
            ProbabilityLevel.LOW: 2,
            ProbabilityLevel.MEDIUM: 3,
            ProbabilityLevel.HIGH: 4,
            ProbabilityLevel.VERY_HIGH: 5
        }
        
        impact_values = {
            ImpactLevel.VERY_LOW: 1,
            ImpactLevel.LOW: 2,
            ImpactLevel.MEDIUM: 3,
            ImpactLevel.HIGH: 4,
            ImpactLevel.VERY_HIGH: 5
        }
        
        # Calculate risk score
        risk_score = prob_values[probability] * impact_values[impact]
        
        # Determine risk level
        if risk_score <= 2:
            risk_level = RiskLevel.VERY_LOW
        elif risk_score <= 4:
            risk_level = RiskLevel.LOW
        elif risk_score <= 9:
            risk_level = RiskLevel.MEDIUM
        elif risk_score <= 16:
            risk_level = RiskLevel.MEDIUM_HIGH
        elif risk_score <= 20:
            risk_level = RiskLevel.HIGH
        else:
            risk_level = RiskLevel.VERY_HIGH
        
        return {
            'risk_score': risk_score,
            'risk_level': risk_level,
            'probability': probability.value,
            'impact': impact.value,
            'assessment': self._assess_risk(risk_score)
        }
    
    def _assess_risk(self, risk_score: int) -> str:
        """Assess risk based on score"""
        if risk_score <= 2:
            return "Minimal risk, unlikely to significantly impact investment"
        elif risk_score <= 4:
            return "Low risk, minor impact expected"
        elif risk_score <= 9:
            return "Moderate risk, requires monitoring"
        elif risk_score <= 16:
            return "High risk, significant impact possible"
        else:
            return "Very high risk, could materially impact investment"
    
    def create_risk_matrix(self, risks: List[Dict]) -> Dict:
        """
        Create probability × impact matrix for multiple risks
        
        Args:
            risks: List of risk dicts with 'name', 'probability', 'impact' keys
        
        Returns:
            Risk matrix with prioritized risks
        """
        quantified_risks = []
        
        for risk in risks:
            quantified = self.quantify_risk(
                ProbabilityLevel[risk['probability'].upper().replace('-', '_')],
                ImpactLevel[risk['impact'].upper().replace('-', '_')]
            )
            quantified_risks.append({
                'name': risk['name'],
                'description': risk.get('description', ''),
                **quantified
            })
        
        # Sort by risk score (highest first)
        quantified_risks.sort(key=lambda x: x['risk_score'], reverse=True)
        
        return {
            'risks': quantified_risks,
            'total_risks': len(quantified_risks),
            'high_risk_count': len([r for r in quantified_risks if r['risk_level'] in [RiskLevel.HIGH, RiskLevel.VERY_HIGH]]),
            'top_risks': quantified_risks[:5]  # Top 5 risks
        }
    
    def prioritize_risks(self, risk_matrix: Dict) -> List[Dict]:
        """Prioritize risks by score"""
        return risk_matrix['top_risks']
    
    def risk_mitigation_strategies(self, risk: Dict) -> List[str]:
        """
        Generate risk mitigation strategies for a specific risk
        
        Args:
            risk: Risk dict with 'name', 'risk_level', 'probability', 'impact'
        
        Returns:
            List of mitigation strategies
        """
        strategies = []
        risk_level = risk['risk_level']
        
        # General strategies based on risk level
        if risk_level in [RiskLevel.HIGH, RiskLevel.VERY_HIGH]:
            strategies.append("Consider reducing position size")
            strategies.append("Set tighter stop-loss levels")
            strategies.append("Monitor closely for early warning signs")
            strategies.append("Diversify exposure to this risk")
        
        if risk_level in [RiskLevel.MEDIUM, RiskLevel.MEDIUM_HIGH]:
            strategies.append("Monitor regularly")
            strategies.append("Have exit strategy ready")
            strategies.append("Consider hedging if appropriate")
        
        # Risk-specific strategies
        risk_name_lower = risk['name'].lower()
        
        if 'valuation' in risk_name_lower:
            strategies.append("Wait for better entry point if valuation improves")
            strategies.append("Consider dollar-cost averaging")
        
        if 'technical' in risk_name_lower:
            strategies.append("Wait for technical confirmation before entry")
            strategies.append("Use technical levels as stop-loss points")
        
        if 'fundamental' in risk_name_lower:
            strategies.append("Monitor quarterly earnings closely")
            strategies.append("Review financial metrics regularly")
        
        if 'regulatory' in risk_name_lower or 'legal' in risk_name_lower:
            strategies.append("Stay informed on regulatory developments")
            strategies.append("Consider regulatory risk in position sizing")
        
        if 'market' in risk_name_lower or 'economic' in risk_name_lower:
            strategies.append("Diversify across sectors/geographies")
            strategies.append("Consider defensive positioning")
        
        return strategies
    
    def assess_overall_risk(
        self,
        valuation_risk: float,
        technical_risk: str,
        fundamental_concerns: List[str],
        market_risk: str = "Medium"
    ) -> RiskLevel:
        """
        Assess overall risk level (same as in recommendation engine for consistency)
        """
        risk_score = 0
        
        # Valuation risk
        if valuation_risk >= 2.0:
            risk_score += 3
        elif valuation_risk >= 1.5:
            risk_score += 2
        elif valuation_risk >= 1.2:
            risk_score += 1
        
        # Technical risk
        if technical_risk == "High":
            risk_score += 2
        elif technical_risk == "Medium":
            risk_score += 1
        
        # Fundamental concerns
        risk_score += len(fundamental_concerns)
        
        # Market risk
        if market_risk == "High":
            risk_score += 2
        elif market_risk == "Medium":
            risk_score += 1
        
        # Map to risk level
        if risk_score >= 6:
            return RiskLevel.VERY_HIGH
        elif risk_score >= 4:
            return RiskLevel.HIGH
        elif risk_score >= 3:
            return RiskLevel.MEDIUM_HIGH
        elif risk_score >= 2:
            return RiskLevel.MEDIUM
        elif risk_score >= 1:
            return RiskLevel.LOW
        else:
            return RiskLevel.VERY_LOW
    
    def analyze_risks(
        self,
        symbol: str,
        fundamental_data: Dict = None,
        technical_data: Dict = None,
        valuation_data: Dict = None
    ) -> Dict:
        """
        Comprehensive risk analysis
        
        Args:
            symbol: Stock symbol
            fundamental_data: Fundamental analysis data
            technical_data: Technical analysis data
            valuation_data: Valuation analysis data
        """
        print(f"\n{'='*80}")
        print(f"RISK ANALYSIS: {symbol}")
        print(f"{'='*80}\n")
        
        risks = []
        
        # Valuation risks
        if valuation_data:
            pe_ratio = valuation_data.get('pe_ratio')
            peg_ratio = valuation_data.get('peg_ratio')
            sector_multiple = valuation_data.get('sector_multiple')
            
            if pe_ratio and sector_multiple:
                if sector_multiple >= 2.0:
                    risks.append({
                        'name': 'Valuation Risk',
                        'description': f'Stock trades at {sector_multiple:.2f}x sector average P/E',
                        'probability': 'High',
                        'impact': 'High'
                    })
                elif sector_multiple >= 1.5:
                    risks.append({
                        'name': 'Valuation Risk',
                        'description': f'Stock trades at {sector_multiple:.2f}x sector average P/E',
                        'probability': 'Medium',
                        'impact': 'Medium'
                    })
            
            if peg_ratio and isinstance(peg_ratio, (int, float)) and peg_ratio > 2.0:
                risks.append({
                    'name': 'Growth Valuation Risk',
                    'description': f'PEG ratio of {peg_ratio:.2f} indicates overvaluation relative to growth',
                    'probability': 'Medium',
                    'impact': 'High'
                })
        
        # Technical risks
        if technical_data:
            trend = technical_data.get('trend_analysis', {}).get('trend')
            rsi = technical_data.get('indicators', {}).get('rsi')
            
            if trend == 'Downtrend':
                risks.append({
                    'name': 'Technical Risk',
                    'description': 'Stock is in downtrend',
                    'probability': 'Medium',
                    'impact': 'Medium'
                })
            
            if rsi and rsi > 70:
                risks.append({
                    'name': 'Overbought Risk',
                    'description': f'RSI of {rsi:.1f} indicates overbought conditions',
                    'probability': 'Medium',
                    'impact': 'Low'
                })
        
        # Fundamental risks
        if fundamental_data:
            debt_equity = fundamental_data.get('debt_equity')
            current_ratio = fundamental_data.get('current_ratio')
            
            if debt_equity and debt_equity > 1.0:
                risks.append({
                    'name': 'Leverage Risk',
                    'description': f'Debt-to-equity ratio of {debt_equity:.2f} indicates high leverage',
                    'probability': 'Low',
                    'impact': 'High'
                })
            
            if current_ratio and current_ratio < 1.0:
                risks.append({
                    'name': 'Liquidity Risk',
                    'description': f'Current ratio of {current_ratio:.2f} indicates liquidity concerns',
                    'probability': 'Medium',
                    'impact': 'High'
                })
        
        # Create risk matrix
        if risks:
            risk_matrix = self.create_risk_matrix(risks)
            
            print("📊 RISK MATRIX (Probability × Impact)")
            print("-" * 80)
            print(f"Total Risks Identified: {risk_matrix['total_risks']}")
            print(f"High Risk Count: {risk_matrix['high_risk_count']}")
            print()
            
            print("Top Risks:")
            for i, risk in enumerate(risk_matrix['top_risks'], 1):
                print(f"\n{i}. {risk['name']}")
                print(f"   Description: {risk.get('description', 'N/A')}")
                print(f"   Risk Score: {risk['risk_score']}/25")
                print(f"   Risk Level: {risk['risk_level'].value}")
                print(f"   Probability: {risk['probability']}")
                print(f"   Impact: {risk['impact']}")
                print(f"   Assessment: {risk['assessment']}")
                
                # Mitigation strategies
                strategies = self.risk_mitigation_strategies(risk)
                if strategies:
                    print(f"   Mitigation Strategies:")
                    for strategy in strategies:
                        print(f"     • {strategy}")
        else:
            print("No significant risks identified")
            risk_matrix = {'risks': [], 'total_risks': 0, 'high_risk_count': 0, 'top_risks': []}
        
        print()
        print(f"{'='*80}")
        print(f"Analysis completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}\n")
        
        return risk_matrix


def main():
    """Test the risk analyzer"""
    analyzer = RiskAnalyzer()
    
    # Test risk quantification
    print("="*80)
    print("Risk Quantification Test")
    print("="*80)
    
    risk = analyzer.quantify_risk(ProbabilityLevel.HIGH, ImpactLevel.HIGH)
    print(f"Risk Score: {risk['risk_score']}/25")
    print(f"Risk Level: {risk['risk_level'].value}")
    print(f"Assessment: {risk['assessment']}")
    
    # Test risk matrix
    print("\n" + "="*80)
    print("Risk Matrix Test")
    print("="*80)
    
    risks = [
        {
            'name': 'Valuation Risk',
            'description': 'Stock trades at premium valuation',
            'probability': 'High',
            'impact': 'Medium'
        },
        {
            'name': 'Technical Risk',
            'description': 'Stock in downtrend',
            'probability': 'Medium',
            'impact': 'High'
        }
    ]
    
    matrix = analyzer.create_risk_matrix(risks)
    print(f"Total Risks: {matrix['total_risks']}")
    print(f"Top Risks: {len(matrix['top_risks'])}")
    
    for risk in matrix['top_risks']:
        print(f"\n{risk['name']}: {risk['risk_level'].value} (Score: {risk['risk_score']})")
        strategies = analyzer.risk_mitigation_strategies(risk)
        print("Mitigation Strategies:")
        for strategy in strategies:
            print(f"  • {strategy}")


if __name__ == "__main__":
    main()

