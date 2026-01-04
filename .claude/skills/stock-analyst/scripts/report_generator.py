#!/usr/bin/env python3
"""
Report Generator Module
Generates comprehensive stock analysis reports with AI interpretation
"""

import os
from datetime import datetime
from typing import Dict
from ai_interpreters import interpret_valuation, interpret_technical_analysis
from report_helpers import generate_price_targets, generate_actionable_recommendation

def step5_report_generation(symbol, fundamental_data, technical_data, sentiment_data, combined_data, fundamental_scorer):
    """Step 5: Report Generation with comprehensive AI interpretation"""
    print("\n" + "="*80)
    print("STEP 5: Report Generation with AI Interpretation")
    print("="*80)
    
    print(f"\nGenerating comprehensive report with AI interpretation for {symbol}...")
    
    profile = fundamental_data.get('profile', {})
    quote = fundamental_data.get('quote', {})
    ratios = fundamental_data.get('ratios', [])
    growth = fundamental_data.get('growth', [])
    valuation = fundamental_data.get('valuation')
    interpretations = fundamental_data.get('interpretations', {})
    data_freshness = fundamental_data.get('data_freshness', {})
    
    # Generate comprehensive report with AI interpretation
    report_content = f"""# {symbol} - Comprehensive Stock Analysis Report
**Generated using Stock Analyst Skill with AI Interpretation**
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
    
    # Add data freshness warning if stale
    if data_freshness.get('is_stale'):
        from data_freshness_checker import get_data_freshness_summary
        freshness_summary = get_data_freshness_summary(data_freshness)
        report_content += f"**⚠️ DATA FRESHNESS WARNING:** {freshness_summary}\n\n"
    
    report_content += """---

## Executive Summary

"""
    
    # Executive summary with AI interpretation (using actual calculated scores)
    if profile:
        company_name = profile.get('companyName', symbol)
        report_content += f"{company_name} ({symbol}) "
    
    if combined_data:
        fundamental_score = combined_data.get('fundamental_score', 5.0)
        technical_score = combined_data.get('technical_score', 5.0)
        sentiment_classification = combined_data.get('sentiment_classification', 'Neutral')
        
        # Get fundamental strength label from scorer
        fundamental_strength_label = fundamental_scorer.get_fundamental_strength_label(fundamental_score)
        
        # Build accurate executive summary based on actual scores
        if fundamental_score >= 7.0:
            fundamental_desc = f"{fundamental_strength_label.lower()} fundamental strength"
        elif fundamental_score >= 5.0:
            fundamental_desc = "moderate fundamental strength"
        else:
            fundamental_desc = "weak fundamental strength"
        
        if technical_score >= 7.0:
            technical_desc = "strong technical momentum"
        elif technical_score >= 5.0:
            technical_desc = "moderate technical setup"
        else:
            technical_desc = "weak technical setup"
        
        report_content += f"demonstrates {fundamental_desc} with {technical_desc}. "
        
        # Add sentiment context
        if sentiment_classification != 'Neutral':
            report_content += f"Market sentiment is {sentiment_classification.lower()}. "
    
    if quote:
        price = quote.get('price', 0)
        pe = quote.get('pe', 0)
        price_str = f"${price:.2f}" if isinstance(price, (int, float)) else str(price)
        pe_str = f"{pe:.2f}" if isinstance(pe, (int, float)) else str(pe)
        report_content += f"The stock currently trades at {price_str} with a P/E ratio of {pe_str}. "
    
    if combined_data:
        recommendation = combined_data.get('recommendation', 'Hold')
        confidence = combined_data.get('confidence', 'Medium')
        report_content += f"\n\n**Investment Recommendation:** **{recommendation.upper()}**  \n"
        report_content += f"**Confidence Level:** **{confidence}**  \n"
        
        if combined_data.get('investment_thesis'):
            report_content += f"\n**Investment Thesis:** {combined_data['investment_thesis']}\n"
    
    # Fundamental Analysis Section with Interpretation
    report_content += "\n---\n\n## Fundamental Analysis\n\n"
    
    if profile:
        report_content += f"""
### Company Overview

- **Company Name:** {profile.get('companyName', 'N/A')}
- **Symbol:** {symbol}
- **Exchange:** {profile.get('exchangeShortName', 'N/A')}
- **Sector:** {profile.get('sector', 'N/A')}
- **Industry:** {profile.get('industry', 'N/A')}
- **Website:** {profile.get('website', 'N/A')}
"""
    
    if quote:
        market_cap = quote.get('marketCap', 0)
        # Format market cap more readably (billions/trillions)
        if isinstance(market_cap, (int, float)) and market_cap > 0:
            if market_cap >= 1_000_000_000_000:  # Trillions
                market_cap_str = f"${market_cap/1_000_000_000_000:.2f}T"
            elif market_cap >= 1_000_000_000:  # Billions
                market_cap_str = f"${market_cap/1_000_000_000:.2f}B"
            elif market_cap >= 1_000_000:  # Millions
                market_cap_str = f"${market_cap/1_000_000:.2f}M"
            else:
                market_cap_str = f"${market_cap:,.0f}"
        else:
            market_cap_str = str(market_cap)
        
        report_content += f"""
### Current Market Data

- **Current Price:** ${quote.get('price', 'N/A')}
- **Market Cap:** {market_cap_str}
- **P/E Ratio:** {quote.get('pe', 'N/A')}
- **EPS:** ${quote.get('eps', 'N/A')}
- **52 Week High:** ${quote.get('yearHigh', 'N/A')}
- **52 Week Low:** ${quote.get('yearLow', 'N/A')}
"""
    
    if ratios:
        report_content += """
### Financial Ratios & Interpretation

"""
        ratio = ratios[0]
        roe = ratio.get('returnOnEquity', 0)
        roa = ratio.get('returnOnAssets', 0)
        debt_equity = ratio.get('debtEquityRatio', 0)
        current_ratio = ratio.get('currentRatio', 0)
        
        report_content += f"- **Return on Equity (ROE):** {roe*100:.2f}%  \n"
        if 'roe' in interpretations:
            report_content += f"  *{interpretations['roe']}*\n"
        
        report_content += f"- **Return on Assets (ROA):** {roa*100:.2f}%  \n"
        if 'roa' in interpretations:
            report_content += f"  *{interpretations['roa']}*\n"
        
        report_content += f"- **Debt-to-Equity:** {debt_equity:.2f}  \n"
        if 'debt' in interpretations:
            report_content += f"  *{interpretations['debt']}*\n"
        
        report_content += f"- **Current Ratio:** {current_ratio:.2f}  \n"
        if 'liquidity' in interpretations:
            report_content += f"  *{interpretations['liquidity']}*\n"
    
    if growth:
        report_content += """
### Growth Metrics & Interpretation

"""
        g = growth[0]
        rev_growth = g.get('revenueGrowth', 0)
        ni_growth = g.get('netIncomeGrowth', 0)
        
        if rev_growth > 1:
            rev_pct = (rev_growth - 1) * 100
        else:
            rev_pct = rev_growth * 100
        
        if ni_growth > 1:
            ni_pct = (ni_growth - 1) * 100
        else:
            ni_pct = ni_growth * 100
        
        report_content += f"- **Revenue Growth:** {rev_pct:.1f}% YoY  \n"
        if 'revenue_growth' in interpretations:
            report_content += f"  *{interpretations['revenue_growth']}*\n"
        
        report_content += f"- **Net Income Growth:** {ni_pct:.1f}% YoY  \n"
        if 'profit_growth' in interpretations:
            report_content += f"  *{interpretations['profit_growth']}*\n"
    
    if valuation:
        report_content += """
### Valuation Analysis & Interpretation

"""
        peg_value = valuation.get('peg_ratio', {}).get('value')
        peg_warning = valuation.get('peg_ratio', {}).get('warning')
        if peg_value is not None:
            if isinstance(peg_value, (int, float)):
                peg_str = f"{peg_value:.2f}"
            else:
                peg_str = str(peg_value)
            report_content += f"- **PEG Ratio:** {peg_str} ({valuation['peg_ratio']['assessment']})  \n"
            if peg_warning:
                report_content += f"  *{peg_warning}*\n"
        
        report_content += f"- **Sector Comparison:** {valuation['sector_comparison']['pe_ratio']['assessment']}  \n"
        
        # ALGORITHMIC: Flag misleading valuation score prominently
        pe_misleading = valuation.get('pe_misleading', False)
        valuation_score_data = valuation.get('valuation_score', {})
        if pe_misleading or valuation_score_data.get('pe_misleading', False):
            report_content += f"- **Valuation Score:** ⚠️ **{valuation_score_data.get('score', 'N/A')}/10 (MISLEADING - P/E not meaningful)**  \n"
            report_content += f"  *⚠️ Warning: Valuation score reflects misleading P/E ratio due to negative/low earnings. Score should not be used for decision-making. Consider P/S ratio or forward P/E estimates instead.*\n"
        else:
            report_content += f"- **Valuation Score:** {valuation_score_data.get('score', 'N/A')}/10 ({valuation_score_data.get('interpretation', 'N/A')})  \n"
        
        # Get fundamental context for valuation interpretation
        fundamental_score = combined_data.get('fundamental_score') if combined_data else None
        roe = ratios[0].get('returnOnEquity') if ratios and len(ratios) > 0 else None
        growth_rate = growth[0].get('revenueGrowth') if growth and len(growth) > 0 else None
        
        valuation_interpretation = interpret_valuation(
            valuation, 
            quote.get('pe') if quote else 0, 
            profile.get('sector', 'Technology') if profile else 'Technology',
            fundamental_score=fundamental_score,
            roe=roe,
            growth_rate=growth_rate,
            eps=quote.get('eps') if quote else None
        )
        report_content += f"\n*{valuation_interpretation}*\n"
    
    # Technical Analysis Section - Include actual data
    report_content += "\n---\n\n## Technical Analysis\n\n"
    
    # Extract technical data
    technical_data_dict = technical_data.get('data', {}) if technical_data else {}
    
    if technical_data_dict:
        trend_analysis = technical_data_dict.get('trend_analysis', {})
        trading_signals = technical_data_dict.get('trading_signals', {})
        price_changes = technical_data_dict.get('price_changes', {})
        indicators = technical_data_dict.get('indicators', {})
        current_price = technical_data_dict.get('current_price')
        
        # Current Price Action
        if price_changes and current_price:
            report_content += f"""
### Current Price Action

- **Current Price:** ${current_price:.2f}
"""
            if '1D' in price_changes:
                report_content += f"- **Price Change (1D):** {price_changes['1D']*100:+.2f}%\n"
            if '1W' in price_changes:
                report_content += f"- **Price Change (1W):** {price_changes['1W']*100:+.2f}%\n"
            if '1M' in price_changes:
                report_content += f"- **Price Change (1M):** {price_changes['1M']*100:+.2f}%\n"
            if '1Y' in price_changes:
                report_content += f"- **Price Change (1Y):** {price_changes['1Y']*100:+.2f}%\n"
        
        # Trend Analysis
        if trend_analysis:
            report_content += f"""
### Trend Analysis

- **Primary Trend:** {trend_analysis.get('trend', 'N/A')}
- **Trend Strength:** {trend_analysis.get('strength', 'N/A')}
- **Price vs SMA 50:** {trend_analysis.get('price_vs_sma50', 'N/A')}
- **Price vs SMA 200:** {trend_analysis.get('price_vs_sma200', 'N/A')}
- **SMA 50 vs SMA 200:** {trend_analysis.get('sma50_vs_sma200', 'N/A')}
"""
        
        # Momentum Indicators
        if indicators:
            rsi = indicators.get('rsi')
            macd_signal = indicators.get('macd_signal', 'N/A')
            
            report_content += """
### Momentum Indicators

"""
            if rsi is not None:
                # Improved RSI interpretation
                if rsi > 80:
                    rsi_status = "Extremely Overbought"
                elif rsi > 70:
                    rsi_status = "Overbought"
                elif rsi > 65:
                    rsi_status = "Approaching Overbought"
                elif rsi < 20:
                    rsi_status = "Extremely Oversold"
                elif rsi < 30:
                    rsi_status = "Oversold"
                elif rsi < 35:
                    rsi_status = "Approaching Oversold"
                else:
                    rsi_status = "Neutral"
                report_content += f"- **RSI (14):** {rsi:.2f} ({rsi_status})\n"
            else:
                report_content += f"- **RSI (14):** N/A\n"
            
            report_content += f"- **MACD Signal:** {macd_signal}\n"
        
        # Trading Signals
        if trading_signals:
            report_content += f"""
### Trading Signals

- **RSI Signal:** {trading_signals.get('rsi_signal', 'N/A')}
- **MACD Signal:** {trading_signals.get('macd_signal', 'N/A')}
- **Trend Signal:** {trading_signals.get('trend_signal', 'N/A')}
- **Overall Signal:** {trading_signals.get('overall_signal', 'N/A')}
"""
        
        # Add Technical Interpretation
        if technical_data_dict:
            fundamental_score = combined_data.get('fundamental_score') if combined_data else None
            technical_interpretation = interpret_technical_analysis(
                technical_data_dict,
                fundamental_score=fundamental_score
            )
            if technical_interpretation:
                report_content += f"""
### Technical Interpretation

{technical_interpretation}
"""
                # ALGORITHMIC + AI: Add disclaimer when fundamentals are weak
                if fundamental_score is not None and fundamental_score < 5.0:
                    recommendation = combined_data.get('recommendation', 'Hold') if combined_data else 'Hold'
                    report_content += f"""
**⚠️ Important Note:** While technical indicators may suggest entry opportunities, weak fundamentals ({fundamental_score:.1f}/10) make technical signals unreliable. The {recommendation} recommendation reflects fundamental weakness that overrides technical signals. Wait for fundamental improvement before considering entry, regardless of technical setup. Quality companies can recover from technical weakness, but weak fundamentals make technical strength unreliable.
"""
        
        # Technical Score Breakdown
        technical_score_details = combined_data.get('technical_score_details') if combined_data else None
        if technical_score_details:
            report_content += f"""
### Technical Score Breakdown

- **Overall:** {technical_score_details.get('overall_score', 'N/A')}/10
- **Trend:** {technical_score_details.get('trend_score', 'N/A')}/10
- **Momentum:** {technical_score_details.get('momentum_score', 'N/A')}/10
- **Price Action:** {technical_score_details.get('price_action_score', 'N/A')}/10
- **Volatility:** {technical_score_details.get('volatility_score', 'N/A')}/10
"""
        else:
            # Only show placeholder if we truly have no technical data
            if not technical_data_dict:
                report_content += """
*Technical analysis data not available. See comprehensive technical analysis output above for detailed indicators, trends, and signals.*

**Key Technical Insights:**
- Trend direction and strength analyzed
- Momentum indicators (RSI, MACD) interpreted
- Support and resistance levels identified
- Trading signals generated

"""
    
    # Sentiment Analysis Section (Step 3.5 per skill)
    if sentiment_data:
        report_content += "\n---\n\n## Sentiment Analysis\n\n"
        analyst_sentiment = sentiment_data.get('analyst_sentiment', {})
        news_sentiment = sentiment_data.get('news_sentiment', {})
        combined_sentiment = sentiment_data.get('combined_sentiment', {})
        
        # Debug: Verify articles are present
        # print(f"DEBUG: news_sentiment keys: {list(news_sentiment.keys())}")
        # print(f"DEBUG: Has positive_articles: {'positive_articles' in news_sentiment}")
        
        report_content += """
### Analyst Sentiment

"""
        total_recommendations = analyst_sentiment.get('total_recommendations', 0)
        report_content += f"- **Total Recommendations:** {total_recommendations}  \n"
        
        if analyst_sentiment.get('average_rating'):
            report_content += f"- **Average Rating:** {analyst_sentiment['average_rating']:.2f}/5.0  \n"
        
        rating_dist = analyst_sentiment.get('rating_distribution', {})
        if rating_dist:
            report_content += f"- **Rating Distribution:** {rating_dist}  \n"
            # Show breakdown
            dist_parts = []
            for rating, count in sorted(rating_dist.items(), key=lambda x: x[1], reverse=True):
                dist_parts.append(f"{rating.title()}: {count}")
            if dist_parts:
                report_content += f"  *Breakdown: {', '.join(dist_parts)}*\n"
        
        report_content += f"- **Sentiment Score:** {analyst_sentiment.get('sentiment_score', 0):.3f}  \n"
        report_content += f"- **Summary:** {analyst_sentiment.get('recommendation_summary', 'N/A')}  \n"
        
        # Show recent recommendations even if parsing failed
        raw_recs = analyst_sentiment.get('raw_recommendations', [])
        if raw_recs and not analyst_sentiment.get('average_rating'):
            report_content += "\n**Recent Analyst Actions:**\n"
            for rec in raw_recs[:5]:
                company = rec.get('gradingCompany', 'Unknown')
                date = rec.get('date', 'N/A')
                new_grade = rec.get('newGrade', rec.get('grade', 'N/A'))
                prev_grade = rec.get('previousGrade', 'N/A')
                if new_grade and new_grade != 'N/A':
                    if prev_grade and prev_grade != 'N/A' and prev_grade != new_grade:
                        report_content += f"- **{company}** ({date}): {prev_grade} → {new_grade}\n"
                    else:
                        report_content += f"- **{company}** ({date}): {new_grade}\n"
        
        report_content += """
### News Sentiment

"""
        report_content += f"- **Average Sentiment:** {news_sentiment.get('average_sentiment', 0):.3f}  \n"
        report_content += f"- **Positive Articles:** {news_sentiment.get('positive_count', 0)}  \n"
        report_content += f"- **Negative Articles:** {news_sentiment.get('negative_count', 0)}  \n"
        report_content += f"- **Neutral Articles:** {news_sentiment.get('neutral_count', 0)}  \n"
        report_content += f"- **Summary:** {news_sentiment.get('news_summary', 'N/A')}  \n"
        
        # Add top headlines with hyperlinks
        positive_articles = news_sentiment.get('positive_articles', [])
        negative_articles = news_sentiment.get('negative_articles', [])
        neutral_articles = news_sentiment.get('neutral_articles', [])
        
        # Add headlines section if we have any articles
        if positive_articles or negative_articles or neutral_articles:
            report_content += "\n### Top Headlines\n\n"
            
            if positive_articles:
                report_content += "**Top Positive Headlines:**\n\n"
                for i, article in enumerate(positive_articles[:5], 1):
                    title = article.get('title', 'No title')
                    url = article.get('url', '')
                    site = article.get('site', '')
                    date = article.get('publishedDate', '')
                    
                    if url:
                        report_content += f"{i}. [{title}]({url})"
                    else:
                        report_content += f"{i}. {title}"
                    
                    if site:
                        report_content += f" *({site})*"
                    if date:
                        report_content += f" - {date[:10]}"
                    report_content += "\n"
                report_content += "\n"
            
            if negative_articles:
                report_content += "**Top Negative Headlines:**\n\n"
                for i, article in enumerate(negative_articles[:5], 1):
                    title = article.get('title', 'No title')
                    url = article.get('url', '')
                    site = article.get('site', '')
                    date = article.get('publishedDate', '')
                    
                    if url:
                        report_content += f"{i}. [{title}]({url})"
                    else:
                        report_content += f"{i}. {title}"
                    
                    if site:
                        report_content += f" *({site})*"
                    if date:
                        report_content += f" - {date[:10]}"
                    report_content += "\n"
                report_content += "\n"
            
            if neutral_articles and len(positive_articles) < 3 and len(negative_articles) < 3:
                report_content += "**Recent Headlines:**\n\n"
                for i, article in enumerate(neutral_articles[:3], 1):
                    title = article.get('title', 'No title')
                    url = article.get('url', '')
                    site = article.get('site', '')
                    date = article.get('publishedDate', '')
                    
                    if url:
                        report_content += f"{i}. [{title}]({url})"
                    else:
                        report_content += f"{i}. {title}"
                    
                    if site:
                        report_content += f" *({site})*"
                    if date:
                        report_content += f" - {date[:10]}"
                    report_content += "\n"
                report_content += "\n"
        
        report_content += """
### Combined Sentiment

"""
        report_content += f"- **Combined Sentiment Score:** {combined_sentiment.get('score', 0):.3f}  \n"
        report_content += f"- **Overall Sentiment:** **{combined_sentiment.get('sentiment', 'N/A')}**  \n"
        report_content += f"- **Weighting:** {combined_sentiment.get('analyst_weight', 0.6)*100:.0f}% analyst, {combined_sentiment.get('news_weight', 0.4)*100:.0f}% news  \n"
        
        # Expanded sentiment interpretation with themes
        report_content += "\n### Sentiment Interpretation & Key Themes\n\n"
        
        sentiment_classification = combined_sentiment.get('sentiment', 'Neutral')
        sentiment_score = combined_sentiment.get('score', 0)
        
        # Interpret sentiment score
        if sentiment_score > 0.3:
            sentiment_desc = "strongly bullish"
        elif sentiment_score > 0.1:
            sentiment_desc = "bullish"
        elif sentiment_score > -0.1:
            sentiment_desc = "neutral"
        elif sentiment_score > -0.3:
            sentiment_desc = "bearish"
        else:
            sentiment_desc = "strongly bearish"
        
        report_content += f"**Overall Assessment:** Market sentiment is {sentiment_desc} (score: {sentiment_score:.3f}). "
        
        # News sentiment themes
        positive_count = news_sentiment.get('positive_count', 0)
        negative_count = news_sentiment.get('negative_count', 0)
        total_articles = positive_count + negative_count + news_sentiment.get('neutral_count', 0)
        
        if total_articles > 0:
            positive_pct = (positive_count / total_articles) * 100
            if positive_pct > 70:
                report_content += f"News coverage is overwhelmingly positive ({positive_pct:.0f}% positive articles), indicating strong market confidence and favorable coverage. "
            elif positive_pct > 50:
                report_content += f"News coverage is generally positive ({positive_pct:.0f}% positive articles), suggesting favorable market perception. "
            elif positive_pct < 30:
                report_content += f"News coverage shows concerns ({positive_pct:.0f}% positive articles), indicating potential headwinds or negative sentiment. "
            else:
                report_content += f"News coverage is mixed ({positive_pct:.0f}% positive articles), reflecting balanced market views. "
        
        # Analyst sentiment context
        if analyst_sentiment.get('average_rating'):
            avg_rating = analyst_sentiment['average_rating']
            if avg_rating >= 4.0:
                report_content += f"Analyst consensus is strongly bullish (average rating: {avg_rating:.2f}/5.0), supporting positive outlook. "
            elif avg_rating >= 3.5:
                report_content += f"Analyst consensus is moderately bullish (average rating: {avg_rating:.2f}/5.0), indicating favorable professional opinion. "
            elif avg_rating >= 2.5:
                report_content += f"Analyst consensus is neutral (average rating: {avg_rating:.2f}/5.0), reflecting mixed professional views. "
            else:
                report_content += f"Analyst consensus is bearish (average rating: {avg_rating:.2f}/5.0), indicating professional concerns. "
        
        # Sentiment trend (if available from news)
        if sentiment_score > 0.2:
            report_content += "The positive sentiment suggests continued market confidence and potential for further price appreciation. "
        elif sentiment_score < -0.2:
            report_content += "The negative sentiment suggests market concerns that may weigh on near-term performance. "
        
        report_content += "\n"
    
    # Combined Assessment with AI Synthesis
    if combined_data:
        report_content += "\n---\n\n## Combined Assessment\n\n### Analysis Alignment\n\n"
        report_content += f"**Alignment:** {combined_data.get('alignment', 'N/A')}\n\n"
        report_content += "### Scoring\n\n"
        report_content += f"- **Fundamental Score:** {combined_data.get('fundamental_score', 'N/A')}/10\n"
        report_content += f"- **Technical Score:** {combined_data.get('technical_score', 'N/A')}/10\n"
        sentiment_score = combined_data.get('sentiment_score', 0)
        sentiment_score_str = f"{sentiment_score:.3f}" if isinstance(sentiment_score, (int, float)) else str(sentiment_score)
        report_content += f"- **Sentiment Score:** {sentiment_score_str} ({combined_data.get('sentiment_classification', 'N/A')})\n"
        valuation_risk = combined_data.get('valuation_risk', 'N/A')
        valuation_risk_str = f"{valuation_risk:.2f}x" if isinstance(valuation_risk, (int, float)) else str(valuation_risk)
        report_content += f"- **Valuation Risk:** {valuation_risk_str} sector average\n"
        report_content += f"- **Overall Risk:** {combined_data.get('overall_risk', 'N/A')}\n\n"
        report_content += "### Fundamental Score Breakdown\n\n"
        fundamental_score_details = combined_data.get('fundamental_score_details')
        if fundamental_score_details:
            fundamental_score = combined_data.get('fundamental_score', 0)
            report_content += f"- **Overall Score:** {fundamental_score_details.get('overall_score', fundamental_score)}/10 ({fundamental_scorer.get_fundamental_strength_label(fundamental_score_details.get('overall_score', fundamental_score))})\n"
            report_content += f"- **Profitability:** {fundamental_score_details.get('profitability_score', 'N/A')}/10\n"
            report_content += "  - Based on ROE, ROA, and profit margins\n"
            report_content += f"- **Growth:** {fundamental_score_details.get('growth_score', 'N/A')}/10\n"
            report_content += "  - Based on revenue and earnings growth rates\n"
            report_content += f"- **Financial Health:** {fundamental_score_details.get('financial_health_score', 'N/A')}/10\n"
            report_content += "  - Based on debt levels, liquidity, and cash flow\n"
            valuation_score = fundamental_score_details.get('valuation_score', 'N/A')
            # Check if valuation score is misleading
            valuation_data = fundamental_data.get('valuation') if fundamental_data else None
            pe_misleading = valuation_data.get('pe_misleading', False) if valuation_data else False
            
            if pe_misleading:
                report_content += f"- **Valuation:** ⚠️ **{valuation_score}/10 (MISLEADING - P/E not meaningful)**\n"
                report_content += "  - ⚠️ Score reflects misleading P/E ratio. Use P/S ratio or forward P/E estimates instead\n"
            else:
                report_content += f"- **Valuation:** {valuation_score}/10\n"
                report_content += "  - Based on P/E, PEG, and sector comparison\n"
        else:
            report_content += f"- **Overall Score:** {combined_data.get('fundamental_score', 'N/A')}/10\n"
            report_content += "- Component breakdown not available\n"
        
        report_content += "\n### Investment Thesis\n\n"
        report_content += f"{combined_data.get('investment_thesis', 'Analysis complete.')}\n\n"
    
    # Sector/Peer Comparison Section
    if profile and quote and valuation:
        sector = profile.get('sector', '')
        industry = profile.get('industry', '')
        pe_ratio = quote.get('pe')
        sector_comparison = valuation.get('sector_comparison', {})
        
        if sector and pe_ratio:
            report_content += "\n---\n\n## Sector & Peer Comparison\n\n"
            report_content += f"**Sector:** {sector}\n"
            report_content += f"**Industry:** {industry}\n\n"
            
            # Check if P/E is misleading and P/S is being used instead
            pe_misleading = sector_comparison.get('pe_misleading', False)
            primary_metric = sector_comparison.get('primary_metric', 'pe_ratio')
            
            if pe_misleading and sector_comparison.get('ps_ratio'):
                # Use P/S ratio comparison when P/E is misleading
                ps_comp = sector_comparison['ps_ratio']
                ps_ratio = ps_comp.get('current', 'N/A')
                sector_ps = ps_comp.get('sector_avg', 'N/A')
                premium_discount = ps_comp.get('premium_discount', 0)
                multiple = ps_comp.get('multiple')
                
                report_content += "### Valuation Comparison\n\n"
                # Distinguish between negative P/E and extremely high P/E
                if pe_ratio < 0:
                    report_content += f"- **Current P/E Ratio:** {pe_ratio:.2f} ⚠️ *Misleading (negative earnings - P/E not meaningful)*\n"
                else:
                    report_content += f"- **Current P/E Ratio:** {pe_ratio:.2f} ⚠️ *Misleading (negative/low earnings)*\n"
                if isinstance(ps_ratio, (int, float)):
                    report_content += f"- **Current P/S Ratio:** {ps_ratio:.2f}\n"
                else:
                    report_content += f"- **Current P/S Ratio:** {ps_ratio}\n"
                
                if isinstance(sector_ps, (int, float)) and multiple is not None:
                    report_content += f"- **Sector Average P/S:** {sector_ps:.2f}\n"
                    report_content += f"- **Valuation Multiple:** {multiple:.2f}x sector average (P/S)\n"
                    if premium_discount is not None and isinstance(premium_discount, (int, float)):
                        if premium_discount > 0:
                            report_content += f"- **Premium/Discount:** Trading at {premium_discount:.1f}% premium to sector (P/S)\n"
                        else:
                            report_content += f"- **Premium/Discount:** Trading at {abs(premium_discount):.1f}% discount to sector (P/S)\n"
                    report_content += f"- **Assessment:** {ps_comp.get('assessment', 'N/A')}\n"
                else:
                    report_content += f"- **Sector Average P/S:** {sector_ps}\n"
                    report_content += f"- **Assessment:** {ps_comp.get('assessment', 'N/A')}\n"
                
                report_content += "\n**Context:** "
                report_content += "P/E ratio is not meaningful due to negative or very low earnings. "
                report_content += "P/S ratio provides a more appropriate valuation measure for companies with losses. "
                if premium_discount is not None and isinstance(premium_discount, (int, float)):
                    if premium_discount > 50:
                        report_content += "Significant premium valuation requires exceptional performance to justify. "
                    elif premium_discount > 20:
                        report_content += "Premium valuation may be justified by superior fundamentals or growth prospects. "
                    elif premium_discount > -20:
                        report_content += "Valuation is in-line with sector peers, indicating fair pricing. "
                    else:
                        report_content += "Discount valuation may present opportunity if fundamentals improve. "
                report_content += "Consider forward P/E estimates when available.\n"
            
            elif sector_comparison.get('pe_ratio'):
                # Standard P/E comparison
                pe_comp = sector_comparison['pe_ratio']
                sector_pe = pe_comp.get('sector_avg', 'N/A')
                premium_discount = pe_comp.get('premium_discount', 0)
                multiple = pe_comp.get('multiple')
                
                report_content += "### Valuation Comparison\n\n"
                report_content += f"- **Current P/E Ratio:** {pe_ratio:.2f}\n"
                if isinstance(sector_pe, (int, float)) and multiple is not None:
                    report_content += f"- **Sector Average P/E:** {sector_pe:.2f}\n"
                    report_content += f"- **Valuation Multiple:** {multiple:.2f}x sector average\n"
                    if premium_discount is not None and isinstance(premium_discount, (int, float)):
                        if premium_discount > 0:
                            report_content += f"- **Premium/Discount:** Trading at {premium_discount:.1f}% premium to sector\n"
                        else:
                            report_content += f"- **Premium/Discount:** Trading at {abs(premium_discount):.1f}% discount to sector\n"
                    report_content += f"- **Assessment:** {pe_comp.get('assessment', 'N/A')}\n"
                else:
                    report_content += f"- **Sector Average P/E:** {sector_pe}\n"
                    report_content += f"- **Assessment:** {pe_comp.get('assessment', 'N/A')}\n"
                
                report_content += "\n**Context:** "
                if premium_discount is not None and isinstance(premium_discount, (int, float)):
                    if premium_discount > 50:
                        report_content += "Significant premium valuation requires exceptional performance to justify. "
                    elif premium_discount > 20:
                        report_content += "Premium valuation may be justified by superior fundamentals or growth prospects. "
                    elif premium_discount > -20:
                        report_content += "Valuation is in-line with sector peers, indicating fair pricing. "
                    else:
                        report_content += "Discount valuation may present opportunity if fundamentals improve. "
                report_content += "Consider comparing to specific peers within the industry for more detailed analysis.\n"
    
    # Investment Recommendation with Actionable Strategy
    if combined_data:
        # Pass fundamental_data to generate_actionable_recommendation for price targets
        combined_data_with_fundamental = combined_data.copy()
        combined_data_with_fundamental['fundamental_data'] = fundamental_data
        
        strategy = generate_actionable_recommendation(combined_data_with_fundamental, quote, technical_data)
        
        report_content += "\n---\n\n## Investment Recommendation\n\n"
        report_content += f"**Recommendation:** {strategy['recommendation']}  \n"
        report_content += f"**Confidence:** {strategy['confidence']}  \n"
        report_content += f"**Rationale:** {strategy['rationale']}\n\n"
        report_content += f"{strategy.get('entry_strategy', '')}\n\n"
        report_content += f"{strategy.get('exit_strategy', '')}\n\n"
        report_content += f"{strategy.get('risk_management', '')}\n\n"
        
        # Forward-Looking Analysis
    report_content += "\n---\n\n## Forward-Looking Analysis\n\n"
    
    if sentiment_data:
        analyst_sentiment = sentiment_data.get('analyst_sentiment', {})
        if analyst_sentiment and analyst_sentiment.get('recommendations'):
            avg_rating = analyst_sentiment.get('average_rating', 0)
            total_recs = len(analyst_sentiment.get('recommendations', []))
            report_content += f"### Analyst Consensus\n\n"
            report_content += f"- **Average Rating:** {avg_rating:.2f}/5.0\n"
            report_content += f"- **Total Recommendations:** {total_recs}\n"
            report_content += f"- **Consensus:** {'Bullish' if avg_rating >= 3.5 else 'Neutral' if avg_rating >= 2.5 else 'Bearish'}\n\n"
    
    if quote:
        pe_ratio = quote.get('pe', 0)
        eps = quote.get('eps', 0)
        valuation_data = fundamental_data.get('valuation') if fundamental_data else None
        pe_misleading = valuation_data.get('pe_misleading', False) if valuation_data else False
        
        if pe_ratio and eps:
            report_content += f"### Valuation Outlook\n\n"
            # ALGORITHMIC: Don't use P/E for forward analysis when misleading
            if pe_misleading:
                # Use P/S ratio instead
                ratios = fundamental_data.get('ratios', []) if fundamental_data else []
                ps_ratio = ratios[0].get('priceToSalesRatio') if ratios and len(ratios) > 0 else None
                
                # Distinguish between negative P/E and extremely high P/E
                if pe_ratio < 0:
                    # Negative P/E indicates negative earnings
                    if ps_ratio:
                        report_content += f"- ⚠️ Trailing P/E ({pe_ratio:.2f}) is negative, indicating negative earnings (EPS: ${eps:.2f}). P/E ratio is not meaningful for valuation.\n"
                        report_content += f"- Focus on P/S ratio ({ps_ratio:.2f}) and forward P/E estimates for valuation assessment\n"
                        report_content += f"- Monitor forward earnings guidance and cash flow trends for path to profitability\n"
                    else:
                        report_content += f"- ⚠️ Trailing P/E ({pe_ratio:.2f}) is negative, indicating negative earnings (EPS: ${eps:.2f}). P/E ratio is not meaningful for valuation.\n"
                        report_content += f"- Focus on forward P/E estimates, cash flow metrics, or revenue-based valuations\n"
                else:
                    # Extremely high P/E with negative/low earnings
                    if ps_ratio:
                        report_content += f"- ⚠️ Trailing P/E ({pe_ratio:.2f}) is extremely high and not meaningful due to negative/low earnings (EPS: ${eps:.2f})\n"
                        report_content += f"- Focus on P/S ratio ({ps_ratio:.2f}) and forward P/E estimates for valuation assessment\n"
                        report_content += f"- Monitor forward earnings guidance and cash flow trends for valuation improvement\n"
                    else:
                        report_content += f"- ⚠️ Trailing P/E ({pe_ratio:.2f}) is extremely high and not meaningful due to negative/low earnings (EPS: ${eps:.2f})\n"
                        report_content += f"- Focus on forward P/E estimates, cash flow metrics, or revenue-based valuations\n"
            else:
                # Standard P/E-based forward analysis
                if pe_ratio < 20:
                    report_content += f"- Current P/E of {pe_ratio:.2f} suggests reasonable valuation relative to earnings\n"
                elif pe_ratio < 30:
                    report_content += f"- Current P/E of {pe_ratio:.2f} suggests moderate premium, justified by growth prospects\n"
                else:
                    report_content += f"- Current P/E of {pe_ratio:.2f} suggests premium valuation requiring continued strong earnings growth\n"
    
    # Add Trajectory Analysis Section (before Forward-Looking Analysis)
    trajectory_data = fundamental_data.get('trajectory')
    if trajectory_data:
        from trajectory_analyzer import get_trajectory_summary
        trajectory_summary = get_trajectory_summary(trajectory_data)
        
        report_content += "\n### Trajectory Analysis\n\n"
        report_content += f"{trajectory_summary}\n\n"
        
        # Add key improvements/deteriorations
        improvements = trajectory_data.get('key_improvements', [])
        deteriorations = trajectory_data.get('key_deteriorations', [])
        
        if improvements:
            report_content += "**Key Improvements:**\n"
            for improvement in improvements:
                report_content += f"- {improvement}\n"
            report_content += "\n"
        
        if deteriorations:
            report_content += "**Key Concerns:**\n"
            for deterioration in deteriorations:
                report_content += f"- {deterioration}\n"
            report_content += "\n"
    
    # Enhanced Forward-Looking Analysis with Trajectory
    if trajectory_data:
        momentum = trajectory_data.get('momentum', 'unknown')
        profitability_trend = trajectory_data.get('profitability_trend', 'unknown')
        
        report_content += "\n### Path to Profitability Analysis\n\n"
        
        # Check if company is unprofitable
        income = fundamental_data.get('income', [])
        if income and len(income) > 0:
            net_income = income[0].get('netIncome', 0)
            
            if net_income < 0:
                # Unprofitable company - analyze path to profitability
                if momentum == 'improving' and profitability_trend == 'improving_from_losses':
                    report_content += "**Positive Trajectory:** Company shows improving trajectory from losses. "
                    report_content += "If current trend continues, path to profitability appears feasible.\n\n"
                elif momentum == 'deteriorating':
                    report_content += "**Concerning Trajectory:** Company shows deteriorating trajectory with widening losses. "
                    report_content += "Path to profitability requires significant operational improvements.\n\n"
                else:
                    report_content += "**Stable Trajectory:** Company remains unprofitable but trajectory is stable. "
                    report_content += "Monitor quarterly results for signs of improvement.\n\n"
                
                # Add SEC guidance if available, otherwise placeholder
                sec_guidance = fundamental_data.get('sec_guidance')
                if sec_guidance and sec_guidance.get('available'):
                    from sec_guidance_extractor import SECGuidanceExtractor
                    sec_extractor = SECGuidanceExtractor()
                    guidance_summary = sec_extractor.get_guidance_summary(sec_guidance)
                    
                    report_content += "**Management Guidance (from SEC Filings):**\n"
                    report_content += f"- {guidance_summary}\n\n"
                    
                    # Add filing references
                    filings = sec_guidance.get('filings', [])
                    if filings:
                        report_content += "**Recent SEC Filings:**\n"
                        for filing in filings[:5]:
                            form = filing.get('form', 'N/A')
                            date = filing.get('date', 'N/A')
                            report_content += f"- {form} - {date}\n"
                        report_content += "\n"
                    
                    # Add extracted guidance details
                    # First try to get agent-generated comprehensive extraction
                    guidance = {}
                    sec_text = sec_guidance.get('_sec_text_for_ai', '')
                    if sec_text:
                        from agent_interpretation_injector import get_agent_interpretation
                        import json
                        guidance_key = f"sec_guidance_{symbol}_{hash(sec_text[:500])}"
                        agent_extraction_json = get_agent_interpretation(guidance_key)
                        if agent_extraction_json:
                            try:
                                guidance = json.loads(agent_extraction_json)
                            except:
                                pass
                    
                    # Fallback to basic extraction if agent extraction not available
                    if not guidance:
                        guidance = sec_guidance.get('guidance', {})
                    
                    # GMV/Revenue targets
                    if guidance.get('gmv_targets'):
                        gmv_targets = guidance.get('gmv_targets', [])
                        gmv_strs = []
                        for target in gmv_targets:
                            if isinstance(target, dict):
                                gmv_strs.append(f"${target.get('amount', 'N/A')} by {target.get('year', 'N/A')}")
                            else:
                                gmv_strs.append(str(target))
                        if gmv_strs:
                            report_content += f"- **GMV Targets:** {', '.join(gmv_strs)}\n"
                    elif guidance.get('revenue_targets'):
                        targets = guidance.get('revenue_targets', [])
                        if targets:
                            report_content += f"- **Revenue Targets:** {', '.join([str(t) for t in targets])}\n"
                    
                    # Profitability timeline
                    if guidance.get('profitability_timeline'):
                        report_content += f"- **Profitability Timeline:** {guidance['profitability_timeline']}\n"
                    
                    # EBITDA targets
                    if guidance.get('ebitda_targets'):
                        ebitda_str = ', '.join([f"{t['margin']}% by {t['year']}" for t in guidance['ebitda_targets']])
                        report_content += f"- **EBITDA Margin Targets:** {ebitda_str}\n"
                    
                    # Self-funded growth
                    if guidance.get('self_funded_growth') or guidance.get('no_capital_raises'):
                        report_content += "- **Self-Funded Growth:** Management expects growth to be self-funded (no further capital raises expected)\n"
                    
                    # Strategic Initiatives (NEW)
                    strategic_initiatives = guidance.get('strategic_initiatives', [])
                    if strategic_initiatives:
                        report_content += "\n**Strategic Initiatives (from SEC filings):**\n"
                        for initiative in strategic_initiatives[:5]:
                            report_content += f"- {initiative}\n"
                    
                    # Competitive Positioning (NEW)
                    competitive = guidance.get('competitive_positioning', [])
                    if competitive:
                        report_content += "\n**Competitive Positioning (from SEC filings):**\n"
                        for item in competitive[:3]:
                            report_content += f"- {item}\n"
                    
                    # Market Outlook (NEW)
                    market_outlook = guidance.get('market_outlook', [])
                    if market_outlook:
                        report_content += "\n**Market Outlook (from SEC filings):**\n"
                        for outlook in market_outlook[:3]:
                            report_content += f"- {outlook}\n"
                    
                    # Capital Allocation (NEW)
                    capital_allocation = guidance.get('capital_allocation', [])
                    if capital_allocation:
                        report_content += "\n**Capital Allocation Priorities (from SEC filings):**\n"
                        for item in capital_allocation[:3]:
                            report_content += f"- {item}\n"
                    
                    # Management Tone & Confidence (NEW)
                    management_tone = guidance.get('management_tone', 'neutral')
                    confidence_level = guidance.get('confidence_level', 'medium')
                    if management_tone != 'neutral' or confidence_level != 'medium':
                        report_content += f"\n**Management Tone:** {management_tone.title()} | **Confidence Level:** {confidence_level.title()}\n"
                    
                    # Operational metrics
                    operational_metrics = guidance.get('operational_metrics', {})
                    if operational_metrics:
                        report_content += "\n**Operational Improvements (from SEC filings):**\n"
                        
                        if operational_metrics.get('payroll_reduction'):
                            pr = operational_metrics['payroll_reduction']
                            report_content += f"- **Payroll Reduction:** {pr['from']:,} to {pr['to']:,} employees ({pr['reduction_pct']:.1f}% reduction)\n"
                        
                        if operational_metrics.get('pickup_station_percentage'):
                            report_content += f"- **Pickup Stations:** {operational_metrics['pickup_station_percentage']}% of deliveries\n"
                        
                        if operational_metrics.get('fulfillment_cost_reduction'):
                            fcr = operational_metrics['fulfillment_cost_reduction']
                            report_content += f"- **Fulfillment Costs:** {fcr['from']:.1f}% to {fcr['to']:.1f}% of GMV ({fcr['reduction_pct']:.1f}% reduction)\n"
                        
                        if operational_metrics.get('nps_improvement'):
                            nps = operational_metrics['nps_improvement']
                            report_content += f"- **Net Promoter Score:** {nps['from']} to {nps['to']} (+{nps['improvement']} points)\n"
                        
                        if operational_metrics.get('repurchase_rate'):
                            rr = operational_metrics['repurchase_rate']
                            report_content += f"- **Repurchase Rate:** {rr['from']}% to {rr['to']}% (+{rr['improvement']} points)\n"
                        
                        if operational_metrics.get('geographic_expansion'):
                            report_content += f"- **Geographic Expansion:** {operational_metrics['geographic_expansion']}% of orders outside capital cities\n"
                    
                    report_content += "\n"
                else:
                    # Fallback to placeholder
                    report_content += "**Management Guidance:**\n"
                    report_content += "- ⚠️ **Note:** Management guidance extraction from SEC filings is in progress. "
                    report_content += "Review latest earnings calls and investor presentations for:\n"
                    report_content += "  - Revenue growth targets\n"
                    report_content += "  - Profitability timeline (e.g., profitability by 2027)\n"
                    report_content += "  - Key operational milestones\n"
                    report_content += "  - Cost reduction initiatives\n\n"
                
                # Add Earnings Transcript Insights
                transcript_data = fundamental_data.get('transcript')
                if transcript_data and transcript_data.get('available'):
                    report_content += "**Earnings Transcript Insights:**\n"
                    report_content += f"- **Source:** {transcript_data.get('source', 'Unknown')}\n"
                    report_content += f"- **Date:** {transcript_data.get('date', 'Unknown')}\n"
                    
                    # Try to get AI-generated insights
                    try:
                        from agent_interpretation_injector import get_agent_interpretation
                        import json
                        
                        transcript_text = transcript_data.get('transcript', '')
                        if transcript_text:
                            transcript_key = f"transcript_insights_{symbol}_{hash(transcript_text[:500])}"
                            insights_json = get_agent_interpretation(transcript_key)
                            
                            if insights_json:
                                insights = json.loads(insights_json)
                                
                                # Management Guidance from Transcript
                                mgmt_guidance = insights.get('management_guidance', {})
                                if mgmt_guidance:
                                    report_content += "\n**Management Guidance (from Transcript):**\n"
                                    if mgmt_guidance.get('revenue_targets'):
                                        report_content += f"- **Revenue Targets:** {', '.join(mgmt_guidance['revenue_targets'])}\n"
                                    if mgmt_guidance.get('profitability_timeline'):
                                        report_content += f"- **Profitability Timeline:** {mgmt_guidance['profitability_timeline']}\n"
                                    if mgmt_guidance.get('ebitda_targets'):
                                        ebitda_str = ', '.join([f"{t['margin']}% by {t['year']}" for t in mgmt_guidance['ebitda_targets']])
                                        report_content += f"- **EBITDA Margin Targets:** {ebitda_str}\n"
                                
                                # Key Metrics Discussed
                                key_metrics = insights.get('key_metrics_discussed', [])
                                if key_metrics:
                                    report_content += "\n**Key Metrics Discussed:**\n"
                                    for metric in key_metrics[:5]:
                                        report_content += f"- {metric}\n"
                                
                                # Strategic Initiatives
                                strategic = insights.get('strategic_initiatives', [])
                                if strategic:
                                    report_content += "\n**Strategic Initiatives:**\n"
                                    for initiative in strategic[:5]:
                                        report_content += f"- {initiative}\n"
                                
                                # Sentiment Analysis
                                sentiment = insights.get('sentiment', {})
                                if sentiment:
                                    report_content += "\n**Management Sentiment:**\n"
                                    report_content += f"- **Overall Tone:** {sentiment.get('overall', 'neutral').title()}\n"
                                    report_content += f"- **Confidence Level:** {sentiment.get('confidence_level', 'medium').title()}\n"
                                    key_themes = sentiment.get('key_themes', [])
                                    if key_themes:
                                        report_content += f"- **Key Themes:** {', '.join(key_themes[:3])}\n"
                                
                                # Forward Statements
                                forward_statements = insights.get('forward_statements', [])
                                if forward_statements:
                                    report_content += "\n**Forward-Looking Statements:**\n"
                                    for statement in forward_statements[:3]:
                                        report_content += f"- {statement}\n"
                                
                                # Q&A Highlights
                                qa_highlights = insights.get('q_and_a_highlights', [])
                                if qa_highlights:
                                    report_content += "\n**Q&A Highlights:**\n"
                                    for highlight in qa_highlights[:3]:
                                        report_content += f"- {highlight}\n"
                    except Exception as e:
                        # If insights not available, show basic info
                        report_content += "- ⚠️ **Note:** AI insights extraction from transcript is in progress.\n"
                        report_content += f"- Transcript available ({len(transcript_data.get('transcript', ''))} chars)\n"
                    
                    report_content += "\n"
    
    report_content += "\n### Key Catalysts to Monitor\n\n"
    
    # Add company-specific catalysts based on sector/industry/company name
    profile = fundamental_data.get('profile', {}) if fundamental_data else {}
    sector = profile.get('sector', '') if profile else ''
    industry = profile.get('industry', '') if profile else ''
    company_name = profile.get('companyName', '') if profile else ''
    
    # Generic catalysts
    report_content += "- Earnings announcements and guidance updates\n"
    
    # Company-specific catalysts (check company name first for specific companies)
    if 'Apple' in company_name or symbol == 'AAPL':
        report_content += "- iPhone launch cycles and new model releases\n"
        report_content += "- Services revenue growth (App Store, iCloud, Apple Music, Apple TV+)\n"
        report_content += "- China market dynamics and regulatory environment\n"
        report_content += "- App Store regulatory scrutiny and potential changes\n"
        report_content += "- Supply chain resilience and manufacturing diversification\n"
        report_content += "- Wearables (Apple Watch, AirPods) market expansion\n"
    elif 'Microsoft' in company_name or symbol == 'MSFT':
        report_content += "- Azure cloud growth and market share gains\n"
        report_content += "- AI integration across product suite (Copilot, OpenAI partnerships)\n"
        report_content += "- Enterprise software renewal cycles\n"
        report_content += "- Gaming division performance (Xbox, Activision integration)\n"
        report_content += "- Regulatory scrutiny (antitrust, AI governance)\n"
    elif 'Google' in company_name or 'Alphabet' in company_name or symbol == 'GOOGL':
        report_content += "- Search advertising revenue trends\n"
        report_content += "- YouTube monetization and growth\n"
        report_content += "- Cloud Platform (GCP) market share gains\n"
        report_content += "- AI developments (Gemini, Bard integration)\n"
        report_content += "- Regulatory challenges (antitrust, privacy)\n"
    elif 'Amazon' in company_name or symbol == 'AMZN':
        report_content += "- AWS cloud growth and market share\n"
        report_content += "- E-commerce growth and Prime membership trends\n"
        report_content += "- Advertising revenue expansion\n"
        report_content += "- International expansion and profitability\n"
        report_content += "- Logistics and fulfillment efficiency\n"
    # Sector/Industry-specific catalysts
    elif sector == 'Technology':
        if 'Semiconductor' in industry or 'Semiconductor' in company_name:
            report_content += "- AI chip demand trends and data center expansion\n"
            report_content += "- New product launches (GPU generations, AI accelerators)\n"
            report_content += "- Supply chain dynamics and manufacturing capacity\n"
            report_content += "- Competition from AMD, Intel, and custom chip designs\n"
        elif 'Software' in industry or 'Cloud' in industry:
            report_content += "- Cloud infrastructure spending trends\n"
            report_content += "- SaaS subscription growth and retention rates\n"
            report_content += "- Enterprise digital transformation initiatives\n"
            report_content += "- Platform ecosystem expansion and partnerships\n"
        elif 'Consumer Electronics' in industry:
            report_content += "- Product launch cycles and innovation\n"
            report_content += "- Consumer spending trends and economic cycles\n"
            report_content += "- Supply chain and manufacturing dynamics\n"
            report_content += "- Brand strength and market positioning\n"
        else:
            report_content += "- Product launches and market expansion\n"
            report_content += "- Technology adoption cycles\n"
    elif sector == 'Healthcare':
        report_content += "- FDA approvals and clinical trial results\n"
        report_content += "- Drug pipeline developments\n"
        report_content += "- Healthcare policy changes\n"
    elif sector == 'Financial':
        report_content += "- Interest rate changes and monetary policy\n"
        report_content += "- Regulatory capital requirements\n"
        report_content += "- Loan growth and credit quality trends\n"
    else:
        report_content += "- Product launches and market expansion\n"
    
    # Generic catalysts that apply to all
    report_content += "- Regulatory developments\n"
    report_content += "- Competitive dynamics and market share changes\n"
    report_content += "- Macroeconomic factors affecting sector performance\n\n"
    
    # Risk Factors - Generate stock-specific risks
    report_content += "\n---\n\n## Risk Factors\n\n"
    
    if combined_data:
        overall_risk = combined_data.get('overall_risk', 'Medium')
        valuation_risk = combined_data.get('valuation_risk', 1.0)
        fundamental_score = combined_data.get('fundamental_score', 5.0)
        technical_score = combined_data.get('technical_score', 5.0)
        
        risks = []
        
        # Sector-specific risks
        if profile:
            sector = profile.get('sector', '')
            industry = profile.get('industry', '')
            company_name = profile.get('companyName', '')
            
            # Technology/Semiconductor risks
            if sector == 'Technology' and ('Semiconductor' in industry or 'Semiconductor' in company_name):
                risks.append("**Geopolitical Risks:** Semiconductor companies face risks from trade tensions and geopolitical conflicts, particularly for companies with operations in Taiwan or China.")
                risks.append("**Cyclical Industry:** Semiconductor industry is cyclical and subject to demand fluctuations, inventory cycles, and capacity utilization changes.")
            
            # Taiwan-specific risks
            if 'Taiwan' in company_name or symbol == 'TSM':
                risks.append("**Taiwan-China Relations:** Geopolitical tensions between Taiwan and China pose significant risks to operations, supply chains, and market access.")
            
            # Apple-specific risks
            if symbol == 'AAPL' or 'Apple' in company_name:
                risks.append("**China Market Exposure:** Significant revenue exposure to China (~20% of sales) creates vulnerability to geopolitical tensions, regulatory changes, and economic slowdowns.")
                risks.append("**iPhone Dependency:** Heavy reliance on iPhone sales (~50% of revenue) makes Apple vulnerable to product cycle risks, competition, and market saturation.")
                risks.append("**Services Regulatory Scrutiny:** App Store practices face ongoing regulatory challenges globally (EU Digital Markets Act, US antitrust investigations) that could impact Services revenue.")
                risks.append("**Supply Chain Concentration:** Dense supply chain concentration in China/Taiwan creates geopolitical and operational risks.")
                risks.append("**Premium Pricing Vulnerability:** High price points make products sensitive to economic downturns and consumer spending shifts.")
            
            # Microsoft-specific risks
            elif symbol == 'MSFT' or ('Microsoft' in company_name and ('Cloud' in industry or 'Infrastructure' in industry)):
                risks.append("**Regulatory Scrutiny:** Microsoft faces ongoing regulatory scrutiny related to antitrust concerns, AI governance, and cloud market dominance, which could impact business operations.")
                risks.append("**Cloud Market Competition:** Intense competition from AWS and Google Cloud Platform may pressure Azure growth rates and margins.")
                risks.append("**Enterprise Spending Cycles:** Dependence on enterprise IT spending cycles makes Microsoft vulnerable to economic downturns and budget constraints.")
                risks.append("**AI Competition:** Rapid AI innovation from competitors (Google, OpenAI partnerships) could challenge Microsoft's AI leadership position.")
                risks.append("**Azure Growth Sustainability:** Azure growth rates may slow as cloud market matures, impacting overall revenue growth trajectory.")
            
            # Google/Alphabet-specific risks
            elif symbol == 'GOOGL' or 'Google' in company_name or 'Alphabet' in company_name:
                risks.append("**Regulatory Challenges:** Ongoing antitrust investigations and regulatory actions globally (EU, US) could impact search dominance and advertising revenue.")
                risks.append("**Search Market Maturation:** Core search advertising market may face growth headwinds as market matures.")
                risks.append("**AI Disruption Risk:** AI-powered search alternatives could disrupt traditional search model.")
                risks.append("**Privacy Regulations:** Increasing privacy regulations (GDPR, CCPA) may impact advertising targeting capabilities.")
            
            # Amazon-specific risks
            elif symbol == 'AMZN' or 'Amazon' in company_name:
                risks.append("**E-commerce Competition:** Intense competition from Walmart, Target, and other retailers may pressure margins.")
                risks.append("**AWS Market Share:** Cloud market competition from Microsoft Azure and Google Cloud may slow AWS growth.")
                risks.append("**Regulatory Scrutiny:** Antitrust concerns and labor practices may face increased regulatory scrutiny.")
                risks.append("**Capital Intensity:** High capital expenditure requirements for logistics and fulfillment may impact free cash flow.")
            
            elif 'Cloud' in industry or 'Infrastructure' in industry:
                risks.append("**Capital Intensity:** High capital expenditure requirements for data center expansion may impact free cash flow and returns.")
                risks.append("**Competition:** Intense competition from major cloud providers (AWS, Azure, GCP) may pressure margins.")
            
            # REIT risks
            if sector == 'Real Estate' or 'REIT' in industry:
                risks.append("**Interest Rate Sensitivity:** REITs are sensitive to interest rate changes, which can impact valuations and financing costs.")
                risks.append("**Capital Requirements:** Need for capital to fund acquisitions and development may impact dividend sustainability.")
        
        # Valuation risks
        if valuation_risk > 1.5:
            risks.append(f"**Valuation Risk:** Trading at {valuation_risk:.2f}x sector average requires continued exceptional performance to justify premium valuation.")
        elif valuation_risk > 1.2:
            risks.append(f"**Elevated Valuation:** Trading at {valuation_risk:.2f}x sector average may limit upside potential if growth expectations are not met.")
        
        # Fundamental risks
        if fundamental_score < 6.0:
            risks.append("**Fundamental Concerns:** Below-average fundamental metrics indicate potential operational or financial challenges that could impact long-term performance.")
        
        # Technical risks
        if technical_score < 5.0:
            risks.append("**Technical Weakness:** Weak technical indicators suggest potential downside risk and may indicate deteriorating market sentiment.")
        
        # Alignment risks
        alignment = combined_data.get('alignment', '')
        if 'Divergence' in alignment:
            risks.append("**Analysis Divergence:** Conflicting signals between fundamental, technical, and sentiment analysis create uncertainty and require careful monitoring.")
        
        # Growth risks
        if growth:
            rev_growth = growth[0].get('revenueGrowth', 0)
            if rev_growth < 0:
                risks.append("**Revenue Decline:** Negative revenue growth indicates declining business fundamentals and market challenges.")
        
        # Profitability risks
        if ratios:
            roe = ratios[0].get('returnOnEquity', 0)
            if roe < 0.1:
                risks.append("**Low Profitability:** Weak return on equity indicates inefficient use of capital and may signal operational challenges.")
        
        # Debt risks
        if ratios:
            debt_equity = ratios[0].get('debtEquityRatio', 0)
            if debt_equity > 1.5:
                risks.append(f"**High Leverage:** Elevated debt-to-equity ratio ({debt_equity:.2f}) increases financial risk and reduces financial flexibility.")
        
        # Add risks to report
        if risks:
            for risk in risks:
                report_content += f"- {risk}\n"
        else:
            report_content += f"- Risk factors identified from analysis are manageable given strong fundamentals and technicals.\n"
        
        report_content += f"\n**Overall Risk Level:** {overall_risk}\n"
    
    # Price Targets - Using actual technical levels and fundamental analysis
    report_content += "\n---\n\n## Price Targets\n\n"
    
    if quote and combined_data:
        current_price = quote.get('price', 0)
        if current_price:
            fundamental_data_for_targets = fundamental_data
            fundamental_score = combined_data.get('fundamental_score', 5.0)
            valuation_risk = combined_data.get('valuation_risk', 1.0)
            growth = fundamental_data.get('growth', [])
            
            price_targets = generate_price_targets(technical_data, quote, fundamental_score, valuation_risk, growth)
            
            if price_targets:
                report_content += "**Price Targets (based on technical resistance levels and fundamental valuation):**\n\n"
                
                if 'target1' in price_targets:
                    t1 = price_targets['target1']
                    report_content += f"- **Target 1:** ${t1['price']:.2f} ({t1['upside']:.1f}% upside) - {t1['description']}\n"
                    report_content += f"  *Basis: {t1['basis']}*\n\n"
                
                if 'target2' in price_targets:
                    t2 = price_targets['target2']
                    report_content += f"- **Target 2:** ${t2['price']:.2f} ({t2['upside']:.1f}% upside) - {t2['description']}\n"
                    report_content += f"  *Basis: {t2['basis']}*\n\n"
                
                if 'target3' in price_targets:
                    t3 = price_targets['target3']
                    report_content += f"- **Target 3:** ${t3['price']:.2f} ({t3['upside']:.1f}% upside) - {t3['description']}\n"
                    report_content += f"  *Basis: {t3['basis']}*\n\n"
                
                if 'support_levels' in price_targets and price_targets['support_levels']:
                    report_content += "**Support Levels (from technical analysis):**\n"
                    for i, support in enumerate(price_targets['support_levels'][:3], 1):
                        report_content += f"- **Support {i}:** ${support:.2f} ({((support/current_price - 1)*100):.1f}% below current)\n"
                else:
                    report_content += "**Support Levels:**\n"
                    report_content += f"- **Key Support:** ${current_price * 0.95:.2f} (5% below current)\n"
                    report_content += f"- **Strong Support:** ${current_price * 0.90:.2f} (10% below current)\n"
                
                report_content += "\n*Targets derived from actual technical resistance levels and fundamental earnings growth analysis.*\n"
        else:
                # Fallback
                target1 = current_price * 1.05
                target2 = current_price * 1.10
                target3 = current_price * 1.15
                
                report_content += "**Price Targets:**\n\n"
                report_content += f"- **Target 1:** ${target1:.2f} (5% upside) - Near-term target\n"
                report_content += f"- **Target 2:** ${target2:.2f} (10% upside) - Medium-term target\n"
                report_content += f"- **Target 3:** ${target3:.2f} (15% upside) - Optimistic target\n\n"
                report_content += "**Support Levels:**\n"
                report_content += f"- **Key Support:** ${current_price * 0.95:.2f} (5% below current)\n"
                report_content += f"- **Strong Support:** ${current_price * 0.90:.2f} (10% below current)\n"
    
    # Data Sources
    report_content += "\n---\n\n## Data Sources & Verification\n\n**Data Sources:**\n"
    report_content += "- Financial Modeling Prep (FMP) API\n"
    report_content += "- Historical price data: 365 days\n\n"
    
    # Add data freshness information
    if data_freshness:
        from data_freshness_checker import get_data_freshness_summary
        freshness_summary = get_data_freshness_summary(data_freshness)
        report_content += "**Data Freshness:**\n"
        report_content += f"- {freshness_summary}\n"
        
        # Show individual data periods if available
        data_periods = data_freshness.get('data_periods', {})
        if data_periods:
            report_content += "\n**Data Periods:**\n"
            for data_type, period_info in data_periods.items():
                date_str = period_info.get('date', 'N/A')
                days_old = period_info.get('days_old', 'N/A')
                period_type = period_info.get('period', 'unknown')
                if date_str != 'N/A':
                    report_content += f"- **{data_type.capitalize()}:** {date_str} ({days_old} days old, {period_type})\n"
        report_content += "\n"
    
    report_content += f"**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    report_content += "**Methodology:**\n"
    report_content += "This analysis follows the Stock Analyst Skill workflow with AI interpretation:\n"
    report_content += "1. Initialize and Setup\n"
    report_content += "2. Fundamental Analysis (with AI interpretation)\n"
    report_content += "3. Technical Analysis (with AI interpretation)\n"
    report_content += "3.5. Sentiment Analysis (analyst recommendations & news sentiment)\n"
    report_content += "4. Combined Analysis (with AI synthesis including sentiment)\n"
    report_content += "5. Report Generation (with comprehensive AI interpretation)\n\n"
    report_content += "---\n\n"
    report_content += "*Report generated using Stock Analyst Skill with AI Interpretation*\n"
    report_content += "*All metrics interpreted with context and actionable insights*\n"
    
    # Save report to ticker-specific directory with date-based filename
    base_dir = os.path.join(os.path.expanduser('~/personal'), 'stock_analysis')
    ticker_dir = os.path.join(base_dir, symbol)
    os.makedirs(ticker_dir, exist_ok=True)
    
    # Generate date and time-based filename to prevent overwrites
    timestamp_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    report_filename = f"{timestamp_str}_comprehensive_analysis.md"
    report_path = os.path.join(ticker_dir, report_filename)
    
    with open(report_path, 'w') as f:
        f.write(report_content)
    
    print(f"    ✅ Comprehensive report with AI interpretation saved to: {report_path}")
    
    return report_path
