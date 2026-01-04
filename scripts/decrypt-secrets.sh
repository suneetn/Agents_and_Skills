#!/bin/bash
# Decrypt and load secrets into current shell
# Usage: source ./scripts/decrypt-secrets.sh

ENCRYPTED_FILE="secrets.age"
SECRETS_FILE=".secrets.txt"

if [ ! -f "$ENCRYPTED_FILE" ]; then
    echo "❌ $ENCRYPTED_FILE not found"
    echo "   Run ./scripts/encrypt-secrets.sh first"
    return 1 2>/dev/null || exit 1
fi

echo "🔓 Decrypting secrets..."
age -d "$ENCRYPTED_FILE" > "$SECRETS_FILE"

if [ $? -eq 0 ]; then
    source "$SECRETS_FILE"
    rm "$SECRETS_FILE"  # Clean up plaintext immediately
    echo "✅ Secrets loaded into environment"
    echo "   FMP_API_KEY: ${FMP_API_KEY:0:8}..."
    echo "   MAILGUN_DOMAIN: $MAILGUN_DOMAIN"
else
    echo "❌ Decryption failed"
    return 1 2>/dev/null || exit 1
fi

