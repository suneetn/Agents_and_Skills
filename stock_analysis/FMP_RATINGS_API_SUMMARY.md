# FMP Stock Ratings API Summary

**Date:** December 29, 2025  
**Tested Symbol:** MSFT

---

## Available FMP Stock Ratings APIs

### ✅ 1. Stock Rating API (`/rating/{symbol}`)

**Endpoint:** `https://financialmodelingprep.com/api/v3/rating/MSFT`

**Returns:** Overall stock rating with detailed component scores

**Sample Data (MSFT):**
```json
{
  "symbol": "MSFT",
  "date": "2025-12-26",
  "rating": "A-",
  "ratingScore": 4,
  "ratingRecommendation": "Buy",
  "ratingDetailsDCFScore": 4,
  "ratingDetailsDCFRecommendation": "Buy",
  "ratingDetailsROEScore": 5,
  "ratingDetailsROERecommendation": "Strong Buy",
  "ratingDetailsROAScore": 5,
  "ratingDetailsROARecommendation": "Strong Buy",
  "ratingDetailsDEScore": 3,
  "ratingDetailsDERecommendation": "Neutral",
  "ratingDetailsPEScore": 2,
  "ratingDetailsPERecommendation": "Sell",
  "ratingDetailsPBScore": 1,
  "ratingDetailsPBRecommendation": "Strong Sell"
}
```

**Use Cases:**
- Overall stock rating (A-F scale)
- Component-level ratings (DCF, ROE, ROA, DE, PE, PB)
- Quick rating recommendation (Buy/Sell/Hold)

---

### ✅ 2. Stock Grades API (`/grade/{symbol}`)

**Endpoint:** `https://financialmodelingprep.com/api/v3/grade/MSFT`

**Returns:** Historical analyst grades/ratings from various firms

**Sample Data (MSFT - Recent 5):**
```
Grade 1:
  Date: 2025-12-22
  Company: Wedbush
  Previous: Outperform
  New: Outperform

Grade 2:
  Date: 2025-12-04
  Company: DA Davidson
  Previous: Buy
  New: Buy

Grade 3:
  Date: 2025-11-18
  Company: Rothschild & Co
  Previous: Buy
  New: Neutral

Grade 4:
  Date: 2025-10-30
  Company: Morgan Stanley
  Previous: Overweight
  New: Overweight

Grade 5:
  Date: 2025-10-30
  Company: Wells Fargo
  Previous: Overweight
  New: Overweight
```

**Data Available:** 1,469 records for MSFT

**Use Cases:**
- Track analyst rating changes over time
- Identify upgrades/downgrades
- See consensus from multiple firms
- Recent rating activity

---

### ✅ 3. Analyst Estimates API (`/analyst-estimates/{symbol}`)

**Endpoint:** `https://financialmodelingprep.com/api/v3/analyst-estimates/MSFT`

**Returns:** Forward-looking revenue and EPS estimates for multiple periods

**Sample Data (MSFT - Next 5 periods):**
```
Estimate 1 (2030-06-30):
  Revenue Avg: $616.18B
  Revenue Range: $591.98B - $636.64B
  EPS Avg: $35.86
  EPS Range: $34.03 - $37.41

Estimate 2 (2029-06-30):
  Revenue Avg: $499.39B
  Revenue Range: $479.78B - $515.96B
  EPS Avg: $26.40
  EPS Range: $25.05 - $27.54

Estimate 3 (2028-06-30):
  Revenue Avg: $435.50B
  Revenue Range: $435.42B - $435.58B
  EPS Avg: $22.35
  EPS Range: $20.90 - $24.20

Estimate 4 (2027-06-30):
  Revenue Avg: $375.57B
  Revenue Range: $357.10B - $383.53B
  EPS Avg: $18.77
  EPS Range: $16.76 - $19.93

Estimate 5 (2026-06-30):
  Revenue Avg: $326.35B
  Revenue Range: $322.86B - $328.82B
  EPS Avg: $16.09
  EPS Range: $14.80 - $16.58
```

**Data Available:** 33 records for MSFT (multiple future periods)

**Use Cases:**
- Forward-looking revenue estimates
- EPS projections
- Growth trajectory analysis
- Estimate ranges (high/low/avg)

---

### ❌ 4. Price Target API (Not Available)

**Endpoints Tested:**
- `/price-target/MSFT` - Empty
- `/price-target-summary/MSFT` - Empty
- `/analyst-price-target/MSFT` - Empty
- `/target-price/MSFT` - Empty

**Status:** Price target data not available via these endpoints

---

## Integration Recommendations

### 1. Enhance Forward-Looking Analysis Section

**Current:** Basic forward-looking section with generic catalysts

**Enhanced:** Add actual analyst estimates and ratings

**Implementation:**
```python
# Get FMP rating data
rating_data = get_fmp_rating(symbol)
estimates_data = get_fmp_estimates(symbol)
grades_data = get_fmp_grades(symbol, limit=10)

# Add to Forward-Looking Analysis:
- Overall Rating: A- (Buy recommendation)
- Component Ratings: DCF (Buy), ROE (Strong Buy), ROA (Strong Buy), PE (Sell)
- Next Quarter Estimates: Revenue $X, EPS $Y
- Recent Analyst Activity: X upgrades, Y downgrades, Z maintains
```

### 2. Enhance Sentiment Analysis

**Current:** Uses analyst recommendations from news/other sources

**Enhanced:** Use FMP Stock Grades API for actual analyst ratings

**Benefits:**
- More accurate analyst sentiment
- Track rating changes over time
- Identify consensus shifts

### 3. Add Rating Component Analysis

**New Section:** "FMP Rating Breakdown"

**Shows:**
- Overall rating (A-F)
- Component scores (DCF, ROE, ROA, DE, PE, PB)
- Component recommendations
- Identifies strengths/weaknesses

### 4. Add Forward Estimates to Price Targets

**Current:** Price targets based on technical levels only

**Enhanced:** Add fundamental-based targets using:
- Current P/E × Forward EPS estimates
- DCF-based valuation (if available)
- Growth trajectory from estimates

---

## API Integration Code Example

```python
def get_fmp_rating(symbol: str, api_key: str) -> Dict:
    """Get FMP stock rating"""
    url = f"https://financialmodelingprep.com/api/v3/rating/{symbol}"
    response = requests.get(url, params={'apikey': api_key}, timeout=10)
    if response.status_code == 200:
        data = response.json()
        return data[0] if isinstance(data, list) and len(data) > 0 else {}
    return {}

def get_fmp_grades(symbol: str, api_key: str, limit: int = 10) -> List[Dict]:
    """Get recent analyst grades"""
    url = f"https://financialmodelingprep.com/api/v3/grade/{symbol}"
    response = requests.get(url, params={'apikey': api_key}, timeout=10)
    if response.status_code == 200:
        data = response.json()
        return data[:limit] if isinstance(data, list) else []
    return []

def get_fmp_estimates(symbol: str, api_key: str, limit: int = 5) -> List[Dict]:
    """Get analyst estimates"""
    url = f"https://financialmodelingprep.com/api/v3/analyst-estimates/{symbol}"
    response = requests.get(url, params={'apikey': api_key}, timeout=10)
    if response.status_code == 200:
        data = response.json()
        return data[:limit] if isinstance(data, list) else []
    return []
```

---

## Next Steps

1. ✅ **Test APIs** - Completed
2. ⏭️ **Integrate into stock_analysis_combiner.py**
   - Add functions to fetch FMP rating data
   - Enhance Forward-Looking Analysis section
   - Add Rating Component Breakdown section
   - Use estimates for fundamental price targets
3. ⏭️ **Update Sentiment Analysis**
   - Use FMP grades instead of/alongside current method
   - Track rating changes over time
4. ⏭️ **Test with multiple stocks**
   - Verify data availability
   - Handle edge cases (missing data)

---

*Summary Date: December 29, 2025*


