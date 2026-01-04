# SEC EDGAR: Earnings Transcript Availability Analysis
**Date:** 2025-12-30  
**Question:** Can we get earnings call transcripts from SEC EDGAR?

---

## ❌ **ANSWER: NO - Full Transcripts Not Filed with SEC**

### Key Finding:

**Earnings call transcripts are NOT typically filed directly with the SEC.**

According to research:
- Companies file earnings releases and financial information on Form 8-K
- **Full transcripts are usually NOT included** in SEC filings
- Companies typically provide transcripts on their investor relations websites
- Third-party platforms (Seeking Alpha, etc.) aggregate transcripts

---

## ✅ **What SEC EDGAR DOES Provide:**

### 1. Form 8-K (Current Report)
**What it contains:**
- Earnings release announcements
- Press releases about earnings
- **May reference** earnings calls but **not full transcripts**
- Material events and guidance updates

**Example:** "Company will host earnings call on [date]"

### 2. Form 10-K (Annual Report)
**What it contains:**
- Management Discussion & Analysis (MD&A)
- Forward-looking statements
- **Some guidance** in MD&A section
- Strategic commentary
- Risk factors

**Use Case:** Extract guidance from MD&A section

### 3. Form 10-Q (Quarterly Report)
**What it contains:**
- Quarterly MD&A
- **Quarterly guidance updates**
- Forward-looking statements
- Operational updates

**Use Case:** Extract quarterly guidance

### 4. Form DEF 14A (Proxy Statement)
**What it contains:**
- Management compensation
- Strategic initiatives
- Sometimes forward-looking targets

---

## 🔍 **What Can Be Extracted from SEC Filings:**

### Management Guidance Sources:

1. **MD&A Sections (10-K, 10-Q)**
   - Forward-looking statements
   - Revenue expectations
   - Profitability timelines
   - Strategic initiatives

2. **8-K Earnings Releases**
   - Earnings announcements
   - Key metrics highlights
   - **May reference** guidance but not full transcript

3. **Press Releases (8-K)**
   - Strategic announcements
   - Guidance updates
   - Operational milestones

### Limitations:

- ❌ **No full transcripts** - Only summaries/references
- ❌ **No Q&A sections** - Only prepared remarks if included
- ⚠️ **Guidance extraction** - Requires parsing MD&A text
- ⚠️ **Not structured** - Need NLP/text processing

---

## 💡 **SEC EDGAR API Access:**

### Public API (No Key Required):

**Endpoints:**
1. **Company Tickers:** `https://www.sec.gov/files/company_tickers.json`
2. **Company Submissions:** `https://data.sec.gov/submissions/CIK{CIK}.json`
3. **Filing Documents:** `https://www.sec.gov/cgi-bin/viewer?action=view&cik={CIK}&accession_number={ACC}&xbrl_type=v`

**Requirements:**
- Proper User-Agent header (required by SEC)
- CIK (Central Index Key) for company lookup
- Accession number for specific filings

### Example Workflow:

```python
# Step 1: Get CIK from ticker
tickers_url = 'https://www.sec.gov/files/company_tickers.json'
# Find CIK for symbol

# Step 2: Get company filings
submissions_url = f'https://data.sec.gov/submissions/CIK{CIK}.json'
# Get list of filings

# Step 3: Filter for relevant forms (8-K, 10-K, 10-Q)
# Extract filing dates and accession numbers

# Step 4: Download and parse filings
# Extract MD&A sections for guidance
# Parse text for forward-looking statements
```

---

## 🎯 **Comparison: SEC vs FMP vs Other Sources**

| Source | Full Transcripts | Guidance | Structured Data | Cost |
|--------|-----------------|----------|----------------|------|
| **SEC EDGAR** | ❌ No | ⚠️ Yes (in MD&A) | ❌ No (text parsing) | ✅ Free |
| **FMP API** | ✅ Yes* | ✅ Yes* | ✅ Yes | ⚠️ Premium |
| **Company IR** | ✅ Yes | ✅ Yes | ❌ No | ✅ Free |
| **Seeking Alpha** | ✅ Yes | ✅ Yes | ⚠️ Partial | ⚠️ Premium |
| **Web Scraping** | ✅ Yes | ✅ Yes | ❌ No | ✅ Free |

*Requires premium subscription

---

## 📋 **Recommendation:**

### Option 1: SEC EDGAR MD&A Parsing (Free) ✅

**Pros:**
- ✅ Free access
- ✅ Official source
- ✅ Contains guidance in MD&A
- ✅ Structured filing dates

**Cons:**
- ❌ No full transcripts
- ⚠️ Requires text parsing/NLP
- ⚠️ Guidance may be less specific than transcripts
- ⚠️ More complex implementation

**Implementation:**
1. Get CIK for company
2. Fetch recent 10-K and 10-Q filings
3. Extract MD&A sections
4. Use NLP to identify forward-looking statements
5. Extract guidance targets (revenue, profitability, etc.)

### Option 2: Company Investor Relations (Free) ✅

**Pros:**
- ✅ Full transcripts available
- ✅ Official source
- ✅ Free access

**Cons:**
- ⚠️ Requires web scraping
- ⚠️ Different format per company
- ⚠️ May need to handle different layouts

### Option 3: FMP Premium (Paid) 💰

**Pros:**
- ✅ Structured API
- ✅ Full transcripts
- ✅ Easy integration

**Cons:**
- ❌ Requires premium subscription
- ❌ Additional cost

---

## 🔧 **Implementation Example: SEC EDGAR Guidance Extraction**

```python
import requests
import re
from typing import Dict, List

def get_company_cik(symbol: str) -> str:
    """Get CIK from ticker symbol"""
    url = 'https://www.sec.gov/files/company_tickers.json'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    data = response.json()
    
    for company in data.values():
        if company.get('ticker', '').upper() == symbol.upper():
            return str(company.get('cik_str', '')).zfill(10)
    return None

def get_recent_filings(cik: str, form_types: List[str] = ['10-K', '10-Q']) -> List[Dict]:
    """Get recent filings of specified types"""
    url = f'https://data.sec.gov/submissions/CIK{cik}.json'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    data = response.json()
    
    filings = data.get('filings', {}).get('recent', {})
    forms = filings.get('form', [])
    dates = filings.get('filingDate', [])
    accession_numbers = filings.get('accessionNumber', [])
    
    relevant_filings = []
    for i, form in enumerate(forms):
        if form in form_types:
            relevant_filings.append({
                'form': form,
                'date': dates[i],
                'accession': accession_numbers[i]
            })
    return relevant_filings

def extract_guidance_from_mda(text: str) -> Dict:
    """Extract guidance from MD&A text using NLP/regex"""
    guidance = {
        'revenue_targets': [],
        'profitability_timeline': None,
        'ebitda_targets': []
    }
    
    # Example patterns (would need more sophisticated NLP)
    revenue_pattern = r'\$[\d.]+[BMK]?\s*(?:GMV|revenue|sales).*?(?:by|in|target).*?(\d{4})'
    guidance['revenue_targets'] = re.findall(revenue_pattern, text, re.IGNORECASE)
    
    profitability_pattern = r'profitability.*?(?:by|in|target).*?(\d{4})'
    match = re.search(profitability_pattern, text, re.IGNORECASE)
    if match:
        guidance['profitability_timeline'] = match.group(1)
    
    return guidance
```

---

## ✅ **Conclusion:**

**Full transcripts:** ❌ **Not available from SEC**

**Management guidance:** ✅ **Available in MD&A sections** (requires parsing)

**Best approach:**
1. ✅ **SEC EDGAR** for official guidance (free, but requires parsing)
2. ✅ **Company IR pages** for full transcripts (free, but requires scraping)
3. ⚠️ **FMP Premium** for structured API access (paid, easiest)

**Recommendation:** 
- For free tier: Extract guidance from SEC 10-K/10-Q MD&A sections
- More complex but free and official source
- Would require NLP/text processing implementation

