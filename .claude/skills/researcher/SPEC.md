# Researcher Skill - Specification Document

## Overview

The Researcher skill is a meta-skill that orchestrates multiple research tools and skills to conduct comprehensive research on any topic. It leverages the YouTube skill, web search, and other available tools to gather, analyze, and synthesize information from multiple sources into organized research documents.

## Purpose

Enable Claude to conduct thorough, multi-source research by:
- Searching across multiple platforms (YouTube, web, etc.)
- Extracting and analyzing content from various sources
- Synthesizing information into coherent summaries
- Creating well-organized research documents
- Comparing perspectives from different sources
- Identifying the most credible and relevant information

## Core Capabilities

### 1. Multi-Source Research

**Capability:** Search and gather information from multiple sources simultaneously

**Sources:**
- YouTube videos (via YouTube skill)
- Web search results
- Wikipedia articles
- News articles
- Academic sources (when available)
- Reddit discussions (when relevant)
- Official documentation

**Process:**
1. Break down research query into sub-topics
2. Search each source type for relevant information
3. Collect and organize results by source type
4. Identify overlaps and unique insights

### 2. Video Research (Leveraging YouTube Skill)

**Capability:** Find, analyze, and extract insights from YouTube videos

**Process:**
1. Use YouTube skill to search for relevant videos
2. Identify most promising videos based on:
   - View count and engagement
   - Channel credibility
   - Recency
   - Relevance to query
3. Extract transcripts from top videos
4. Analyze transcripts for key insights
5. Compare perspectives across multiple videos
6. Identify common themes and unique points

**Output:**
- List of most relevant videos with metadata
- Key insights extracted from video transcripts
- Comparison of different perspectives
- Video recommendations ranked by relevance

### 3. Web Research

**Capability:** Search the web and extract relevant information

**Process:**
1. Perform targeted web searches
2. Evaluate source credibility
3. Extract key information from search results
4. Cross-reference information across sources
5. Identify authoritative sources

**Output:**
- Summarized information from web sources
- Source citations
- Credibility assessment
- Key facts and statistics

### 4. Information Synthesis

**Capability:** Combine information from multiple sources into coherent insights

**Process:**
1. Identify common themes across sources
2. Note conflicting information and perspectives
3. Highlight unique insights from each source
4. Create structured summary
5. Organize by topic/subtopic

**Output:**
- Comprehensive summary document
- Key findings organized by topic
- Source attribution
- Confidence levels for different claims

### 5. Research Document Creation

**Capability:** Generate well-organized research documents

**Document Structure:**
- Executive summary
- Research methodology
- Findings by topic
- Source citations
- Recommendations (when applicable)
- Appendix with detailed information

**Formats:**
- Markdown documents
- Structured summaries
- Comparison tables
- Timeline/chronology (when relevant)

### 6. Credibility Assessment

**Capability:** Evaluate and rank sources by credibility

**Factors:**
- Source type (academic, official, news, social media)
- Author credentials
- Publication date
- Cross-referencing with other sources
- Bias detection

**Output:**
- Credibility scores for sources
- Flagged information requiring verification
- Recommended authoritative sources

## Use Cases

### 1. Topic Research
**Example:** "Research how to do Jeevan Praman for India"
- Search YouTube for tutorial videos
- Search web for official government information
- Extract step-by-step processes
- Create comprehensive guide

### 2. Travel Planning
**Example:** "Research what to do in Bangkok for 3 days"
- Find popular YouTube travel guides
- Search for official tourism information
- Extract recommendations from multiple sources
- Create itinerary based on synthesis

### 3. Product/Service Research
**Example:** "Research best practices for X"
- Find expert videos on YouTube
- Search for official documentation
- Compare different approaches
- Create best practices guide

### 4. Comparative Analysis
**Example:** "Compare X vs Y"
- Find videos comparing both
- Search for expert opinions
- Extract pros/cons from multiple sources
- Create comparison document

### 5. Learning/Education
**Example:** "Research topic X for beginners"
- Find educational YouTube videos
- Search for tutorials and guides
- Extract key concepts
- Create learning resource

## Integration with Other Skills

### YouTube Skill
- **Primary Integration:** Use YouTube skill for all video research
- **Workflow:** 
  1. Researcher skill identifies need for video research
  2. Calls YouTube skill to search and extract
  3. Receives transcripts and metadata
  4. Synthesizes with other sources

### Web Search
- **Integration:** Use web_search tool for general web research
- **Workflow:**
  1. Researcher skill performs web searches
  2. Analyzes search results
  3. Extracts relevant information
  4. Cross-references with video sources

### Future Skills
- **Wikipedia Skill:** For encyclopedic information
- **News Skill:** For current events and news articles
- **Academic Skill:** For scholarly sources (when available)

## Research Workflow

### Standard Research Process

1. **Query Analysis**
   - Understand research question
   - Break into sub-topics
   - Identify required source types

2. **Source Identification**
   - Determine which sources to search
   - Prioritize source types
   - Plan search strategy

3. **Information Gathering**
   - Execute searches across sources
   - Extract relevant content
   - Collect metadata

4. **Analysis**
   - Identify key insights
   - Compare perspectives
   - Assess credibility
   - Note gaps in information

5. **Synthesis**
   - Combine information logically
   - Resolve conflicts where possible
   - Highlight consensus vs. disagreements
   - Organize by themes

6. **Documentation**
   - Create structured research document
   - Include source citations
   - Add recommendations
   - Format for easy consumption

## Output Formats

### 1. Research Summary
- Executive summary
- Key findings
- Source list
- Recommendations

### 2. Comprehensive Report
- Full research document
- Detailed findings
- Source analysis
- Methodology
- Appendices

### 3. Quick Reference Guide
- Condensed information
- Step-by-step instructions
- Quick tips
- Essential resources

### 4. Comparison Document
- Side-by-side comparisons
- Pros/cons tables
- Feature matrices
- Recommendations

## Quality Criteria

### Research Quality Standards

1. **Comprehensiveness**
   - Multiple sources consulted
   - Different perspectives included
   - Key aspects covered

2. **Accuracy**
   - Information verified across sources
   - Credible sources prioritized
   - Outdated information flagged

3. **Organization**
   - Logical structure
   - Clear headings
   - Easy to navigate

4. **Attribution**
   - All sources cited
   - Clear source identification
   - Links/references provided

5. **Actionability**
   - Practical insights
   - Clear recommendations
   - Next steps identified

## Technical Requirements

### Dependencies
- YouTube skill (required)
- Web search capability (required)
- File writing capability (for documents)
- Browser tools (for web research)

### Tools Used
- `youtube` skill functions
- `web_search` tool
- `browser_navigate`, `browser_snapshot` (for web research)
- `write` tool (for document creation)
- `codebase_search` (for finding relevant code/info when applicable)

### Data Storage
- Research documents saved to specified location
- Metadata stored for future reference
- Source URLs and citations preserved

## Example Research Scenarios

### Scenario 1: "How to do X"
**Process:**
1. Search YouTube for tutorial videos
2. Search web for official guides
3. Extract step-by-step processes
4. Compare different methods
5. Create comprehensive guide

**Output:** Step-by-step guide with video references

### Scenario 2: "Best X for Y"
**Process:**
1. Find comparison videos on YouTube
2. Search for reviews and recommendations
3. Extract pros/cons from sources
4. Create comparison document

**Output:** Comparison table with recommendations

### Scenario 3: "Research topic X"
**Process:**
1. Find educational videos
2. Search for articles and documentation
3. Extract key concepts
4. Organize by subtopics
5. Create research document

**Output:** Comprehensive research document

## Success Metrics

A successful Researcher skill should:
- ✅ Gather information from 3+ source types
- ✅ Identify most relevant sources
- ✅ Synthesize information coherently
- ✅ Create well-organized documents
- ✅ Provide source citations
- ✅ Save time vs. manual research
- ✅ Produce actionable insights

## Future Enhancements

### Phase 2 Features
- **Source Ranking:** Automatic ranking by credibility
- **Fact Checking:** Cross-reference claims across sources
- **Trend Analysis:** Identify patterns over time
- **Expert Identification:** Find and cite domain experts
- **Multi-language Support:** Research in multiple languages

### Phase 3 Features
- **Research Templates:** Pre-built templates for common research types
- **Collaborative Research:** Share and build on previous research
- **Research History:** Track research queries and results
- **Automated Updates:** Re-research topics for updates
- **AI-Powered Insights:** Generate insights beyond source synthesis

## Implementation Notes

### Skill Structure
- **Main Skill File:** `SKILL.md` in `~/.claude/skills/researcher/`
- **Helper Scripts:** Optional Python scripts for complex processing
- **Templates:** Markdown templates for different document types

### Naming Convention
- Skill name: `researcher`
- Description: "Conduct comprehensive multi-source research using YouTube, web search, and other tools. Synthesize information into organized research documents."

### Integration Points
- Calls YouTube skill functions
- Uses web_search tool
- Leverages browser tools when needed
- Creates documents using write tool

---

## Questions to Resolve

1. **Scope:** Should Researcher skill handle all research, or focus on specific types?
2. **Depth:** How deep should research go? (Quick summaries vs. comprehensive reports)
3. **Caching:** Should we cache research results to avoid re-researching?
4. **User Control:** How much control should user have over research process?
5. **Output Location:** Where should research documents be saved by default?

---

*Specification Version: 1.0*  
*Last Updated: December 28, 2025*


