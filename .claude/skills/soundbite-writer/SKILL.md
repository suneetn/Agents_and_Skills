---
name: soundbite-writer
description: Parse sound bite spreadsheets and synthesize them into executive summaries, team narratives, and status reports.
---

# Sound Bite Writer Skill

This skill enables Claude to read sound bite data from Excel/CSV files and transform them into polished leadership narratives.

## Source Files

Sound bite data lives in:
- `/Users/snandwani2/leader-app-RAG/PDX Sound Bites.xlsx` (primary)
- `/Users/snandwani2/leader-app-RAG/PDX Sound Bites (1).xlsx` (backup)

Output should be saved to:
- `/Users/snandwani2/leader-app-RAG/` (with descriptive filename)

## Parsing Sound Bites from XLSX

Run this Node.js script from the leader-app directory to parse sound bites:

```bash
cd /Users/snandwani2/leader-app && node -e "
const XLSX = require('xlsx');
const workbook = XLSX.readFile('/Users/snandwani2/leader-app-RAG/PDX Sound Bites.xlsx');
const sheet = workbook.Sheets[workbook.SheetNames[0]];
const rawData = XLSX.utils.sheet_to_json(sheet, { header: 1 });

// Find header row and parse
const headerIndex = rawData.findIndex(row => row && row.some(cell => cell === 'News Item'));
const headers = rawData[headerIndex];
const dataRows = rawData.slice(headerIndex + 1).filter(row => row && row.length > 0 && row[0]);

const soundBites = dataRows.map(row => {
  const obj = {};
  headers.forEach((h, i) => { if (h) obj[h.toString().trim()] = row[i]; });
  return obj;
}).filter(sb => sb['News Item']);

console.log(JSON.stringify(soundBites, null, 2));
"
```

### Parse with Filters

Filter by impact rating (1 = highest):
```bash
cd /Users/snandwani2/leader-app && node -e "
const XLSX = require('xlsx');
const workbook = XLSX.readFile('/Users/snandwani2/leader-app-RAG/PDX Sound Bites.xlsx');
const sheet = workbook.Sheets[workbook.SheetNames[0]];
const rawData = XLSX.utils.sheet_to_json(sheet, { header: 1 });
const headerIndex = rawData.findIndex(row => row && row.some(cell => cell === 'News Item'));
const headers = rawData[headerIndex];
const dataRows = rawData.slice(headerIndex + 1).filter(row => row && row.length > 0 && row[0]);
const soundBites = dataRows.map(row => {
  const obj = {};
  headers.forEach((h, i) => { if (h) obj[h.toString().trim()] = row[i]; });
  return obj;
}).filter(sb => sb['News Item'] && sb['L0 Domain Stack Rank'] === 1);
console.log(JSON.stringify(soundBites, null, 2));
"
```

Filter by L0 Domain:
```bash
cd /Users/snandwani2/leader-app && node -e "
const XLSX = require('xlsx');
const DOMAIN = 'Identity'; // Change this
const workbook = XLSX.readFile('/Users/snandwani2/leader-app-RAG/PDX Sound Bites.xlsx');
const sheet = workbook.Sheets[workbook.SheetNames[0]];
const rawData = XLSX.utils.sheet_to_json(sheet, { header: 1 });
const headerIndex = rawData.findIndex(row => row && row.some(cell => cell === 'News Item'));
const headers = rawData[headerIndex];
const dataRows = rawData.slice(headerIndex + 1).filter(row => row && row.length > 0 && row[0]);
const soundBites = dataRows.map(row => {
  const obj = {};
  headers.forEach((h, i) => { if (h) obj[h.toString().trim()] = row[i]; });
  return obj;
}).filter(sb => sb['News Item'] && (sb['L0 Domain(s) / PDX Team(s)'] || '').includes(DOMAIN));
console.log(JSON.stringify(soundBites, null, 2));
"
```

### Get Summary Statistics

```bash
cd /Users/snandwani2/leader-app && node -e "
const XLSX = require('xlsx');
const workbook = XLSX.readFile('/Users/snandwani2/leader-app-RAG/PDX Sound Bites.xlsx');
const sheet = workbook.Sheets[workbook.SheetNames[0]];
const rawData = XLSX.utils.sheet_to_json(sheet, { header: 1 });
const headerIndex = rawData.findIndex(row => row && row.some(cell => cell === 'News Item'));
const headers = rawData[headerIndex];
const dataRows = rawData.slice(headerIndex + 1).filter(row => row && row.length > 0 && row[0]);
const soundBites = dataRows.map(row => {
  const obj = {};
  headers.forEach((h, i) => { if (h) obj[h.toString().trim()] = row[i]; });
  return obj;
}).filter(sb => sb['News Item']);

// Stats
const stats = {
  total: soundBites.length,
  byRating: {},
  byDomain: {}
};
soundBites.forEach(sb => {
  const rating = sb['L0 Domain Stack Rank'] || 'unrated';
  const domain = sb['L0 Domain(s) / PDX Team(s)'] || 'unknown';
  stats.byRating[rating] = (stats.byRating[rating] || 0) + 1;
  stats.byDomain[domain] = (stats.byDomain[domain] || 0) + 1;
});
console.log(JSON.stringify(stats, null, 2));
"
```

## CSV Column Reference

| Column | Field Key | Description |
|--------|-----------|-------------|
| Entered By | `Entered By` | Who logged it |
| Date of Entry | `Date of Entry` | When logged (Excel date number) |
| Date of Event | `Date of Event` | When it happened |
| L0 Domain(s) | `L0 Domain(s) / PDX Team(s)` | Team areas |
| Stack Rank | `L0 Domain Stack Rank` | Impact: 1=high, 2=med, 3=low |
| Customer Domain | `Customer Domain: Intuit BU(s)` | CG, SBG, All Intuit BUs |
| Products | `Product(s)\nLIst the products from Product Catalog` | Products affected |
| News Item | `News Item` | **Main content** |
| Customer Impact | `Customer Impact` | **Why it matters** |
| Impact Validation | `Impact Validation` | Metrics/proof |
| Link | `Link for More Info` | URL reference |
| Leads | `PM, XD, PD, TPM Leads` | People involved |
| AI Summary | `AI Summary (auto generated)` | Auto summary |

## Output Formats

**Important:** Do not use emojis or icons in output. Keep formatting clean and professional.

### 1. Executive Summary
Best for: Staff meetings, leadership updates, stakeholder briefs

Template:
```markdown
# [Team/Domain] Executive Summary
**Period: [Date Range]**

---

## [Theme 1]

**[Headline achievement]** ([Date of Event]) — [1-2 sentence context with metrics from Impact Validation]
*(Leads: [Names])*

## [Theme 2]
...

## Key Metrics at a Glance

| Metric | Value |
|--------|-------|
| [Metric 1] | [Value] |
...
```

### 2. Team Narrative
Best for: Biweekly updates, monthly reports

Template:
```markdown
# [Team] Update — [Period]

## Momentum
[1-2 sentences on overall team direction]

## Wins

### [Theme 1]

**[Achievement]** ([Date of Event]) — [Context and impact]
*(Leads: [Names])*

**[Achievement 2]** ([Date of Event]) — [Context and impact]
*(Leads: [Names])*

### [Theme 2]
...

## Impact Highlights
- [Quantified outcome 1]
- [Quantified outcome 2]

## Looking Ahead
- [Upcoming focus area]
```

### 3. All-Hands Slide Content
Best for: Presentation decks, Slack announcements

Template:
```markdown
### [Punchy Headline] (5-8 words)
[Date of Event]
[1-2 sentence supporting context]
*— [Person/Team name]*
```

### 4. Stakeholder Update
Best for: Non-technical leadership, business partners

Template:
```markdown
# [Domain] Business Update

**Bottom Line**: [1 sentence summary of impact]

## What We Delivered
- **[Outcome 1]** ([Date]) — [Brief description]
- **[Outcome 2]** ([Date]) — [Brief description]

## Business Impact
[Connect to company objectives, revenue, customer satisfaction]

## Ask
[Clear request if needed]
```

## Writing Guidelines

### Do
- Use active voice: "shipped", "reduced", "enabled", "unlocked"
- Lead with impact, not activity
- **Always include the Date of Event** for each achievement (format as month/quarter, e.g., "Oct 2025", "Q1 FY26")
- Quantify outcomes when possible (from Impact Validation column)
- Attribute wins to specific people (from Leads column)
- Use commas instead of em dashes for parenthetical phrases
- Group related items into coherent themes
- Connect technical work to customer/business value

### Don't
- **Use emojis or icons** (no 🚀, 🎨, 🎉, 📊, etc.)
- Start with "We worked on..." or "Made progress on..."
- Use passive voice: "was completed", "has been shipped"
- Include jargon without context for stakeholder updates
- Bury the impact at the end
- List items chronologically (group by theme instead)
- Use hyperbole or vague superlatives

## Workflow

When asked to create a writeup from sound bites:

1. **Clarify scope** if not specified:
   - Time period? (last 2 weeks, Q2, November)
   - Which teams/domains? (Identity, APEX, all PDX)
   - Format? (executive summary, narrative, slides)
   - Audience? (Deb, staff meeting, all-hands)

2. **Parse the source file** using the scripts above

3. **Filter and sort**:
   - By Impact Rating (1s first)
   - By domain if specified
   - By date if relevant

4. **Identify themes** that connect multiple sound bites

5. **Draft the narrative** using the appropriate template

6. **Save output** to `/Users/snandwani2/leader-app-RAG/` with descriptive filename like:
   - `PDX-Executive-Summary-Dec-2024.md`
   - `Identity-Team-Narrative-Q4.md`
   - `All-Hands-Slides-November.md`

## Example Prompts

- "Create an executive summary of Identity team wins from the last 30 days"
- "Synthesize all Impact Rating 1 items into a team narrative for Deb's staff meeting"
- "Create all-hands slide content from November sound bites grouped by L0 domain"
- "Write a stakeholder update for CG leadership covering APEX accomplishments"
- "Summarize cross-team collaboration highlights from the past month"

