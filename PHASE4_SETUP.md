# Phase 4: Automation & Notification - Setup Guide

## ✅ Completed Features

### 1. Email Notifications (`api/email_notifier.py`)
- **Price Drop Alerts**: Sends email when price drops > $10
- **Daily Reports**: Sends summary email with best prices
- **HTML Email Templates**: Beautiful formatted emails with flight details

### 2. GitHub Actions Workflow (`.github/workflows/daily_tracking.yml`)
- **Daily Execution**: Runs at 8:00 AM UTC (configurable)
- **Manual Trigger**: Can be triggered manually via GitHub UI
- **Database Backup**: Uploads database as artifact

### 3. Automated Script (`api/phase4_automated.py`)
- Runs tracking for all dates
- Sends email alerts for price drops
- Sends daily summary report

## Email Configuration

### Step 1: Add Email Settings to `.env`

Add these to your `.env` file:

```env
# Email Configuration
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password  # Gmail App Password, not regular password
RECIPIENT_EMAIL=recipient@example.com

# Optional SMTP settings (defaults to Gmail)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

### Step 2: Gmail App Password Setup

For Gmail:
1. Go to Google Account settings
2. Security → 2-Step Verification (must be enabled)
3. App passwords → Generate new app password
4. Use the generated password (not your regular password)

For other email providers:
- **Outlook**: `smtp-mail.outlook.com:587`
- **Yahoo**: `smtp.mail.yahoo.com:587`
- **Custom**: Set `SMTP_SERVER` and `SMTP_PORT` in `.env`

## GitHub Actions Setup

### Step 1: Add Secrets to GitHub

Go to your repository → Settings → Secrets and variables → Actions

Add these secrets:
- `AMADEUS_API_KEY` - Your Amadeus API key
- `AMADEUS_API_SECRET` - Your Amadeus API secret
- `AMADEUS_ENV` - `test` or `production` (optional, defaults to `test`)
- `SENDER_EMAIL` - Email address to send from
- `SENDER_PASSWORD` - Email app password
- `RECIPIENT_EMAIL` - Email address to receive alerts
- `SMTP_SERVER` - SMTP server (optional, defaults to Gmail)
- `SMTP_PORT` - SMTP port (optional, defaults to 587)

### Step 2: Adjust Schedule (Optional)

Edit `.github/workflows/daily_tracking.yml` to change the schedule:

```yaml
schedule:
  - cron: '0 8 * * *'  # 8:00 AM UTC daily
```

Cron format: `minute hour day month weekday`
- `0 8 * * *` = 8:00 AM UTC daily
- `0 0 * * *` = Midnight UTC daily
- `0 8 * * 1-5` = 8:00 AM UTC, weekdays only

### Step 3: Test Workflow

1. Push the workflow file to GitHub
2. Go to Actions tab in your repository
3. Click "Daily Flight Price Tracking"
4. Click "Run workflow" to test manually

## Local Testing

### Test Email Notifications

```bash
# Run automated tracking (will send emails if configured)
python api/phase4_automated.py
```

### Test Email Only

```bash
python -c "
from api.email_notifier import EmailNotifier
notifier = EmailNotifier()
notifier.send_price_drop_alert(
    departure_date='2026-04-03',
    return_date='2026-04-09',
    current_price=200.00,
    previous_price=250.00,
    price_drop=50.00,
    currency='USD',
    inbound_airport='DCA',
    outbound_airport='JFK',
    routing_description='SAN → DC / NYC → SAN',
    flight_numbers='AA123, DL456',
    airlines='American Airlines, Delta'
)
"
```

## Email Features

### Price Drop Alert Email Includes:
- Price drop amount (highlighted)
- Previous vs current price
- Trip dates and route
- Flight numbers and airlines
- Booking URL (if available)
- Beautiful HTML formatting

### Daily Report Email Includes:
- Best price for the day
- Total searches performed
- Number of alerts triggered
- Recent price history table

## Alert Logic

Alerts are sent when:
- Price drops by more than $10 (configurable in `config.json`)
- Compared against last checked price (not daily best)
- Email notifications are properly configured

## Troubleshooting

### Email Not Sending
1. Check `.env` file has all email settings
2. Verify Gmail App Password (not regular password)
3. Check 2-Step Verification is enabled (for Gmail)
4. Test SMTP connection manually

### GitHub Actions Not Running
1. Check workflow file is in `.github/workflows/`
2. Verify all secrets are set
3. Check Actions tab for error messages
4. Ensure workflow file syntax is correct

### Database Not Persisting
- GitHub Actions uploads database as artifact
- Download from Actions → Artifacts
- Or use GitHub Actions to commit database (not recommended for large files)

## Next Steps (Phase 5)

- Itinerary suggestions based on cheapest flights
- Cherry Blossom Festival date integration
- Hotel recommendations
