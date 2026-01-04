# Setup Guide

This guide helps you set up API keys on a new Mac.

## Required API Keys

| Key | Purpose | Get it from |
|-----|---------|-------------|
| `FMP_API_KEY` | Stock data (Financial Modeling Prep) | https://financialmodelingprep.com/ |
| `MAILGUN_API_KEY` | Email sending | https://www.mailgun.com/ |
| `MAILGUN_DOMAIN` | Email domain (default: `mail.quanthub.ai`) | Your Mailgun account |

## Setup (iCloud Sync Method)

If you're using iCloud across multiple Macs, keys sync automatically:

### 1. Create the secrets folder (first time only)
```bash
mkdir -p ~/Library/Mobile\ Documents/com~apple~CloudDocs/secrets
```

### 2. Create api-keys.sh
```bash
cat > ~/Library/Mobile\ Documents/com~apple~CloudDocs/secrets/api-keys.sh << 'EOF'
# API Keys - Synced via iCloud
export FMP_API_KEY="your_fmp_key_here"
export MAILGUN_API_KEY="your_mailgun_key_here"
export MAILGUN_DOMAIN="mail.quanthub.ai"
EOF
```

### 3. Add to ~/.zshrc
```bash
echo 'source ~/Library/Mobile\ Documents/com~apple~CloudDocs/secrets/api-keys.sh 2>/dev/null' >> ~/.zshrc
source ~/.zshrc
```

### 4. Verify
```bash
echo $FMP_API_KEY | head -c 8  # Should show first 8 chars
```

## Alternative: Local .env File

If you prefer a local `.env` file instead of iCloud:

```bash
# Create .env in project root (already in .gitignore)
cat > .env << 'EOF'
FMP_API_KEY=your_fmp_key_here
MAILGUN_API_KEY=your_mailgun_key_here
MAILGUN_DOMAIN=mail.quanthub.ai
EOF

# Add to ~/.zshrc to auto-load
echo 'set -a; source ~/personal/.env 2>/dev/null; set +a' >> ~/.zshrc
```

## Skills Location

Skills are stored in `~/.claude/skills/` (not in this repo). They read API keys from environment variables automatically.

## Verify Everything Works

```bash
# Test stock screener
python3 ~/.claude/skills/stock-screener/scripts/stock_screener.py momentum --limit 3

# Test stock analyst
python3 ~/.claude/skills/stock-analyst/scripts/stock_analysis_fmp.py AAPL
```

