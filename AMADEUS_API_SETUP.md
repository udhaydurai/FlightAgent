# Amadeus API Setup Guide

## Overview
The Amadeus API provides access to flight search, booking, and travel data. You need to create a free developer account to get your API credentials.

## Step-by-Step Setup

### Step 1: Create Amadeus Developer Account

1. **Visit the Amadeus for Developers website:**
   - Go to: https://developers.amadeus.com/

2. **Sign up for a free account:**
   - Click "Sign Up" or "Get Started"
   - Fill in your details (name, email, company)
   - Verify your email address

### Step 2: Create a New App

1. **Log in to your Amadeus account**

2. **Navigate to "My Self-Service Workspace"**
   - This is usually in the dashboard or top navigation

3. **Create a new application:**
   - Click "Create New App" or "Add App"
   - Fill in the application details:
     - **App Name**: e.g., "Flight Agent" or "Spring Break Travel"
     - **Description**: Brief description of your project
     - **Callback URL**: Can be `http://localhost` for testing
     - **Category**: Select "Travel" or "Other"

4. **Submit the application**

### Step 3: Get Your API Credentials

After creating the app, you'll see:
- **API Key** (also called Client ID)
- **API Secret** (also called Client Secret)

**Important:** Copy these immediately - you won't be able to see the secret again!

### Step 4: Choose Your Environment

Amadeus offers two environments:

1. **Test Environment** (Recommended for development)
   - Free tier with limited requests
   - Perfect for testing and development
   - Use `AMADEUS_ENV=test` in your `.env` file

2. **Production Environment**
   - Requires approval/upgrade
   - For live applications
   - Use `AMADEUS_ENV=production` in your `.env` file

### Step 5: Add Credentials to Your Project

1. **Create `.env` file** (if it doesn't exist):
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file** and add your credentials:
   ```env
   AMADEUS_API_KEY=your_actual_api_key_here
   AMADEUS_API_SECRET=your_actual_api_secret_here
   AMADEUS_ENV=test
   ```

3. **Never commit `.env` to git!**
   - It's already in `.gitignore`
   - Keep your credentials secure

## Testing Your API Keys

Once you've added your credentials, test the connection:

```bash
python api/test_connection.py
```

Or run the comprehensive Phase 1 test:

```bash
python api/test_phase1.py
```

## Free Tier Limits

The Amadeus test environment typically includes:
- Limited number of API calls per month
- Access to flight search APIs
- Test data (not real-time pricing in test mode)

Check your Amadeus dashboard for current limits and usage.

## Troubleshooting

### "Invalid credentials" error
- Double-check your API Key and Secret
- Make sure there are no extra spaces
- Verify you're using the correct environment (test vs production)

### "Rate limit exceeded"
- You've hit the free tier limit
- Wait for the limit to reset or upgrade your plan

### "API not available"
- Check Amadeus status page
- Verify your account is active
- Ensure you're using the correct API endpoint

## Resources

- **Amadeus Developer Portal**: https://developers.amadeus.com/
- **API Documentation**: https://developers.amadeus.com/self-service
- **Support**: Available through the developer portal

## Security Best Practices

1. ✅ Never commit `.env` file to version control
2. ✅ Don't share your API keys publicly
3. ✅ Use test environment for development
4. ✅ Rotate keys if they're accidentally exposed
5. ✅ Monitor your API usage in the Amadeus dashboard
