# Refactoring Plan: stock_analysis_combiner.py

## Current State
- **File:** `stock_analysis_combiner.py`
- **Lines:** 2,222
- **Issues:** 
  - Recurring indentation errors
  - Hard to debug
  - Difficult to maintain
  - Functions are tightly coupled

## Proposed Structure

### 1. `ai_interpreters.py` (~500 lines)
**Purpose:** All AI interpretation functions
**Functions:**
- `call_ai_for_interpretation()`
- `interpret_fundamental_metrics()`
- `interpret_technical_indicators()`
- `interpret_valuation()`
- `interpret_technical_analysis()`
- `synthesize_investment_thesis()`

### 2. `report_helpers.py` (~200 lines)
**Purpose:** Helper functions for report generation
**Functions:**
- `generate_price_targets()`
- `generate_actionable_recommendation()`
- `format_market_cap()`
- `format_currency()`

### 3. `workflow_steps.py` (~400 lines)
**Purpose:** Step-by-step analysis functions
**Functions:**
- `step2_fundamental_analysis()`
- `step3_technical_analysis()`
- `step35_sentiment_analysis()`
- `step4_combined_analysis()`

### 4. `report_generator.py` (~800 lines)
**Purpose:** Report generation logic
**Functions:**
- `step5_report_generation()` - Main report generator
- `_generate_executive_summary()`
- `_generate_fundamental_section()`
- `_generate_technical_section()`
- `_generate_sentiment_section()`
- `_generate_recommendation_section()`
- `_generate_forward_looking_section()`
- `_generate_risk_section()`
- `_generate_price_targets_section()`

### 5. `stock_analysis_combiner.py` (~200 lines)
**Purpose:** Main orchestrator - imports and coordinates everything
**Functions:**
- `main()` - Entry point
- Setup and initialization
- Orchestrates the workflow

## Benefits

1. **Easier Debugging:** Each module has a clear purpose
2. **Better Maintainability:** Changes isolated to specific modules
3. **Reduced Errors:** Smaller files = fewer indentation issues
4. **Testability:** Each module can be tested independently
5. **Reusability:** Functions can be imported separately if needed

## Migration Strategy

1. Create new modular files
2. Move functions to appropriate modules
3. Update imports in main file
4. Test with existing stocks
5. Verify all functionality works
6. Remove old monolithic file (after verification)

## File Structure

```
~/.claude/skills/stock-analyst/scripts/
├── stock_analysis_combiner.py      # Main orchestrator (~200 lines)
├── ai_interpreters.py              # AI interpretation functions (~500 lines)
├── report_helpers.py                # Helper functions (~200 lines)
├── workflow_steps.py                # Step functions (~400 lines)
├── report_generator.py              # Report generation (~800 lines)
└── [existing files...]
```

## Implementation Order

1. Create `ai_interpreters.py` - Move all interpretation functions
2. Create `report_helpers.py` - Move helper functions
3. Create `workflow_steps.py` - Move step functions
4. Create `report_generator.py` - Move report generation
5. Refactor `stock_analysis_combiner.py` - Keep only orchestration
6. Test thoroughly
7. Update skill documentation if needed



