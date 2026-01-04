---
name: newsletter-formatter
description: Use this skill to format content into professional HTML email newsletters. Supports stock picks, market summaries, comparison tables, and sparkline charts. Generates responsive templates that work across email clients (Gmail, Outlook, Apple Mail). Invoke when users want to create newsletters, format stock analysis for email, or generate HTML email content.
---

# Newsletter Formatter Skill

This skill enables Claude to generate professional HTML email newsletters from structured data. It creates responsive, email-client-compatible templates with support for stock data tables, sparkline charts, and market summaries.

## When to Use This Skill

Use this skill when:
- User wants to create a newsletter from stock data
- User needs to format analysis results for email
- User wants to generate HTML email content
- User asks to "create a newsletter" or "format for email"
- User wants stock picks formatted with charts

**Examples:**
- "Format these stock picks as a newsletter"
- "Create an email newsletter from this analysis"
- "Generate HTML email with stock comparison table"
- "Make a daily stock picks newsletter"

## Core Capabilities

### 1. Stock Picks Newsletter
- Formatted table with stock metrics
- Sparkline price charts (optional)
- FMP ratings and growth data
- Color-coded signals (Buy/Hold/Sell)

### 2. Market Summary
- Daily market overview
- Index performance
- Key news highlights

### 3. Responsive Design
- Mobile-friendly layout
- Works in Gmail, Outlook, Apple Mail
- Inline CSS for compatibility
- Dark mode support

## Workflow

### Standard Newsletter Generation

1. **Receive Data:** Accept stock data dict with metrics
2. **Select Template:** Choose appropriate template (stock-picks, market-summary)
3. **Generate Charts:** Create sparkline PNGs (if enabled)
4. **Render Template:** Apply Jinja2 template with data
5. **Inline CSS:** Convert styles for email compatibility
6. **Output:** Return HTML + plain text versions

## Tool Usage Instructions

### Using the Newsletter Generator Script

**Script Location:** `~/.claude/skills/newsletter-formatter/scripts/newsletter_generator.py`

**Basic Usage:**
```bash
# Generate from JSON data file
python3 newsletter_generator.py --data stocks.json --output newsletter.html

# Generate with sample data (for testing)
python3 newsletter_generator.py --sample --output test_newsletter.html

# Generate without charts (faster)
python3 newsletter_generator.py --data stocks.json --no-charts --output newsletter.html
```

### Input Data Format

```python
{
    "title": "Daily Stock Picks",
    "date": "January 3, 2026",
    "edition": 42,
    "stocks": [
        {
            "rank": 1,
            "ticker": "PLTR",
            "name": "Palantir Technologies",
            "price": 167.86,
            "change_percent": 2.5,
            "score": 85.0,
            "fmp_rating": {
                "grade": "A+",
                "recommendation": "Strong Buy"
            },
            "growth": {
                "revenue_growth": 28.8,
                "eps_growth": 114.9
            },
            "metrics": {
                "pe_ratio": 390,
                "price_vs_50sma": 15.2
            },
            "price_history": [150, 155, 160, 165, 168]  # For sparkline
        }
    ],
    "market_summary": "Markets rallied on strong earnings...",
    "footer_text": "This is not financial advice."
}
```

### Output Format

- **HTML:** Complete email-ready HTML with inline CSS
- **Plain Text:** Fallback text version for email clients
- **Subject:** Suggested email subject line

## Templates

### Available Templates

| Template | Use Case | Features |
| -------- | -------- | -------- |
| `stock-picks` | Daily stock picks | Table, ratings, sparklines |
| `market-summary` | Market overview | Indices, news |
| `comparison` | Stock comparison | Side-by-side metrics |

### Template Customization

Templates are located in `~/.claude/skills/newsletter-formatter/templates/`

- `base.html` - Base template with styles
- `stock-picks.html` - Stock picks template
- `market-summary.html` - Market summary template

## Inputs

| Parameter | Type | Description | Default |
| --------- | ---- | ----------- | ------- |
| data | dict | Stock/content data | Required |
| template | string | Template name | stock-picks |
| include_charts | bool | Generate sparklines | True |
| dark_mode | bool | Use dark theme | False |
| output_path | string | Output file path | None |

## Outputs

| Field | Type | Description |
| ----- | ---- | ----------- |
| html | string | Complete HTML email |
| text | string | Plain text fallback |
| subject | string | Suggested subject line |
| charts | list | Generated chart paths (if any) |

## Best Practices

- ✅ Always provide price_history for sparklines
- ✅ Include both HTML and plain text versions
- ✅ Test in multiple email clients
- ✅ Keep subject lines under 50 characters
- ✅ Use inline CSS (premailer handles this)
- ❌ Don't use external images (may be blocked)
- ❌ Don't use JavaScript (not supported in email)

## Integration

Works with:
- **stock-screener:** Format screened stocks as newsletter
- **stock-analyst:** Include detailed analysis
- **email-sender:** Send the generated newsletter

---

*Newsletter Formatter Skill Version: 1.0*  
*Last Updated: January 3, 2026*




