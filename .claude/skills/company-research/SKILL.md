---
name: company-research
description: Conduct comprehensive company research including fundamental analysis, sentiment analysis, and investment evaluation. Follows prescribed workflow hierarchy: (1) Invoke researcher skill first for general information gathering, (2) Add specialized financial analysis using prescribed sources (SEC EDGAR, Yahoo Finance), (3) Add sentiment analysis using prescribed sources (Bloomberg, Reuters, Yahoo Finance Statistics). Uses prescriptive source hierarchy for consistency, reliability, and data freshness verification.
---

# Company Research Skill

This skill enables Claude to conduct thorough company research by following a **prescribed workflow hierarchy**: (1) **First, explicitly invoke the researcher skill** for general information gathering, (2) **Then add specialized financial analysis** using prescribed sources (SEC EDGAR, Yahoo Finance), (3) **Finally add sentiment analysis** using prescribed sources (Bloomberg, Reuters, Yahoo Finance Statistics). **Critical focus on data freshness and authenticity** - all data sources are verified for recency and credibility.

**Important:** This skill prioritizes **current, verified data** over historical information. All sources are checked for publication dates, and stale data is flagged or excluded.

**⚠️ PRESCRIPTIVE WORKFLOW:** This skill follows a strict hierarchy: Researcher skill MUST be invoked first, then financial analysis, then sentiment analysis. See "Research Workflow" section below.

**⚠️ PRESCRIPTIVE SOURCES:** This skill uses a prescribed hierarchy of financial data sources to ensure consistency, reliability, and freshness. See "Prescribed Financial Data Sources" section below.

## When to Use This Skill

Use this skill when:
- User asks to research a company for investment purposes
- User needs fundamental analysis of a company
- User wants sentiment analysis on a company
- User requests investment recommendations (Buy/Hold/Sell)
- User needs to compare companies
- User wants to understand a company's financial health
- User needs analysis of recent company news or events
- User requests evaluation of company's competitive position
- User asks to find top companies in a category/industry (e.g., "top 10 AI companies")
- User needs ranking/identification of companies by criteria (revenue, market cap, growth, etc.)

**Examples:**
- "Research Company X for investment"
- "Analyze Company Y's financials and give me a buy/sell recommendation"
- "What's the sentiment around Company Z?"
- "Compare Company A vs Company B"
- "Research Company C's recent earnings and stock performance"
- "Find the top 10 AI companies by market cap"
- "What are the best-performing fintech companies?"
- "Rank the top 5 cloud infrastructure companies by revenue growth"

## Core Capabilities

### 1. Multi-Source Information Gathering (Prescribed Hierarchy)

**Capability:** Gather comprehensive information using prescribed source hierarchy

**⚠️ PRESCRIPTIVE WORKFLOW HIERARCHY:** Follow this exact order - researcher skill first, then specialized analysis

#### Phase 1: General Information Gathering (Prescribed Primary Method)

**⭐ REQUIRED FIRST STEP: Invoke Researcher Skill**

**Why Researcher Skill First:**
- Provides comprehensive multi-source synthesis
- Handles YouTube research automatically
- Synthesizes information from multiple sources
- Establishes baseline company understanding
- More efficient than manual web searches

**Process:**
1. **Explicitly invoke Researcher Skill** with query:
   ```
   "Research [Company Name] ([Ticker]) - company overview, recent news, 
   industry context, management team, products/services, recent developments"
   ```

2. **Researcher Skill Will:**
   - Search web for company information (multiple sources)
   - Search YouTube for earnings calls, investor presentations, CEO interviews
   - Extract information from company websites
   - Synthesize information from multiple sources
   - Provide comprehensive overview

3. **Extract from Researcher Skill Output:**
   - Company overview and history
   - Recent news and press releases
   - Industry context and competitive landscape
   - Management team information
   - Product/service information
   - Recent developments and events

**Output:**
- Comprehensive company overview (from researcher skill)
- Recent news and events (synthesized by researcher skill)
- Industry context (from researcher skill)
- Management insights (from researcher skill)
- Product/service information (from researcher skill)

**⚠️ CRITICAL:** Do NOT skip researcher skill and go directly to financial analysis. Researcher skill provides essential context and ensures comprehensive information gathering.

#### Phase 2: Specialized Financial Analysis (After Researcher Skill)

**Purpose:** Add financial analysis using prescribed sources

**Process:**
1. **SEC EDGAR (Prescribed Primary):** Extract financial statements
2. **Yahoo Finance (Prescribed Primary):** Get market data and ratios
3. **Financial Ratio Analysis:** Calculate and interpret ratios
4. **Trend Analysis:** Analyze financial trends over time

**Integration:**
- Researcher skill provides general company context (Phase 1)
- Company research skill adds specialized financial analysis (Phase 2)
- Both phases work together seamlessly

---

### 2. Data Freshness & Authenticity Verification ⭐ *Critical Capability*

**Capability:** Verify all data sources for recency, authenticity, and credibility

**Why Critical:**
- Financial data changes quarterly (earnings, financials)
- Stock prices change daily
- News sentiment can shift rapidly
- Stale data leads to poor investment decisions
- Unverified sources can contain misinformation

**Freshness Checks:**

1. **Publication Date Verification:**
   - Check publication date of all articles, reports, filings
   - Prioritize sources from last 3 months for financial data
   - Prioritize sources from last 1 month for news/sentiment
   - Flag data older than 6 months as potentially stale
   - Exclude data older than 1 year unless historical context needed

2. **Source Credibility Assessment:**
   - **High Credibility:** SEC filings, official company IR pages, major financial news (Bloomberg, Reuters, WSJ, Financial Times)
   - **Medium Credibility:** Reputable financial blogs, industry publications, verified analyst reports
   - **Low Credibility:** Unverified blogs, social media (unless analyzing sentiment), anonymous sources
   - Always verify source authenticity before using data

3. **Data Recency Requirements by Type:**
   - **Stock Price:** Must be current (same day or previous trading day) - **Source: Yahoo Finance (prescribed)**
   - **Financial Statements:** Latest quarterly filing (10-Q) or annual filing (10-K) - **Source: SEC EDGAR (prescribed)**
   - **Earnings Reports:** Most recent quarter - **Source: Company IR page or SEC EDGAR (prescribed)**
   - **News/Sentiment:** Last 1-3 months preferred - **Source: Bloomberg, Reuters, WSJ (prescribed order)**
   - **Analyst Reports:** Last 6 months preferred - **Source: Yahoo Finance Statistics tab (prescribed)**

4. **Verification Process:**
   ```
   For each data source:
   1. Extract publication date
   2. Calculate age of data
   3. Check source credibility
   4. Verify data hasn't been superseded
   5. Flag if stale or low credibility
   6. Prioritize freshest, most credible sources
   ```

5. **Stale Data Handling:**
   - **Flag stale data** with warning: "⚠️ Data from [date] - may be outdated"
   - **Exclude stale data** from primary analysis if fresher data available
   - **Note in report** when using older data for historical context
   - **Prioritize** most recent data in all analysis

**Authenticity Checks:**

1. **Source Verification:**
   - Verify URLs point to official sources
   - Check for official company domains (.com IR pages)
   - Verify SEC EDGAR filings are from sec.gov
   - Cross-reference claims across multiple credible sources

2. **Data Consistency:**
   - Cross-check financial numbers across multiple sources
   - Verify stock prices match across financial data providers
   - Check for discrepancies and flag them

3. **Red Flags:**
   - Data without publication dates
   - Unverifiable claims
   - Sources that don't match official records
   - Suspicious URLs or domains

**Output:**
- All sources tagged with freshness status
- Credibility scores for each source
- Warnings for potentially stale data
- Verification notes in final report

---

### 3. Financial Data Extraction & Analysis

**Capability:** Extract and analyze financial data from SEC filings and financial sources

**⚠️ PRESCRIPTIVE SOURCE HIERARCHY:** Use sources in this exact order of preference for maximum reliability and freshness

#### Prescribed Financial Data Sources

**1. SEC EDGAR (sec.gov) - PRIMARY SOURCE FOR U.S. COMPANIES ⭐ REQUIRED**
- **URL:** https://www.sec.gov/edgar/searchedgar/companysearch.html
- **Why Preferred:** Official, authoritative, most current, legally required filings
- **What to Extract:**
  - **10-K (Annual Report):** Most comprehensive, filed within 60-90 days of fiscal year end
  - **10-Q (Quarterly Report):** Filed within 40-45 days of quarter end
  - **8-K (Current Report):** Material events, filed within 4 business days
  - **Proxy Statements:** Executive compensation, governance
- **Freshness:** Always use latest available filing
- **Verification:** Check filing date on SEC website
- **Process:**
  1. Navigate to SEC EDGAR company search
  2. Search by company name or CIK (Central Index Key)
  3. Filter by filing type (10-K, 10-Q)
  4. Select most recent filing
  5. Extract financial statements from filing
  6. **Verify filing date** - should be within last 90 days for quarterly, last year for annual
- **Fallback:** If SEC EDGAR unavailable, use company IR page

**2. Company Investor Relations (IR) Pages - SECONDARY SOURCE**
- **URL Pattern:** https://[company].com/investors or https://investor.[company].com
- **Why Preferred:** Official company source, often more user-friendly than SEC filings
- **What to Extract:**
  - Latest earnings releases
  - Financial statements (often formatted better than SEC filings)
  - Earnings call transcripts
  - Investor presentations
  - Guidance and forward-looking statements
- **Freshness:** Check "Last Updated" or publication date
- **Verification:** Cross-reference with SEC filings for accuracy
- **Process:**
  1. Navigate to company IR page
  2. Find "Financials" or "Reports" section
  3. Download latest quarterly/annual report
  4. Extract financial statements
  5. Verify dates match SEC EDGAR
- **Fallback:** If IR page unavailable, use financial data aggregators

**3. Financial Data Aggregators - TERTIARY SOURCE (For Ratios & Market Data)**

**Preferred Order:**
1. **Yahoo Finance** (finance.yahoo.com) ⭐ PRIMARY FOR MARKET DATA
   - **Why:** Free, comprehensive, real-time stock prices, historical data
   - **What to Extract:** Stock price, market cap, P/E ratio, financial ratios, historical prices
   - **Freshness:** Real-time stock prices, daily updates for ratios
   - **URL Pattern:** https://finance.yahoo.com/quote/[TICKER]
   - **Process:**
     1. Navigate to company quote page
     2. Check "Statistics" tab for detailed ratios
     3. Verify data is current (same day)
     4. Extract: P/E, P/B, EV/EBITDA, ROE, ROA, margins, etc.
   - **Fallback:** Google Finance

2. **Google Finance** (google.com/finance) ⭐ SECONDARY FOR MARKET DATA
   - **Why:** Free, clean interface, good for quick lookups
   - **What to Extract:** Stock price, market data, basic ratios
   - **Freshness:** Real-time updates
   - **URL Pattern:** https://www.google.com/finance/quote/[TICKER]
   - **Use When:** Yahoo Finance unavailable
   - **Fallback:** MarketWatch

3. **MarketWatch** (marketwatch.com) ⭐ TERTIARY FOR MARKET DATA
   - **Why:** Free, comprehensive financial data, news integration
   - **What to Extract:** Stock data, financials, ratios, analyst ratings
   - **Freshness:** Real-time updates
   - **URL Pattern:** https://www.marketwatch.com/investing/stock/[TICKER]
   - **Use When:** Both Yahoo and Google unavailable

**4. Financial News Sources - FOR CONTEXT & ANALYSIS**

**Preferred Order:**
1. **Bloomberg** (bloomberg.com) ⭐ PRIMARY FOR NEWS
   - **Why:** Premium financial news, comprehensive analysis, reliable data
   - **What to Extract:** News articles, analyst reports, market analysis
   - **Freshness:** Real-time news, check publication dates
   - **Access:** May require subscription, use web search for free articles
   - **Fallback:** Reuters

2. **Reuters** (reuters.com) ⭐ SECONDARY FOR NEWS
   - **Why:** Reliable financial news, good global coverage
   - **What to Extract:** News articles, earnings reports, market updates
   - **Freshness:** Real-time news, check publication dates
   - **Access:** Free articles available
   - **Fallback:** WSJ

3. **Wall Street Journal** (wsj.com) ⭐ TERTIARY FOR NEWS
   - **Why:** Premium financial news, in-depth analysis
   - **What to Extract:** News articles, analysis, market commentary
   - **Freshness:** Daily updates, check publication dates
   - **Access:** May require subscription, use web search for free articles
   - **Fallback:** Financial Times

4. **Financial Times** (ft.com)
   - **Why:** Premium international financial news
   - **What to Extract:** News articles, analysis, global perspective
   - **Freshness:** Daily updates, check publication dates
   - **Access:** May require subscription, use web search for free articles

**5. Analyst Reports & Ratings**

**Preferred Sources (In Order):**
1. **Yahoo Finance Statistics Tab** ⭐ PRIMARY
   - **URL:** https://finance.yahoo.com/quote/[TICKER]/analysis
   - **Why:** Free, comprehensive ratings, price targets
   - **What to Extract:** Buy/Hold/Sell counts, average price target, analyst recommendations
   - **Freshness:** Updated regularly, verify date
   - **Fallback:** Company IR page

2. **Company IR Page** ⭐ SECONDARY
   - **Why:** Official analyst coverage list
   - **What to Extract:** List of covering analysts, official analyst reports
   - **Freshness:** Check last updated date
   - **Fallback:** MarketWatch

3. **MarketWatch** ⭐ TERTIARY
   - **Why:** Free ratings and recommendations
   - **What to Extract:** Analyst ratings, recommendations
   - **Freshness:** Verify date

**⚠️ IMPORTANT:** Always verify analyst report dates - prefer reports from last 6 months

#### Financial Data Extraction Process (Prescribed Method)

**Step 1: Identify Latest Filings (Prescribed Method)**
1. **Start with SEC EDGAR (REQUIRED):**
   - Navigate to: https://www.sec.gov/edgar/searchedgar/companysearch.html
   - Search by company name or ticker symbol
   - Filter by filing type: "10-K" (annual) or "10-Q" (quarterly)
   - Sort by filing date (most recent first)
   - Select the most recent filing
   - **Verify filing date** - should be within last 90 days for quarterly, last year for annual
   - Extract financial statements from filing

2. **If SEC EDGAR unavailable, use Company IR Page:**
   - Navigate to company investor relations page
   - Find "SEC Filings" or "Financial Reports" section
   - Download latest 10-K or 10-Q
   - Verify filing date matches SEC EDGAR (if available)

**Step 2: Extract Key Financial Data (From SEC Filing or IR Page)**
- **Income Statement:** Revenue, Net Income, EPS, Operating Income, Gross Profit
- **Balance Sheet:** Total Assets, Total Liabilities, Shareholders' Equity, Cash & Equivalents
- **Cash Flow Statement:** Operating Cash Flow, Free Cash Flow, Capital Expenditures, Financing Activities
- **Key Metrics:** Revenue growth, Profit margins, ROE, ROA, Debt-to-Equity

**Step 3: Get Market Data & Ratios (Prescribed Method)**
1. **Start with Yahoo Finance (REQUIRED):**
   - Navigate to: https://finance.yahoo.com/quote/[TICKER]
   - Extract: Current stock price, market cap, P/E ratio, P/B ratio, dividend yield
   - Navigate to "Statistics" tab for detailed ratios
   - Extract: All valuation, profitability, liquidity, debt ratios
   - **Verify data is current** (same day or previous trading day)

2. **If Yahoo Finance unavailable, use Google Finance:**
   - Navigate to: https://www.google.com/finance/quote/[TICKER]
   - Extract: Stock price, basic ratios
   - Verify freshness

3. **If both unavailable, use MarketWatch:**
   - Navigate to: https://www.marketwatch.com/investing/stock/[TICKER]
   - Extract: Stock data, ratios
   - Verify freshness

**Step 4: Calculate Additional Financial Ratios**
- **Valuation:** P/E ratio, P/B ratio, EV/EBITDA, PEG ratio
- **Profitability:** Net margin, Operating margin, ROE, ROA
- **Liquidity:** Current ratio, Quick ratio
- **Debt:** Debt-to-equity, Interest coverage
- **Efficiency:** Asset turnover, Inventory turnover

**Step 5: Trend Analysis**
- Compare current period to previous periods (QoQ, YoY)
- Identify trends (growth, decline, stability)
- Calculate growth rates
- **Source:** Use historical data from SEC filings or Yahoo Finance historical data

**Step 6: Peer Comparison**
- Identify competitors/peers (from industry reports or company filings)
- Compare financial ratios using same data sources (Yahoo Finance for consistency)
- Benchmark against industry averages (from financial aggregators or industry reports)

#### Source Verification Checklist

**For Each Financial Data Source:**
- [ ] Source is from prescribed list (SEC EDGAR, Company IR, Yahoo Finance, etc.)
- [ ] Publication/filing date verified
- [ ] Data is current (within freshness requirements)
- [ ] Cross-referenced with another source if possible
- [ ] Source credibility assessed (High/Medium/Low)
- [ ] Stale data flagged if used
- [ ] Fallback source documented if primary unavailable

#### Freshness Requirements by Source Type

**SEC Filings:**
- **10-Q (Quarterly):** Must be latest filing, filed within 40-45 days of quarter end
- **10-K (Annual):** Must be latest filing, filed within 60-90 days of fiscal year end
- **Flag if:** Filing is more than 90 days old (for quarterly) or more than 1 year old (for annual)

**Stock Price & Market Data:**
- **Source:** Yahoo Finance (prescribed primary)
- **Requirement:** Same day or previous trading day
- **Flag if:** More than 1 day old

**Financial Ratios:**
- **Source:** Yahoo Finance Statistics tab (prescribed)
- **Requirement:** Updated daily, verify date
- **Flag if:** More than 1 week old

**News & Analysis:**
- **Source:** Bloomberg, Reuters, WSJ, Financial Times (prescribed order)
- **Requirement:** Last 1-3 months preferred
- **Flag if:** More than 3 months old

**Analyst Reports:**
- **Source:** Yahoo Finance Statistics tab (prescribed primary)
- **Requirement:** Last 6 months preferred
- **Flag if:** More than 6 months old

---

### 4. Sentiment Analysis

**Capability:** Analyze sentiment from news, earnings calls, and analyst reports

**Sources (Prescribed Order):**
- **News Articles:** Bloomberg, Reuters, WSJ, Financial Times (prescribed order)
- **Earnings Call Transcripts:** From company IR pages or financial news sites
- **Analyst Reports:** From Yahoo Finance Statistics tab (prescribed) or company IR page
- **Social Media:** Twitter/X, LinkedIn (if analyzing public sentiment)

**Process:**
1. **News Sentiment:**
   - Gather recent news articles (last 1-3 months) from prescribed sources
   - Start with Bloomberg, then Reuters, then WSJ/FT
   - Analyze tone: Positive, Negative, Neutral
   - Identify key themes and concerns
   - Track sentiment trends over time
   - **Verify publication dates** - prefer last 1-3 months

2. **Earnings Call Analysis:**
   - Extract transcripts from latest earnings call (from company IR page)
   - Analyze management tone and confidence
   - Identify key messages and forward guidance
   - Note any concerns or red flags mentioned
   - **Verify call date** - use most recent call

3. **Analyst Sentiment:**
   - Find analyst ratings from Yahoo Finance Statistics tab (prescribed)
   - Track changes in analyst recommendations
   - Note price targets and rationale
   - **Verify report dates** - prefer last 6 months

4. **Social Media Sentiment** (if relevant):
   - Analyze public sentiment from social media
   - Note trends and concerns
   - Consider volume and engagement

**Freshness Requirements:**
- Prioritize news from last 1-3 months
- Use most recent earnings call transcript
- Check dates on all sentiment sources
- Flag if sentiment data is more than 3 months old

**Output:**
- Overall sentiment score (Positive/Negative/Neutral)
- Key themes and concerns
- Sentiment trends
- Analyst consensus
- All sources dated and verified

---

### 5. Investment Analysis & Recommendation

**Capability:** Synthesize all research into investment analysis and recommendation

**Process:**
1. **Fundamental Analysis:**
   - Evaluate financial health (using data from SEC EDGAR and Yahoo Finance)
   - Assess growth prospects
   - Analyze competitive position
   - Review management quality

2. **Risk Assessment:**
   - Identify key risks
   - Assess risk factors
   - Evaluate risk/reward ratio

3. **Valuation:**
   - Compare current valuation to peers (using Yahoo Finance for consistency)
   - Assess if overvalued/undervalued
   - Consider growth prospects

4. **Investment Thesis:**
   - Develop investment thesis
   - Identify key catalysts
   - Note key risks

5. **Recommendation:**
   - **Buy:** Strong fundamentals, good growth, reasonable valuation
   - **Hold:** Decent company but no strong catalyst or fully valued
   - **Sell:** Weak fundamentals, poor growth, overvalued, or high risk

**Output:**
- Investment analysis report
- Investment thesis
- Risk assessment
- Recommendation (Buy/Hold/Sell)
- Confidence level
- Key catalysts and risks

---

## Research Workflow

### Standard Company Research Process

#### Step 1: Query Analysis
**Purpose:** Understand research request and plan approach

**Tasks:**
- Identify company name and ticker symbol
- Understand research goal (investment, general info, comparison)
- Determine depth needed (quick overview vs. deep analysis)
- Plan data sources to consult (using prescribed sources)

**Example:**
```
Query: "Research Apple Inc. (AAPL) for investment"

Prescribed Workflow Plan:
1. Phase 1: Invoke Researcher Skill (REQUIRED FIRST) ⭐
   - Query: "Research Apple Inc. (AAPL) - company overview, recent news, 
     industry context, management team, products/services, recent developments"
   - Researcher skill will handle: web search, YouTube research, synthesis

2. Phase 2: Financial Analysis (Prescribed Sources)
   - SEC EDGAR: Latest 10-K/10-Q filings
   - Yahoo Finance: Stock price, ratios, market data

3. Phase 3: Sentiment Analysis (Prescribed Sources)
   - Bloomberg, Reuters: Recent news
   - Yahoo Finance Statistics: Analyst ratings

4. Phase 4: Investment Recommendation
   - Synthesize all information
   - Provide Buy/Hold/Sell recommendation
```

#### Step 2: Data Freshness & Source Planning
**Purpose:** Plan sources with freshness requirements using prescribed hierarchy

**Tasks:**
- Identify required data types (financials, news, sentiment)
- Determine freshness requirements for each
- Plan source priority using prescribed hierarchy:
  - Financials: SEC EDGAR → Company IR
  - Market Data: Yahoo Finance → Google Finance → MarketWatch
  - News: Bloomberg → Reuters → WSJ → FT
  - Analyst Ratings: Yahoo Finance Statistics → Company IR → MarketWatch
- Set up freshness verification checks

**Freshness Priorities:**
- **Critical (Same Day):** Stock price (Yahoo Finance)
- **Very Recent (Last Month):** News, earnings, sentiment (Bloomberg, Reuters)
- **Recent (Last Quarter):** Financial statements (SEC EDGAR)
- **Acceptable (Last 6 Months):** Analyst reports (Yahoo Finance Statistics)

#### Step 3: Information Gathering (Prescribed Hierarchy)

**⚠️ PRESCRIPTIVE ORDER:** Follow this exact sequence - researcher skill first, then financial, then sentiment

**Phase 1: General Information (Researcher Skill) ⭐ REQUIRED FIRST STEP**

**Action:** Explicitly invoke Researcher Skill

**Query Format:**
```
"Research [Company Name] ([Ticker]) - company overview, recent news, 
industry context, management team, products/services, recent developments, 
competitive position"
```

**Researcher Skill Will:**
- Search web for company information (multiple sources)
- Search YouTube for earnings calls, investor presentations, CEO interviews
- Extract information from company websites and investor relations pages
- Synthesize information from multiple sources
- Provide comprehensive overview

**Extract from Researcher Skill Output:**
- Company overview and history
- Recent news and press releases (with dates)
- Industry context and competitive landscape
- Management team information
- Product/service information
- Recent developments and events
- Competitive position

**⚠️ DO NOT SKIP:** Researcher skill must be invoked first. It provides essential context and ensures comprehensive information gathering before specialized analysis.

**Phase 2: Financial Data Extraction (Prescribed Sources) ⭐ AFTER RESEARCHER SKILL**

**Action:** Add specialized financial analysis using prescribed sources

**Process:**
1. **Start with SEC EDGAR (Prescribed Primary):**
   - Navigate to SEC EDGAR company search
   - Search for latest filings (10-K/10-Q)
   - Verify filing date (should be most recent)
   - Extract financial statements: Income Statement, Balance Sheet, Cash Flow
   - **Fallback:** If SEC EDGAR unavailable, use Company IR page

2. **Get Market Data (Prescribed Primary):**
   - Navigate to Yahoo Finance for stock price and ratios
   - Navigate to Yahoo Finance Statistics tab for detailed ratios
   - Verify freshness: Stock price same day, ratios current
   - **Fallback:** If Yahoo Finance unavailable, use Google Finance

**Phase 3: Sentiment Analysis (Prescribed Sources) ⭐ AFTER FINANCIAL DATA**

**Action:** Add sentiment analysis using prescribed sources

**Process:**
1. **Gather News (Prescribed Order):**
   - Start with Bloomberg (prescribed primary)
   - Then Reuters (prescribed secondary)
   - Then WSJ/FT (prescribed tertiary)
   - Verify dates: News last 1-3 months preferred

2. **Extract Earnings Call:**
   - From company IR page (most recent)
   - Or from researcher skill output if available

3. **Get Analyst Ratings (Prescribed Primary):**
   - From Yahoo Finance Statistics tab
   - Verify dates: Analyst reports last 6 months preferred
   - **Fallback:** Company IR page or MarketWatch

**Freshness Checks During Gathering:**
- Verify publication date of each source
- Check if data is superseded by newer information
- Flag stale data immediately
- Prioritize freshest sources from prescribed hierarchy

#### Step 4: Data Verification & Freshness Assessment
**Purpose:** Verify all data is current and authentic using prescribed sources

**Tasks:**
- Check publication dates of all sources
- Verify source credibility (prescribed sources are high credibility)
- Cross-reference data across sources
- Flag any stale or unverified data
- Calculate data freshness scores
- Document which prescribed source was used

**Verification Checklist:**
- [ ] All sources are from prescribed hierarchy
- [ ] All sources have publication dates
- [ ] Financial data is from latest SEC EDGAR filing
- [ ] Stock price is current from Yahoo Finance (same day or previous trading day)
- [ ] News articles are from prescribed sources (Bloomberg, Reuters, WSJ, FT)
- [ ] Analyst ratings from Yahoo Finance Statistics tab
- [ ] All sources are credible (prescribed sources are high credibility)
- [ ] No stale data used in primary analysis
- [ ] Stale data flagged if used for context
- [ ] Fallback sources documented if primary unavailable

#### Step 5: Financial Analysis
**Purpose:** Analyze company's financial health using prescribed sources

**Tasks:**
- Extract key financial metrics from SEC EDGAR filings
- Calculate financial ratios (or use from Yahoo Finance Statistics tab)
- Analyze trends (revenue growth, profitability, etc.)
- Compare to peers using same data sources (Yahoo Finance for consistency)
- Assess financial strength

**Output:**
- Financial statements summary (from SEC EDGAR)
- Key ratios and metrics (from Yahoo Finance Statistics)
- Trend analysis
- Peer comparison (using Yahoo Finance for consistency)
- Financial health assessment

#### Step 6: Sentiment Analysis
**Purpose:** Understand market sentiment using prescribed sources

**Tasks:**
- Analyze news sentiment (from Bloomberg, Reuters, WSJ, FT)
- Analyze earnings call sentiment (from company IR page)
- Review analyst ratings (from Yahoo Finance Statistics tab)
- Identify key themes and concerns
- Track sentiment trends

**Output:**
- Overall sentiment score
- Key themes
- Analyst consensus (from Yahoo Finance Statistics)
- Sentiment trends
- All sources dated and verified

#### Step 7: Investment Analysis & Synthesis
**Purpose:** Synthesize all research into investment analysis

**Tasks:**
- Combine financial analysis (SEC EDGAR + Yahoo Finance) with sentiment
- Assess competitive position
- Evaluate growth prospects
- Identify risks and catalysts
- Develop investment thesis
- Make recommendation

**Output:**
- Investment analysis report
- Investment thesis
- Risk assessment
- Recommendation (Buy/Hold/Sell)
- Confidence level

#### Step 8: Documentation
**Purpose:** Create comprehensive investment research report

**Tasks:**
- Create structured report using template
- Include all data with freshness dates
- Document which prescribed sources were used
- Flag any stale data used
- Include source citations with prescribed source hierarchy
- Add recommendations and rationale

**Document Checklist:**
- [ ] All sources cited with dates and prescribed source type
- [ ] Freshness status noted for all data
- [ ] Prescribed source hierarchy documented
- [ ] Stale data flagged if used
- [ ] Financial analysis included (SEC EDGAR + Yahoo Finance)
- [ ] Sentiment analysis included (Bloomberg, Reuters, Yahoo Finance Statistics)
- [ ] Investment recommendation included
- [ ] Risks and catalysts identified

---

## Tool Usage Instructions

### 1. Using Researcher Skill ⭐ REQUIRED FIRST STEP

**Purpose:** Gather general company information (prescribed primary method)

**⚠️ PRESCRIPTIVE WORKFLOW:** Researcher skill MUST be invoked first, before financial analysis

**Usage:**
```markdown
Step 1: Explicitly invoke Researcher Skill with query:
"Research [Company Name] ([Ticker]) - company overview, recent news, 
industry context, management team, products/services, recent developments, 
competitive position"

Researcher skill will:
- Search web for company information (multiple sources)
- Search YouTube for earnings calls, investor presentations, CEO interviews
- Extract information from company websites and investor relations pages
- Synthesize information from multiple sources
- Provide comprehensive overview with source citations

Step 2: Extract from Researcher Skill Output:
- Company overview and history
- Recent news and events (with dates)
- Industry context
- Management team information
- Product/service information
- Competitive position
```

**Why Researcher Skill First:**
- Provides comprehensive multi-source synthesis
- Handles YouTube research automatically
- More efficient than manual web searches
- Ensures no important information is missed
- Establishes baseline understanding before specialized analysis

**Integration:**
- **Phase 1:** Researcher skill handles general information gathering (REQUIRED FIRST)
- **Phase 2:** Company research skill adds financial analysis using prescribed sources (SEC EDGAR, Yahoo Finance)
- **Phase 3:** Company research skill adds sentiment analysis using prescribed sources (Bloomberg, Reuters, Yahoo Finance Statistics)
- All phases work together in prescribed hierarchy

### 2. Using web_search for Financial Data (Prescribed Sources)

**Purpose:** Find financial data, stock prices, analyst reports using prescribed sources

**Usage:**
```python
# Search for latest financial data (prescribed sources)
web_search(search_term="[Company Name] [Ticker] SEC EDGAR latest filing 10-K 2024")
web_search(search_term="[Company Name] [Ticker] Yahoo Finance stock price today")
web_search(search_term="[Company Name] [Ticker] Bloomberg analyst ratings 2024")
web_search(search_term="[Company Name] [Ticker] Reuters earnings Q4 2024")
```

**Best Practices:**
- Include current year in search terms
- Use "latest" or "recent" keywords
- Search for specific filing types (10-K, 10-Q)
- Prioritize prescribed sources (Bloomberg, Reuters, Yahoo Finance)
- Verify dates in search results

### 3. Using Browser Tools for SEC EDGAR (Prescribed Primary Source)

**Purpose:** Extract detailed financial data from SEC EDGAR (prescribed primary source)

**Process:**
```markdown
1. Navigate to SEC EDGAR: https://www.sec.gov/edgar/searchedgar/companysearch.html
2. Search for company by name or ticker
3. Filter by filing type: 10-K (annual) or 10-Q (quarterly)
4. Sort by filing date (most recent first)
5. Select most recent filing
6. Verify filing date (should be within last 90 days for quarterly)
7. Extract financial statements:
   - Income Statement
   - Balance Sheet
   - Cash Flow Statement
8. Extract key metrics and ratios
9. Verify freshness - flag if filing is more than 90 days old
```

**Freshness Check:**
- Always check filing date
- Use latest available filing
- Flag if filing is more than 90 days old (quarterly) or 1 year old (annual)
- Document if using fallback source (Company IR page)

### 4. Using Browser Tools for Yahoo Finance (Prescribed Primary for Market Data)

**Purpose:** Get stock price and financial ratios (prescribed primary source)

**Process:**
```markdown
1. Navigate to Yahoo Finance: https://finance.yahoo.com/quote/[TICKER]
2. Extract current stock price (verify it's same day)
3. Navigate to "Statistics" tab
4. Extract all ratios:
   - Valuation: P/E, P/B, EV/EBITDA
   - Profitability: Margins, ROE, ROA
   - Liquidity: Current ratio, Quick ratio
   - Debt: Debt-to-equity, Interest coverage
5. Verify data freshness (should be updated daily)
6. If unavailable, fallback to Google Finance
```

**Freshness Check:**
- Stock price must be same day or previous trading day
- Ratios should be updated daily
- Flag if data is more than 1 day old
- Document if using fallback source

### 5. Using Browser Tools for Company IR Pages (Prescribed Secondary)

**Purpose:** Get official company information and financial data

**Process:**
```markdown
1. Navigate to company investor relations page
   (Pattern: https://[company].com/investors or https://investor.[company].com)
2. Find latest earnings reports
3. Extract financial statements
4. Get management commentary
5. Check for latest press releases
6. Verify dates match SEC EDGAR (if available)
```

**Freshness Check:**
- Check dates on all documents
- Prioritize most recent reports
- Verify data matches SEC EDGAR
- Use as fallback if SEC EDGAR unavailable

### 6. Data Freshness Verification (Prescribed Sources)

**Purpose:** Verify all data is current and authentic using prescribed source hierarchy

**Process:**
```markdown
For each data source:
1. Verify source is from prescribed hierarchy:
   - Financials: SEC EDGAR (primary) → Company IR (fallback)
   - Market Data: Yahoo Finance (primary) → Google Finance (fallback) → MarketWatch (tertiary)
   - News: Bloomberg (primary) → Reuters (fallback) → WSJ/FT (tertiary)
   - Analyst Ratings: Yahoo Finance Statistics (primary) → Company IR (fallback) → MarketWatch (tertiary)

2. Extract publication/filing date

3. Calculate age:
   - Stock price: Must be same day or previous trading day (Yahoo Finance)
   - Financials: Should be latest filing (SEC EDGAR, check filing date)
   - News: Prefer last 1-3 months (Bloomberg, Reuters)
   - Analyst reports: Prefer last 6 months (Yahoo Finance Statistics)

4. Check source credibility:
   - Prescribed sources = High credibility
   - Fallback sources = High-Medium credibility
   - Non-prescribed sources = Flag and justify

5. Flag stale data:
   - ⚠️ "Data from [date] - may be outdated"
   - Note which prescribed source was used
   - Document if fallback source was used

6. Prioritize freshest sources from prescribed hierarchy
```

**Verification Script:**
```python
def verify_freshness(source, date, data_type, prescribed_source):
    age = calculate_age(date)
    is_prescribed = source in prescribed_sources[data_type]
    
    if not is_prescribed:
        return "NON-PRESCRIBED - Flag and justify"
    
    if data_type == "stock_price" and age > 1:
        return "STALE - Stock price must be same day (Yahoo Finance)"
    elif data_type == "financials" and age > 90:
        return "STALE - Financial data should be latest filing (SEC EDGAR)"
    elif data_type == "news" and age > 90:
        return "STALE - News should be last 1-3 months (Bloomberg, Reuters)"
    
    return "FRESH" if is_prescribed else "VERIFY"
```

---

## Output Format Templates

### 1. Company Research Report Template

```markdown
# [Company Name] ([Ticker]) - Investment Research Report

**Research Date:** [Current Date]  
**Data Freshness:** All data verified as of [Date]  
**Report Type:** [Quick Overview / Standard Analysis / Deep Dive]

**Prescribed Sources Used:**
- Financial Statements: [SEC EDGAR / Company IR] (Filing Date: [Date])
- Market Data: [Yahoo Finance / Google Finance / MarketWatch] (Data Date: [Date])
- News Sources: [Bloomberg / Reuters / WSJ / FT] (Date Range: [Range])
- Analyst Ratings: [Yahoo Finance Statistics / Company IR / MarketWatch] (Date: [Date])

---

## Executive Summary

[2-3 paragraph overview of company, financial health, and investment recommendation]

**Investment Recommendation:** [Buy/Hold/Sell]  
**Confidence Level:** [High/Medium/Low]  
**Key Catalysts:** [List 2-3 key catalysts]  
**Key Risks:** [List 2-3 key risks]

---

## Data Freshness & Source Verification

### Prescribed Source Usage
- ✅ **SEC EDGAR:** Used for financial statements ([Filing Date])
- ✅ **Yahoo Finance:** Used for market data and ratios ([Data Date])
- ✅ **Bloomberg/Reuters:** Used for news analysis ([Date Range])
- ✅ **Yahoo Finance Statistics:** Used for analyst ratings ([Date])

### Source Credibility Summary
- **High Credibility Sources:** [Number] sources (SEC EDGAR, Yahoo Finance, Bloomberg, Reuters - all prescribed)
- **Medium Credibility Sources:** [Number] sources (if any fallback sources used)
- **Low Credibility Sources:** [Number] sources (if any, with justification)

### Freshness Status
- ✅ **Current:** [List current data sources with dates and prescribed source type]
- ⚠️ **Stale (Flagged):** [List stale data used for context, with dates]
- ❌ **Excluded:** [List excluded stale data]

### Source Dates
- **Latest Financial Filing:** [Date] ([Type]: 10-K/10-Q) - **Source: SEC EDGAR** ⭐ Prescribed Primary
- **Latest Earnings Report:** [Date] - **Source: [Company IR / SEC EDGAR]**
- **Stock Price Date:** [Date] - **Source: Yahoo Finance** ⭐ Prescribed Primary
- **News Articles Range:** [Date Range] - **Sources: Bloomberg, Reuters** ⭐ Prescribed
- **Analyst Reports Range:** [Date Range] - **Source: Yahoo Finance Statistics** ⭐ Prescribed Primary

---

## Company Overview

### Basic Information
- **Company Name:** [Name]
- **Ticker Symbol:** [Ticker]
- **Industry:** [Industry]
- **Headquarters:** [Location]
- **Founded:** [Year]
- **CEO:** [Name]

### Business Description
[Description of company's business, products, services]

### Recent News & Events
[Summary of recent news, with dates and sources]
- [News item 1] ([Date]) - **Source: Bloomberg** ⭐ Prescribed
- [News item 2] ([Date]) - **Source: Reuters** ⭐ Prescribed
- [News item 3] ([Date]) - **Source: WSJ** ⭐ Prescribed

---

## Financial Analysis

### Latest Financial Data
**Source:** [SEC Filing Type] filed [Date] ⭐ *SEC EDGAR - Prescribed Primary*

#### Income Statement Highlights
- **Revenue:** [Amount] ([Growth %] YoY)
- **Net Income:** [Amount] ([Growth %] YoY)
- **EPS:** [Amount] ([Growth %] YoY)
- **Operating Income:** [Amount]

#### Balance Sheet Highlights
- **Total Assets:** [Amount]
- **Total Liabilities:** [Amount]
- **Shareholders' Equity:** [Amount]
- **Cash & Equivalents:** [Amount]

#### Cash Flow Highlights
- **Operating Cash Flow:** [Amount]
- **Free Cash Flow:** [Amount]
- **Capital Expenditures:** [Amount]

### Financial Ratios

#### Valuation Ratios
**Source: Yahoo Finance Statistics Tab** ⭐ Prescribed Primary
- **P/E Ratio:** [Ratio] (vs. Industry Avg: [Ratio])
- **P/B Ratio:** [Ratio] (vs. Industry Avg: [Ratio])
- **EV/EBITDA:** [Ratio] (vs. Industry Avg: [Ratio])

#### Profitability Ratios
**Source: Yahoo Finance Statistics Tab** ⭐ Prescribed Primary
- **Net Margin:** [%] (vs. Industry Avg: [%])
- **Operating Margin:** [%] (vs. Industry Avg: [%])
- **ROE:** [%] (vs. Industry Avg: [%])
- **ROA:** [%] (vs. Industry Avg: [%])

#### Liquidity Ratios
**Source: Yahoo Finance Statistics Tab** ⭐ Prescribed Primary
- **Current Ratio:** [Ratio]
- **Quick Ratio:** [Ratio]

#### Debt Ratios
**Source: Yahoo Finance Statistics Tab** ⭐ Prescribed Primary
- **Debt-to-Equity:** [Ratio]
- **Interest Coverage:** [Ratio]

### Financial Trends
[Analysis of trends over last few quarters/years]
**Data Source:** SEC EDGAR filings (historical) + Yahoo Finance (ratios)

### Peer Comparison
[Comparison to competitors/peers]
**Data Source:** Yahoo Finance (for consistency across companies)

---

## Sentiment Analysis

### News Sentiment
**Analysis Period:** [Date Range] ⭐ *Verified Current*
**Sources:** Bloomberg, Reuters, WSJ (Prescribed Order)

- **Overall Sentiment:** [Positive/Negative/Neutral]
- **Sentiment Score:** [Score if calculated]
- **Key Themes:**
  - [Theme 1]: [Description]
  - [Theme 2]: [Description]
  - [Theme 3]: [Description]

### Earnings Call Analysis
**Latest Call:** [Date] ⭐ *Verified Current*
**Source:** Company IR Page (Prescribed Secondary)

- **Management Tone:** [Confident/Cautious/Concerned]
- **Key Messages:**
  - [Message 1]
  - [Message 2]
- **Forward Guidance:** [Summary]
- **Concerns Mentioned:** [List any concerns]

### Analyst Consensus
**As of:** [Date] ⭐ *Verified Current*
**Source: Yahoo Finance Statistics Tab** ⭐ Prescribed Primary

- **Buy Ratings:** [Number]
- **Hold Ratings:** [Number]
- **Sell Ratings:** [Number]
- **Average Price Target:** [Price]
- **Consensus:** [Buy/Hold/Sell]

---

## Competitive Analysis

### Competitive Position
[Analysis of company's competitive position]

### Key Competitors
- [Competitor 1]: [Brief comparison] - **Data Source: Yahoo Finance** (for consistency)
- [Competitor 2]: [Brief comparison] - **Data Source: Yahoo Finance**
- [Competitor 3]: [Brief comparison] - **Data Source: Yahoo Finance**

### Competitive Advantages
[List key competitive advantages]

### Competitive Risks
[List competitive risks]

---

## Investment Analysis

### Investment Thesis
[Detailed investment thesis - why invest or not invest]

### Key Catalysts
1. [Catalyst 1]: [Description]
2. [Catalyst 2]: [Description]
3. [Catalyst 3]: [Description]

### Key Risks
1. [Risk 1]: [Description]
2. [Risk 2]: [Description]
3. [Risk 3]: [Description]

### Valuation Assessment
[Assessment of whether company is overvalued, undervalued, or fairly valued]
**Based on:** Yahoo Finance ratios and peer comparison

### Investment Recommendation

**Recommendation:** [Buy/Hold/Sell]  
**Confidence Level:** [High/Medium/Low]  
**Target Price:** [Price if applicable]  
**Time Horizon:** [Short-term/Medium-term/Long-term]

**Rationale:**
[Detailed rationale for recommendation]

---

## Source Citations

### Financial Data Sources (Prescribed)
1. **[SEC Filing Title]** - [URL] (Filed: [Date]) ⭐ *SEC EDGAR - Prescribed Primary*
2. **[Company IR Page]** - [URL] (Last Updated: [Date]) ⭐ *Prescribed Secondary*
3. **[Yahoo Finance]** - [URL] (Data Date: [Date]) ⭐ *Prescribed Primary for Market Data*

### News Sources (Prescribed)
1. **[Article Title]** - Bloomberg - [URL] (Published: [Date]) ⭐ *Prescribed Primary*
2. **[Article Title]** - Reuters - [URL] (Published: [Date]) ⭐ *Prescribed Secondary*

### Analyst Reports (Prescribed)
1. **[Report Title]** - Yahoo Finance Statistics - [URL] (Date: [Date]) ⭐ *Prescribed Primary*

### Other Sources
[List other sources with dates, verification status, and prescribed source type]

---

## Data Freshness Notes

### Current Data Used (Prescribed Sources)
- ✅ All primary financial data from latest SEC EDGAR filing ([Date]) ⭐ Prescribed Primary
- ✅ Stock price current as of [Date] from Yahoo Finance ⭐ Prescribed Primary
- ✅ Financial ratios from Yahoo Finance Statistics tab ([Date]) ⭐ Prescribed Primary
- ✅ News analysis based on articles from Bloomberg, Reuters ([Date Range]) ⭐ Prescribed
- ✅ Sentiment analysis based on data from [Date Range]
- ✅ Analyst ratings from Yahoo Finance Statistics ([Date]) ⭐ Prescribed Primary

### Stale Data (Flagged)
- ⚠️ [Data point] from [Date] - used for historical context only
- ⚠️ [Data point] from [Date] - may be outdated

### Excluded Data
- ❌ [Data point] from [Date] - excluded due to staleness
- ❌ [Source] - excluded due to low credibility or non-prescribed source

### Fallback Sources Used
- [If any fallback sources were used, document here with justification]

---

*Report generated: [Date]*  
*All data verified for freshness and authenticity*  
*Prescribed sources used for consistency and reliability*  
*Research conducted using Company Research skill*

```

---

## Quality Checks

### Minimum Requirements

**Before completing research:**
- [ ] Latest financial filing identified from SEC EDGAR (prescribed primary)
- [ ] Stock price is current from Yahoo Finance (prescribed primary)
- [ ] All sources are from prescribed hierarchy
- [ ] All sources have publication dates
- [ ] Freshness verified for all data
- [ ] Stale data flagged if used
- [ ] Source credibility assessed
- [ ] Financial analysis completed using prescribed sources
- [ ] Sentiment analysis completed using prescribed sources
- [ ] Investment recommendation provided
- [ ] All sources cited with dates and prescribed source type

### Freshness Thresholds

**Critical (Must be Current):**
- Stock price: Same day or previous trading day (Yahoo Finance)
- Latest earnings: Most recent quarter (SEC EDGAR or Company IR)

**Very Recent (Preferred):**
- Financial statements: Latest filing (SEC EDGAR, check filing date)
- News articles: Last 1-3 months (Bloomberg, Reuters, WSJ, FT)
- Earnings calls: Most recent call (Company IR page)

**Recent (Acceptable):**
- Analyst reports: Last 6 months (Yahoo Finance Statistics)
- Industry analysis: Last 6 months

**Stale (Flag or Exclude):**
- Financial data: More than 90 days old (unless latest filing)
- News: More than 3 months old (unless historical context)
- Analyst reports: More than 6 months old

### Credibility Thresholds

**High Credibility (Prescribed Sources):**
- SEC EDGAR (sec.gov) - Prescribed Primary
- Company IR pages - Prescribed Secondary
- Yahoo Finance - Prescribed Primary for Market Data
- Bloomberg, Reuters, WSJ, Financial Times - Prescribed for News

**Medium Credibility (Fallback Sources):**
- Google Finance, MarketWatch - Prescribed Fallbacks
- Reputable financial blogs
- Industry publications

**Low Credibility (Use with Caution or Exclude):**
- Unverified blogs
- Social media (unless analyzing sentiment)
- Anonymous sources
- Non-prescribed sources (flag and justify if used)

---

## Best Practices

### Do

- ✅ **Always use prescribed sources** in order of preference
- ✅ **Always check dates** on all sources
- ✅ **Verify source credibility** - prescribed sources are high credibility
- ✅ **Use latest available data** from prescribed sources
- ✅ **Flag stale data** if used for context
- ✅ **Exclude stale data** from primary analysis
- ✅ **Cross-reference** data across multiple prescribed sources
- ✅ **Prioritize official sources** (SEC EDGAR, Company IR)
- ✅ **Note freshness status** in all reports
- ✅ **Document prescribed source** used for each data point
- ✅ **Document fallback sources** if primary unavailable
- ✅ **Update recommendations** if new data becomes available

### Don't

- ❌ **Don't use data without dates** - always verify publication date
- ❌ **Don't use stale financial data** - always use latest SEC EDGAR filing
- ❌ **Don't trust unverified sources** - stick to prescribed sources
- ❌ **Don't ignore data freshness** - it's critical for investment decisions
- ❌ **Don't use outdated stock prices** - must be current from Yahoo Finance
- ❌ **Don't skip freshness checks** - verify all data
- ❌ **Don't use low-credibility sources** without flagging
- ❌ **Don't make recommendations** based on stale data
- ❌ **Don't use non-prescribed sources** without justification

---

## Integration Notes

### With Researcher Skill ⭐ PRESCRIBED FIRST STEP

- **Workflow Hierarchy:** Company research skill MUST invoke researcher skill FIRST (prescribed primary method)
- **Researcher Skill Role:** Handles general information gathering (web search, YouTube research, browser deep dives, synthesis)
- **Company Research Skill Role:** Adds specialized analysis (financial analysis, sentiment analysis, investment evaluation)
- **Integration:** Both skills work together in prescribed hierarchy: Researcher Skill → Financial Analysis → Sentiment Analysis
- **Prescribed Sources:** Company research skill uses prescribed sources for financial data (SEC EDGAR, Yahoo Finance) and sentiment (Bloomberg, Reuters, Yahoo Finance Statistics)
- **⚠️ CRITICAL:** Do NOT skip researcher skill and go directly to financial analysis. Researcher skill provides essential context and ensures comprehensive information gathering.

### With Web Search

- Use for finding financial data, stock prices, analyst reports
- **Prioritize prescribed sources** in search terms (Bloomberg, Reuters, Yahoo Finance)
- Always include current year in search terms
- Verify dates in search results
- Prioritize credible sources from prescribed hierarchy

### With Browser Tools

- Essential for SEC EDGAR filings (prescribed primary)
- Use for Yahoo Finance (prescribed primary for market data)
- Use for company IR pages (prescribed secondary)
- Extract financial statements
- Verify all dates
- Document which prescribed source was used

### With Financial Data Sources (Prescribed)

- **SEC EDGAR:** Official source for financial filings (prescribed primary)
- **Company IR Pages:** Official company information (prescribed secondary)
- **Yahoo Finance:** Market data and ratios (prescribed primary)
- **Bloomberg, Reuters, WSJ, FT:** Financial news (prescribed order)
- **Yahoo Finance Statistics:** Analyst ratings (prescribed primary)

---

## Example Research Scenarios

### Scenario 1: "Research Apple Inc. for Investment"

**Process (Prescribed Hierarchy):**

**Step 1: Query Analysis**
- Identify: Apple Inc. (AAPL)
- Goal: Investment research
- Plan: Follow prescribed workflow hierarchy

**Step 2: Phase 1 - Researcher Skill (REQUIRED FIRST) ⭐**
- **Action:** Explicitly invoke Researcher Skill
- **Query:** "Research Apple Inc. (AAPL) - company overview, recent news, industry context, management team, products/services, recent developments, competitive position"
- **Researcher Skill Output:**
  - Company overview and history
  - Recent news and events (with dates)
  - Industry context
  - Management insights
  - Product/service information
  - Competitive position

**Step 3: Phase 2 - Financial Data (Prescribed Sources) ⭐**
- **SEC EDGAR (Prescribed Primary):**
  - Navigate to SEC EDGAR
  - Extract latest 10-K/10-Q filing
  - Verify filing date (should be most recent)
- **Yahoo Finance (Prescribed Primary):**
  - Navigate to Yahoo Finance quote page
  - Get stock price (verify same day)
  - Navigate to Statistics tab for ratios
  - Verify freshness

**Step 4: Phase 3 - Sentiment Analysis (Prescribed Sources) ⭐**
- **Bloomberg/Reuters (Prescribed Order):**
  - Search for recent news (last 1-3 months)
  - Analyze sentiment
- **Yahoo Finance Statistics (Prescribed Primary):**
  - Get analyst ratings
  - Verify dates (last 6 months preferred)

**Step 5: Financial Analysis**
- Calculate ratios (or use from Yahoo Finance Statistics)
- Compare to peers (using Yahoo Finance for consistency)
- Analyze trends

**Step 6: Investment Analysis**
- Synthesize researcher skill output + financial analysis + sentiment
- Develop investment thesis
- Make recommendation

**Step 7: Documentation**
- Create investment research report
- Cite all sources with prescribed source hierarchy
- Document workflow: Researcher Skill → Financial → Sentiment

**Output:** Comprehensive investment research report with Buy/Hold/Sell recommendation, all sources from prescribed hierarchy, workflow documented

### Scenario 2: "Compare Tesla vs Rivian"

**Process:**
1. **Query Analysis:** Comparative analysis of two companies
2. **Researcher Skill:** Gather information on both companies
3. **Financial Data (Prescribed):**
   - **SEC EDGAR:** Extract financials for both companies
   - **Yahoo Finance:** Get market data for both (for consistency)
   - **Verify freshness:** Both companies' data is current
4. **Comparative Analysis:** Compare financials, sentiment, competitive position
5. **Documentation:** Create comparison report with prescribed sources

**Output:** Comparative analysis report using prescribed sources for consistency

### Scenario 3: "Find the top 10 AI companies by market cap"

**Process (Prescribed Hierarchy):**

**Step 1: Query Analysis**
- Identify: Category = AI companies, Ranking metric = Market cap, Count = Top 10
- Plan: Follow prescribed workflow for company discovery and ranking

**Step 2: Phase 1 - Category Discovery (Researcher Skill) ⭐ REQUIRED FIRST**
- **Action:** Explicitly invoke Researcher Skill
- **Query:** "Research AI companies - identify major players, market leaders, key companies in artificial intelligence, industry landscape, public companies"
- **Researcher Skill Output:**
  - List of AI companies (NVIDIA, Microsoft, Alphabet, Meta, etc.)
  - Company names and ticker symbols
  - Industry context
  - Market structure

**Step 3: Phase 2 - Ranking Criteria**
- **Metric:** Market capitalization (specified in query)
- **Count:** Top 10 (specified in query)

**Step 4: Phase 3 - Data Collection (Prescribed Sources)**
- **For Each Identified Company:**
  - **Yahoo Finance (Prescribed Primary):**
    - Navigate to each company's quote page
    - Extract market cap (verify same day)
    - Extract additional metrics (revenue, P/E ratio) for context
    - Verify freshness

**Step 5: Phase 4 - Ranking**
- Sort all companies by market cap (descending)
- Select top 10
- Include key metrics for each (from Yahoo Finance)

**Step 6: Phase 5 - Validation**
- Cross-reference with industry reports (if available)
- Verify no major companies missed
- Check data freshness (all from Yahoo Finance, same day)
- Note limitations (private companies excluded)

**Step 7: Documentation**
- Create ranked list report
- Include ranking criteria and methodology
- Cite all sources (Yahoo Finance for all market data)
- Note data freshness

**Output:** Ranked list of top 10 AI companies by market cap, with key metrics, all data from Yahoo Finance (prescribed primary), freshness verified

---

## Troubleshooting

### Data Not Found

**Solution:**
- Try alternative search terms
- Check company name variations
- Search by ticker symbol
- Use SEC EDGAR company search (prescribed primary)
- Try fallback sources in prescribed order

### Prescribed Source Unavailable

**Solution:**
- Use next source in prescribed hierarchy (fallback)
- Document which fallback source was used
- Note why primary source was unavailable
- Verify fallback source data matches primary if possible

### Stale Data Only Available

**Solution:**
- Flag stale data clearly
- Note limitations in report
- Use for historical context only
- Recommend updating when new data available
- Document which prescribed source had stale data

### Conflicting Data

**Solution:**
- Prioritize official sources (SEC EDGAR, Company IR)
- Cross-reference multiple prescribed sources
- Note discrepancies in report
- Use most recent data from prescribed sources

---

*Company Research Skill Version: 1.0*  
*Last Updated: December 28, 2025*  
*Focus: Current data, verified sources, prescribed source hierarchy, comprehensive analysis*

