#!/usr/bin/env python3
"""
Stock Recommendation Engine
Provides consistent, quantitative recommendation scoring based on fundamental,
technical, valuation, and risk factors.
"""

from typing import Dict, Tuple, Optional
from enum import Enum

class Recommendation(Enum):
    STRONG_BUY = "Strong Buy"
    BUY = "Buy"
    HOLD = "Hold"
    SELL = "Sell"

class ConfidenceLevel(Enum):
    VERY_HIGH = "Very High"
    HIGH = "High"
    MEDIUM_HIGH = "Medium-High"
    MEDIUM = "Medium"
    MEDIUM_LOW = "Medium-Low"
    LOW = "Low"

class RiskLevel(Enum):
    VERY_LOW = "Very Low"
    LOW = "Low"
    MEDIUM = "Medium"
    MEDIUM_HIGH = "Medium-High"
    HIGH = "High"
    VERY_HIGH = "Very High"

class StockRecommendationEngine:
    """
    Calculates stock recommendations using consistent scoring logic
    """
    
    def __init__(self):
        self.sector_avg_pe = 25.0  # Default tech sector average, can be overridden
        
    def calculate_recommendation(
        self,
        fundamental_score: float,
        technical_score: float,
        valuation_risk: float,
        overall_risk: RiskLevel,
        pe_ratio: Optional[float] = None,
        sector_avg_pe: Optional[float] = None,
        trajectory_score: Optional[float] = None,
        trajectory_momentum: Optional[str] = None
    ) -> Tuple[Recommendation, ConfidenceLevel, str]:
        """
        Calculate recommendation based on scores and risk factors
        
        Args:
            fundamental_score: Score out of 10
            technical_score: Score out of 10
            valuation_risk: Valuation multiple vs sector (e.g., 1.5 = 50% premium)
            overall_risk: Risk level enum
            pe_ratio: Current P/E ratio (optional)
            sector_avg_pe: Sector average P/E (optional)
            
        Returns:
            Tuple of (Recommendation, ConfidenceLevel, Rationale)
        """
        
        # Use provided sector average or default
        if sector_avg_pe:
            self.sector_avg_pe = sector_avg_pe
        
        # Adaptive weighting based on fundamental strength
        # Strong fundamentals get more weight (quality company)
        if fundamental_score >= 7.5:
            fundamental_weight = 0.60
            technical_weight = 0.30
            valuation_weight = 0.10
        elif fundamental_score >= 5.0:
            # Balanced weighting
            fundamental_weight = 0.50
            technical_weight = 0.40
            valuation_weight = 0.10
        else:
            # Weak fundamentals, technicals matter more
            fundamental_weight = 0.40
            technical_weight = 0.50
            valuation_weight = 0.10
        
        # Calculate composite score with adaptive weights
        composite_score = (fundamental_score * fundamental_weight) + (technical_score * technical_weight) + (10 - valuation_risk * 10) * valuation_weight
        
        # Risk adjustment
        risk_adjustment = self._get_risk_adjustment(overall_risk)
        adjusted_score = composite_score * risk_adjustment
        
        # Trajectory adjustment (if available)
        trajectory_adjustment = 0.0
        if trajectory_momentum == "improving" and trajectory_score and trajectory_score >= 7.0:
            # Improving trajectory with strong score: upgrade potential
            trajectory_adjustment = 0.3
        elif trajectory_momentum == "deteriorating" and trajectory_score and trajectory_score <= 5.0:
            # Deteriorating trajectory: downgrade potential
            trajectory_adjustment = -0.3
        
        # Apply trajectory adjustment to adjusted score
        if trajectory_adjustment != 0.0:
            adjusted_score = max(0.0, min(10.0, adjusted_score + trajectory_adjustment))
        
        # Determine recommendation
        recommendation, confidence, rationale = self._determine_recommendation(
            fundamental_score,
            technical_score,
            valuation_risk,
            overall_risk,
            adjusted_score,
            pe_ratio,
            fundamental_weight,  # Pass weight for override logic
            trajectory_momentum,
            trajectory_score
        )
        
        return recommendation, confidence, rationale
    
    def _get_risk_adjustment(self, risk_level: RiskLevel) -> float:
        """Get risk adjustment multiplier"""
        adjustments = {
            RiskLevel.VERY_LOW: 1.1,
            RiskLevel.LOW: 1.05,
            RiskLevel.MEDIUM: 1.0,
            RiskLevel.MEDIUM_HIGH: 0.95,
            RiskLevel.HIGH: 0.85,
            RiskLevel.VERY_HIGH: 0.75
        }
        return adjustments.get(risk_level, 1.0)
    
    def _determine_recommendation(
        self,
        fundamental_score: float,
        technical_score: float,
        valuation_risk: float,
        overall_risk: RiskLevel,
        adjusted_score: float,
        pe_ratio: Optional[float],
        fundamental_weight: float = 0.5,
        trajectory_momentum: Optional[str] = None,
        trajectory_score: Optional[float] = None
    ) -> Tuple[Recommendation, ConfidenceLevel, str]:
        """
        Determine recommendation using consistent logic
        """
        
        rationale_parts = []
        
        # Strong Buy Criteria
        if (fundamental_score >= 9.0 and 
            technical_score >= 8.0 and 
            valuation_risk <= 1.2 and 
            overall_risk.value in ["Very Low", "Low", "Medium"]):
            
            confidence = ConfidenceLevel.HIGH if adjusted_score >= 8.5 else ConfidenceLevel.MEDIUM_HIGH
            rationale_parts.append(f"Exceptional fundamentals ({fundamental_score:.1f}/10) and strong technicals ({technical_score:.1f}/10)")
            if valuation_risk <= 1.0:
                rationale_parts.append("Reasonable valuation")
            else:
                rationale_parts.append(f"Premium valuation ({valuation_risk:.2f}x sector) justified by exceptional fundamentals")
            
            return Recommendation.STRONG_BUY, confidence, ". ".join(rationale_parts) + "."
        
        # Buy Criteria
        buy_condition_1 = (fundamental_score >= 8.0 and technical_score >= 7.0 and valuation_risk <= 1.5)
        buy_condition_2 = (fundamental_score >= 9.0 and technical_score >= 6.0 and valuation_risk <= 1.3)
        buy_condition_3 = (fundamental_score >= 7.5 and technical_score >= 7.5 and valuation_risk <= 1.2)
        # NEW: Trajectory-based upgrade (improving trajectory with moderate fundamentals)
        buy_condition_4 = (trajectory_momentum == "improving" and 
                           trajectory_score and trajectory_score >= 7.0 and
                           fundamental_score >= 6.5 and technical_score >= 6.0 and valuation_risk <= 1.5)
        
        if (buy_condition_1 or buy_condition_2 or buy_condition_3 or buy_condition_4) and overall_risk.value != "Very High":
            
            confidence = self._calculate_confidence(fundamental_score, technical_score, adjusted_score)
            
            if buy_condition_1:
                rationale_parts.append(f"Strong fundamentals ({fundamental_score:.1f}/10) and good technicals ({technical_score:.1f}/10)")
            elif buy_condition_2:
                rationale_parts.append(f"Exceptional fundamentals ({fundamental_score:.1f}/10) offsetting weaker technicals ({technical_score:.1f}/10)")
            elif buy_condition_4:
                rationale_parts.append(f"Improving trajectory (score {trajectory_score:.1f}/10) with solid fundamentals ({fundamental_score:.1f}/10) and technicals ({technical_score:.1f}/10)")
            else:
                rationale_parts.append(f"Balanced strong fundamentals ({fundamental_score:.1f}/10) and technicals ({technical_score:.1f}/10)")
            
            if valuation_risk > 1.2:
                rationale_parts.append(f"Premium valuation ({valuation_risk:.2f}x sector) requires continued strong performance")
            else:
                rationale_parts.append("Reasonable valuation")
            
            return Recommendation.BUY, confidence, ". ".join(rationale_parts) + "."
        
        # Hold Criteria
        hold_condition_1 = (fundamental_score >= 7.0 and technical_score >= 6.0)
        hold_condition_2 = (fundamental_score >= 6.0 and technical_score >= 7.0)
        hold_condition_3 = (fundamental_score >= 8.0 and technical_score >= 5.0 and valuation_risk > 1.5)
        # NEW: Deteriorating trajectory downgrades to HOLD
        hold_condition_4 = (trajectory_momentum == "deteriorating" and 
                           trajectory_score and trajectory_score <= 5.0 and
                           fundamental_score >= 7.0)  # Would be BUY but trajectory concerns
        
        if hold_condition_1 or hold_condition_2 or hold_condition_3 or hold_condition_4:
            
            confidence = self._calculate_confidence(fundamental_score, technical_score, adjusted_score)
            
            if hold_condition_4:
                rationale_parts.append(f"Strong fundamentals ({fundamental_score:.1f}/10) but deteriorating trajectory (score {trajectory_score:.1f}/10) suggests caution")
            elif fundamental_score >= 8.0 and technical_score < 6.0:
                rationale_parts.append(f"Strong fundamentals ({fundamental_score:.1f}/10) but weak technicals ({technical_score:.1f}/10)")
                if valuation_risk > 1.5:
                    rationale_parts.append(f"Premium valuation ({valuation_risk:.2f}x sector) combined with technical weakness suggests waiting for better entry")
            elif technical_score >= 7.0 and fundamental_score < 7.0:
                rationale_parts.append(f"Good technicals ({technical_score:.1f}/10) but moderate fundamentals ({fundamental_score:.1f}/10)")
            else:
                rationale_parts.append(f"Moderate fundamentals ({fundamental_score:.1f}/10) and technicals ({technical_score:.1f}/10)")
            
            if valuation_risk > 1.5:
                rationale_parts.append(f"Premium valuation ({valuation_risk:.2f}x sector) limits upside potential")
            
            return Recommendation.HOLD, confidence, ". ".join(rationale_parts) + "."
        
        # Sell Criteria
        if (fundamental_score <= 5.0 or 
            technical_score <= 4.0 or 
            overall_risk == RiskLevel.VERY_HIGH or
            (fundamental_score <= 6.0 and technical_score <= 5.0 and valuation_risk > 2.0)):
            
            confidence = ConfidenceLevel.MEDIUM if adjusted_score < 5.0 else ConfidenceLevel.MEDIUM_LOW
            
            if fundamental_score <= 5.0:
                rationale_parts.append(f"Weak fundamentals ({fundamental_score:.1f}/10)")
            if technical_score <= 4.0:
                rationale_parts.append(f"Poor technicals ({technical_score:.1f}/10)")
            if valuation_risk > 2.0:
                rationale_parts.append(f"Extreme valuation premium ({valuation_risk:.2f}x sector)")
            if overall_risk == RiskLevel.VERY_HIGH:
                rationale_parts.append("Very high risk level")
            
            return Recommendation.SELL, confidence, ". ".join(rationale_parts) + "."
        
        # Default Hold
        confidence = ConfidenceLevel.MEDIUM
        rationale = f"Mixed signals: Fundamentals {fundamental_score:.1f}/10, Technicals {technical_score:.1f}/10. Awaiting clearer direction."
        return Recommendation.HOLD, confidence, rationale
    
    def _calculate_confidence(
        self,
        fundamental_score: float,
        technical_score: float,
        adjusted_score: float
    ) -> ConfidenceLevel:
        """Calculate confidence level"""
        
        score_diff = abs(fundamental_score - technical_score)
        avg_score = (fundamental_score + technical_score) / 2
        
        # High confidence: scores align and both strong
        if score_diff <= 1.0 and avg_score >= 8.0:
            return ConfidenceLevel.HIGH
        
        # Medium-High: scores align or one very strong
        if (score_diff <= 1.5 and avg_score >= 7.0) or max(fundamental_score, technical_score) >= 9.0:
            return ConfidenceLevel.MEDIUM_HIGH
        
        # Medium: moderate scores
        if avg_score >= 6.5:
            return ConfidenceLevel.MEDIUM
        
        # Medium-Low: lower scores
        return ConfidenceLevel.MEDIUM_LOW
    
    def calculate_valuation_risk(self, pe_ratio: float, sector_avg_pe: float, 
                                 pe_misleading: bool = False, ps_ratio: Optional[float] = None,
                                 sector_avg_ps: Optional[float] = None) -> float:
        """
        Calculate valuation risk as multiple of sector average
        
        ALGORITHMIC: Uses P/S ratio when P/E is misleading
        
        Args:
            pe_ratio: P/E ratio
            sector_avg_pe: Sector average P/E
            pe_misleading: Whether P/E is misleading (negative/low earnings)
            ps_ratio: P/S ratio (used when P/E misleading)
            sector_avg_ps: Sector average P/S (used when P/E misleading)
        
        Returns:
            Multiple (e.g., 1.5 = 50% premium, 0.8 = 20% discount)
        """
        # ALGORITHMIC: Use P/S when P/E is misleading
        if pe_misleading and ps_ratio is not None and sector_avg_ps is not None and sector_avg_ps > 0:
            return ps_ratio / sector_avg_ps
        
        # Standard P/E-based calculation
        if sector_avg_pe == 0:
            return 1.0  # Default neutral
        return pe_ratio / sector_avg_pe
    
    def assess_overall_risk(
        self,
        valuation_risk: float,
        technical_risk: str,
        fundamental_concerns: list,
        market_risk: str = "Medium"
    ) -> RiskLevel:
        """
        Assess overall risk level
        
        Args:
            valuation_risk: Valuation multiple vs sector
            technical_risk: "Low", "Medium", "High"
            fundamental_concerns: List of fundamental risk factors
            market_risk: Market risk level
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


def main():
    """Test the recommendation engine"""
    engine = StockRecommendationEngine()
    
    # Test Case 1: NVDA
    print("="*80)
    print("Test Case 1: NVDA")
    print("="*80)
    print("Fundamental Score: 9.0/10")
    print("Technical Score: 8.0/10")
    print("P/E Ratio: 47.16")
    print("Sector Avg P/E: 25.0")
    
    valuation_risk = engine.calculate_valuation_risk(47.16, 25.0)
    overall_risk = engine.assess_overall_risk(
        valuation_risk=valuation_risk,
        technical_risk="Low",
        fundamental_concerns=["Premium valuation"],
        market_risk="Medium"
    )
    
    rec, conf, rationale = engine.calculate_recommendation(
        fundamental_score=9.0,
        technical_score=8.0,
        valuation_risk=valuation_risk,
        overall_risk=overall_risk,
        pe_ratio=47.16,
        sector_avg_pe=25.0
    )
    
    print(f"\nRecommendation: {rec.value}")
    print(f"Confidence: {conf.value}")
    print(f"Rationale: {rationale}")
    print(f"Valuation Risk: {valuation_risk:.2f}x sector average")
    print(f"Overall Risk: {overall_risk.value}")
    
    # Test Case 2: META
    print("\n" + "="*80)
    print("Test Case 2: META")
    print("="*80)
    print("Fundamental Score: 8.0/10")
    print("Technical Score: 6.5/10")
    print("P/E Ratio: 29.32")
    print("Sector Avg P/E: 25.0")
    
    valuation_risk = engine.calculate_valuation_risk(29.32, 25.0)
    overall_risk = engine.assess_overall_risk(
        valuation_risk=valuation_risk,
        technical_risk="Medium",
        fundamental_concerns=[],
        market_risk="Medium"
    )
    
    rec, conf, rationale = engine.calculate_recommendation(
        fundamental_score=8.0,
        technical_score=6.5,
        valuation_risk=valuation_risk,
        overall_risk=overall_risk,
        pe_ratio=29.32,
        sector_avg_pe=25.0
    )
    
    print(f"\nRecommendation: {rec.value}")
    print(f"Confidence: {conf.value}")
    print(f"Rationale: {rationale}")
    print(f"Valuation Risk: {valuation_risk:.2f}x sector average")
    print(f"Overall Risk: {overall_risk.value}")


if __name__ == "__main__":
    main()

