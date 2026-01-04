# Prescriptive Financial Data Sources for Company Research Skill

## Decision: Yes, Be Prescriptive

**Rationale:** Financial data quality and freshness are critical for investment decisions. Being prescriptive ensures:
- **Consistency:** Same high-quality sources used every time
- **Reliability:** Official sources prioritized over unverified sources
- **Freshness:** Clear hierarchy ensures latest data is always used
- **Verification:** Easier to verify data when sources are standardized

## Prescribed Source Hierarchy

### 1. Financial Statements & Filings

**PRIMARY: SEC EDGAR (sec.gov)** ⭐ REQUIRED FOR U.S. COMPANIES
- **URL:** https://www.sec.gov/edgar/searchedgar/companysearch.html
- **Why:** Official, authoritative, legally required, most current
- **Process:**
  1. Search by company name or ticker
  2. Filter by filing type (10-K for annual, 10-Q for quarterly)
  3. Select most recent filing
  4. Verify filing date
  5. Extract financial statements
- **Fallback:** Company Investor Relations page

**SECONDARY: Company Investor Relations Pages**
- **URL Pattern:** https://[company].com/investors
- **Why:** Official company source, often better formatted
- **Process:**
  1. Navigate to IR page
  2. Find "SEC Filings" or "Financial Reports"
  3. Download latest report
  4. Cross-reference with SEC EDGAR for accuracy

### 2. Stock Price & Market Data

**PRIMARY: Yahoo Finance** ⭐ REQUIRED
- **URL:** https://finance.yahoo.com/quote/[TICKER]
- **Why:** Free, comprehensive, real-time, reliable
- **Extract:** Stock price, market cap, P/E, P/B, ratios
- **Freshness:** Same day or previous trading day
- **Fallback:** Google Finance → MarketWatch

**SECONDARY: Google Finance**
- **URL:** https://www.google.com/finance/quote/[TICKER]
- **Why:** Free, clean interface
- **Use When:** Yahoo Finance unavailable

**TERTIARY: MarketWatch**
- **URL:** https://www.marketwatch.com/investing/stock/[TICKER]
- **Use When:** Both Yahoo and Google unavailable

### 3. Financial News & Analysis

**PRIMARY: Bloomberg** ⭐ PREFERRED
- **Why:** Premium, comprehensive, reliable
- **Access:** May require subscription (use web search for free articles)
- **Fallback Order:** Reuters → WSJ → Financial Times

**SECONDARY: Reuters**
- **Why:** Reliable, good global coverage
- **Access:** Free articles available

**TERTIARY: Wall Street Journal**
- **Why:** Premium analysis
- **Access:** May require subscription (use web search)

### 4. Analyst Ratings

**PRIMARY: Yahoo Finance Statistics Tab**
- **URL:** https://finance.yahoo.com/quote/[TICKER]/analysis
- **Why:** Free, comprehensive ratings
- **Extract:** Buy/Hold/Sell counts, price targets, recommendations

**SECONDARY: Company IR Page**
- **Why:** Official analyst coverage list
- **Extract:** List of covering analysts

**TERTIARY: MarketWatch**
- **Why:** Free ratings and recommendations

## Implementation in Skill

The skill should:
1. **Always start with prescribed sources** in order
2. **Verify freshness** at each step
3. **Use fallbacks** only if primary unavailable
4. **Document source used** in final report
5. **Flag if** non-prescribed sources used (with explanation)

## Benefits

- ✅ Consistent data quality
- ✅ Easier verification
- ✅ Faster research (know where to look)
- ✅ Better freshness (prescribed sources update frequently)
- ✅ More reliable recommendations

## Flexibility

While prescriptive, the skill maintains flexibility:
- **Fallbacks** for each source type
- **Alternative sources** allowed with justification
- **International companies** may require different sources
- **Non-U.S. markets** may need local sources




