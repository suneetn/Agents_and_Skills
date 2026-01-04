---
name: researcher
description: Conduct comprehensive multi-source research on any topic (travel, food, technology, science, finance, health, business, education, arts, etc.) using YouTube, web search, and browser tools. Synthesize information from videos, articles, and web sources into organized research documents.
---

# Researcher Skill

This skill enables Claude to conduct thorough, multi-source research by orchestrating YouTube searches, web searches, and browser-based deep dives. It synthesizes information from multiple sources into well-organized research documents.

**Important:** YouTube research is a **standard part** of the workflow, not optional. Always search YouTube in parallel with web search to ensure comprehensive coverage and multiple perspectives.

## When to Use This Skill

Use this skill when:
- User asks for research on **any topic** ("Research X", "Find information about Y")
- User needs comprehensive information gathering from multiple sources
- User wants multi-source synthesis and comparison ("Compare X vs Y", "What are the best options for Z")
- User needs organized research documents with citations
- User requests step-by-step guides based on multiple sources ("How to do X")
- User wants to understand a topic from different perspectives
- User needs credible, well-sourced information on **any subject** (travel, food, technology, science, finance, health, business, education, arts, etc.)
- User asks for travel planning, product research, learning resources, or any domain-specific research

**Examples:**
- "Research how to do Jeevan Praman for India"
- "Find the best practices for X"
- "Research what to do in Bangkok for 3 days"
- "Compare X vs Y and create a comparison document"
- "Research topic X for beginners"

## Domain Versatility

The Researcher skill is **domain-agnostic** and can conduct research across **any topic or field**. It works equally well for:

### Travel & Tourism
- **Destinations:** "Research best places to visit in [country]"
- **Itineraries:** "Create a 5-day itinerary for [city]"
- **Travel Tips:** "Research travel tips for [destination]"
- **Accommodations:** "Compare hotels in [location]"
- **Activities:** "Research things to do in [place]"

**Example Sources:**
- Travel blogs, official tourism websites, YouTube travel vlogs, review sites

### Food & Cuisine
- **Recipes:** "Research authentic [cuisine] recipes"
- **Restaurants:** "Find best restaurants in [city]"
- **Cooking Techniques:** "Research how to [cooking method]"
- **Food Culture:** "Research [cuisine] food traditions"
- **Dietary Information:** "Research [diet] meal plans"

**Example Sources:**
- Food blogs, cooking YouTube channels, restaurant review sites, culinary websites

### Technology
- **Products:** "Compare [product A] vs [product B]"
- **Tutorials:** "Research how to use [technology]"
- **Best Practices:** "Research best practices for [tech topic]"
- **Trends:** "Research latest trends in [technology field]"
- **Reviews:** "Research reviews of [product/service]"

**Example Sources:**
- Tech blogs, official documentation, YouTube tech channels, review sites, forums

### Science & Research
- **Scientific Concepts:** "Research [scientific topic]"
- **Studies:** "Research studies on [topic]"
- **Explanations:** "Research how [scientific phenomenon] works"
- **Latest Discoveries:** "Research recent discoveries in [field]"
- **Educational Content:** "Research [topic] for beginners"

**Example Sources:**
- Academic papers, science websites, educational YouTube channels, Wikipedia, research institutions

### Finance & Economics
- **Investment:** "Research investment options for [goal]"
- **Financial Planning:** "Research financial planning strategies"
- **Market Analysis:** "Research [market] trends"
- **Products:** "Compare [financial product A] vs [product B]"
- **Regulations:** "Research [financial] regulations"

**Example Sources:**
- Financial news sites, official regulatory websites, financial YouTube channels, comparison sites

### Health & Wellness
- **Health Conditions:** "Research [condition] treatment options"
- **Fitness:** "Research [fitness] programs"
- **Nutrition:** "Research [nutrition] information"
- **Wellness:** "Research [wellness] practices"
- **Medical Information:** "Research [medical topic]"

**Example Sources:**
- Medical websites, health blogs, fitness YouTube channels, official health organizations

### Business & Entrepreneurship
- **Business Models:** "Research [business model] examples"
- **Marketing:** "Research [marketing] strategies"
- **Startups:** "Research [startup] best practices"
- **Industry Analysis:** "Research [industry] trends"
- **Case Studies:** "Research [business] case studies"

**Example Sources:**
- Business news, industry publications, business YouTube channels, case study databases

### Education & Learning
- **Learning Resources:** "Research learning resources for [topic]"
- **Courses:** "Compare [course A] vs [course B]"
- **Study Methods:** "Research effective study methods"
- **Subject Matter:** "Research [subject] for beginners"
- **Certifications:** "Research [certification] requirements"

**Example Sources:**
- Educational websites, online course platforms, educational YouTube channels, official certification sites

### Arts & Culture
- **Art History:** "Research [art movement] history"
- **Cultural Practices:** "Research [culture] traditions"
- **Artistic Techniques:** "Research [art technique] methods"
- **Cultural Events:** "Research [cultural event] information"
- **Artists:** "Research [artist] biography"

**Example Sources:**
- Museum websites, cultural blogs, art YouTube channels, cultural organizations

### And Many More...
The skill adapts to **any research query** regardless of domain. The same workflow applies:
1. Search across multiple sources
2. Identify credible information
3. Synthesize findings
4. Create organized documents

**Key Point:** The Researcher skill doesn't need domain-specific knowledge - it leverages the power of web search, YouTube, and browser tools to find and synthesize information from any field.

## Core Capabilities

### 1. Multi-Source Research

**Capability:** Search and gather information from multiple sources simultaneously

**Sources:**
- YouTube videos (via YouTube skill)
- Web search results (via `web_search` tool)
- Full articles (via browser tools)
- Wikipedia articles
- News articles
- Official documentation
- Reddit discussions (when relevant)

**Process:**
1. Break down research query into sub-topics
2. Search each source type for relevant information
3. Collect and organize results by source type
4. Identify overlaps and unique insights
5. Cross-reference information for accuracy

**Output:**
- Comprehensive information from multiple sources
- Source attribution and citations
- Cross-referenced facts and claims

---

### 2. Video Research (Leveraging YouTube Skill)

**Capability:** Find, analyze, and extract insights from YouTube videos

**Process:**
1. **Always search YouTube** - Video research is standard for comprehensive research, not optional
2. Use YouTube skill to search for relevant videos:
   - Navigate to YouTube using browser tools: `browser_navigate(url="https://www.youtube.com/results?search_query=YOUR_QUERY")`
   - Use `browser_snapshot()` to capture search results
   - Extract video URLs, titles, view counts, and channel names from search results
   - **Preferred Method:** Use Python script (`extract_video.py`) for transcript extraction
   - **Alternative:** Use browser tools if Python script unavailable
3. Identify most promising videos based on:
   - View count and engagement (higher = more popular, but consider recency)
   - Channel credibility (official channels, verified creators, reputable sources like CNBC, Bloomberg)
   - Recency (recent videos may have updated information)
   - Relevance to query (title and description match)
4. Extract transcripts from top videos (3-5 videos recommended):
   - **Preferred:** Use Python script: `python3 ~/personal/youtube/extract_video.py VIDEO_URL`
   - **Fallback:** Use browser tools if Python script unavailable
   - Transcripts are saved to `~/personal/youtube/transcripts/`
5. Analyze transcripts for key insights
6. Compare perspectives across multiple videos
7. Identify common themes and unique points
8. Cross-reference video insights with web article findings

**When to Use:**
- ✅ **Always** - YouTube research is standard for comprehensive research
- ✅ Provides expert analysis and recent insights
- ✅ Offers video explanations and tutorials
- ✅ Complements written articles with different perspectives

**Integration with YouTube Skill:**
- The YouTube skill handles video search and transcript extraction
- Researcher skill orchestrates the process and synthesizes results
- **Standard Workflow:** Always search YouTube in parallel with web search
- Use browser tools to navigate YouTube and extract video information
- Use Python scripts (preferred) for API-based transcript extraction
- Synthesize video insights with web article findings for comprehensive research

**Output:**
- List of most relevant videos with metadata
- Key insights extracted from video transcripts
- Comparison of different perspectives
- Video recommendations ranked by relevance

**Example:**
```markdown
1. Search YouTube for "how to do X"
2. Identify top 5 videos (by views, credibility, recency)
3. Extract transcripts from each video
4. Analyze and synthesize key steps
5. Create comprehensive guide combining all insights
```

---

### 3. Web Research (Two-Phase Approach)

**Capability:** Search the web and extract relevant information using a two-phase approach

#### Phase 1: Discovery (web_search tool)

**Purpose:** Fast source discovery and initial information gathering

**Process:**
1. Perform targeted web searches using `web_search` tool
2. Analyze search result snippets and summaries
3. Extract key information from search results
4. Evaluate source credibility based on URLs and snippets:
   - Official government/educational sites (.gov, .edu)
   - Established news sources
   - Reputable organizations
   - Recent publication dates
5. Cross-reference information across multiple search results
6. Identify authoritative sources
7. Select 3-5 most promising sources for deep dive

**Why web_search first:**
- ✅ Fast and efficient
- ✅ Provides summaries from multiple sources
- ✅ Good for synthesis and overview research
- ✅ Returns URLs for citation
- ✅ Helps identify most relevant sources

**Output:**
- Summarized information from search snippets
- List of promising sources with URLs
- Initial credibility assessment
- Key facts and statistics

#### Phase 2: Deep Dive (Browser Tools)

**Purpose:** Read full articles for comprehensive understanding

**When to use:** For promising topics requiring full article content

**Process:**
1. Identify promising URLs from `web_search` results (top 3-5 sources)
2. Use `browser_navigate` to open each URL
3. Use `browser_snapshot` to capture page structure
4. Use `browser_evaluate` to extract full article content:
   ```javascript
   // Extract main article content
   browser_evaluate({
     function: () => {
       // Try common article selectors
       const article = document.querySelector('article') || 
                      document.querySelector('.article-content') ||
                      document.querySelector('main') ||
                      document.querySelector('[role="article"]');
       return article ? article.innerText : document.body.innerText;
     }
   });
   ```
5. Extract detailed information not available in snippets
6. Verify complex claims from original sources
7. Capture nuanced perspectives and full context

**When to use browser tools:**
- ✅ Topic identified as "promising" for deep research
- ✅ Need to read entire articles for comprehensive understanding
- ✅ Extracting detailed information not available in snippets
- ✅ Verifying complex claims from original sources
- ✅ Accessing content that requires page interaction (e.g., clicking "read more")

**Output:**
- Full article content from top sources
- Detailed information and context
- Verified claims and facts
- Nuanced perspectives

**Combined Output:**
- Information from snippets (Phase 1) + full articles (Phase 2)
- Comprehensive understanding of the topic
- Well-sourced research document

---

### 4. Information Synthesis

**Capability:** Combine information from multiple sources into coherent insights

**Process:**
1. **Identify Common Themes:**
   - Group similar information from different sources
   - Identify recurring points and consensus
   - Note patterns across sources

2. **Note Conflicting Information:**
   - Identify disagreements between sources
   - Note different perspectives
   - Highlight areas of uncertainty

3. **Highlight Unique Insights:**
   - Identify information unique to specific sources
   - Note expert opinions or specialized knowledge
   - Capture innovative or novel approaches

4. **Create Structured Summary:**
   - Organize by topic/subtopic
   - Prioritize most credible information
   - Include source attribution

5. **Organize by Themes:**
   - Group related information together
   - Create logical flow
   - Make information easy to navigate

**Output:**
- Comprehensive summary document
- Key findings organized by topic
- Source attribution for all claims
- Confidence levels for different information
- Comparison of perspectives where relevant

---

### 5. Research Document Creation

**Capability:** Generate well-organized research documents

**Document Structure:**
- **Executive Summary:** High-level overview of findings
- **Research Methodology:** Sources consulted and approach used
- **Findings by Topic:** Detailed information organized by subtopic
- **Source Citations:** All sources with URLs and titles
- **Recommendations:** Actionable insights (when applicable)
- **Appendix:** Detailed information, raw data, or additional context

**Formats:**
- Markdown documents (primary format)
- Structured summaries
- Comparison tables
- Timeline/chronology (when relevant)
- Step-by-step guides

**File Organization:**
- Save to: `research/[topic]/` (relative to workspace root) or user-specified location
- **Important:** Use relative paths from workspace root (e.g., `research/[topic]/`) or absolute paths (e.g., `/Users/[username]/personal/research/[topic]/`)
- **Note:** The `~` tilde expansion does NOT work with the write tool - use relative paths or absolute paths instead
- Filename: `[topic]-research.md` or user-specified
- Include date and version if needed

**Output Location Field:**
- Research documents should include an `**Output Location:**` field in the header
- Use absolute path format: `/Users/[username]/personal/research/[topic]/[topic]-research.md`
- Do NOT use tilde notation (`~/personal/...`) in the Output Location field
- This field helps track where research documents are saved

**Templates:** See "Output Format Templates" section below

---

### 6. Credibility Assessment

**Capability:** Evaluate and rank sources by credibility

**Factors:**
- **Source Type:**
  - Academic sources (.edu, research papers) - Highest credibility
  - Official government sites (.gov) - High credibility
  - Established news sources - High credibility
  - Reputable organizations - Medium-high credibility
  - Personal blogs/social media - Lower credibility

- **Author Credentials:**
  - Expert in the field
  - Verified professional
  - Official representative

- **Publication Date:**
  - Recent information preferred
  - Historical context when relevant
  - Outdated information flagged

- **Cross-Referencing:**
  - Information verified across multiple sources
  - Consensus vs. outlier claims
  - Conflicting information noted

- **Bias Detection:**
  - Identify potential biases
  - Note commercial interests
  - Consider source motivations

**Output:**
- Credibility scores for sources
- Flagged information requiring verification
- Recommended authoritative sources
- Confidence levels for different claims

---

## Research Workflow

### Standard 6-Step Research Process

#### Step 1: Query Analysis
**Purpose:** Understand research question and plan approach

**Tasks:**
- Understand what user wants to know
- Break down into sub-topics if complex
- Identify required source types (videos, articles, official docs)
- Determine research depth needed (quick, standard, deep)
- Plan search strategy

**Example:**
```
Query: "Research how to do Jeevan Praman for India"
Sub-topics:
- What is Jeevan Praman?
- Step-by-step process
- Required documents
- Common issues/troubleshooting
- Official sources
```

#### Step 2: Source Identification
**Purpose:** Determine which sources to search

**Tasks:**
- **Always include:** YouTube videos AND web search (both are standard)
- Plan search queries for each source type
- Identify which sources will provide complementary information

**Standard Source Types (Always Use):**
- ✅ **YouTube videos** - For expert analysis, tutorials, recent insights, video explanations
- ✅ **Web search** - For articles, official docs, written guides, news
- ✅ **Browser tools** - For deep dives into promising sources

**Decision Tree:**
```
For ANY research query:
  → ALWAYS search YouTube in parallel with web search
  → Extract transcripts from top 3-5 YouTube videos
  → Search web for articles and official sources
  → Read top 3-5 web articles in full
  → Synthesize information from both sources

If query is "how to do X":
  → Search YouTube for tutorial videos (standard)
  → Search web for official guides (standard)
  → Extract transcripts from top YouTube videos
  → Read top web sources in full

If query is "compare X vs Y":
  → Search YouTube for video comparisons (standard)
  → Search web for written comparisons (standard)
  → Extract transcripts and read articles
  → Synthesize both perspectives

If query is "research topic X":
  → Search YouTube for educational content (standard)
  → Search web for articles and overviews (standard)
  → Extract transcripts and read articles
  → Combine insights from both sources
```

**Key Principle:** YouTube and web search are **complementary**, not alternatives. Always use both for comprehensive research.

#### Step 3: Information Gathering
**Purpose:** Execute searches and collect information

**Tasks:**
- **Phase 1 - Parallel Discovery (Standard):**
  - **Web Search:** Use `web_search` to find articles and written sources
  - **YouTube Search:** Use browser tools to search YouTube for relevant videos
  - Analyze snippets and video metadata
  - Identify promising sources from both (top 3-5 each)
  
- **Phase 2 - Deep Dive:**
  - **Web Articles:** Use browser tools to read full articles from promising web sources
  - **Video Transcripts:** Extract transcripts from top YouTube videos using Python script (preferred) or browser tools
  - Extract detailed information from both sources
  - Verify claims from original sources

- **Collect Metadata:**
  - Save URLs, titles, publication dates, view counts
  - Note source credibility (channel reputation, publication source)
  - Track information by source type (video vs. article)

**Tools Used:**
- `web_search` - For web article discovery (standard)
- `browser_navigate`, `browser_snapshot`, `browser_evaluate` - For web article deep dives
- YouTube skill (browser tools) - For YouTube video search (standard)
- Python script (`extract_video.py`) - For video transcript extraction (preferred method)
- File operations - For saving intermediate results if needed

**Important:** YouTube research is **not optional** - it's a standard part of comprehensive research. Always search YouTube in parallel with web search to get multiple perspectives and recent insights.

#### Step 4: Analysis
**Purpose:** Identify key insights and assess information

**Tasks:**
- Identify key insights from each source
- Compare perspectives across sources
- Assess credibility of information
- Note gaps in information
- Identify conflicting information
- Highlight consensus vs. disagreements

**Analysis Checklist:**
- [ ] Key points extracted from each source
- [ ] Common themes identified
- [ ] Unique insights noted
- [ ] Conflicts identified and explained
- [ ] Credibility assessed
- [ ] Gaps identified

#### Step 5: Synthesis
**Purpose:** Combine information logically

**Tasks:**
- Combine information from all sources
- Resolve conflicts where possible
- Highlight consensus vs. disagreements
- Organize by themes/topics
- Create logical flow
- Prioritize most credible information

**Synthesis Process:**
1. Group similar information together
2. Create topic-based sections
3. Include multiple perspectives where relevant
4. Note areas of consensus
5. Highlight unique insights
6. Add source attribution throughout

#### Step 6: Documentation
**Purpose:** Create final research document

**Tasks:**
- Create structured research document
- Use appropriate template (see "Output Format Templates")
- Include source citations
- Add recommendations if applicable
- Format for easy consumption
- Save to specified location

**Document Checklist:**
- [ ] Executive summary included
- [ ] Findings organized by topic
- [ ] All sources cited with URLs
- [ ] Recommendations included (if applicable)
- [ ] Proper formatting and structure
- [ ] Saved to correct location

---

## Tool Usage Instructions

### 1. Using web_search Tool

**Purpose:** Fast source discovery and initial information gathering

**Usage:**
```python
# Basic search
web_search(search_term="how to do Jeevan Praman India")

# Multiple searches for comprehensive coverage
web_search(search_term="Jeevan Praman official guide")
web_search(search_term="Jeevan Praman step by step")
web_search(search_term="Jeevan Praman requirements documents")
```

**Best Practices:**
- Use specific, targeted search terms
- Perform multiple searches for comprehensive coverage
- Analyze snippets to identify promising sources
- Extract URLs and titles from results
- Note publication dates and source credibility

**When to Use:**
- Always start with `web_search` for Phase 1 discovery
- Use for quick overview research
- Use to identify sources for deep dive

**Limitations:**
- Only provides snippets, not full articles
- May miss detailed information
- Need browser tools for full content

---

### 2. Using Browser Tools for Deep Research

**Purpose:** Read full articles for comprehensive understanding

**Tools:**
- `browser_navigate` - Navigate to URL
- `browser_snapshot` - Capture page structure
- `browser_evaluate` - Extract content via JavaScript
- `browser_wait_for` - Wait for page to load

**Usage Pattern:**
```markdown
1. Navigate to promising URL:
   browser_navigate(url="https://example.com/article")

2. Wait for page to load:
   browser_wait_for(text="article content")

3. Capture page structure:
   browser_snapshot()

4. Extract article content:
   browser_evaluate({
     function: () => {
       const article = document.querySelector('article') || 
                       document.querySelector('.content') ||
                       document.querySelector('main');
       return article ? article.innerText : document.body.innerText;
     }
   })
```

**Best Practices:**
- Only read top 3-5 most promising sources
- Extract main content, skip navigation/ads
- Save URLs for citation
- Handle errors gracefully (fallback to snippets)

**When to Use:**
- After `web_search` identifies promising sources
- When detailed information is needed
- When verifying claims from original sources
- When snippets don't provide enough context

---

### 3. Using YouTube Skill

**Purpose:** Find and extract information from YouTube videos

**Integration:**
- Researcher skill orchestrates YouTube research
- **Preferred Method:** Uses Python script (`extract_video.py`) for transcript extraction (faster, more reliable)
- **Alternative:** Uses browser tools to search YouTube and extract information
- Extracts video information and transcripts
- Synthesizes video content with other sources

**Python Script Usage:**
```bash
# Extract transcript from a video (no API key needed for transcripts)
python3 ~/personal/youtube/extract_video.py VIDEO_URL

# Extract with full metadata (requires YouTube Data API key)
python3 ~/personal/youtube/extract_video.py VIDEO_URL API_KEY
```

The script automatically:
- Extracts video ID from URL
- Gets transcript via `youtube-transcript-api` library
- Gets metadata via YouTube Data API v3 (if API key provided)
- Saves files to organized directories (`~/personal/youtube/`)

**Process:**
```markdown
1. Navigate to YouTube:
   browser_navigate(url="https://www.youtube.com")

2. Search for videos:
   browser_type(element="Search box", text="research topic")
   browser_click(element="Search button")

3. Extract video information:
   - Video titles, URLs, channels
   - View counts, upload dates
   - Descriptions

4. Identify top videos (3-5):
   - High views + credibility
   - Recent uploads
   - Relevant content

5. Extract transcripts:
   - Use YouTube skill methods
   - Or use Python script if available

6. Analyze and synthesize:
   - Extract key insights
   - Compare with other sources
   - Include in research document
```

**Best Practices:**
- Prioritize official channels and verified creators
- Look for recent videos (updated information)
- Extract transcripts for analysis
- Compare multiple video perspectives
- Include video URLs in citations

**When to Use:**
- ✅ **Always** - YouTube research is standard for comprehensive research
- ✅ Provides expert analysis, recent insights, and video explanations
- ✅ Complements written articles with different perspectives
- ✅ Especially valuable for tutorials, step-by-step guides, and expert analysis
- ✅ Recent videos often contain updated information not yet in articles
- ✅ Video content provides visual explanations and demonstrations

**Important:** Don't skip YouTube research - it's a standard part of the workflow, not optional. Always search YouTube in parallel with web search to ensure comprehensive coverage.

---

### 4. Using write Tool for Documents

**Purpose:** Create and save research documents

**Usage:**
```python
# Create research document (use relative path from workspace root)
write(
    file_path="research/jeevan-praman/research-guide.md",
    contents="# Research Document\n\n..."
)

# OR use absolute path (if workspace root is /Users/[username]/personal)
write(
    file_path="/Users/[username]/personal/research/jeevan-praman/research-guide.md",
    contents="# Research Document\n\n..."
)
```

**Important Path Notes:**
- The `~` tilde expansion does NOT work with the write tool
- Use relative paths from workspace root (recommended): `research/[topic]/filename.md`
- Or use absolute paths: `/Users/[username]/personal/research/[topic]/filename.md`
- Workspace root is typically `/Users/[username]/personal` for this user

**Best Practices:**
- Use descriptive filenames
- Organize by topic in directories
- Include date if relevant
- Use markdown formatting
- Include source citations

**File Organization:**
```
research/  (relative to workspace root, which is typically /Users/[username]/personal)
  └── [topic]/
      ├── research-summary.md
      ├── sources.md (optional)
      └── [other documents]
```

**Path Format:**
- ✅ Use: `research/[topic]/filename.md` (relative path)
- ✅ Use: `/Users/[username]/personal/research/[topic]/filename.md` (absolute path)
- ❌ Avoid: `~/personal/research/[topic]/filename.md` (tilde expansion doesn't work)

---

## Output Format Templates

### 1. Research Summary Template

**Use Case:** Quick overview of research findings

```markdown
# [Topic] - Research Summary

**Research Date:** [Date]  
**Sources Consulted:** [Number] sources (videos, articles, official docs)

---

## Executive Summary

[2-3 paragraph high-level overview of findings]

## Key Findings

### [Topic 1]
- [Finding 1]
- [Finding 2]
- [Finding 3]

### [Topic 2]
- [Finding 1]
- [Finding 2]

## Recommendations

- [Recommendation 1]
- [Recommendation 2]

## Sources

1. [Source Title] - [URL]
2. [Source Title] - [URL]
3. [Video Title] - [YouTube URL]

---

*Research conducted using multi-source analysis including web search, video research, and article analysis.*
```

---

### 2. Comprehensive Report Template

**Use Case:** Detailed research document with full findings

```markdown
# [Topic] - Comprehensive Research Report

**Research Query:** [Research question or topic]  
**Date:** [Date]  
**Output Location:** /Users/[username]/personal/research/[topic]/[topic]-research.md

---

## Executive Summary

[Comprehensive overview of research findings, methodology, and key conclusions]

## Research Methodology

### Sources Consulted
- **Web Search:** [Number] articles and documents
- **YouTube Videos:** [Number] videos analyzed
- **Official Documentation:** [Number] official sources
- **Other Sources:** [List other sources]

### Research Approach
1. [Step 1 description]
2. [Step 2 description]
3. [Step 3 description]

---

## Findings by Topic

### [Topic 1]

**Overview:**
[Introduction to topic]

**Key Information:**
- [Information point 1] ([Source])
- [Information point 2] ([Source])
- [Information point 3] ([Source])

**Different Perspectives:**
- **Perspective A:** [Description] ([Source])
- **Perspective B:** [Description] ([Source])

**Consensus:**
[What sources agree on]

**Areas of Disagreement:**
[Where sources differ]

### [Topic 2]
[Same structure as Topic 1]

---

## Detailed Analysis

### [Sub-topic 1]
[Detailed information with citations]

### [Sub-topic 2]
[Detailed information with citations]

---

## Comparison and Synthesis

### Common Themes
- [Theme 1]: [Description]
- [Theme 2]: [Description]

### Unique Insights
- [Source] provides unique insight: [Description]
- [Source] offers different perspective: [Description]

### Credibility Assessment
- **High Credibility Sources:** [List]
- **Medium Credibility Sources:** [List]
- **Areas Requiring Verification:** [List]

---

## Recommendations

### Based on Research Findings
1. [Recommendation 1 with rationale]
2. [Recommendation 2 with rationale]
3. [Recommendation 3 with rationale]

### Next Steps
- [Action item 1]
- [Action item 2]

---

## Source Citations

### Web Sources
1. **[Article Title]** - [URL]
   - Author: [Name]
   - Publication Date: [Date]
   - Credibility: [Assessment]

2. **[Article Title]** - [URL]
   - [Metadata]

### Video Sources
1. **[Video Title]** - [YouTube URL]
   - Channel: [Channel Name]
   - Views: [Count]
   - Upload Date: [Date]
   - Transcript: [Available/Not Available]

### Official Documentation
1. **[Document Title]** - [URL]
   - Organization: [Name]
   - Date: [Date]

---

## Appendix

### Additional Resources
- [Resource 1]
- [Resource 2]

### Research Notes
[Any additional notes, limitations, or considerations]

---

*Report generated: [Date]*  
*Research conducted using Researcher skill*
```

---

### 3. Quick Reference Guide Template

**Use Case:** Condensed, actionable information

```markdown
# [Topic] - Quick Reference Guide

**Last Updated:** [Date]

---

## Quick Overview

[1-2 sentence summary]

## Essential Information

### [Key Point 1]
[Brief description]

### [Key Point 2]
[Brief description]

## Step-by-Step Process

### Step 1: [Action]
[Description]

### Step 2: [Action]
[Description]

### Step 3: [Action]
[Description]

## Quick Tips

- [Tip 1]
- [Tip 2]
- [Tip 3]

## Common Issues & Solutions

**Issue:** [Problem]  
**Solution:** [Answer]

**Issue:** [Problem]  
**Solution:** [Answer]

## Essential Resources

- [Resource 1] - [URL]
- [Resource 2] - [URL]
- [Resource 3] - [URL]

---

*For detailed research, see comprehensive report.*
```

---

### 4. Comparison Document Template

**Use Case:** Comparing options, products, or approaches

```markdown
# [Topic A] vs [Topic B] - Comparison

**Research Date:** [Date]  
**Sources:** [Number] sources consulted

---

## Executive Summary

[Brief comparison overview]

## Comparison Matrix

| Feature | [Option A] | [Option B] | [Option C] |
|---------|------------|------------|------------|
| [Feature 1] | [Value] | [Value] | [Value] |
| [Feature 2] | [Value] | [Value] | [Value] |
| [Feature 3] | [Value] | [Value] | [Value] |

## Detailed Comparison

### [Option A]

**Pros:**
- [Advantage 1]
- [Advantage 2]

**Cons:**
- [Disadvantage 1]
- [Disadvantage 2]

**Best For:**
[Use cases]

**Sources:**
- [Source 1]
- [Source 2]

### [Option B]

[Same structure as Option A]

---

## Key Differences

1. **Difference 1:** [Description]
2. **Difference 2:** [Description]
3. **Difference 3:** [Description]

## Recommendations

**Choose [Option A] if:**
- [Condition 1]
- [Condition 2]

**Choose [Option B] if:**
- [Condition 1]
- [Condition 2]

## Sources

[Full source citations]

---

*Comparison based on multi-source research*
```

---

## Examples and Use Cases

### Example 1: "How-to" Research

**Query:** "Research how to do Jeevan Praman for India"

**Process:**
1. **Query Analysis:**
   - Sub-topics: What is it, step-by-step process, requirements, troubleshooting
   - Sources: Official government sites, YouTube tutorials, news articles

2. **Source Identification:**
   - YouTube: Search for "Jeevan Praman tutorial"
   - Web: Search for "Jeevan Praman official guide"
   - Browser: Read full articles from government sites

3. **Information Gathering:**
   - Phase 1: `web_search` finds 10+ sources
   - Phase 2: Read top 3 official government articles
   - YouTube: Extract transcripts from top 3 tutorial videos

4. **Analysis:**
   - Common steps identified across sources
   - Official process verified
   - Common issues noted

5. **Synthesis:**
   - Create step-by-step guide
   - Include official requirements
   - Add troubleshooting section

6. **Documentation:**
   - Create comprehensive guide
   - Include all sources
   - Save to `research/jeevan-praman/` (relative to workspace root)

**Output:** Step-by-step guide with official requirements and video references

---

### Example 2: Travel Planning Research

**Query:** "Research what to do in Bangkok for 3 days"

**Process:**
1. **Query Analysis:**
   - Sub-topics: Attractions, food, transportation, itinerary
   - Sources: Travel blogs, YouTube travel guides, official tourism sites

2. **Source Identification:**
   - YouTube: Search for "Bangkok 3 day itinerary"
   - Web: Search for "Bangkok top attractions"
   - Browser: Read full travel guides

3. **Information Gathering:**
   - Phase 1: `web_search` finds travel guides
   - Phase 2: Read top 3 comprehensive travel articles
   - YouTube: Extract recommendations from top 5 travel videos

4. **Analysis:**
   - Most recommended attractions identified
   - Common itinerary patterns noted
   - Food recommendations compiled

5. **Synthesis:**
   - Create 3-day itinerary
   - Include transportation tips
   - Add food recommendations

6. **Documentation:**
   - Create travel itinerary document
   - Include video references
   - Save to `travel/bangkok/` (relative to workspace root)

**Output:** 3-day itinerary with attractions, food, and transportation details

---

### Example 3: Comparison Research

**Query:** "Compare X vs Y"

**Process:**
1. **Query Analysis:**
   - Sub-topics: Features, pros/cons, use cases, pricing
   - Sources: Comparison articles, reviews, official docs

2. **Source Identification:**
   - Web: Search for "X vs Y comparison"
   - Browser: Read full comparison articles
   - YouTube: Find comparison videos if available

3. **Information Gathering:**
   - Phase 1: `web_search` finds comparison articles
   - Phase 2: Read top 3 detailed comparisons
   - Extract pros/cons from each source

4. **Analysis:**
   - Common pros/cons identified
   - Different perspectives noted
   - Use cases clarified

5. **Synthesis:**
   - Create comparison matrix
   - Organize pros/cons
   - Add recommendations

6. **Documentation:**
   - Create comparison document
   - Include source citations
   - Save to research directory

**Output:** Comparison document with matrix, pros/cons, and recommendations

---

## Research Depth Options

### Quick Research Mode
**Use When:** User needs quick overview or summary

**Process:**
- Use `web_search` only
- Analyze snippets and summaries
- Create brief summary document
- **Time:** 5-10 minutes
- **Sources:** 5-10 search results

**Output:** Quick summary with key points

---

### Standard Research Mode (Default)
**Use When:** User needs comprehensive information

**Process:**
- Phase 1: `web_search` for discovery
- Phase 2: Read top 3-5 articles in full
- YouTube: Extract 3-5 video transcripts
- Create comprehensive document
- **Time:** 20-30 minutes
- **Sources:** 3-5 articles + 3-5 videos

**Output:** Comprehensive research document

---

### Deep Research Mode
**Use When:** User needs exhaustive research or academic-level depth

**Process:**
- Phase 1: `web_search` for discovery
- Phase 2: Read 5+ articles in full
- YouTube: Extract 5+ video transcripts
- Cross-reference extensively
- Create detailed report with analysis
- **Time:** 45-60 minutes
- **Sources:** 5+ articles + 5+ videos + official docs

**Output:** Detailed research report with extensive analysis

---

## Source Prioritization Logic

### How to Identify "Promising Sources"

**Criteria (in order of importance):**

1. **Credibility:**
   - Official government sites (.gov)
   - Educational institutions (.edu)
   - Established news sources
   - Verified experts/channels

2. **Relevance:**
   - Title matches query closely
   - Description contains key terms
   - Content directly addresses question

3. **Recency:**
   - Recent publication (prefer < 2 years)
   - Updated information
   - Current best practices

4. **Comprehensiveness:**
   - Detailed, in-depth content
   - Covers multiple aspects
   - Includes examples or case studies

5. **Engagement (for videos):**
   - High view count
   - Positive engagement (likes, comments)
   - Recent upload date

**Selection Algorithm:**
```
For each source:
  Score = 0
  
  If official/government source: Score += 10
  If .edu or academic: Score += 9
  If established news: Score += 8
  If verified expert: Score += 7
  If recent (< 1 year): Score += 5
  If comprehensive: Score += 5
  If highly relevant: Score += 5
  
  Select top 3-5 sources by score
```

---

## Quality Checks

### Minimum Requirements

**Before completing research:**
- [ ] At least 3 sources consulted
- [ ] At least 1 official/credible source included
- [ ] Information cross-referenced across sources
- [ ] All claims have source attribution
- [ ] Document is well-organized and readable

### Credibility Thresholds

**High Credibility:**
- Official government sites
- Academic sources
- Established news organizations
- Verified experts

**Medium Credibility:**
- Reputable blogs
- Industry publications
- Unverified but established sources

**Low Credibility (use with caution):**
- Personal blogs
- Social media
- Unverified sources

### Information Completeness

**Checklist:**
- [ ] Key aspects of query addressed
- [ ] Multiple perspectives included
- [ ] Gaps in information noted
- [ ] Recommendations provided (if applicable)

### Synthesis Quality

**Checklist:**
- [ ] Information logically organized
- [ ] Common themes identified
- [ ] Conflicts explained
- [ ] Sources properly cited
- [ ] Document is actionable

---

## Error Handling

### When web_search Fails

**Fallback Strategy:**
1. Try alternative search terms
2. Use browser tools to search directly
3. Navigate to known authoritative sites
4. Inform user of limitations

**User Communication:**
"Web search encountered an issue. Proceeding with browser-based research..."

---

### When Browser Tools Fail

**Fallback Strategy:**
1. Use `web_search` snippets only
2. Try alternative URLs if available
3. Extract information from search summaries
4. Note limitations in document

**User Communication:**
"Unable to access full article content. Research based on available summaries and snippets."

---

### When YouTube Skill Fails

**Fallback Strategy:**
1. Use `web_search` for video topics
2. Extract video information from search results
3. Note that transcripts unavailable
4. Focus on other source types

**User Communication:**
"YouTube video extraction unavailable. Research based on web sources and video metadata."

---

### When Information is Insufficient

**Strategy:**
1. Note gaps in information
2. Suggest alternative search terms
3. Recommend consulting experts
4. Provide partial findings with caveats

**User Communication:**
"Limited information available on [topic]. Research findings may be incomplete. Consider consulting [expert/source type]."

---

## Best Practices

### Do

- ✅ **Start with web_search** for fast discovery
- ✅ **Use browser tools** for deep dives on promising sources
- ✅ **Cross-reference** information across multiple sources
- ✅ **Cite all sources** with URLs and titles
- ✅ **Organize by themes** rather than chronologically
- ✅ **Prioritize credible sources** (official, academic, established)
- ✅ **Note conflicts** and different perspectives
- ✅ **Include recommendations** when applicable
- ✅ **Save to organized directories** with descriptive filenames
- ✅ **Use appropriate templates** for different research types

### Don't

- ❌ **Don't rely on single source** - always consult multiple sources
- ❌ **Don't skip source attribution** - always cite sources
- ❌ **Don't ignore conflicts** - note disagreements between sources
- ❌ **Don't read too many sources** - prioritize top 3-5 for deep dives
- ❌ **Don't skip credibility assessment** - evaluate source quality
- ❌ **Don't create documents without structure** - use templates
- ❌ **Don't forget to synthesize** - combine information logically
- ❌ **Don't skip error handling** - have fallback strategies

---

## Integration Notes

### With YouTube Skill

- Researcher skill orchestrates YouTube research
- Uses browser tools to search YouTube
- Extracts video information and transcripts
- Synthesizes video content with web sources

### With web_search Tool

- Primary method for Phase 1 discovery
- Fast and efficient for initial research
- Identifies sources for deep dive
- Provides snippets and summaries

### With Browser Tools

- Essential for Phase 2 deep dives
- Reads full articles from promising sources
- Extracts detailed information
- Verifies claims from original sources

### With File Operations

- Saves research documents
- Organizes files by topic
- Creates structured output
- Manages research history

---

## Troubleshooting

### Research Takes Too Long

**Solution:**
- Limit sources (top 3-5 for deep dives)
- Use Quick Research mode for simple queries
- Skip browser tools if snippets sufficient

### Information Quality is Low

**Solution:**
- Prioritize credible sources
- Cross-reference more extensively
- Use Deep Research mode
- Consult official documentation

### Too Many Conflicting Sources

**Solution:**
- Note all perspectives
- Identify consensus vs. disagreements
- Prioritize most credible sources
- Explain conflicts in document

### Sources Not Found

**Solution:**
- Try alternative search terms
- Use browser tools to search directly
- Consult known authoritative sites
- Inform user of limitations

---

## Example Prompts

- "Research how to do [X] and create a step-by-step guide"
- "Find information about [topic] from multiple sources"
- "Research [topic] and create a comprehensive report"
- "Compare [X] vs [Y] and create a comparison document"
- "Research [topic] for beginners and create a learning guide"
- "Find the best practices for [X] based on multiple sources"
- "Research [topic] and synthesize findings into a summary"
- "Create a research document on [topic] with citations"

---

## Advanced Features

### Research Templates

Pre-built templates for common research types:
- How-to guides
- Comparison documents
- Learning resources
- Travel itineraries
- Product research

### Custom Output Formats

- Markdown (default)
- Structured summaries
- Comparison tables
- Timeline/chronology
- Step-by-step guides

### Research History

- Track research queries
- Save intermediate results
- Reference previous research
- Build on existing knowledge

---

*Researcher Skill Version: 1.0*  
*Last Updated: December 28, 2025*

