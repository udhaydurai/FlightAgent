#!/bin/bash
# Quick script to check and setup SSH for GitHub

echo "=========================================="
echo "GitHub SSH Key Check for udhaydurai"
echo "=========================================="
echo ""

# Check if SSH key exists
if [ -f ~/.ssh/id_rsa.pub ]; then
    echo "✅ SSH key found: ~/.ssh/id_rsa.pub"
    echo ""
    echo "Your public key:"
    echo "----------------------------------------"
    cat ~/.ssh/id_rsa.pub
    echo "----------------------------------------"
    echo ""
    echo "📋 Copy the key above (starts with 'ssh-rsa')"
    echo ""
else
    echo "❌ No SSH key found"
    echo ""
    echo "Generate a new key with:"
    echo "  ssh-keygen -t ed25519 -C 'udhayakumar.d@gmail.com'"
    exit 1
fi

echo "Next steps:"
echo "1. Go to: https://github.com/settings/keys"
echo "2. Click 'New SSH key'"
echo "3. Paste the key above"
echo "4. Title: 'FlightAgent Mac'"
echo "5. Click 'Add SSH key'"
echo ""
echo "Then test with:"
echo "  ssh -T git@github.com"
echo ""
echo "Expected: 'Hi udhaydurai! You've successfully authenticated...'"
echo ""
