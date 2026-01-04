# SEC Guidance Extraction: AI-Driven Approach
**Date:** 2025-12-30  
**Decision:** ✅ **SWITCH TO FULLY AI-DRIVEN EXTRACTION**

---

## 🎯 **WHY AI-DRIVEN IS CORRECT**

### **SEC Filings Are Unstructured Text**

**Reality:**
- SEC filings are natural language documents
- Highly variable formats across companies
- Management guidance expressed in many ways
- Context matters (e.g., "expect" vs "plan" vs "target")
- Nuanced language (e.g., "self-funded growth", "no capital raises")

**Pattern Matching Limitations:**
- ❌ Brittle - breaks with format variations
- ❌ Misses edge cases - can't handle all variations
- ❌ No context understanding - doesn't understand meaning
- ❌ Constant maintenance - patterns must be updated
- ❌ False positives - matches historical data as guidance

**AI Advantages:**
- ✅ Understands context - knows what's guidance vs historical
- ✅ Handles variations - natural language understanding
- ✅ Extracts nuance - "self-funded growth", "no capital raises"
- ✅ Validates extraction - can verify targets make sense
- ✅ Better accuracy - understands meaning, not just patterns

---

## 🔄 **ALIGNMENT WITH "JUDICIOUS MIX"**

### **Correct Application:**

**Algorithms for Structured Data:**
- ✅ API responses (FMP, SEC metadata)
- ✅ Calculated metrics (P/E, PEG, RSI)
- ✅ Score calculations (fundamental, technical scores)
- ✅ Data transformations (ratios, growth rates)

**AI for Unstructured Text:**
- ✅ SEC filing text extraction
- ✅ Management guidance interpretation
- ✅ Context understanding
- ✅ Nuanced language extraction

**This is the RIGHT mix!**

---

## 🏗️ **IMPLEMENTATION APPROACH**

### **Agent-Based AI Generation (No API Costs)**

The system already has agent-based AI generation:
- `agent_ai_generator_live.py` - Agent generates interpretations directly
- No API calls needed - agent IS the LLM
- Full context available during workflow execution

### **New Function: `extract_guidance_ai()`**

```python
def extract_guidance_ai(text: str, symbol: str) -> Dict:
    """
    Extract management guidance from SEC filing text using AI
    
    Agent (Claude) generates structured extraction directly:
    - GMV targets
    - EBITDA margin targets
    - Profitability timelines
    - Operational metrics
    - Self-funded growth commitments
    - Forward-looking statements
    """
    # Agent generates extraction based on full text context
    # Returns structured dict with all guidance types
```

### **Fallback Strategy:**

1. **Agent-Generated (Primary)** ✅
   - Agent extracts guidance directly from text
   - Full context, no API costs
   - Best accuracy

2. **Pattern Matching (Fallback)** ✅
   - If agent not available
   - Basic extraction for standalone scripts
   - Always works

---

## 📊 **BEFORE vs AFTER**

### **Before (Pattern Matching):**
```python
# Brittle regex patterns
pattern = r'\$[\d.]+[BMK]?\s*(?:to|-)?\s*\$?[\d.]+[BMK]?\s*GMV.*?(?:by|in).*?(20[2-3][6-9]|203[0-5])'
match = re.search(pattern, text)
# Misses: "We expect GMV to reach $2.5-$3 billion by 2030"
# Misses: "Our target is achieving $2.5B-$3B in GMV by the end of 2030"
# False positive: "2025 GMV was $2.5B" (historical, not guidance)
```

### **After (AI-Driven):**
```python
# Agent understands context and extracts guidance
prompt = f"""
Extract management guidance from this SEC filing text for {symbol}:

{text}

Extract:
1. GMV/revenue targets (amount, year, context)
2. EBITDA margin targets (percentage, year)
3. Profitability timelines (year, conditions)
4. Operational metrics (payroll, pickup stations, fulfillment costs, NPS, repurchase rate)
5. Self-funded growth commitments
6. Forward-looking statements

Return structured JSON with all extracted guidance.
Distinguish guidance from historical data.
"""
# Agent generates extraction with full context understanding
```

---

## ✅ **BENEFITS**

### **Accuracy:**
- ✅ Understands context (guidance vs historical)
- ✅ Handles variations naturally
- ✅ Extracts nuanced language
- ✅ Validates extraction

### **Maintenance:**
- ✅ No pattern updates needed
- ✅ Handles new formats automatically
- ✅ Adapts to company-specific language

### **Cost:**
- ✅ No API costs (agent generates directly)
- ✅ No latency (instant generation)
- ✅ Full context available

---

## 🚀 **IMPLEMENTATION PLAN**

### **Phase 1: Create AI Extraction Function** ✅
- Add `extract_guidance_ai()` to `sec_guidance_extractor.py`
- Agent generates structured extraction from text
- Returns same dict format as pattern matching

### **Phase 2: Update Workflow** ✅
- Call `extract_guidance_ai()` instead of pattern matching
- Keep pattern matching as fallback
- Agent generates extraction during workflow

### **Phase 3: Test & Refine** ✅
- Test with JMIA SEC filings
- Compare with Seeking Alpha PDF
- Refine extraction prompts

---

## 📝 **CONCLUSION**

**User is 100% correct:**
- SEC filings are unstructured text → AI is the right tool
- Pattern matching is brittle → AI handles variations
- Context matters → AI understands meaning
- Agent-based generation exists → No API costs

**Switch to fully AI-driven extraction for SEC guidance!** ✅

