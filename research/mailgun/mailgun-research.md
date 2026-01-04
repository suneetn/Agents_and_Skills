# Mailgun Research: Plans, Capabilities, and Bulk Sending

**Research Date:** January 3, 2025  
**Focus:** Pricing plans, features, and bulk sending capabilities, particularly on the free plan

---

## Executive Summary

Mailgun offers four pricing tiers, from a free plan (100 emails/day) to enterprise-scale plans. The free plan supports bulk sending but with significant volume limitations. For production bulk email campaigns, paid plans provide better capacity, features, and reliability.

**Key Finding:** Yes, you can do bulk sends on the free plan, but you're limited to 100 emails per day, which may not be sufficient for most bulk email campaigns.

---

## Pricing Plans Overview

### 1. Free Plan
- **Cost:** $0/month
- **Volume:** 100 emails per day
- **Monthly Limit:** ~3,000 emails/month (based on daily limit)
- **Best For:** Testing, development, very small projects
- **Limitations:**
  - Daily sending cap (not monthly)
  - Basic features only
  - Limited support

### 2. Basic Plan
- **Cost:** $15/month
- **Volume:** 10,000 emails per month
- **Daily Limit:** None (can send all 10,000 in one day if needed)
- **Best For:** Small businesses, startups, moderate email volumes
- **Additional Features:**
  - No daily sending restrictions
  - Better deliverability
  - Email support

### 3. Foundation Plan
- **Cost:** $35/month
- **Volume:** 50,000 emails per month
- **Daily Limit:** None
- **Best For:** Growing businesses, regular newsletters
- **Additional Features:**
  - Multiple custom sending domains (up to 1,000)
  - Email template builder
  - Extended log retention
  - Priority support

### 4. Scale Plan
- **Cost:** $90/month
- **Volume:** 100,000 emails per month
- **Daily Limit:** None
- **Best For:** High-volume senders, marketing campaigns
- **Additional Features:**
  - Dedicated IP pools
  - Send time optimization
  - Advanced analytics
  - Premium support

---

## Bulk Send API

### Is There a Bulk Send API?

**Yes!** Mailgun provides a bulk sending API that is **accessible on the free plan**. The API supports multiple methods for sending to multiple recipients:

#### Method 1: Multiple Recipients in Single API Call
You can send to multiple recipients in a single API request by passing comma-separated email addresses in the `to` field:

```python
POST https://api.mailgun.net/v3/{domain}/messages
{
  "from": "sender@example.com",
  "to": "user1@example.com,user2@example.com,user3@example.com",
  "subject": "Bulk Email",
  "html": "<html>...</html>",
  "text": "Plain text version"
}
```

**Limitations:**
- All recipients see each other's email addresses (not ideal for privacy)
- Limited to ~1,000 recipients per API call (Mailgun recommendation)
- Still counts against daily limit (100 emails/day on free plan)

#### Method 2: Recipient Variables (Personalized Bulk Sending)
For personalized bulk emails, use recipient variables:

```python
POST https://api.mailgun.net/v3/{domain}/messages
{
  "from": "sender@example.com",
  "to": ["user1@example.com", "user2@example.com", "user3@example.com"],
  "subject": "Hello %recipient.name%",
  "html": "<html>Hi %recipient.name%...</html>",
  "recipient-variables": {
    "user1@example.com": {"name": "John"},
    "user2@example.com": {"name": "Jane"},
    "user3@example.com": {"name": "Bob"}
  }
}
```

**Benefits:**
- Each recipient receives a personalized email
- Recipients don't see other recipients' addresses
- Better for newsletters and marketing emails

#### Method 3: Batch Sending (Current Script Implementation)
Your current script sends emails one at a time in a loop, which works but is slower:

```python
# Current approach: One API call per recipient
for recipient in recipients:
    send_email(to=recipient, ...)
    time.sleep(1)  # Rate limiting
```

**Note:** This approach works but is less efficient than using Mailgun's bulk API methods above.

### Free Plan Access

✅ **Yes, bulk send API is accessible on the free plan**
- All bulk sending methods work on free plan
- Same API endpoints and features
- Only limitation is the **100 emails/day volume cap**

---

## Bulk Sending on Free Plan

### Can You Do Bulk Sends?

**Yes, but with significant limitations:**

1. **Volume Limit:** Maximum 100 emails per day
   - This means you can send to up to 100 recipients in a single day
   - If you need to send to more recipients, you'd need to spread it across multiple days
   - Example: 500 recipients = 5 days of sending

2. **Rate Limiting:** 
   - According to the email-sender skill documentation, Mailgun free tier has a rate limit of 100 emails/hour
   - The daily limit is 100 emails total
   - Scripts should implement delays (1 second between sends recommended)

3. **Technical Capability:**
   - The Mailgun API supports bulk sending on all plans
   - You can send to multiple recipients in a single API call
   - Batch sending is supported
   - The limitation is purely volume-based, not feature-based

### Free Plan Bulk Sending Scenarios

| Scenario | Feasible on Free Plan? | Notes |
|----------|----------------------|-------|
| 50 recipients | ✅ Yes | Well within daily limit |
| 100 recipients | ✅ Yes | Exactly at daily limit |
| 200 recipients | ⚠️ Partial | Requires 2 days |
| 1,000 recipients | ❌ Not practical | Requires 10 days |
| Weekly newsletter (500 subs) | ⚠️ Possible but slow | 5 days to send |

---

## Core Capabilities Across Plans

### API Features (Available on All Plans)
- RESTful API
- SMTP relay
- Webhooks for events (delivered, bounced, opened, clicked)
- Email validation
- Route management
- Suppression lists (bounces, unsubscribes, complaints)
- Message storage and retrieval
- Analytics and tracking

### Advanced Features (Paid Plans)
- **Multiple Sending Domains:** Foundation+ plans support multiple custom domains
- **Email Template Builder:** Foundation+ plans include template builder
- **Dedicated IP Pools:** Scale plan provides dedicated IP addresses
- **Send Time Optimization:** Scale plan optimizes delivery times
- **Extended Log Retention:** Longer retention on paid plans
- **Priority Support:** Better support tiers on paid plans

---

## Rate Limiting and Best Practices

### Rate Limits
- **Free Plan:** 100 emails/hour, 100 emails/day
- **Paid Plans:** Higher limits (varies by plan)
- **Best Practice:** Implement 1-second delays between sends to avoid hitting rate limits

### Bulk Sending Best Practices
1. **Batch Processing:** Send in batches rather than all at once
2. **Retry Logic:** Implement exponential backoff for failed sends
3. **Error Handling:** Track bounces, unsubscribes, and failures
4. **Compliance:** Include unsubscribe links, respect opt-outs
5. **Testing:** Always test with small batches first
6. **Monitoring:** Track delivery rates, opens, clicks

---

## Comparison: Free vs Paid Plans

| Feature | Free Plan | Basic Plan ($15) | Foundation Plan ($35) | Scale Plan ($90) |
|---------|-----------|------------------|----------------------|------------------|
| **Monthly Volume** | ~3,000 | 10,000 | 50,000 | 100,000 |
| **Daily Limit** | 100/day | None | None | None |
| **Bulk Sending** | ✅ Yes (limited) | ✅ Yes | ✅ Yes | ✅ Yes |
| **API Access** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Webhooks** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Multiple Domains** | ❌ No | ❌ No | ✅ Yes (1,000) | ✅ Yes |
| **Template Builder** | ❌ No | ❌ No | ✅ Yes | ✅ Yes |
| **Dedicated IPs** | ❌ No | ❌ No | ❌ No | ✅ Yes |
| **Send Optimization** | ❌ No | ❌ No | ❌ No | ✅ Yes |
| **Support** | Basic | Email | Priority | Premium |

---

## Recommendations

### Use Free Plan If:
- You're testing or developing
- You send fewer than 100 emails per day
- You don't need advanced features
- You're okay with spreading bulk sends across multiple days

### Upgrade to Basic Plan ($15/month) If:
- You need to send more than 100 emails per day
- You want to send bulk campaigns without daily restrictions
- You need better deliverability
- You send 10,000 or fewer emails per month

### Upgrade to Foundation Plan ($35/month) If:
- You send 10,000-50,000 emails per month
- You need multiple sending domains
- You want email templates
- You need extended log retention

### Upgrade to Scale Plan ($90/month) If:
- You send 50,000-100,000 emails per month
- You need dedicated IP addresses
- You want send time optimization
- You require premium support

---

## Integration Notes

Based on the existing `email-sender` skill in this workspace:

- **Current Setup:** Uses Mailgun API with domain `quanthub.ai`
- **Script Location:** `~/.claude/skills/email-sender/scripts/email_sender.py`
- **Features Implemented:**
  - Bulk sending to subscriber lists
  - Retry logic with exponential backoff
  - Failed send tracking
  - Newsletter archiving
  - Rate limiting compliance (1 second delays)

**Current Rate Limiting Implementation:**
- Script implements 1 second delay between sends
- Batch size configurable (default: 50)
- Respects Mailgun free tier: 100 emails/hour

**Current Implementation Analysis:**
- Your script currently sends emails **one at a time** in a loop
- This works but is less efficient than Mailgun's bulk API
- Each email = 1 API call = slower sending
- For 500 recipients = 500 API calls (with 1 second delays = ~8+ minutes)

**Optimization Opportunity:**
You could optimize the script to use Mailgun's bulk API by:
1. Using recipient variables for personalized bulk sends
2. Sending to multiple recipients per API call (up to 1,000 per call)
3. Reducing from 500 API calls to ~1 API call for 500 recipients
4. Much faster sending (seconds instead of minutes)

**Example Optimized Approach:**
```python
# Instead of 500 individual API calls:
for recipient in recipients:
    send_email(to=recipient, ...)  # 500 API calls

# Use bulk API (1 API call for all recipients):
send_bulk_email(
    recipients=recipients,  # All 500 at once
    recipient_variables={...},  # Personalized data
    ...
)  # 1 API call
```

**Note:** Even with optimized bulk API, free plan still limits to 100 emails/day total.

---

## Sources

- Mailgun Pricing Page: https://www.mailgun.com/pricing
- Mailgun Free Plan Documentation: https://help.mailgun.com/hc/en-us/articles/203068914-What-does-the-Free-plan-offer-
- Email Sender Skill: `~/.claude/skills/email-sender/SKILL.md`

---

## Conclusion

**Can you do bulk sends with the free plan?** Yes, technically you can, but you're limited to 100 emails per day. This means:

- ✅ Small bulk sends (≤100 recipients): Fully supported
- ⚠️ Medium bulk sends (100-500 recipients): Possible but requires multiple days
- ❌ Large bulk sends (500+ recipients): Not practical on free plan

For any serious bulk email campaigns, upgrading to at least the Basic plan ($15/month) is recommended to remove daily restrictions and improve deliverability.

