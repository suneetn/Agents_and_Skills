---
name: daily-newsletter
description: Use this skill to generate and send daily stock newsletter emails with AI-enhanced investment thesis. Orchestrates stock screening, AI thesis generation, newsletter formatting, and email delivery. Invoke when users want to "send a newsletter", "/newsletter", "create stock picks email", "email daily stocks", or "generate and send stock analysis to subscribers".
---

# Daily Newsletter Skill

This skill orchestrates the complete daily stock newsletter workflow by combining the `stock-screener`, `analyst-light`, `newsletter-formatter`, and `email-sender` skills into a single end-to-end process.

**Key Feature:** When Claude orchestrates this workflow, it generates **AI-enhanced investment thesis** for each stock, providing richer insights than template-based output.

## When to Use This Skill

Use this skill when:
- User wants to "send a daily newsletter"
- User says "/newsletter" (slash command)
- User asks to "email stock picks to subscribers"
- User wants to "create and send a stock newsletter"
- User asks to "generate newsletter with momentum/value/growth stocks"
- User wants to "send today's top picks"

**Trigger Phrases:**
- "/newsletter" ← **Slash command for AI-enhanced newsletter**
- "Send daily newsletter"
- "Email stock picks"
- "Create newsletter with momentum stocks"
- "Send stock analysis to subscribers"
- "Generate and email top 5 stocks"

## Core Capabilities

### 1. End-to-End Newsletter Generation
- Screen stocks using configurable criteria
- Generate professional HTML newsletter
- Send to subscriber list via Mailgun

### 2. Multiple Screen Types
- `momentum` - High momentum stocks with growth-adjusted ratings
- `value` - Undervalued stocks with strong fundamentals
- `growth` - High-growth companies
- `quality` - Blue-chip quality stocks
- `oversold` - Technically oversold bounce candidates

### 3. Flexible Delivery
- Send to all subscribers
- Test send to specific email
- Preview without sending (dry-run)

## Workflow

### AI-Enhanced Newsletter Flow (Recommended)

**When Claude orchestrates the workflow**, follow these steps to inject AI-generated thesis:

#### Step 1: Run Screener + Analyst
```bash
python3 ~/personal/capabilities/daily-stock-newsletter/orchestrator.py \
  --screens momentum,value --limit 5 --actionable --preview
```

#### Step 2: Claude Reads Output and Enhances Thesis
After seeing the stock picks and template thesis, Claude generates **richer AI thesis** for each stock:

**For each stock, Claude provides:**
1. **Why This Stock Now:** Specific catalyst or setup making it actionable today
2. **The Trade:** Clear entry, target, stop with rationale
3. **The Risk:** Primary risk to the thesis
4. **Conviction Level:** High/Medium/Low based on data alignment

**Example AI-Enhanced Thesis (Claude generates):**
> **MU (Micron) — High Conviction**
> 
> Memory chip leader riding the AI infrastructure wave. The +10% pop today follows better-than-expected HBM guidance, and the stock is breaking out to new highs. With 993% EPS growth and datacenter demand accelerating, the premium 30x P/E is justified by the growth trajectory.
> 
> **Trade:** Enter on any pullback to $290-300 (near 20 SMA). Target $344 (3x ATR). Stop $277.
> 
> **Risk:** Memory pricing cycles are brutal. Any demand softening could trigger 20-30% correction.

#### Step 3: Claude Presents Enhanced Newsletter
Claude formats the AI thesis and presents to user, or injects into the final HTML before sending.

---

### Standard Newsletter Flow (Script-Only)

For automated/cron execution without Claude's AI layer:

1. **Screen Stocks:** Use `stock-screener` skill to find top picks
2. **Enrich Data:** Add FMP ratings and growth metrics  
3. **Format Newsletter:** Use `newsletter-formatter` to create HTML
4. **Send Email:** Use `email-sender` to deliver via Mailgun
5. **Archive:** Save copy for reference

*Note: Standard flow uses template-based thesis. AI-enhanced flow recommended for richer content.*

## Tool Usage Instructions

### Using the Orchestrator Script

**Script Location:** `~/personal/capabilities/daily-stock-newsletter/orchestrator.py`

**Configuration:** `~/personal/capabilities/daily-stock-newsletter/config.py`

### Basic Commands

```bash
# Generate and preview newsletter (opens in browser)
python3 ~/personal/capabilities/daily-stock-newsletter/orchestrator.py \
  --screen momentum --limit 5 --preview

# Generate and send to all subscribers
python3 ~/personal/capabilities/daily-stock-newsletter/orchestrator.py \
  --screen momentum --limit 5 --send

# Test send to specific email
python3 ~/personal/capabilities/daily-stock-newsletter/orchestrator.py \
  --screen momentum --limit 5 --send --to user@example.com

# Dry run (no actual send)
python3 ~/personal/capabilities/daily-stock-newsletter/orchestrator.py \
  --screen momentum --limit 5 --send --dry-run
```

### Available Options

| Option | Description | Default |
| ------ | ----------- | ------- |
| `--screen` | Screen type (momentum, value, growth, quality, oversold) | momentum |
| `--sector` | Filter by sector (Technology, Healthcare, etc.) | All |
| `--limit` | Number of stocks to include | 5 |
| `--preview` | Open newsletter in browser | False |
| `--send` | Send to subscribers | False |
| `--to` | Send to specific email(s) | None |
| `--dry-run` | Preview without sending | False |

## Configuration

**Config File:** `~/personal/capabilities/daily-stock-newsletter/config.py`

```python
MAILGUN_API_KEY = "your-api-key"
MAILGUN_DOMAIN = "mail.quanthub.ai"
FMP_API_KEY = "your-fmp-key"
NEWSLETTER_FROM_EMAIL = "newsletter@mail.quanthub.ai"
```

**Subscriber List:** `~/.claude/skills/email-sender/data/subscribers.csv`

```csv
email,name,subscribed_date,active
user@example.com,John Doe,2026-01-01,true
```

## Examples

### Example 1: AI-Enhanced Newsletter (Slash Command)
**User:** "/newsletter"

**Claude's Workflow:**
1. Run screener with actionable mode
2. Review each stock's data (technicals, fundamentals, news)
3. Generate AI thesis for each stock
4. Present enhanced newsletter to user
5. Ask if user wants to send

### Example 2: AI-Enhanced with Specific Screens
**User:** "/newsletter momentum and growth stocks"

**Claude's Workflow:**
1. Run: `--screens momentum,growth --limit 5 --actionable`
2. Generate AI thesis with screen-specific insights
3. Present and offer to send

### Example 3: Quick Send (Standard Template)
**User:** "Send daily newsletter with momentum stocks"

**Action:**
```bash
python3 ~/personal/capabilities/daily-stock-newsletter/orchestrator.py \
  --screen momentum --limit 5 --send
```
*Uses template thesis (faster, no AI enhancement)*

### Example 4: Preview with AI Enhancement
**User:** "Generate newsletter and show me first"

**Claude's Workflow:**
1. Run orchestrator with `--preview`
2. Read the generated data
3. Generate enhanced AI thesis
4. Present enhanced version
5. Ask: "Ready to send?"

### Example 5: Test Send
**User:** "Send test newsletter to my email test@example.com"

**Action:**
```bash
python3 ~/personal/capabilities/daily-stock-newsletter/orchestrator.py \
  --screen momentum --limit 5 --send --to test@example.com
```

## Output

### Newsletter Contents
- **Header:** Title, date, screen type
- **Market Summary:** Brief market context
- **Stock Table:** Top picks with price, rating, growth, score
- **Quick Analysis:** Details for top 3 stocks
- **Footer:** Disclaimer

### Delivery Confirmation
```
✅ Found 5 stocks
✅ HTML saved: output/newsletter_20260103_060650.html
✅ Sent to 3 recipients
```

## Integration

This skill orchestrates:
- **stock-screener:** For finding top stocks
- **newsletter-formatter:** For HTML generation
- **email-sender:** For Mailgun delivery

## File Structure

```
~/personal/capabilities/daily-stock-newsletter/
├── orchestrator.py      # Main workflow script
├── config.py            # API keys and settings
├── output/              # Generated newsletters
└── REQUIREMENTS_AND_DESIGN.md

~/.claude/skills/
├── stock-screener/      # Stock screening logic
├── newsletter-formatter/ # HTML template generation
├── email-sender/        # Mailgun email delivery
└── daily-newsletter/    # This orchestrator skill
```

---

*Daily Newsletter Skill Version: 1.0*  
*Last Updated: January 3, 2026*

