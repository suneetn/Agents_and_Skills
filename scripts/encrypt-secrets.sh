#!/bin/bash
# Encrypt secrets for cross-platform sync
# Usage: ./scripts/encrypt-secrets.sh

set -e

SECRETS_FILE=".secrets.txt"
ENCRYPTED_FILE="secrets.age"

if [ ! -f "$SECRETS_FILE" ]; then
    echo "Creating $SECRETS_FILE template..."
    cat > "$SECRETS_FILE" << 'EOF'
# API Keys for Agents_and_Skills
# After editing, run: ./scripts/encrypt-secrets.sh

export FMP_API_KEY="your_fmp_key_here"
export MAILGUN_API_KEY="your_mailgun_key_here"
export MAILGUN_DOMAIN="mail.quanthub.ai"
EOF
    echo "✏️  Edit $SECRETS_FILE with your keys, then run this script again"
    exit 0
fi

echo "🔐 Encrypting $SECRETS_FILE..."
echo "   You'll be prompted for a password (remember it!)"
echo ""

age -p "$SECRETS_FILE" > "$ENCRYPTED_FILE"

echo ""
echo "✅ Created $ENCRYPTED_FILE"
echo ""
echo "Next steps:"
echo "  1. Delete the plaintext: rm $SECRETS_FILE"
echo "  2. Commit encrypted file: git add $ENCRYPTED_FILE && git commit -m 'Add encrypted secrets'"
echo "  3. Push: git push"



