#!/usr/bin/env python3
"""
Narrative Generator for Stock Analysis
Transforms structured analysis data into compelling narrative stories
"""

from typing import Dict, List, Optional
from datetime import datetime


class NarrativeGenerator:
    """
    Generates compelling narrative stories from stock analysis data
    """
    
    def __init__(self):
        self.narrative_frameworks = {
            'turnaround': self._generate_turnaround_narrative,
            'growth': self._generate_growth_narrative,
            'value': self._generate_value_narrative,
            'momentum': self._generate_momentum_narrative,
            'cautious': self._generate_cautious_narrative,
        }
    
    def generate_narrative(
        self,
        symbol: str,
        fundamental_data: Dict,
        technical_data: Dict,
        sentiment_data: Dict,
        combined_data: Dict,
        sec_guidance: Optional[Dict] = None
    ) -> Dict[str, str]:
        """
        Generate comprehensive narrative story from analysis data
        
        Returns:
            Dict with narrative sections:
            - opening_hook: Compelling opening paragraph
            - company_story: Company background and context
            - fundamental_narrative: Story of financial performance
            - technical_narrative: Story of price action and trends
            - catalyst_story: Key catalysts and opportunities
            - risk_story: Risk factors in narrative form
            - investment_story: Investment thesis as a story
            - conclusion: Compelling conclusion
        """
        
        # Determine narrative framework based on analysis
        framework = self._determine_framework(fundamental_data, technical_data, combined_data)
        
        # Generate narrative sections
        narrative = {
            'framework': framework,
            'opening_hook': self._generate_opening_hook(symbol, fundamental_data, combined_data),
            'company_story': self._generate_company_story(symbol, fundamental_data),
            'fundamental_narrative': self._generate_fundamental_narrative(fundamental_data, framework),
            'technical_narrative': self._generate_technical_narrative(technical_data, framework),
            'catalyst_story': self._generate_catalyst_story(symbol, fundamental_data, sec_guidance),
            'risk_story': self._generate_risk_story(combined_data, fundamental_data),
            'investment_story': self._generate_investment_story(combined_data, framework),
            'conclusion': self._generate_conclusion(symbol, combined_data, framework),
        }
        
        return narrative
    
    def _determine_framework(
        self,
        fundamental_data: Dict,
        technical_data: Dict,
        combined_data: Dict
    ) -> str:
        """Determine which narrative framework to use"""
        
        fundamental_score = combined_data.get('fundamental_score', 0)
        technical_score = combined_data.get('technical_score', 0)
        recommendation = combined_data.get('recommendation', 'Hold')
        
        # Turnaround story: Weak fundamentals but improving trajectory
        if fundamental_score < 6 and combined_data.get('trajectory_data', {}).get('momentum') == 'improving':
            return 'turnaround'
        
        # Growth story: Strong fundamentals and growth
        if fundamental_score >= 7 and fundamental_data.get('growth', [{}])[0].get('revenueGrowth', 0) > 0.15:
            return 'growth'
        
        # Value story: Strong fundamentals, reasonable valuation
        if fundamental_score >= 7 and combined_data.get('valuation_risk', 1.0) < 1.2:
            return 'value'
        
        # Momentum story: Strong technicals, positive sentiment
        if technical_score >= 7 and combined_data.get('sentiment_score', 0) > 0.2:
            return 'momentum'
        
        # Cautious story: Mixed signals or concerns
        return 'cautious'
    
    def _generate_opening_hook(
        self,
        symbol: str,
        fundamental_data: Dict,
        combined_data: Dict
    ) -> str:
        """Generate compelling opening hook"""
        
        profile = fundamental_data.get('profile', {})
        company_name = profile.get('companyName', symbol)
        quote = fundamental_data.get('quote', {})
        current_price = quote.get('price', 0)
        recommendation = combined_data.get('recommendation', 'Hold')
        
        # Get key metric for hook
        growth = fundamental_data.get('growth', [{}])[0]
        revenue_growth = growth.get('revenueGrowth', 0)
        
        if revenue_growth > 0.2:
            return f"{company_name} ({symbol}) is experiencing explosive growth, with revenue surging {revenue_growth*100:.1f}% year-over-year. Trading at ${current_price:.2f}, this {profile.get('sector', 'company')} stock presents a compelling opportunity—but is the growth sustainable?"
        
        fundamental_score = combined_data.get('fundamental_score', 0)
        if fundamental_score < 5:
            return f"{company_name} ({symbol}) faces significant challenges. With fundamentals scoring just {fundamental_score}/10, the stock trades at ${current_price:.2f} amid uncertainty. Yet, there may be more to this story than meets the eye."
        
        return f"{company_name} ({symbol}) stands at a crossroads. Trading at ${current_price:.2f}, the stock presents a complex investment picture that requires careful analysis of fundamentals, technicals, and market sentiment."
    
    def _generate_company_story(
        self,
        symbol: str,
        fundamental_data: Dict
    ) -> str:
        """Generate company background story"""
        
        profile = fundamental_data.get('profile', {})
        company_name = profile.get('companyName', symbol)
        sector = profile.get('sector', '')
        industry = profile.get('industry', '')
        description = profile.get('description', '')
        
        story = f"{company_name} operates in the {industry} sector"
        if sector:
            story += f" within the broader {sector} industry"
        
        if description:
            # Use first 200 chars of description
            desc_short = description[:200].rsplit(' ', 1)[0] + '...'
            story += f". {desc_short}"
        
        quote = fundamental_data.get('quote', {})
        market_cap = quote.get('marketCap', 0)
        if market_cap:
            if market_cap > 10_000_000_000:
                size = "large-cap"
            elif market_cap > 2_000_000_000:
                size = "mid-cap"
            else:
                size = "small-cap"
            story += f" As a {size} company with a market capitalization of ${market_cap/1_000_000_000:.2f}B, {company_name} plays a significant role in its market."
        
        return story
    
    def _generate_fundamental_narrative(
        self,
        fundamental_data: Dict,
        framework: str
    ) -> str:
        """Generate fundamental analysis narrative"""
        
        ratios = fundamental_data.get('ratios', [{}])[0]
        growth = fundamental_data.get('growth', [{}])[0]
        quote = fundamental_data.get('quote', {})
        
        roe = ratios.get('returnOnEquity', 0)
        revenue_growth = growth.get('revenueGrowth', 0)
        net_income_growth = growth.get('netIncomeGrowth', 0)
        
        narrative = "The financial picture reveals "
        
        if framework == 'turnaround':
            if revenue_growth > 0:
                narrative += f"a company in transition. Revenue growth of {revenue_growth*100:.1f}% shows promise, "
            if roe < 0:
                narrative += "but profitability remains elusive. The negative return on equity indicates the company is still working through operational challenges, "
            narrative += "suggesting this is a turnaround story in progress."
        
        elif framework == 'growth':
            narrative += f"exceptional strength. Revenue is surging {revenue_growth*100:.1f}% year-over-year, "
            if roe > 0.15:
                narrative += f"while profitability metrics are impressive with a {roe*100:.1f}% return on equity. "
            narrative += "This is a growth company firing on all cylinders."
        
        elif framework == 'value':
            narrative += "solid fundamentals. "
            if roe > 0.1:
                narrative += f"With a {roe*100:.1f}% return on equity, the company demonstrates efficient capital allocation. "
            narrative += "The financial metrics suggest a well-run business trading at reasonable valuations."
        
        else:  # cautious
            narrative += "mixed signals. "
            if revenue_growth > 0:
                narrative += f"While revenue growth of {revenue_growth*100:.1f}% is positive, "
            if roe < 0:
                narrative += "profitability concerns remain. "
            narrative += "Investors should proceed with caution."
        
        return narrative
    
    def _generate_technical_narrative(
        self,
        technical_data: Dict,
        framework: str
    ) -> str:
        """Generate technical analysis narrative"""
        
        trend = technical_data.get('trend', {})
        signals = technical_data.get('signals', {})
        
        trend_direction = trend.get('direction', 'Neutral')
        trend_strength = trend.get('strength', 'Moderate')
        rsi = technical_data.get('indicators', {}).get('rsi', {}).get('value', 50)
        
        narrative = "From a technical perspective, "
        
        if trend_direction == 'Uptrend' and trend_strength == 'Strong':
            narrative += f"the stock is in a strong uptrend, with price action showing consistent momentum. "
        elif trend_direction == 'Uptrend':
            narrative += f"the stock shows positive momentum, though the trend strength is {trend_strength.lower()}. "
        elif trend_direction == 'Downtrend':
            narrative += f"the stock faces headwinds, with a {trend_strength.lower()} downtrend in place. "
        else:
            narrative += "the stock is in a consolidation phase, with no clear directional bias. "
        
        if rsi < 30:
            narrative += "The RSI reading below 30 suggests the stock may be oversold, potentially presenting a buying opportunity for patient investors. "
        elif rsi > 70:
            narrative += "However, with RSI above 70, the stock appears overbought, suggesting near-term caution may be warranted. "
        else:
            narrative += f"With RSI at {rsi:.1f}, the stock is in neutral territory, providing flexibility for movement in either direction. "
        
        return narrative
    
    def _generate_catalyst_story(
        self,
        symbol: str,
        fundamental_data: Dict,
        sec_guidance: Optional[Dict]
    ) -> str:
        """Generate catalyst story"""
        
        story = "Key catalysts could drive the stock's performance: "
        
        catalysts = []
        
        # SEC guidance catalysts
        if sec_guidance and sec_guidance.get('available'):
            guidance = sec_guidance.get('guidance', {})
            profitability_timeline = guidance.get('profitability_timeline')
            if profitability_timeline:
                catalysts.append(f"management's target for profitability by {profitability_timeline}")
            
            strategic_initiatives = guidance.get('strategic_initiatives', [])
            if strategic_initiatives:
                catalysts.append(f"strategic initiatives including {strategic_initiatives[0].lower()}")
        
        # Growth catalysts
        growth = fundamental_data.get('growth', [{}])[0]
        revenue_growth = growth.get('revenueGrowth', 0)
        if revenue_growth > 0.2:
            catalysts.append("sustained revenue growth momentum")
        
        # Generic catalysts
        if not catalysts:
            catalysts = [
                "upcoming earnings announcements",
                "product launches and market expansion",
                "regulatory developments"
            ]
        
        story += ", ".join(catalysts[:3]) + ". "
        story += "Investors should monitor these developments closely as they could significantly impact the investment thesis."
        
        return story
    
    def _generate_risk_story(
        self,
        combined_data: Dict,
        fundamental_data: Dict
    ) -> str:
        """Generate risk narrative"""
        
        fundamental_score = combined_data.get('fundamental_score', 0)
        risks = []
        
        if fundamental_score < 5:
            risks.append("weak fundamental metrics indicating operational challenges")
        
        alignment = combined_data.get('alignment', '')
        if 'divergence' in alignment.lower():
            risks.append("conflicting signals between fundamental and technical analysis")
        
        ratios = fundamental_data.get('ratios', [{}])[0]
        roe = ratios.get('returnOnEquity', 0)
        if roe < 0:
            risks.append("negative profitability raising concerns about sustainability")
        
        if not risks:
            risks = ["market volatility", "sector-specific headwinds", "regulatory changes"]
        
        story = "Investors should be aware of several risk factors: "
        story += ", ".join(risks[:3]) + ". "
        story += "These risks could impact the stock's performance and should be carefully considered before making an investment decision."
        
        return story
    
    def _generate_investment_story(
        self,
        combined_data: Dict,
        framework: str
    ) -> str:
        """Generate investment thesis narrative"""
        
        recommendation = combined_data.get('recommendation', 'Hold')
        confidence = combined_data.get('confidence', 'Medium')
        fundamental_score = combined_data.get('fundamental_score', 0)
        technical_score = combined_data.get('technical_score', 0)
        
        story = f"Given the comprehensive analysis, the investment recommendation is {recommendation.upper()} "
        story += f"with {confidence.lower()} confidence. "
        
        if framework == 'turnaround':
            story += "This is a turnaround play, requiring patience and careful monitoring of execution. "
            story += "The improving trajectory suggests potential, but success is not guaranteed."
        
        elif framework == 'growth':
            story += "Strong fundamentals and growth metrics support a positive outlook. "
            story += "However, investors should be mindful of valuation and ensure growth expectations are realistic."
        
        elif framework == 'value':
            story += "The stock presents a value opportunity with solid fundamentals at reasonable prices. "
            story += "Patient investors may be rewarded as the market recognizes the company's intrinsic value."
        
        elif framework == 'momentum':
            story += "Technical momentum and positive sentiment suggest near-term strength. "
            story += "However, momentum can reverse quickly, so position sizing and risk management are critical."
        
        else:  # cautious
            story += "Mixed signals and concerns warrant a cautious approach. "
            story += "Wait for clearer direction before committing significant capital."
        
        return story
    
    def _generate_conclusion(
        self,
        symbol: str,
        combined_data: Dict,
        framework: str
    ) -> str:
        """Generate compelling conclusion"""
        
        recommendation = combined_data.get('recommendation', 'Hold')
        
        conclusion = f"For {symbol}, the analysis points to a {recommendation.upper()} recommendation. "
        
        if framework == 'turnaround':
            conclusion += "This is a story of transformation—one that requires careful monitoring but could deliver significant returns if execution improves. "
            conclusion += "The key is timing: enter too early and you face continued losses; enter too late and you miss the recovery."
        
        elif framework == 'growth':
            conclusion += "The growth story is compelling, but sustainability is the question. "
            conclusion += "Investors should focus on whether the company can maintain its momentum while managing the challenges that come with rapid expansion."
        
        elif framework == 'value':
            conclusion += "Value investors may find this opportunity attractive, but patience is required. "
            conclusion += "The market may take time to recognize the company's true worth."
        
        elif framework == 'momentum':
            conclusion += "Momentum is on your side, but it's a fickle friend. "
            conclusion += "Ride the wave while it lasts, but always have an exit strategy."
        
        else:  # cautious
            conclusion += "The path forward is uncertain. "
            conclusion += "Wait for clearer signals before making a significant commitment."
        
        conclusion += " As always, conduct your own research and consider your risk tolerance before investing."
        
        return conclusion
    
    # Framework-specific generators (can be expanded)
    def _generate_turnaround_narrative(self, data: Dict) -> str:
        """Generate turnaround story narrative"""
        return "This is a turnaround story..."
    
    def _generate_growth_narrative(self, data: Dict) -> str:
        """Generate growth story narrative"""
        return "This is a growth story..."
    
    def _generate_value_narrative(self, data: Dict) -> str:
        """Generate value story narrative"""
        return "This is a value story..."
    
    def _generate_momentum_narrative(self, data: Dict) -> str:
        """Generate momentum story narrative"""
        return "This is a momentum story..."
    
    def _generate_cautious_narrative(self, data: Dict) -> str:
        """Generate cautious story narrative"""
        return "This is a cautious story..."



