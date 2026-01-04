# Gmail App Password Setup

Gmail requires an **App Password** (not your regular password) for SMTP authentication.

## Steps to Create Gmail App Password

1. **Enable 2-Step Verification** (if not already enabled):
   - Go to: https://myaccount.google.com/security
   - Enable "2-Step Verification"

2. **Create App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Sign in with your Gmail account
   - Select "Mail" as the app
   - Select "Other (Custom name)" as the device
   - Enter "Flight Agent" as the name
   - Click "Generate"
   - Copy the 16-character password (spaces don't matter)

3. **Update Your Configuration**:
   - **Local `.env` file**: Update `SENDER_PASSWORD` with the App Password
   - **GitHub Secrets**: Update `SENDER_PASSWORD` secret with the App Password

## Example

```
SENDER_EMAIL=your.email@gmail.com
SENDER_PASSWORD=abcd efgh ijkl mnop  # 16-character App Password (spaces optional)
```

## Important Notes

- **Never use your regular Gmail password** - it won't work
- App Passwords are 16 characters (may include spaces)
- You can revoke App Passwords anytime from the same page
- Each App Password is unique and can only be used once

## Troubleshooting

If you still get authentication errors:
- Verify 2-Step Verification is enabled
- Make sure you copied the entire 16-character password
- Check that "Less secure app access" is NOT the issue (App Passwords replace this)
- Try generating a new App Password
