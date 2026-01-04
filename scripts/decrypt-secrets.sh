#!/bin/bash
# Decrypt and load secrets
# 
# Usage:
#   source ./scripts/decrypt-secrets.sh          # Load into current session only
#   ./scripts/decrypt-secrets.sh --persist       # Create .env file for auto-loading

ENCRYPTED_FILE="secrets.age"
ENV_FILE=".env"
TEMP_FILE=".secrets.txt"

if [ ! -f "$ENCRYPTED_FILE" ]; then
    echo "❌ $ENCRYPTED_FILE not found"
    echo "   Run ./scripts/encrypt-secrets.sh first"
    return 1 2>/dev/null || exit 1
fi

echo "🔓 Decrypting secrets..."
age -d "$ENCRYPTED_FILE" > "$TEMP_FILE"

if [ $? -ne 0 ]; then
    echo "❌ Decryption failed"
    rm -f "$TEMP_FILE"
    return 1 2>/dev/null || exit 1
fi

# Check if --persist flag is passed
if [ "$1" = "--persist" ]; then
    # Create .env file (without 'export' for dotenv compatibility)
    sed 's/^export //' "$TEMP_FILE" | grep -v '^#' | grep -v '^$' > "$ENV_FILE"
    rm "$TEMP_FILE"
    echo "✅ Created $ENV_FILE"
    echo ""
    echo "Add to ~/.zshrc or ~/.bashrc to auto-load:"
    echo "  set -a; source $(pwd)/$ENV_FILE; set +a"
    echo ""
    echo "Or for this session only:"
    echo "  set -a; source $ENV_FILE; set +a"
else
    # Load into current session only
    source "$TEMP_FILE"
    rm "$TEMP_FILE"
    echo "✅ Secrets loaded into current session"
    echo "   FMP_API_KEY: ${FMP_API_KEY:0:8}..."
    echo "   MAILGUN_DOMAIN: $MAILGUN_DOMAIN"
    echo ""
    echo "💡 To create persistent .env file, run:"
    echo "   ./scripts/decrypt-secrets.sh --persist"
fi
