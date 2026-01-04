# FMP API: Earnings Transcript Endpoints (Premium Feature)
**Date:** 2025-12-30  
**Source:** [FMP API Documentation](https://site.financialmodelingprep.com/developer/docs#latest-transcripts)

---

## ✅ **Earnings Transcript Endpoints Available**

According to FMP documentation, the following endpoints are available for earnings call transcripts:

### 1. Latest Earnings Transcripts
**Endpoint:** `/latest-transcripts`  
**Description:** List of companies with available earnings transcripts  
**URL:** `https://financialmodelingprep.com/api/v3/latest-transcripts`  
**Parameters:** `apikey` (required)

### 2. Earnings Transcript by Symbol
**Endpoint:** `/earnings-transcript/{symbol}`  
**Description:** Full transcript text for specific earnings calls  
**URL:** `https://financialmodelingprep.com/api/v3/earnings-transcript/{symbol}`  
**Parameters:** 
- `apikey` (required)
- `date` (optional) - Specific earnings call date

### 3. Search Transcripts
**Endpoint:** `/search-transcripts`  
**Description:** Search transcripts by company name or symbol  
**URL:** `https://financialmodelingprep.com/api/v3/search-transcripts`  
**Parameters:** 
- `apikey` (required)
- `query` (required) - Company name or symbol

### 4. Transcript Dates by Symbol
**Endpoint:** `/transcripts-dates-by-symbol/{symbol}`  
**Description:** Available transcript dates organized by fiscal year and quarter  
**URL:** `https://financialmodelingprep.com/api/v3/transcripts-dates-by-symbol/{symbol}`  
**Parameters:** `apikey` (required)

### 5. Earnings Transcript List
**Endpoint:** `/earnings-transcript-list`  
**Description:** List of companies with available transcripts and total count  
**URL:** `https://financialmodelingprep.com/api/v3/earnings-transcript-list`  
**Parameters:** `apikey` (required)

---

## ⚠️ **Subscription Tier Requirement**

**Test Results:**
- ✅ Endpoints exist and respond (HTTP 200)
- ❌ Return empty results with free tier API key
- ✅ Premium subscription required for transcript access

**Conclusion:** Earnings transcripts are a **premium feature** and require a paid subscription tier.

---

## 💡 **Implementation Example (If Premium Tier Available)**

```python
def get_earnings_transcript(symbol: str, date: str = None) -> Dict:
    """Get earnings call transcript (requires premium subscription)"""
    url = f"https://financialmodelingprep.com/api/v3/earnings-transcript/{symbol}"
    params = {'apikey': api_key}
    if date:
        params['date'] = date
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if data and isinstance(data, dict) and data.get('content'):
        return {
            'available': True,
            'date': data.get('date'),
            'quarter': data.get('quarter'),
            'year': data.get('year'),
            'content': data.get('content'),
            'transcript': data.get('content')  # Full transcript text
        }
    return {'available': False, 'reason': 'No transcript found or premium tier required'}


def extract_management_guidance(transcript_content: str) -> Dict:
    """Extract management guidance from transcript text"""
    guidance = {
        'revenue_targets': [],
        'profitability_timeline': None,
        'ebitda_targets': [],
        'operational_milestones': []
    }
    
    # Use NLP/text processing to extract:
    # - Revenue targets (e.g., "$2.5-$3B GMV by 2030")
    # - Profitability timeline (e.g., "profitability by 2027")
    # - EBITDA targets (e.g., "20% EBITDA margin")
    # - Operational milestones
    
    # Example regex patterns:
    import re
    
    # Revenue targets
    revenue_pattern = r'\$[\d.]+[BMK]?\s*(?:GMV|revenue|sales).*?(?:by|in)\s*(\d{4})'
    guidance['revenue_targets'] = re.findall(revenue_pattern, transcript_content, re.IGNORECASE)
    
    # Profitability timeline
    profitability_pattern = r'profitability.*?(?:by|in)\s*(\d{4})'
    match = re.search(profitability_pattern, transcript_content, re.IGNORECASE)
    if match:
        guidance['profitability_timeline'] = match.group(1)
    
    return guidance
```

---

## 📊 **What Can Be Extracted from Transcripts**

1. **Management Guidance:**
   - Revenue targets and growth expectations
   - Earnings guidance
   - Profitability timelines

2. **Strategic Commentary:**
   - Business model changes
   - Operational improvements
   - Market expansion plans

3. **Long-Term Targets:**
   - GMV targets (e.g., "$2.5-$3B GMV by 2030")
   - EBITDA margin targets (e.g., "20% EBITDA margin")
   - Profitability timelines (e.g., "profitability by 2027")

4. **Operational Metrics:**
   - Cost reduction initiatives
   - Geographic expansion
   - Customer satisfaction improvements

---

## 🎯 **Recommendation**

### Current (Free Tier):
- ✅ Keep placeholder approach
- ✅ Manual review instructions
- ✅ Reference external sources (Seeking Alpha)

### If Premium Tier Available:
- ✅ Implement transcript extraction
- ✅ Add NLP parsing for guidance extraction
- ✅ Automatically include in analysis reports
- ✅ Update "Path to Profitability" section with actual guidance

---

## 📚 **References**

- [FMP API Documentation - Latest Transcripts](https://site.financialmodelingprep.com/developer/docs#latest-transcripts)
- [FMP Pricing](https://site.financialmodelingprep.com/pricing) - Check premium tier features


