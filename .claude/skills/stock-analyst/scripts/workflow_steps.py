#!/usr/bin/env python3
"""
Workflow Step Functions
Implements the step-by-step analysis workflow
"""

from typing import Dict
from ai_interpreters import (
    interpret_fundamental_metrics,
    interpret_valuation,
    synthesize_investment_thesis
)


def step2_fundamental_analysis(symbol, fundamental_analyzer, valuation_analyzer):
    """Step 2: Fundamental Analysis with AI interpretation"""
    print("\n" + "="*80)
    print("STEP 2: Fundamental Analysis")
    print("="*80)
    
    print(f"\nAnalyzing {symbol} fundamentals...")
    
    # Fetch all fundamental data
    # ALGORITHMIC: Try quarterly data first (more recent), fall back to annual if unavailable
    profile = fundamental_analyzer.get_profile(symbol)
    quote = fundamental_analyzer.get_quote(symbol)
    
    # Try quarterly data first for more recent information
    try:
        ratios = fundamental_analyzer.get_ratios(symbol, period='quarter', limit=1)
        if not ratios or len(ratios) == 0:
            ratios = fundamental_analyzer.get_ratios(symbol, period='annual', limit=1)
    except:
        ratios = fundamental_analyzer.get_ratios(symbol, period='annual', limit=1)
    
    try:
        metrics = fundamental_analyzer.get_key_metrics(symbol, period='quarter', limit=1)
        if not metrics or len(metrics) == 0:
            metrics = fundamental_analyzer.get_key_metrics(symbol, period='annual', limit=1)
    except:
        metrics = fundamental_analyzer.get_key_metrics(symbol, period='annual', limit=1)
    
    try:
        income = fundamental_analyzer.get_income_statement(symbol, period='quarter', limit=1)
        if not income or len(income) == 0:
            income = fundamental_analyzer.get_income_statement(symbol, period='annual', limit=1)
    except:
        income = fundamental_analyzer.get_income_statement(symbol, period='annual', limit=1)
    
    try:
        growth = fundamental_analyzer.get_financial_growth(symbol, period='quarter', limit=1)
        if not growth or len(growth) == 0:
            growth = fundamental_analyzer.get_financial_growth(symbol, period='annual', limit=1)
    except:
        growth = fundamental_analyzer.get_financial_growth(symbol, period='annual', limit=1)
    
    # Run analyzer's built-in analysis
    print("\n" + "-"*80)
    print("Fundamental Data:")
    print("-"*80)
    fundamental_analyzer.analyze_stock(symbol)
    
    # AI Interpretation
    print("\n" + "-"*80)
    print("AI Interpretation of Fundamental Metrics:")
    print("-"*80)
    interpretations = interpret_fundamental_metrics(ratios, growth, quote)
    
    for metric, interpretation in interpretations.items():
        print(f"\n📊 {metric.replace('_', ' ').title()}:")
        print(f"   {interpretation}")
    
    # Valuation analysis with interpretation
    pe_ratio = quote.get('pe') if quote else None
    sector = profile.get('sector', 'Technology') if profile else 'Technology'
    net_income_growth = growth[0].get('netIncomeGrowth') if growth else None
    eps = quote.get('eps') if quote else None
    ps_ratio = ratios[0].get('priceToSalesRatio') if ratios and len(ratios) > 0 else None
    pb_ratio = ratios[0].get('priceToBookRatio') if ratios and len(ratios) > 0 else None
    
    valuation_data = None
    if pe_ratio and net_income_growth:
        if net_income_growth > 1:
            growth_percentage = (net_income_growth - 1) * 100
        else:
            growth_percentage = net_income_growth * 100
        
        valuation_data = valuation_analyzer.analyze_valuation(
            symbol=symbol,
            pe_ratio=pe_ratio,
            growth_rate=growth_percentage,
            sector=sector,
            pb_ratio=pb_ratio,
            ps_ratio=ps_ratio,
            eps=eps
        )
        
        print("\n📊 Valuation Interpretation:")
        # Get available context (fundamental_score calculated later in step4)
        roe = ratios[0].get('returnOnEquity') if ratios and len(ratios) > 0 else None
        growth_rate = growth[0].get('revenueGrowth') if growth and len(growth) > 0 else None
        # quote is already defined above from fundamental_analyzer.get_quote()
        eps = quote.get('eps') if quote else None
        valuation_interpretation = interpret_valuation(
            valuation_data, 
            pe_ratio, 
            sector,
            fundamental_score=None,  # Calculated later in step4
            roe=roe,
            growth_rate=growth_rate,
            eps=eps
        )
        print(f"   {valuation_interpretation}")
    
    # Check data freshness
    from data_freshness_checker import check_data_freshness
    freshness_data = check_data_freshness({
        'income': income,
        'ratios': ratios,
        'growth': growth
    })
    
    # Analyze trajectory
    from trajectory_analyzer import analyze_trajectory
    trajectory_data = analyze_trajectory({
        'income': income,
        'ratios': ratios,
        'growth': growth
    })
    
    # Extract SEC guidance (if available)
    sec_guidance_data = None
    try:
        from sec_guidance_extractor import SECGuidanceExtractor
        sec_extractor = SECGuidanceExtractor()
        sec_guidance_data = sec_extractor.extract_guidance(symbol)
        if sec_guidance_data.get('available'):
            print(f"\n📋 SEC Guidance: Found {len(sec_guidance_data.get('filings', []))} relevant filings")
    except Exception as e:
        print(f"\n⚠️ SEC Guidance extraction failed: {e}")
        sec_guidance_data = None
    
    # Extract earnings transcript (if available)
    transcript_data = None
    try:
        from earnings_transcript_extractor import EarningsTranscriptExtractor
        transcript_extractor = EarningsTranscriptExtractor()
        transcript_data = transcript_extractor.extract_transcript(symbol)
        if transcript_data.get('available'):
            print(f"\n📞 Earnings Transcript: Found transcript from {transcript_data.get('source', 'unknown')} ({transcript_data.get('date', 'unknown date')})")
    except Exception as e:
        print(f"\n⚠️ Earnings transcript extraction failed: {e}")
        transcript_data = None
    
    return {
        'profile': profile,
        'quote': quote,
        'ratios': ratios,
        'metrics': metrics,
        'income': income,
        'growth': growth,
        'valuation': valuation_data,
        'interpretations': interpretations,
        'data_freshness': freshness_data,  # Add freshness data
        'trajectory': trajectory_data,  # Add trajectory data
        'sec_guidance': sec_guidance_data,  # Add SEC guidance data
        'transcript': transcript_data  # Add earnings transcript data
    }


def step3_technical_analysis(symbol, technical_analyzer):
    """Step 3: Technical Analysis with AI interpretation"""
    print("\n" + "="*80)
    print("STEP 3: Technical Analysis")
    print("="*80)
    
    print(f"\nAnalyzing {symbol} technicals...")
    
    print("\n" + "-"*80)
    print("Technical Data:")
    print("-"*80)
    technical_data = technical_analyzer.analyze_stock(symbol)
    
    # AI Interpretation would parse the output and provide insights
    print("\n" + "-"*80)
    print("AI Interpretation of Technical Indicators:")
    print("-"*80)
    print("📈 Technical patterns and indicators analyzed above provide insights into:")
    print("   - Trend direction and strength")
    print("   - Momentum and potential reversals")
    print("   - Key support and resistance levels")
    print("   - Entry and exit timing")
    
    return {
        'analyzer': technical_analyzer,
        'symbol': symbol,
        'data': technical_data if technical_data else {}
    }


def step35_sentiment_analysis(symbol, sentiment_analyzer):
    """Step 3.5: Sentiment Analysis per skill workflow"""
    print("\n" + "="*80)
    print("STEP 3.5: Sentiment Analysis")
    print("="*80)
    
    print(f"\nAnalyzing {symbol} sentiment...")
    
    # Use the sentiment analyzer from the skill
    sentiment_result = sentiment_analyzer.analyze_stock_sentiment(symbol)
    
    return sentiment_result


def step4_combined_analysis(symbol, fundamental_data, technical_data, sentiment_data,
                            recommendation_engine, fundamental_scorer, trajectory_data=None):
    """Step 4: Combined Analysis with AI synthesis"""
    print("\n" + "="*80)
    print("STEP 4: Combined Analysis")
    print("="*80)
    
    print(f"\nSynthesizing insights for {symbol}...")
    
    # Calculate fundamental score from actual data
    ratios = fundamental_data.get('ratios', [])
    growth = fundamental_data.get('growth', [])
    income = fundamental_data.get('income', [])
    quote = fundamental_data.get('quote', {})
    valuation = fundamental_data.get('valuation')
    
    pe_ratio = quote.get('pe') if quote else None
    peg_ratio = None
    sector_premium = 1.0
    valuation_score_val = None
    
    if valuation:
        peg_ratio = valuation.get('peg_ratio', {}).get('value')
        sector_comparison = valuation.get('sector_comparison', {})
        if sector_comparison.get('pe_ratio', {}).get('premium_discount'):
            premium_pct = sector_comparison['pe_ratio']['premium_discount']
            sector_premium = 1.0 + (premium_pct / 100.0)  # Convert % to multiplier
        valuation_score_val = valuation.get('valuation_score', {}).get('score')
    
    # Calculate fundamental score using scorer
    fundamental_score = 5.0  # Default neutral
    fundamental_score_details = None
    
    if pe_ratio and ratios and growth and income:
        fundamental_score_details = fundamental_scorer.calculate_fundamental_score(
            ratios=ratios,
            growth=growth,
            income=income,
            pe_ratio=pe_ratio,
            peg_ratio=peg_ratio,
            sector_premium=sector_premium,
            valuation_score=valuation_score_val
        )
        fundamental_score = fundamental_score_details['overall_score']
        print(f"\n📊 Fundamental Score Breakdown:")
        print(f"   Overall: {fundamental_score}/10 ({fundamental_scorer.get_fundamental_strength_label(fundamental_score)})")
        print(f"   Profitability: {fundamental_score_details['profitability_score']}/10")
        print(f"   Growth: {fundamental_score_details['growth_score']}/10")
        print(f"   Financial Health: {fundamental_score_details['financial_health_score']}/10")
        print(f"   Valuation: {fundamental_score_details['valuation_score']}/10")
    else:
        print(f"⚠️  Warning: Insufficient data for accurate fundamental scoring, using neutral score")
    
    # Calculate technical score using TechnicalScorer
    technical_score = 5.0  # Default neutral
    technical_score_details = None
    
    technical_data_dict = technical_data.get('data', {})
    if technical_data_dict:
        from stock_technical_scorer import TechnicalScorer
        technical_scorer = TechnicalScorer()
        
        trend_analysis = technical_data_dict.get('trend_analysis', {})
        trading_signals = technical_data_dict.get('trading_signals', {})
        price_changes = technical_data_dict.get('price_changes', {})
        indicators = technical_data_dict.get('indicators', {})
        current_price = technical_data_dict.get('current_price')
        
        if trend_analysis and trading_signals:
            technical_score_details = technical_scorer.calculate_technical_score(
                trend_analysis=trend_analysis,
                trading_signals=trading_signals,
                price_changes=price_changes,
                indicators=indicators,
                current_price=current_price
            )
            technical_score = technical_score_details['overall_score']
            print(f"\n📊 Technical Score Breakdown:")
            print(f"   Overall: {technical_score}/10 ({technical_scorer.get_technical_strength_label(technical_score)})")
            print(f"   Trend: {technical_score_details['trend_score']}/10")
            print(f"   Momentum: {technical_score_details['momentum_score']}/10")
            print(f"   Price Action: {technical_score_details['price_action_score']}/10")
        else:
            print(f"⚠️  Warning: Insufficient technical data for accurate scoring, using neutral score")
    else:
        print(f"⚠️  Warning: No technical data available, using neutral score")
    
    # Get sentiment score
    sentiment_score = 0.0
    sentiment_classification = "Neutral"
    if sentiment_data and 'combined_sentiment' in sentiment_data:
        sentiment_score = sentiment_data['combined_sentiment'].get('score', 0.0)
        sentiment_classification = sentiment_data['combined_sentiment'].get('sentiment', 'Neutral')
    
    sector = fundamental_data.get('profile', {}).get('sector', 'Technology') if fundamental_data.get('profile') else 'Technology'
    
    # Get valuation data to check if P/E is misleading
    valuation_data = fundamental_data.get('valuation')
    pe_misleading = False
    ps_ratio = None
    sector_avg_ps = None
    
    if valuation_data:
        pe_misleading = valuation_data.get('pe_misleading', False)
        sector_comparison = valuation_data.get('sector_comparison', {})
        if pe_misleading and sector_comparison.get('ps_ratio'):
            ps_ratio = sector_comparison['ps_ratio'].get('current')
            sector_avg_ps = sector_comparison['ps_ratio'].get('sector_avg')
        elif not pe_misleading:
            # Get P/S ratio from ratios if available
            ratios = fundamental_data.get('ratios', [])
            if ratios and len(ratios) > 0:
                ps_ratio = ratios[0].get('priceToSalesRatio')
                # Get sector P/S average (would ideally fetch from API)
                from stock_valuation_analyzer import ValuationAnalyzer
                temp_analyzer = ValuationAnalyzer()
                sector_avg_ps = temp_analyzer._get_sector_ps_average(sector)
    
    if pe_ratio:
        # ALGORITHMIC: Use P/S-based risk when P/E is misleading
        valuation_risk = recommendation_engine.calculate_valuation_risk(
            pe_ratio, 
            25.0,  # sector_avg_pe
            pe_misleading=pe_misleading,
            ps_ratio=ps_ratio,
            sector_avg_ps=sector_avg_ps
        )
        overall_risk = recommendation_engine.assess_overall_risk(
            valuation_risk=valuation_risk,
            technical_risk="Low" if technical_score >= 7.5 else "Medium",
            fundamental_concerns=[],
            market_risk="Medium"
        )
        
        # Extract trajectory data for recommendation
        trajectory_score = trajectory_data.get('trajectory_score') if trajectory_data else None
        trajectory_momentum = trajectory_data.get('momentum') if trajectory_data else None
        
        rec, conf, rationale = recommendation_engine.calculate_recommendation(
            fundamental_score=fundamental_score,
            technical_score=technical_score,
            valuation_risk=valuation_risk,
            overall_risk=overall_risk,
            pe_ratio=pe_ratio,
            sector_avg_pe=25.0,
            trajectory_score=trajectory_score,
            trajectory_momentum=trajectory_momentum
        )
        
        # Override recommendation if sentiment strongly supports it
        # If fundamentals are exceptional (8.8+) and sentiment is strongly bullish, upgrade to BUY
        sentiment_bullish = sentiment_score > 0.3
        if rec.value == 'Hold' and fundamental_score >= 8.5 and sentiment_bullish and technical_score >= 6.5:
            rec = recommendation_engine.Recommendation.BUY
            rationale = f"Upgraded to BUY: Exceptional fundamentals ({fundamental_score:.1f}/10) and strongly bullish sentiment ({sentiment_score:.3f}) override moderate technical setup ({technical_score:.1f}/10). {rationale}"
        
        # Determine alignment including sentiment
        sentiment_bullish = sentiment_score > 0.1
        sentiment_bearish = sentiment_score < -0.1
        
        if fundamental_score >= 8 and technical_score >= 7 and sentiment_bullish:
            alignment = "Strong Alignment - Fundamentals, technicals, and sentiment all bullish"
        elif fundamental_score >= 8 and technical_score >= 7:
            alignment = "Strong Alignment - Fundamentals and technicals bullish, sentiment neutral"
        elif fundamental_score >= 8 and technical_score < 7:
            alignment = "Divergence - Strong fundamentals, weak technicals"
        elif fundamental_score < 7 and technical_score >= 8:
            alignment = "Divergence - Weak fundamentals, strong technicals"
        elif sentiment_bullish and fundamental_score < 7 and technical_score < 7:
            alignment = "Divergence - Bullish sentiment but weak fundamentals and technicals"
        elif sentiment_bullish and fundamental_score < 7 and technical_score >= 7:
            alignment = "Divergence - Bullish sentiment but weak fundamentals, strong technicals"
        elif sentiment_bullish and fundamental_score >= 7 and technical_score < 7:
            alignment = "Divergence - Bullish sentiment and strong fundamentals, but weak technicals"
        elif sentiment_bearish and (fundamental_score >= 8 or technical_score >= 8):
            alignment = "Divergence - Bearish sentiment but strong fundamentals/technicals"
        else:
            alignment = "Weak Alignment - Mixed signals across dimensions"
        
        # AI Synthesis
        print("\n" + "-"*80)
        print("AI Synthesis of Combined Analysis:")
        print("-"*80)
        
        investment_thesis = synthesize_investment_thesis(
            fundamental_data,
            technical_data,
            {
                'fundamental_score': fundamental_score,
                'technical_score': technical_score,
                'technical_score_details': technical_score_details,
                'sentiment_score': sentiment_score,
                'sentiment_classification': sentiment_classification,
                'alignment': alignment,
                'valuation_risk': valuation_risk,
                'recommendation': rec.value  # Pass recommendation for contradiction detection
            }
        )
        
        print(f"\n💡 Investment Thesis:")
        print(f"   {investment_thesis}")
        
        print(f"\n🎯 Recommendation: {rec.value}")
        print(f"   Confidence: {conf.value}")
        print(f"   Rationale: {rationale}")
        
        return {
            'recommendation': rec.value,
            'confidence': conf.value,
            'rationale': rationale,
            'fundamental_score': fundamental_score,
            'fundamental_score_details': fundamental_score_details,
            'technical_score': technical_score,
            'sentiment_score': sentiment_score,
            'sentiment_classification': sentiment_classification,
            'valuation_risk': valuation_risk,
            'overall_risk': overall_risk.value,
            'alignment': alignment,
            'investment_thesis': investment_thesis
        }
    else:
        print("    ⚠️  Cannot calculate recommendation (missing P/E ratio)")
        return None

