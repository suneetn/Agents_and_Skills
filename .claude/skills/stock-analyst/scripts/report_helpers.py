#!/usr/bin/env python3
"""
Report Helper Functions
Provides helper functions for generating price targets and actionable recommendations
"""

from typing import Dict, List


def generate_price_targets(technical_data: Dict, quote: Dict, fundamental_score: float, valuation_risk: float, growth: List[Dict], forward_data: Dict = None) -> Dict:
    """Generate price targets based on technical resistance levels and fundamental valuation"""
    current_price = quote.get('price', 0) if quote else 0
    if not current_price:
        return {}
    
    targets = {}
    technical_data_dict = technical_data.get('data', {}) if technical_data else {}
    
    # Get technical resistance levels
    resistance_levels = technical_data_dict.get('resistance_levels', [])
    support_levels = technical_data_dict.get('support_levels', [])
    
    # Use actual resistance levels as targets if available
    if resistance_levels and len(resistance_levels) > 0:
        # Filter resistance levels above current price
        above_price = [r for r in resistance_levels if r > current_price]
        if above_price:
            targets['target1'] = {
                'price': above_price[0],
                'upside': ((above_price[0] / current_price) - 1) * 100,
                'basis': 'Technical Resistance',
                'description': 'Near-term resistance level'
            }
            if len(above_price) > 1:
                targets['target2'] = {
                    'price': above_price[1],
                    'upside': ((above_price[1] / current_price) - 1) * 100,
                    'basis': 'Technical Resistance',
                    'description': 'Medium-term resistance level'
                }
            if len(above_price) > 2:
                targets['target3'] = {
                    'price': above_price[2],
                    'upside': ((above_price[2] / current_price) - 1) * 100,
                    'basis': 'Technical Resistance',
                    'description': 'Long-term resistance level'
                }
    
    # Add fundamental-based targets if strong fundamentals (using P/E multiple expansion, not direct growth application)
    # This is more realistic than directly applying earnings growth to stock price
    if fundamental_score >= 8.0 and quote:
        pe_ratio = quote.get('pe', 0)
        current_eps = quote.get('eps', 0)
        
        # Flag extreme growth rates as potentially cyclical (recovery from low base)
        is_cyclical_growth = False
        if growth and len(growth) > 0:
            net_income_growth = growth[0].get('netIncomeGrowth', 0)
            if net_income_growth > 1:
                growth_rate = (net_income_growth - 1) * 100
            else:
                growth_rate = net_income_growth * 100
            
            # Flag growth > 200% as potentially cyclical
            if growth_rate > 200:
                is_cyclical_growth = True
        
        # Use P/E multiple expansion method (more realistic than direct growth application)
        if pe_ratio and pe_ratio > 0 and current_eps and current_eps > 0:
            # Conservative: 10% P/E expansion
            # Moderate: 20% P/E expansion
            # Optimistic: 30% P/E expansion
            # This assumes earnings stay stable or grow modestly, not at extreme rates
            
            if 'target1' not in targets:
                conservative_pe = pe_ratio * 1.10
                conservative_price = current_eps * conservative_pe
                if conservative_price > current_price:
                    cyclical_note = " (Note: Recent growth may be cyclical recovery, not sustainable)" if is_cyclical_growth else ""
                    targets['target1'] = {
                        'price': conservative_price,
                        'upside': ((conservative_price / current_price) - 1) * 100,
                        'basis': f'Fundamental (10% P/E multiple expansion){cyclical_note} - Assumes modest multiple expansion with stable earnings',
                        'description': 'Conservative fundamental target'
                    }
            
            if 'target2' not in targets:
                moderate_pe = pe_ratio * 1.20
                moderate_price = current_eps * moderate_pe
                if moderate_price > current_price:
                    cyclical_note = " (Note: Recent growth may be cyclical recovery, not sustainable)" if is_cyclical_growth else ""
                    targets['target2'] = {
                        'price': moderate_price,
                        'upside': ((moderate_price / current_price) - 1) * 100,
                        'basis': f'Fundamental (20% P/E multiple expansion){cyclical_note} - Assumes moderate multiple expansion with stable earnings',
                        'description': 'Moderate fundamental target'
                    }
            
            if 'target3' not in targets:
                optimistic_pe = pe_ratio * 1.30
                optimistic_price = current_eps * optimistic_pe
                if optimistic_price > current_price:
                    cyclical_note = " (Note: Recent growth may be cyclical recovery, not sustainable)" if is_cyclical_growth else ""
                    targets['target3'] = {
                        'price': optimistic_price,
                        'upside': ((optimistic_price / current_price) - 1) * 100,
                        'basis': f'Fundamental (30% P/E multiple expansion){cyclical_note} - Assumes strong multiple expansion with stable earnings',
                        'description': 'Optimistic fundamental target'
                    }
    
    # Fallback to improved targets if no technical/fundamental targets
    if not targets:
        # Try to use technical resistance levels if available
        if technical_data and technical_data.get('data', {}).get('resistance_levels'):
            resistance_levels = technical_data['data']['resistance_levels']
            above_price = [r for r in resistance_levels if r > current_price]
            if above_price:
                # Use nearest resistance as target 1
                targets['target1'] = {
                    'price': above_price[0],
                    'upside': ((above_price[0] / current_price) - 1) * 100,
                    'basis': f'Technical Resistance Level (${above_price[0]:.2f})',
                    'description': 'Near-term technical target'
                }
                if len(above_price) > 1:
                    targets['target2'] = {
                        'price': above_price[1],
                        'upside': ((above_price[1] / current_price) - 1) * 100,
                        'basis': f'Technical Resistance Level (${above_price[1]:.2f})',
                        'description': 'Medium-term technical target'
                    }
                if len(above_price) > 2:
                    targets['target3'] = {
                        'price': above_price[2],
                        'upside': ((above_price[2] / current_price) - 1) * 100,
                        'basis': f'Technical Resistance Level (${above_price[2]:.2f})',
                        'description': 'Long-term technical target'
                    }
        
        # If still no targets, use conservative percentage-based with explanation
        if not targets:
            targets['target1'] = {
                'price': current_price * 1.05,
                'upside': 5.0,
                'basis': 'Conservative estimate (5% upside) - Based on historical average returns, no specific fundamental or technical catalyst identified',
                'description': 'Near-term conservative target'
            }
            targets['target2'] = {
                'price': current_price * 1.10,
                'upside': 10.0,
                'basis': 'Moderate estimate (10% upside) - Based on historical average returns, no specific fundamental or technical catalyst identified',
                'description': 'Medium-term moderate target'
            }
            targets['target3'] = {
                'price': current_price * 1.15,
                'upside': 15.0,
                'basis': 'Optimistic estimate (15% upside) - Based on historical average returns, no specific fundamental or technical catalyst identified',
                'description': 'Long-term optimistic target'
            }
    
    # Get support levels - use realistic levels based on stock strength
    if support_levels and len(support_levels) > 0:
        # Filter support levels below current price
        below_price = [s for s in support_levels if s < current_price]
        # For strong stocks, only show support levels within reasonable range (< 20% below)
        reasonable_support = [s for s in below_price if s >= current_price * 0.80]
        if reasonable_support:
            targets['support_levels'] = reasonable_support[:3]  # Top 3 reasonable support levels
        else:
            # If no reasonable support found, use calculated levels based on stock strength
            if fundamental_score >= 8.0:
                # Strong stock: tighter support (5-10% below)
                targets['support_levels'] = [
                    current_price * 0.95,  # 5% below
                    current_price * 0.90   # 10% below
                ]
            else:
                # Moderate stock: wider support (10-15% below)
                targets['support_levels'] = [
                    current_price * 0.90,  # 10% below
                    current_price * 0.85   # 15% below
                ]
    else:
        # Fallback support levels based on stock strength
        if fundamental_score >= 8.0:
            # Strong stock: tighter support
            targets['support_levels'] = [
                current_price * 0.95,  # 5% below
                current_price * 0.90   # 10% below
            ]
        else:
            # Moderate stock: wider support
            targets['support_levels'] = [
                current_price * 0.90,  # 10% below
                current_price * 0.85   # 15% below
            ]
    
    return targets


def generate_actionable_recommendation(combined_data: Dict, quote: Dict, technical_data: Dict) -> Dict[str, str]:
    """Generate actionable recommendation with entry/exit strategy using actual technical levels"""
    recommendation = combined_data.get('recommendation', 'Hold')
    confidence = combined_data.get('confidence', 'Medium')
    rationale = combined_data.get('rationale', '')
    
    current_price = quote.get('price', 0) if quote else 0
    
    # Enhance rationale with actionable guidance
    fundamental_score = combined_data.get('fundamental_score', 5.0)
    technical_score = combined_data.get('technical_score', 5.0)
    sentiment_score = combined_data.get('sentiment_score', 0.0)
    
    # Get support/resistance for rationale
    technical_data_dict = technical_data.get('data', {}) if technical_data else {}
    support_levels = technical_data_dict.get('support_levels', [])
    actual_supports = [s for s in support_levels if s < current_price] if support_levels and current_price else []
    nearest_support = actual_supports[0] if actual_supports else current_price * 0.95 if current_price else 0
    
    # Always regenerate rationale with proper score descriptors
    if not rationale or "Mixed signals" in rationale or "Moderate fundamentals" in rationale or "moderate fundamentals" in rationale:
        # Generate enhanced rationale with proper descriptors
        if fundamental_score >= 7.0 and technical_score < 5.0:
            rationale = f"Strong fundamentals ({fundamental_score:.1f}/10) and bullish sentiment ({sentiment_score:.3f}) support long-term investment thesis, but short-term technical weakness ({technical_score:.1f}/10) suggests waiting for better entry. For long-term investors, current price may be acceptable given fundamental strength. For tactical traders, wait for technical confirmation above ${current_price * 1.02:.2f} or pullback to ${nearest_support:.2f} support."
        elif fundamental_score >= 7.0:
            # Use proper descriptors
            fund_desc = "Exceptional" if fundamental_score >= 9.0 else "Strong" if fundamental_score >= 8.0 else "Good"
            tech_desc = "Strong" if technical_score >= 8.0 else "Good" if technical_score >= 7.0 else "Moderate"
            rationale = f"{fund_desc} fundamentals ({fundamental_score:.1f}/10) and {tech_desc.lower()} technical setup ({technical_score:.1f}/10) support investment thesis. Bullish sentiment ({sentiment_score:.3f}) reinforces positive outlook."
        elif technical_score >= 7.0 and fundamental_score < 5.0:
            rationale = f"Strong technical momentum ({technical_score:.1f}/10) but weak fundamentals ({fundamental_score:.1f}/10) create risk. Technical strength may be short-lived without fundamental support."
        else:
            rationale = f"Mixed signals: Fundamentals {fundamental_score:.1f}/10, Technicals {technical_score:.1f}/10. Awaiting clearer directional confirmation from either fundamental improvement or technical breakout."
    
    technical_data_dict = technical_data.get('data', {}) if technical_data else {}
    support_levels = technical_data_dict.get('support_levels', [])
    resistance_levels = technical_data_dict.get('resistance_levels', [])
    
    strategy = {
        'recommendation': recommendation,
        'confidence': confidence,
        'rationale': rationale,
        'entry_strategy': '',
        'exit_strategy': '',
        'risk_management': ''
    }
    
    # Get actual support levels below current price
    actual_supports = [s for s in support_levels if s < current_price] if support_levels else []
    nearest_support = actual_supports[0] if actual_supports else current_price * 0.95
    
    # Get actual resistance levels above current price
    actual_resistances = [r for r in resistance_levels if r > current_price] if resistance_levels else []
    nearest_resistance = actual_resistances[0] if actual_resistances else current_price * 1.05
    
    # Calculate overall strength score for entry strategy alignment
    overall_strength = (fundamental_score + technical_score) / 2.0
    sentiment_bullish = sentiment_score > 0.1
    
    # Entry strategy based on recommendation with actual technical levels
    if recommendation == 'Buy' or recommendation == 'Strong Buy':
        if current_price:
            # For strong stocks (high fundamentals + technicals + bullish sentiment), use tighter entry ranges
            if overall_strength >= 7.5 and sentiment_bullish:
                # Very strong stock: current levels or small pullback acceptable
                if actual_supports and len(actual_supports) > 0:
                    # Use realistic support levels (within 10% of current)
                    reasonable_supports = [s for s in actual_supports if s >= current_price * 0.90]
                    if reasonable_supports:
                        conservative_entry = reasonable_supports[0]
                    else:
                        conservative_entry = current_price * 0.95  # 5% below
                else:
                    conservative_entry = current_price * 0.95  # 5% below
                
                strategy['entry_strategy'] = f"""**Entry Strategy:**
- **Conservative:** Current levels acceptable, or small pullback to ${conservative_entry:.2f} ({((conservative_entry/current_price - 1)*100):.1f}% below) for better entry
- **Moderate:** Current levels acceptable with stop-loss at ${conservative_entry * 0.98:.2f} (below key support)
- **Aggressive:** Break above resistance at ${nearest_resistance:.2f} with volume confirmation for momentum entry"""
            else:
                # Moderate strength: use standard entry strategy
                entry_parts = ["**Entry Strategy:**"]
                
                if actual_supports:
                    # Use realistic support levels (within 15% of current)
                    reasonable_supports = [s for s in actual_supports if s >= current_price * 0.85]
                    if reasonable_supports:
                        conservative_entry = reasonable_supports[0]
                    else:
                        conservative_entry = current_price * 0.93  # 7% below
                    entry_parts.append(f"- **Conservative:** Wait for pullback to key support at ${conservative_entry:.2f} ({((conservative_entry/current_price - 1)*100):.1f}% below) for better risk/reward")
                else:
                    entry_parts.append(f"- **Conservative:** Wait for pullback to 5-7% below current price (${current_price * 0.93:.2f} - ${current_price * 0.95:.2f}) for better risk/reward")
                
                if actual_supports:
                    reasonable_supports = [s for s in actual_supports if s >= current_price * 0.85]
                    if reasonable_supports:
                        stop_loss = reasonable_supports[0] * 0.98  # Just below nearest support
                        entry_parts.append(f"- **Moderate:** Current levels acceptable with stop-loss at ${stop_loss:.2f} (below key support at ${reasonable_supports[0]:.2f})")
                    else:
                        entry_parts.append(f"- **Moderate:** Current levels acceptable with tight stop-loss at ${current_price * 0.93:.2f}")
                else:
                    entry_parts.append(f"- **Moderate:** Current levels acceptable with tight stop-loss at ${current_price * 0.93:.2f}")
                
                if actual_resistances:
                    entry_parts.append(f"- **Aggressive:** Break above resistance at ${nearest_resistance:.2f} with volume confirmation for momentum entry")
                else:
                    entry_parts.append(f"- **Aggressive:** Break above recent high with volume confirmation for momentum entry")
                
                strategy['entry_strategy'] = "\n".join(entry_parts)
    elif recommendation == 'Hold':
        fundamental_score = combined_data.get('fundamental_score', 5.0)
        technical_score = combined_data.get('technical_score', 5.0)
        sentiment_score = combined_data.get('sentiment_score', 0.0)
        
        entry_parts = ["**Entry Strategy:**"]
        entry_parts.append("")
        
        # For long-term investors
        if fundamental_score >= 7.0:
            entry_parts.append("**For Long-Term Investors:**")
            entry_parts.append(f"- Current price (${current_price:.2f}) acceptable given strong fundamentals ({fundamental_score:.1f}/10)")
            if sentiment_score > 0.3:
                entry_parts.append(f"- Bullish sentiment ({sentiment_score:.3f}) supports long-term thesis")
            entry_parts.append("- Consider dollar-cost averaging if entering now")
            if actual_supports:
                entry_range_low = actual_supports[0]
                entry_range_high = current_price * 1.02
                entry_parts.append(f"- Entry range: ${entry_range_low:.2f}-${entry_range_high:.2f} ({((entry_range_low/current_price - 1)*100):.1f}% to {((entry_range_high/current_price - 1)*100):.1f}% from current)")
            entry_parts.append("")
        
        # For tactical traders
        entry_parts.append("**For Tactical Traders:**")
        if actual_supports:
            entry_parts.append(f"- Wait for pullback to ${actual_supports[0]:.2f}-${actual_supports[0]*1.02:.2f} support zone ({((actual_supports[0]/current_price - 1)*100):.1f}% discount)")
        else:
            entry_parts.append(f"- Wait for pullback to ${current_price * 0.97:.2f}-${current_price * 0.95:.2f} support zone (3-5% discount)")
        if actual_resistances:
            entry_parts.append(f"- OR wait for breakout above ${nearest_resistance:.2f} with volume confirmation")
        else:
            entry_parts.append(f"- OR wait for breakout above ${current_price * 1.03:.2f} with volume confirmation")
        entry_parts.append("- Avoid entering at current levels without technical confirmation")
        
        strategy['entry_strategy'] = "\n".join(entry_parts)
    else:
        strategy['entry_strategy'] = """
**Entry Strategy:**
- Avoid new positions
- Consider reducing exposure
- Wait for improved fundamentals or technical setup
"""
    
    # Generate price targets using actual technical levels
    fundamental_data = combined_data.get('fundamental_data', {})
    growth = fundamental_data.get('growth', []) if isinstance(fundamental_data, dict) else []
    fundamental_score = combined_data.get('fundamental_score', 5.0)
    valuation_risk = combined_data.get('valuation_risk', 1.0)
    
    forward_data = combined_data.get('forward_data', {})  # Get forward-looking data if available
    price_targets = generate_price_targets(technical_data, quote, fundamental_score, valuation_risk, growth, forward_data)
    
    # Exit strategy with actual targets
    if current_price and price_targets:
        exit_parts = ["**Exit Strategy:**"]
        
        if 'target1' in price_targets:
            t1 = price_targets['target1']
            exit_parts.append(f"- **Target 1:** ${t1['price']:.2f} ({t1['upside']:.1f}% upside) - {t1['description']} ({t1['basis']})")
        
        if 'target2' in price_targets:
            t2 = price_targets['target2']
            exit_parts.append(f"- **Target 2:** ${t2['price']:.2f} ({t2['upside']:.1f}% upside) - {t2['description']} ({t2['basis']})")
        
        if 'target3' in price_targets:
            t3 = price_targets['target3']
            exit_parts.append(f"- **Target 3:** ${t3['price']:.2f} ({t3['upside']:.1f}% upside) - {t3['description']} ({t3['basis']})")
        
        # Stop loss based on actual support
        if 'support_levels' in price_targets and price_targets['support_levels']:
            stop_loss = price_targets['support_levels'][0] * 0.98
            exit_parts.append(f"- **Stop Loss:** ${stop_loss:.2f} (below key support at ${price_targets['support_levels'][0]:.2f}) - Risk management")
        else:
            stop_loss = current_price * 0.95
            exit_parts.append(f"- **Stop Loss:** ${stop_loss:.2f} (5% downside) - Risk management")
        
        exit_parts.append("- **Trailing Stop:** If position moves favorably, trail stop below key support levels")
        
        strategy['exit_strategy'] = "\n".join(exit_parts)
    elif current_price:
        # Fallback to percentage-based
        target1 = current_price * 1.05
        target2 = current_price * 1.10
        stop_loss = current_price * 0.95
        
        strategy['exit_strategy'] = f"""
**Exit Strategy:**
- **Target 1:** ${target1:.2f} (5% upside) - Take partial profits
- **Target 2:** ${target2:.2f} (10% upside) - Full profit target
- **Stop Loss:** ${stop_loss:.2f} (5% downside) - Risk management
- **Trailing Stop:** If position moves favorably, trail stop below key support
"""
    
    # Risk management
    overall_risk = combined_data.get('overall_risk', 'Medium')
    strategy['risk_management'] = f"""
**Risk Management:**
- **Risk Level:** {overall_risk}
- **Position Size:** {'Moderate to Large' if recommendation in ['Buy', 'Strong Buy'] and confidence in ['High', 'Very High'] else 'Moderate'}
- **Stop Loss:** Essential - protects against unexpected downside
- **Monitoring:** Watch for fundamental deterioration or technical breakdown signals
"""
    
    return strategy

