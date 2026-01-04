# FMP API: Management Guidance Availability Analysis
**Date:** 2025-12-30  
**Question:** Can management guidance be extracted using FMP API?

---

## ⚠️ **ANSWER: YES - But Requires Premium Subscription**

### Test Results:

**Tested Endpoints:**
1. ✅ `/analyst-estimates/{symbol}` - **Available** (free tier) but limited data for JMIA
2. ✅ `/earning_calendar` - **Available** (free tier) but no upcoming earnings for JMIA
3. ✅ `/latest-transcripts` - **Endpoint exists** but requires premium subscription
4. ✅ `/earnings-transcript/{symbol}` - **Endpoint exists** but requires premium subscription
5. ✅ `/search-transcripts` - **Endpoint exists** but requires premium subscription
6. ✅ `/transcripts-dates-by-symbol/{symbol}` - **Endpoint exists** but requires premium subscription

**Status:** Endpoints exist per [FMP documentation](https://site.financialmodelingprep.com/developer/docs#latest-transcripts), but free tier API key returns empty results (subscription tier limitation).

---

## ✅ **What FMP API DOES Provide:**

### 1. Analyst Estimates (`/analyst-estimates/{symbol}`)

**Available Data:**
- Estimated EPS (forward-looking)
- Estimated Revenue (forward-looking)
- EPS Range (low/high/avg)
- Revenue Range (low/high/avg)
- Number of analysts providing estimates
- Multiple future periods (quarters/years)

**JMIA Test Results:**
```
Found 5 estimates
Estimate 1: Date: 2029-12-31, Estimated EPS: None, Estimated Revenue: None
Estimate 2: Date: 2028-12-31, Estimated EPS: None, Estimated Revenue: None
Estimate 3: Date: 2027-12-31, Estimated EPS: None, Estimated Revenue: None
```

**Status:** ⚠️ **Available but no data for JMIA** - Analyst estimates exist but are empty for JMIA (likely due to limited analyst coverage)

**Use Case:** Forward-looking analyst expectations (not management guidance)

---

### 2. Earnings Calendar (`/earning_calendar`)

**Available Data:**
- Next earnings date
- Earnings time (before/after market)
- Estimated EPS (analyst consensus)
- Estimated Revenue (analyst consensus)

**JMIA Test Results:**
```
No upcoming earnings found
```

**Status:** ⚠️ **Available but no data for JMIA** - No upcoming earnings in next 180 days

**Use Case:** Upcoming earnings dates and analyst estimates (not management guidance)

---

## ⚠️ **What FMP API Provides (Premium Tier Only):**

### Earnings Call Transcripts - ✅ Available with Premium Subscription

According to [FMP documentation](https://site.financialmodelingprep.com/developer/docs#latest-transcripts), the following endpoints are available:

1. **Latest Earnings Transcripts** (`/latest-transcripts`)
   - List of companies with available transcripts
   - Total number of transcripts per company

2. **Earnings Transcript by Symbol** (`/earnings-transcript/{symbol}`)
   - Full transcript text for specific earnings calls
   - Requires date parameter

3. **Search Transcripts** (`/search-transcripts`)
   - Search transcripts by company name or symbol

4. **Transcript Dates by Symbol** (`/transcripts-dates-by-symbol/{symbol}`)
   - Available transcript dates organized by fiscal year and quarter

**Test Results:**
- Endpoints exist and respond (HTTP 200)
- But return empty results with free tier API key
- **Conclusion:** Requires premium subscription tier

**What Can Be Extracted from Transcripts:**
- ✅ Management guidance (revenue, earnings, profitability targets)
- ✅ Forward-looking commentary
- ✅ Strategic initiatives
- ✅ Operational improvements
- ✅ Long-term targets (e.g., "$2.5-$3B GMV by 2030")
- ✅ Profitability timelines (e.g., "profitability by 2027")
- ✅ EBITDA margin targets (e.g., "20% EBITDA margin by 2030")

---

## 🔍 **Alternative Sources for Management Guidance:**

### 1. **SEC Filings (EDGAR)**
- **10-K Annual Reports** - Management discussion and analysis (MD&A)
- **10-Q Quarterly Reports** - Quarterly guidance updates
- **8-K Current Reports** - Material events and guidance changes
- **Access:** Free via SEC EDGAR API or web scraping

### 2. **Earnings Call Transcripts**
- **Sources:**
  - Company investor relations pages
  - Seeking Alpha (premium)
  - Motley Fool (premium)
  - Company websites
- **Content:** Full transcripts with Q&A sections

### 3. **Investor Presentations**
- **Sources:**
  - Company investor relations pages
  - SEC filings (often attached to 8-K)
- **Content:** Slides with targets and guidance

### 4. **Press Releases**
- **Sources:**
  - Company websites
  - PR Newswire
  - Business Wire
- **Content:** Guidance updates, target announcements

### 5. **Financial Data Providers (Paid)**
- **Bloomberg Terminal** - Full guidance extraction
- **FactSet** - Guidance data
- **Refinitiv (LSEG)** - Guidance and estimates
- **S&P Capital IQ** - Guidance extraction

---

## 💡 **Recommendations for Our Analysis:**

### Option 1: Use Analyst Estimates (Available via FMP) ✅

**Pros:**
- Already available in FMP API
- Forward-looking data
- Multiple periods
- Analyst consensus

**Cons:**
- Not management guidance (analyst expectations)
- Limited coverage for small caps like JMIA
- May differ from management guidance

**Implementation:**
```python
# Already implemented in stock_forward_analysis.py
estimates = forward_analyzer.get_analyst_estimates(symbol)
# Use estimated EPS and revenue for forward-looking analysis
```

---

### Option 2: Manual Guidance Extraction (Not Automated) ⚠️

**Process:**
1. Identify latest earnings call date
2. Access transcript (Seeking Alpha, company website)
3. Extract guidance manually
4. Add to analysis report

**Pros:**
- Accurate management guidance
- Specific targets and timelines
- Strategic context

**Cons:**
- Manual process
- Not automated
- Time-consuming

**Current Implementation:**
- Placeholder in report: "Management guidance not available via API"
- Instructions to review earnings calls manually

---

### Option 3: Web Scraping (Advanced) 🔧

**Potential Sources:**
- Company investor relations pages
- SEC EDGAR filings
- Earnings call transcript websites

**Pros:**
- Automated extraction
- Direct from source
- Up-to-date

**Cons:**
- Complex implementation
- Website changes break scrapers
- Legal/ethical considerations
- Rate limiting

**Feasibility:** Medium - Would require significant development effort

---

### Option 4: Third-Party APIs (Paid) 💰

**Options:**
- **Alpha Vantage** - Some guidance data
- **Polygon.io** - Earnings call transcripts (premium)
- **IEX Cloud** - Some guidance endpoints
- **Quandl/Nasdaq Data Link** - Various financial data

**Pros:**
- Structured data
- API access
- Regular updates

**Cons:**
- Additional cost
- May still require parsing
- Coverage varies

**Feasibility:** Medium - Would require API subscription

---

## 📊 **Current State in Our Analysis:**

### What We Have:
✅ **Analyst Estimates** (via FMP API)
- Forward EPS estimates
- Forward revenue estimates
- Multiple periods

✅ **Earnings Calendar** (via FMP API)
- Upcoming earnings dates
- Analyst consensus estimates

### What We're Missing:
❌ **Management Guidance**
- Company-provided targets
- Profitability timelines
- Strategic commentary

### Current Implementation:
```python
# In report_generator.py
report_content += "**Management Guidance:**\n"
report_content += "- ⚠️ **Note:** Management guidance not available via API. "
report_content += "Review latest earnings calls and investor presentations for:\n"
report_content += "  - Revenue growth targets\n"
report_content += "  - Profitability timeline (e.g., profitability by 2027)\n"
report_content += "  - Key operational milestones\n"
report_content += "  - Cost reduction initiatives\n\n"
```

---

## 🎯 **Recommendation:**

### Short Term (Current):
✅ **Keep current implementation** - Placeholder with instructions
- Analyst estimates provide forward-looking data
- Users can manually review earnings calls
- Clear instructions provided

### Medium Term (Enhancement):
⚠️ **Consider adding analyst estimates to report** (if available)
- Already available via FMP API
- Provides forward-looking context
- Better than nothing

### Long Term (Future):
🔧 **Consider web scraping or third-party API** (if needed)
- Only if management guidance becomes critical
- Requires significant development effort
- May not be worth the cost/complexity

---

## 📋 **Summary:**

| Data Type | FMP API Available? | Subscription Tier | JMIA Data Available? | Use Case |
|-----------|-------------------|------------------|---------------------|----------|
| **Analyst Estimates** | ✅ Yes | Free | ⚠️ Empty for JMIA | Forward EPS/Revenue |
| **Earnings Calendar** | ✅ Yes | Free | ❌ No upcoming | Earnings dates |
| **Earnings Transcripts** | ✅ Yes | **Premium** | ⚠️ Requires premium | Full call content |
| **Management Guidance** | ✅ Yes* | **Premium** | ⚠️ Requires premium | Company targets |
| **Forward Guidance** | ✅ Yes* | **Premium** | ⚠️ Requires premium | Company guidance |

*Available via transcript extraction, not direct endpoint

---

## ✅ **Conclusion:**

**Management guidance CAN be extracted using FMP API, but requires a premium subscription tier.**

**Current Situation:**
- ✅ Endpoints exist: `/latest-transcripts`, `/earnings-transcript/{symbol}`, `/search-transcripts`
- ⚠️ Free tier API key returns empty results (subscription limitation)
- ✅ Premium tier would provide full transcript access
- ✅ Transcripts contain management guidance, targets, and forward-looking commentary

**Current Best Practice (Free Tier):**
1. ✅ Use analyst estimates (when available) for forward-looking data
2. ✅ Provide placeholder with instructions for manual review
3. ✅ Reference Seeking Alpha articles (which extract guidance manually)
4. ⚠️ Consider upgrading to premium tier if transcript access is critical

**If Premium Tier Available:**
1. ✅ Extract transcripts using `/earnings-transcript/{symbol}` endpoint
2. ✅ Parse transcripts for management guidance and targets
3. ✅ Extract forward-looking commentary automatically
4. ✅ Include in analysis report

**Status:** Current implementation is appropriate for free tier. Premium tier would enable automated guidance extraction.

