#!/bin/bash
# Setup script for GitHub repository

echo "=========================================="
echo "Setting up GitHub Repository: FlightAgent"
echo "=========================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Initialize git repository
if [ -d ".git" ]; then
    echo "⚠️  Git repository already initialized"
else
    echo "Initializing git repository..."
    git init
    echo "✅ Git repository initialized"
fi

# Add all files
echo ""
echo "Staging files..."
git add .

# Check if .env exists and warn
if [ -f ".env" ]; then
    echo ""
    echo "⚠️  WARNING: .env file exists"
    echo "   Make sure .env is in .gitignore (it should be)"
    echo "   Never commit API keys or secrets!"
fi

# Show what will be committed
echo ""
echo "Files to be committed:"
git status --short

echo ""
echo "=========================================="
echo "Next Steps:"
echo "=========================================="
echo ""
echo "1. Create repository on GitHub:"
echo "   - Go to https://github.com/new"
echo "   - Repository name: FlightAgent"
echo "   - Description: Flight price tracking agent for East Coast Spring Break trip"
echo "   - Choose Public or Private"
echo "   - DO NOT initialize with README, .gitignore, or license"
echo "   - Click 'Create repository'"
echo ""
echo "2. After creating, run these commands:"
echo ""
echo "   git commit -m 'Initial commit: Flight Agent - Phases 1-4 complete'"
echo ""
echo "   git branch -M main"
echo ""
echo "   git remote add origin https://github.com/udhaydurai/FlightAgent.git"
echo ""
echo "   git push -u origin main"
echo ""
echo "3. Add GitHub Secrets (Settings → Secrets and variables → Actions):"
echo "   - AMADEUS_API_KEY"
echo "   - AMADEUS_API_SECRET"
echo "   - SENDER_EMAIL"
echo "   - SENDER_PASSWORD"
echo "   - RECIPIENT_EMAIL"
echo ""
echo "=========================================="
