# Agent AI Extraction Guide - SEC Guidance
**Date:** 2025-12-30  
**Purpose:** Guide for agent to generate SEC guidance extraction

---

## 🎯 **HOW IT WORKS**

### **When Agent Orchestrates Workflow:**

1. **Workflow calls:** `sec_extractor.extract_guidance(symbol)`
2. **SEC extractor:** Fetches filings and extracts text
3. **Calls:** `extract_guidance_ai(text, symbol)`
4. **Agent intercepts:** Agent generates extraction directly
5. **Agent populates:** Returns structured guidance dict
6. **Report displays:** AI-extracted guidance

---

## 📝 **AGENT EXTRACTION PROCESS**

### **Step 1: Agent Receives SEC Text**

When `extract_guidance_ai(text, symbol)` is called:
- Agent receives full SEC filing text
- Agent has context about the company (symbol)
- Agent can see the full workflow context

### **Step 2: Agent Analyzes Text**

Agent reads the SEC filing text and identifies:
- **Guidance vs Historical:** Distinguishes forward-looking statements from historical data
- **Targets:** GMV, revenue, EBITDA margin targets
- **Timelines:** Profitability timelines
- **Operational Metrics:** Payroll, pickup stations, fulfillment costs, NPS, repurchase rate
- **Commitments:** Self-funded growth, no capital raises
- **Forward Statements:** Key forward-looking statements

### **Step 3: Agent Generates Structured Extraction**

Agent creates structured dict:

```python
{
    'revenue_targets': [
        {'amount': '$2.5-$3B', 'year': '2030', 'context': 'expect to reach'}
    ],
    'gmv_targets': [
        {'amount': '$2.5-$3 billion', 'year': '2030', 'context': 'target'}
    ],
    'profitability_timeline': '2027',
    'ebitda_targets': [
        {'margin': '20', 'year': '2030', 'context': 'target'}
    ],
    'operational_metrics': {
        'payroll_reduction': {
            'from': 4500,
            'to': 2000,
            'reduction_pct': 55.6
        },
        'pickup_station_percentage': 72,
        'fulfillment_cost_reduction': {
            'from': 9.2,
            'to': 5.3,
            'reduction_pct': 42.4
        },
        'nps_improvement': {
            'from': 46,
            'to': 64,
            'improvement': 18
        },
        'repurchase_rate': {
            'from': 39,
            'to': 43,
            'improvement': 4
        },
        'geographic_expansion': 60
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

### **Step 4: Agent Returns Extraction**

Agent populates the dict and returns it. The function `extract_guidance_ai()` currently returns an empty structure - **the agent fills it during workflow execution**.

---

## 🔍 **EXTRACTION GUIDELINES**

### **Distinguish Guidance from Historical:**

**Guidance (Extract):**
- "We expect to reach $2.5-$3B GMV by 2030"
- "Our target is 20% EBITDA margin by 2030"
- "We plan to achieve profitability by 2027"

**Historical (Ignore):**
- "2024 GMV was $1.2B"
- "We achieved 15% EBITDA margin in 2024"
- "We were profitable in 2023"

### **Extract Nuanced Language:**

**Self-Funded Growth:**
- "self-funded growth"
- "no further capital raises"
- "growth without capital raise"
- "not expect to raise capital"

**Operational Improvements:**
- Payroll: "reduced from 4,500 to 2,000 employees"
- Pickup stations: "72% of deliveries at pickup stations"
- Fulfillment: "fulfillment costs reduced from 9.2% to 5.3% of GMV"
- NPS: "NPS increased from 46 to 64"
- Repurchase: "repurchase rate improved from 39% to 43%"
- Geographic: "60% of orders outside capital cities"

---

## ✅ **BENEFITS OF AI EXTRACTION**

### **Accuracy:**
- ✅ Understands context (guidance vs historical)
- ✅ Handles format variations
- ✅ Extracts nuanced language
- ✅ Validates extraction

### **No API Costs:**
- ✅ Agent generates directly
- ✅ No external API calls
- ✅ Full context available

### **Better Results:**
- ✅ More accurate than pattern matching
- ✅ Handles edge cases
- ✅ Company-specific language

---

## 🚀 **IMPLEMENTATION STATUS**

✅ **Infrastructure Created:**
- `extract_guidance_ai()` function added
- `extract_guidance()` updated to use AI first
- Pattern matching kept as fallback

🔄 **Agent Generation:**
- Agent generates extraction during workflow
- Agent populates guidance dict
- Report displays AI-extracted guidance

---

## 📋 **EXAMPLE: JMIA SEC Filing**

### **Input Text:**
```
"We expect to reach $2.5-$3 billion in GMV by 2030. Our target is achieving 
20% EBITDA margin by 2030. We plan to reach profitability by 2027. 
We have reduced payroll from 4,500 to 2,000 employees, representing a 
55.6% reduction. We expect growth to be self-funded and do not anticipate 
needing additional capital raises. 72% of our deliveries are now at pickup 
stations. Fulfillment costs have decreased from 9.2% to 5.3% of GMV."
```

### **Agent Extraction:**
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
        'payroll_reduction': {'from': 4500, 'to': 2000, 'reduction_pct': 55.6},
        'pickup_station_percentage': 72,
        'fulfillment_cost_reduction': {'from': 9.2, 'to': 5.3, 'reduction_pct': 42.4}
    },
    'self_funded_growth': True,
    'no_capital_raises': True
}
```

---

## ✅ **READY FOR AGENT GENERATION**

The infrastructure is ready. When the agent orchestrates the workflow:
1. Agent receives SEC filing text
2. Agent analyzes with full context
3. Agent generates structured extraction
4. Agent populates guidance dict
5. Report displays AI-extracted guidance

**Pattern matching remains as fallback for standalone scripts.**

