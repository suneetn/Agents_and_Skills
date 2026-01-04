# Setup Guide

This guide helps you set up API keys on any platform (Mac, Linux, Windows).

## Required API Keys

| Key | Purpose | Get it from |
|-----|---------|-------------|
| `FMP_API_KEY` | Stock data (Financial Modeling Prep) | https://financialmodelingprep.com/ |
| `MAILGUN_API_KEY` | Email sending | https://www.mailgun.com/ |
| `MAILGUN_DOMAIN` | Email domain (default: `mail.quanthub.ai`) | Your Mailgun account |

---

## Cross-Platform Setup (Recommended)

Uses `age` encryption - works on Mac, Linux, and Windows.

### Step 1: Install age

```bash
# Mac
brew install age

# Linux (Debian/Ubuntu)
sudo apt install age

# Windows (using scoop)
scoop install age

# Or download from: https://github.com/FiloSottile/age/releases
```

### Step 2: First Time Setup (Creating Encrypted Secrets)

```bash
# Clone the repo
git clone https://github.com/suneetn/Agents_and_Skills.git
cd Agents_and_Skills

# Create and edit secrets file
./scripts/encrypt-secrets.sh
# Edit .secrets.txt with your actual keys
nano .secrets.txt

# Encrypt (choose a strong password!)
./scripts/encrypt-secrets.sh

# Clean up and commit
rm .secrets.txt
git add secrets.age
git commit -m "Add encrypted secrets"
git push
```

### Step 3: On a New Machine

```bash
# Clone the repo
git clone https://github.com/suneetn/Agents_and_Skills.git
cd Agents_and_Skills

# Option A: Load into current session only (no file created)
source ./scripts/decrypt-secrets.sh

# Option B: Create persistent .env file
./scripts/decrypt-secrets.sh --persist
```

### Step 4: Auto-load on Shell Startup

**If you used `--persist` (creates .env file):**

Add to `~/.zshrc` or `~/.bashrc`:
```bash
# Auto-load API keys from .env
set -a; source ~/Agents_and_Skills/.env 2>/dev/null; set +a
```

**If you prefer on-demand loading:**

Add an alias:
```bash
alias load-secrets='cd ~/Agents_and_Skills && source ./scripts/decrypt-secrets.sh && cd -'
```

Then run `load-secrets` when you need the keys.

---

## Alternative: iCloud Sync (Mac Only)

If you only use Macs with the same iCloud account:

```bash
# Create secrets folder in iCloud
mkdir -p ~/Library/Mobile\ Documents/com~apple~CloudDocs/secrets

# Create api-keys.sh
cat > ~/Library/Mobile\ Documents/com~apple~CloudDocs/secrets/api-keys.sh << 'EOF'
export FMP_API_KEY="your_key_here"
export MAILGUN_API_KEY="your_key_here"
export MAILGUN_DOMAIN="mail.quanthub.ai"
EOF

# Add to ~/.zshrc
echo 'source ~/Library/Mobile\ Documents/com~apple~CloudDocs/secrets/api-keys.sh 2>/dev/null' >> ~/.zshrc
```

---

## Skills Location

Skills are stored in `~/.claude/skills/` (not in this repo). They read API keys from environment variables automatically using `os.environ.get()`.

## Verify Everything Works

```bash
# Test stock screener
python3 ~/.claude/skills/stock-screener/scripts/stock_screener.py momentum --limit 3

# Test stock analyst  
python3 ~/.claude/skills/stock-analyst/scripts/stock_analysis_fmp.py AAPL
```

---

## Updating Secrets

If you need to update your keys:

```bash
# Decrypt to plaintext
age -d secrets.age > .secrets.txt

# Edit
nano .secrets.txt

# Re-encrypt (use same password!)
age -p .secrets.txt > secrets.age

# Clean up and commit
rm .secrets.txt
git add secrets.age
git commit -m "Update secrets"
git push
```
