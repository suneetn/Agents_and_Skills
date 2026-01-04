#!/usr/bin/env python3
"""
Stock Analyst Skill - Enhanced Workflow with AI Interpretation (REFACTORED)
Main orchestrator that coordinates all analysis modules
"""

import os
import sys
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()  # Load .env file if it exists
except ImportError:
    pass  # python-dotenv not installed, fall back to environment variables

# ============================================================================
# STEP 1: Initialize and Setup
# ============================================================================
print("="*80)
print("STOCK ANALYST SKILL - ENHANCED WORKFLOW WITH AI INTERPRETATION")
print("="*80)
print("\n" + "="*80)
print("STEP 1: Initialize and Setup")
print("="*80)

# Task 1: Verify FMP API key is set
api_key = os.getenv('FMP_API_KEY')
if not api_key:
    print("❌ Error: FMP_API_KEY not found in .env file or environment variable")
    print("Create a .env file with: FMP_API_KEY=your_key")
    print("Or set it with: export FMP_API_KEY=your_key")
    sys.exit(1)
print("✅ Task 1: FMP API key verified")

# Task 2: Import required modules
skill_script_dir = os.path.expanduser('~/.claude/skills/stock-analyst/scripts')
if not os.path.exists(skill_script_dir):
    skill_script_dir = os.path.expanduser('~/personal')

sys.path.insert(0, skill_script_dir)

try:
    from stock_analysis_fmp import FMPStockAnalyzer
    from stock_technical_analysis import FMPTechnicalAnalyzer
    from stock_sentiment_analysis import FMPSentimentAnalyzer
    from stock_recommendation_engine import StockRecommendationEngine, RiskLevel
    from stock_valuation_analyzer import ValuationAnalyzer
    from stock_fundamental_scorer import FundamentalScorer
    import pandas as pd
    import numpy as np
    
    # Import refactored modules
    from workflow_steps import (
        step2_fundamental_analysis,
        step3_technical_analysis,
        step35_sentiment_analysis,
        step4_combined_analysis
    )
    from report_generator import step5_report_generation
    
    print(f"✅ Task 2: Required modules imported from {skill_script_dir}")
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Task 3: Initialize analyzers
try:
    fundamental_analyzer = FMPStockAnalyzer()
    technical_analyzer = FMPTechnicalAnalyzer()
    sentiment_analyzer = FMPSentimentAnalyzer()
    recommendation_engine = StockRecommendationEngine()
    valuation_analyzer = ValuationAnalyzer()
    fundamental_scorer = FundamentalScorer()
    print("✅ Task 3: Analyzers initialized")
except Exception as e:
    print(f"❌ Error initializing analyzers: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================================
# MAIN EXECUTION
# ============================================================================
if __name__ == "__main__":
    symbol = sys.argv[1].upper() if len(sys.argv) > 1 else "AAPL"
    
    print(f"\n{'='*80}")
    print(f"ANALYZING: {symbol}")
    print(f"{'='*80}\n")
    
    try:
        # Execute workflow with AI interpretation (following Stock Analyst Skill)
        fundamental_data = step2_fundamental_analysis(symbol, fundamental_analyzer, valuation_analyzer)
        technical_data = step3_technical_analysis(symbol, technical_analyzer)
        sentiment_data = step35_sentiment_analysis(symbol, sentiment_analyzer)  # Step 3.5 per skill documentation
        combined_data = step4_combined_analysis(
            symbol, 
            fundamental_data, 
            technical_data, 
            sentiment_data,
            recommendation_engine,
            fundamental_scorer
        )
        report_path = step5_report_generation(
            symbol, 
            fundamental_data, 
            technical_data, 
            sentiment_data, 
            combined_data,
            fundamental_scorer
        )
        
        print("\n" + "="*80)
        print("✅ ANALYSIS COMPLETE - WITH AI INTERPRETATION")
        print("="*80)
        print("\nWorkflow Steps Completed (following Stock Analyst Skill):")
        print("1. ✅ Initialize and Setup")
        print("2. ✅ Fundamental Analysis (with AI interpretation)")
        print("3. ✅ Technical Analysis (with AI interpretation)")
        print("3.5. ✅ Sentiment Analysis (analyst recommendations & news)")
        print("4. ✅ Combined Analysis (with AI synthesis including sentiment)")
        print("5. ✅ Report Generation (with comprehensive AI interpretation)")
        print(f"\n📄 Comprehensive report saved to: {report_path}")
        print("\n✨ This report includes:")
        print("   - Contextual interpretation of all metrics")
        print("   - Investment thesis synthesis")
        print("   - Actionable recommendations")
        print("   - Risk assessment with context")
        print("   - Entry/exit strategies")
        
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)



