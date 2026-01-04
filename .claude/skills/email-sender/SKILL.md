---
name: email-sender
description: Use this skill to send emails via Mailgun API. Supports HTML newsletters, bulk sending to subscriber lists, retry logic for failed sends, and newsletter archiving. Invoke when users want to send emails, manage subscriber lists, or distribute newsletters to an audience.
---

# Email Sender Skill

This skill enables Claude to send emails through the Mailgun API. It handles subscriber management, batch sending, retry logic, and maintains an archive of sent newsletters.

## When to Use This Skill

Use this skill when:
- User wants to send a newsletter to subscribers
- User needs to manage an email subscriber list
- User asks to "send email" or "email to subscribers"
- User wants to distribute content via email
- User needs to check email sending status

**Examples:**
- "Send this newsletter to all subscribers"
- "Add these emails to the subscriber list"
- "Email the stock picks to my audience"
- "Check if yesterday's newsletter was sent"
- "Retry failed email sends"

## Core Capabilities

### 1. Email Sending
- Send HTML + plain text emails via Mailgun
- Support for bulk recipient sending
- Configurable from address and reply-to
- Custom subject lines

### 2. Subscriber Management
- CSV-based subscriber storage
- Add/remove subscribers
- List all subscribers
- Import from external sources

### 3. Reliability
- Automatic retry with exponential backoff
- Failed send logging
- Delivery status tracking
- Rate limiting compliance

### 4. Archiving
- Archive sent newsletters
- Track send history
- Query past newsletters

## Workflow

### Standard Email Send Flow

1. **Load Subscribers:** Read subscriber list from CSV
2. **Validate Content:** Ensure HTML and text versions exist
3. **Send Emails:** Batch send via Mailgun API
4. **Track Results:** Log successes and failures
5. **Retry Failures:** Attempt resend with backoff
6. **Archive:** Store sent newsletter copy

## Tool Usage Instructions

### Using the Email Sender Script

**Script Location:** `~/.claude/skills/email-sender/scripts/email_sender.py`

**Environment Setup:**
```bash
# Required environment variables
export MAILGUN_API_KEY="your-mailgun-api-key"
export MAILGUN_DOMAIN="quanthub.ai"
```

**Basic Usage:**
```bash
# Send newsletter to all subscribers
python3 email_sender.py --send newsletter.html --subject "Daily Stock Picks"

# Send to specific email (for testing)
python3 email_sender.py --send newsletter.html --to test@example.com

# Preview without sending (dry run)
python3 email_sender.py --send newsletter.html --dry-run

# Check send status
python3 email_sender.py --status

# Retry failed sends
python3 email_sender.py --retry
```

### Subscriber Management

```bash
# List all subscribers
python3 email_sender.py --subscribers list

# Add subscriber
python3 email_sender.py --subscribers add user@example.com "John Doe"

# Remove subscriber
python3 email_sender.py --subscribers remove user@example.com

# Import from file
python3 email_sender.py --subscribers import contacts.csv
```

### Archive Operations

```bash
# List archived newsletters
python3 email_sender.py --archive list

# View specific archive
python3 email_sender.py --archive view 2026-01-03
```

## Configuration

### Environment Variables

| Variable | Description | Required |
| -------- | ----------- | -------- |
| MAILGUN_API_KEY | Mailgun API key | Yes |
| MAILGUN_DOMAIN | Sending domain (quanthub.ai) | Yes |
| MAILGUN_FROM | From address | No (default: newsletter@quanthub.ai) |

### Subscriber CSV Format

```csv
email,name,subscribed_date,active
user@example.com,John Doe,2026-01-01,true
```

**File Location:** `~/.claude/skills/email-sender/data/subscribers.csv`

## Inputs

| Parameter | Type | Description | Default |
| --------- | ---- | ----------- | ------- |
| html_content | string | HTML email body | Required |
| text_content | string | Plain text fallback | Required |
| subject | string | Email subject | Required |
| recipients | list | Email addresses (or use subscriber list) | None |
| from_email | string | Sender email | newsletter@quanthub.ai |
| dry_run | bool | Preview without sending | False |

## Outputs

| Field | Type | Description |
| ----- | ---- | ----------- |
| sent_count | int | Successfully sent emails |
| failed_count | int | Failed email count |
| failures | list | List of failed recipients |
| message_ids | list | Mailgun message IDs |

## Retry Logic

Failed sends are automatically retried with exponential backoff:

1. **Attempt 1:** Immediate
2. **Attempt 2:** Wait 30 seconds
3. **Attempt 3:** Wait 2 minutes  
4. **Attempt 4:** Wait 5 minutes
5. **Give up:** Log failure, continue with others

Failed sends are logged to `~/.claude/skills/email-sender/data/failed_sends.json`

## Rate Limiting

- Mailgun free tier: 100 emails/hour
- Script implements 1 second delay between sends
- Batch size configurable (default: 50)

## Best Practices

- ✅ Always test with `--dry-run` first
- ✅ Test with single email before bulk send
- ✅ Include unsubscribe link in footer
- ✅ Use both HTML and plain text versions
- ✅ Keep subject lines under 50 characters
- ❌ Don't send without proper authentication
- ❌ Don't exceed rate limits
- ❌ Don't send to unverified addresses

## Integration

Works with:
- **newsletter-formatter:** Generate HTML content to send
- **stock-screener:** Get stock picks for newsletter

### Complete Workflow Example

```python
# 1. Screen stocks
stocks = stock_screener.screen("momentum", limit=5)

# 2. Generate newsletter
newsletter = newsletter_formatter.generate(stocks)

# 3. Send to subscribers
result = email_sender.send(
    html_content=newsletter['html'],
    text_content=newsletter['text'],
    subject=newsletter['subject']
)
```

## File Structure

```
~/.claude/skills/email-sender/
├── SKILL.md
├── scripts/
│   └── email_sender.py
├── data/
│   ├── subscribers.csv
│   ├── failed_sends.json
│   └── send_log.json
└── archive/
    └── 2026-01-03/
        ├── newsletter.html
        ├── newsletter.txt
        └── metadata.json
```

---

*Email Sender Skill Version: 1.0*  
*Last Updated: January 3, 2026*




