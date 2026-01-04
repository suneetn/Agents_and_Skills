# AI-Driven SEC Guidance Extraction - Implementation
**Date:** 2025-12-30  
**Status:** ✅ **IMPLEMENTING**

---

## 🎯 **APPROACH: FULLY AI-DRIVEN**

### **Why AI-Driven:**
- ✅ SEC filings are unstructured text
- ✅ Highly variable formats
- ✅ Context matters (guidance vs historical)
- ✅ Nuanced language extraction
- ✅ Agent-based generation (no API costs)

---

## 🏗️ **IMPLEMENTATION**

### **New Function: `extract_guidance_ai()`**

**Location:** `sec_guidance_extractor.py`

**Purpose:**
- Agent generates structured extraction from SEC filing text
- Understands context (guidance vs historical data)
- Extracts nuanced information (self-funded growth, etc.)
- Returns structured dict format

**How It Works:**
1. Agent receives SEC filing text
2. Agent analyzes text with full context
3. Agent extracts guidance directly:
   - GMV/revenue targets
   - EBITDA margin targets
   - Profitability timelines
   - Operational metrics
   - Self-funded growth commitments
   - Forward-looking statements
4. Agent returns structured dict

**Fallback:**
- If agent not available → pattern matching
- Pattern matching still works for standalone scripts

---

## 📝 **AGENT EXTRACTION PROMPT**

When agent calls `extract_guidance_ai()`, agent generates extraction based on:

```
Extract management guidance from this SEC filing text for {symbol}:

{text}

Extract the following guidance (distinguish from historical data):

1. **GMV/Revenue Targets:**
   - Amount (e.g., "$2.5-$3B")
   - Year (e.g., "2030")
   - Context (e.g., "target", "expect", "plan")

2. **EBITDA Margin Targets:**
   - Percentage (e.g., "20%")
   - Year (e.g., "2030")
   - Context

3. **Profitability Timeline:**
   - Year when profitability expected
   - Conditions (if any)

4. **Operational Metrics:**
   - Payroll reduction (from/to, percentage)
   - Pickup station percentage
   - Fulfillment cost reduction (from/to, percentage)
   - NPS improvement (from/to, points)
   - Repurchase rate (from/to, percentage)
   - Geographic expansion (percentage)

5. **Self-Funded Growth:**
   - Commitment to self-funded growth
   - No capital raises expected

6. **Forward-Looking Statements:**
   - Key forward-looking statements (max 5)

Return structured dict:
{
    'revenue_targets': [],
    'gmv_targets': [],
    'profitability_timeline': None,
    'ebitda_targets': [],
    'operational_metrics': {},
    'self_funded_growth': False,
    'no_capital_raises': False,
    'forward_statements': []
}
```

---

## 🔄 **WORKFLOW INTEGRATION**

### **Current Flow:**
```
workflow_steps.py → sec_extractor.extract_guidance(symbol)
  → Fetches SEC filings
  → Extracts text
  → extract_guidance_from_text() (pattern matching)
  → Returns guidance
```

### **New Flow:**
```
workflow_steps.py → sec_extractor.extract_guidance(symbol)
  → Fetches SEC filings
  → Extracts text
  → extract_guidance_ai(text, symbol) (AI extraction)
    → Agent generates extraction directly
    → Returns structured guidance
  → Fallback to pattern matching if needed
```

---

## ✅ **BENEFITS**

### **Accuracy:**
- ✅ Understands context (guidance vs historical)
- ✅ Handles format variations
- ✅ Extracts nuanced language
- ✅ Validates extraction

### **Maintenance:**
- ✅ No pattern updates needed
- ✅ Handles new formats automatically
- ✅ Adapts to company-specific language

### **Cost:**
- ✅ No API costs (agent generates)
- ✅ No latency (instant)
- ✅ Full context available

---

## 📊 **EXAMPLE EXTRACTION**

### **Input Text (SEC Filing):**
```
"We expect to reach $2.5-$3 billion in GMV by 2030. Our target is achieving 
20% EBITDA margin by 2030. We plan to reach profitability by 2027. 
We have reduced payroll from 4,500 to 2,000 employees, representing a 
55.6% reduction. We expect growth to be self-funded and do not anticipate 
needing additional capital raises."
```

### **AI Extraction Output:**
```python
{
    'gmv_targets': [
        {'amount': '$2.5-$3 billion', 'year': '2030', 'context': 'expect to reach'}
    ],
    'ebitda_targets': [
        {'margin': '20', 'year': '2030', 'context': 'target'}
    ],
    'profitability_timeline': '2027',
    'operational_metrics': {
        'payroll_reduction': {
            'from': 4500,
            'to': 2000,
            'reduction_pct': 55.6
        }
    },
    'self_funded_growth': True,
    'no_capital_raises': True,
    'forward_statements': [
        "We expect to reach $2.5-$3 billion in GMV by 2030",
        "Our target is achieving 20% EBITDA margin by 2030",
        "We plan to reach profitability by 2027"
    ]
}
```

---

## 🚀 **NEXT STEPS**

1. ✅ **Created `extract_guidance_ai()` function**
2. ✅ **Updated `extract_guidance()` to use AI first**
3. ✅ **Kept pattern matching as fallback**
4. 🔄 **Agent generates extraction during workflow**
5. 📋 **Test with JMIA SEC filings**

---

## ✅ **STATUS: READY FOR AGENT GENERATION**

The infrastructure is in place. When the agent orchestrates the workflow:
1. Agent receives SEC filing text
2. Agent generates structured extraction
3. Agent populates guidance dict
4. Report displays AI-extracted guidance

**Pattern matching remains as fallback for standalone scripts.**


