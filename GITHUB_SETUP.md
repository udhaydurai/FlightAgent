# GitHub Repository Setup Guide

## Step 1: Create Repository on GitHub

1. Go to https://github.com/new
2. **Repository name**: `FlightAgent`
3. **Description**: `Automated flight price tracking agent for East Coast Spring Break trip`
4. Choose **Public** or **Private**
5. **DO NOT** check:
   - ❌ Add a README file
   - ❌ Add .gitignore
   - ❌ Choose a license
6. Click **"Create repository"**

## Step 2: Initialize Local Repository

Run the setup script:

```bash
./setup_github.sh
```

Or manually:

```bash
# Initialize git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Flight Agent - Phases 1-4 complete

- Phase 1: Environment & API Foundation
- Phase 2: Flexible Multi-City Search Engine
- Phase 3: Memory & Comparison (SQLite database)
- Phase 4: Automation & Notification (Email alerts, GitHub Actions)"
```

## Step 3: Connect to GitHub

```bash
# Set main branch
git branch -M main

# Add remote
git remote add origin https://github.com/udhaydurai/FlightAgent.git

# Push to GitHub
git push -u origin main
```

## Step 4: Add GitHub Secrets

Go to your repository → **Settings** → **Secrets and variables** → **Actions**

Add these secrets:

### Required Secrets:
- `AMADEUS_API_KEY` - Your Amadeus API key
- `AMADEUS_API_SECRET` - Your Amadeus API secret
- `SENDER_EMAIL` - Email address to send from
- `SENDER_PASSWORD` - Email app password (Gmail App Password)
- `RECIPIENT_EMAIL` - Email address to receive alerts

### Optional Secrets:
- `AMADEUS_ENV` - `test` or `production` (defaults to `test`)
- `SMTP_SERVER` - SMTP server (defaults to `smtp.gmail.com`)
- `SMTP_PORT` - SMTP port (defaults to `587`)

## Step 5: Verify GitHub Actions

1. Go to **Actions** tab in your repository
2. You should see "Daily Flight Price Tracking" workflow
3. Click on it and select **"Run workflow"** to test
4. The workflow will run daily at 8:00 AM UTC

## Important Notes

### Files NOT Committed (Protected by .gitignore):
- ✅ `.env` - Contains API keys and secrets
- ✅ `travel_tracker.db` - Database file
- ✅ `venv/` - Virtual environment
- ✅ `node_modules/` - Node dependencies
- ✅ `.next/` - Next.js build files

### Files Committed:
- ✅ All source code
- ✅ Configuration files (config.json)
- ✅ GitHub Actions workflow
- ✅ Documentation

## Troubleshooting

### "Permission denied" error
- Make sure you have write access to the repository
- Check your GitHub authentication (SSH keys or HTTPS credentials)

### "Repository not found" error
- Verify the repository name matches exactly
- Check your GitHub username is correct
- Ensure repository exists on GitHub

### GitHub Actions not running
- Check all secrets are set
- Verify workflow file is in `.github/workflows/`
- Check Actions tab for error messages
