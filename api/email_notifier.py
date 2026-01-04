"""Email notification system for price drop alerts."""
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)


class EmailNotifier:
    """Send email notifications for price drops."""
    
    def __init__(self):
        """Initialize email notifier with SMTP settings."""
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.sender_email = os.getenv("SENDER_EMAIL", "")
        self.sender_password = os.getenv("SENDER_PASSWORD", "")  # App password for Gmail
        self.recipient_email = os.getenv("RECIPIENT_EMAIL", "")
        
        # Validate configuration
        if not self.sender_email or not self.sender_password or not self.recipient_email:
            raise ValueError(
                "Email configuration missing. Set SENDER_EMAIL, SENDER_PASSWORD, "
                "and RECIPIENT_EMAIL in .env file"
            )
    
    def create_price_drop_email(
        self,
        departure_date: str,
        return_date: str,
        current_price: float,
        previous_price: float,
        price_drop: float,
        currency: str,
        inbound_airport: str,
        outbound_airport: str,
        routing_description: str,
        flight_numbers: Optional[str] = None,
        airlines: Optional[str] = None,
        booking_url: Optional[str] = None
    ) -> MIMEMultipart:
        """Create email message for price drop alert."""
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"🔔 Flight Price Drop Alert: ${price_drop:.2f} Savings!"
        msg["From"] = self.sender_email
        msg["To"] = self.recipient_email
        
        # Email body (HTML)
        html_body = f"""
        <html>
          <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
              <h2 style="color: #2c3e50;">✈️ Flight Price Drop Alert</h2>
              
              <div style="background-color: #e8f5e9; border-left: 4px solid #4caf50; padding: 15px; margin: 20px 0;">
                <h3 style="margin-top: 0; color: #2e7d32;">💰 Price Dropped by {currency} ${price_drop:.2f}!</h3>
                <p style="font-size: 18px; margin: 10px 0;">
                  <strong>Previous Price:</strong> {currency} ${previous_price:.2f}<br>
                  <strong>Current Price:</strong> {currency} ${current_price:.2f}
                </p>
              </div>
              
              <div style="background-color: #f5f5f5; padding: 15px; margin: 20px 0; border-radius: 5px;">
                <h3 style="margin-top: 0;">📅 Trip Details</h3>
                <p><strong>Departure:</strong> {departure_date}</p>
                <p><strong>Return:</strong> {return_date}</p>
                <p><strong>Route:</strong> {routing_description}</p>
                <p><strong>Inbound Airport:</strong> {inbound_airport}</p>
                <p><strong>Outbound Airport:</strong> {outbound_airport}</p>
              </div>
              
              {f'<div style="background-color: #e3f2fd; padding: 15px; margin: 20px 0; border-radius: 5px;"><h3 style="margin-top: 0;">🛫 Flight Information</h3><p><strong>Flight Numbers:</strong> {flight_numbers}</p><p><strong>Airlines:</strong> {airlines}</p></div>' if flight_numbers or airlines else ''}
              
              {f'<div style="text-align: center; margin: 30px 0;"><a href="{booking_url}" style="background-color: #2196F3; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">🔗 Book Now</a></div>' if booking_url else '<p style="text-align: center; color: #666; font-style: italic;">Booking link will be available after flight selection</p>'}
              
              <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 12px;">
                <p>This is an automated alert from Flight Agent.</p>
                <p>Alert triggered when price drops by more than $10.</p>
              </div>
            </div>
          </body>
        </html>
        """
        
        # Plain text version
        text_body = f"""
Flight Price Drop Alert!

Price Dropped by {currency} ${price_drop:.2f}!

Previous Price: {currency} ${previous_price:.2f}
Current Price: {currency} ${current_price:.2f}

Trip Details:
- Departure: {departure_date}
- Return: {return_date}
- Route: {routing_description}
- Inbound Airport: {inbound_airport}
- Outbound Airport: {outbound_airport}

{f'Flight Numbers: {flight_numbers}' if flight_numbers else ''}
{f'Airlines: {airlines}' if airlines else ''}

{f'Booking URL: {booking_url}' if booking_url else ''}

This is an automated alert from Flight Agent.
Alert triggered when price drops by more than $10.
        """
        
        # Attach both versions
        msg.attach(MIMEText(text_body, "plain"))
        msg.attach(MIMEText(html_body, "html"))
        
        return msg
    
    def create_daily_report_email(
        self,
        date: str,
        best_price: float,
        currency: str,
        total_searches: int,
        alerts_count: int,
        price_history: List[Dict[str, Any]]
    ) -> MIMEMultipart:
        """Create daily summary email report."""
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"📊 Daily Flight Price Report - {date}"
        msg["From"] = self.sender_email
        msg["To"] = self.recipient_email
        
        # Build price history table
        history_rows = ""
        for record in price_history[:10]:  # Last 10 records
            history_rows += f"""
            <tr>
              <td>{record.get('departure_date', 'N/A')}</td>
              <td>{record.get('return_date', 'N/A')}</td>
              <td>{record.get('currency', 'USD')} ${record.get('total_price', 0):.2f}</td>
              <td>{record.get('routing_description', 'N/A')[:50]}</td>
            </tr>
            """
        
        html_body = f"""
        <html>
          <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
              <h2 style="color: #2c3e50;">📊 Daily Flight Price Report</h2>
              <p><strong>Date:</strong> {date}</p>
              
              <div style="background-color: #f5f5f5; padding: 15px; margin: 20px 0; border-radius: 5px;">
                <h3 style="margin-top: 0;">Summary</h3>
                <p><strong>Best Price Today:</strong> {currency} ${best_price:.2f}</p>
                <p><strong>Total Searches:</strong> {total_searches}</p>
                <p><strong>Price Drop Alerts:</strong> {alerts_count}</p>
              </div>
              
              <h3>Recent Price History</h3>
              <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                <thead>
                  <tr style="background-color: #2196F3; color: white;">
                    <th style="padding: 10px; text-align: left;">Departure</th>
                    <th style="padding: 10px; text-align: left;">Return</th>
                    <th style="padding: 10px; text-align: left;">Price</th>
                    <th style="padding: 10px; text-align: left;">Route</th>
                  </tr>
                </thead>
                <tbody>
                  {history_rows}
                </tbody>
              </table>
              
              <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 12px;">
                <p>This is an automated daily report from Flight Agent.</p>
              </div>
            </div>
          </body>
        </html>
        """
        
        msg.attach(MIMEText(html_body, "html"))
        return msg
    
    def send_email(self, msg: MIMEMultipart) -> bool:
        """
        Send email message.
        
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            return True
        except smtplib.SMTPAuthenticationError as e:
            error_msg = str(e)
            if "BadCredentials" in error_msg or "535" in error_msg:
                print(f"❌ Error sending email: Gmail authentication failed")
                print(f"   Gmail requires an App Password, not your regular password.")
                print(f"   To create an App Password:")
                print(f"   1. Go to: https://myaccount.google.com/apppasswords")
                print(f"   2. Sign in and create a new app password for 'Mail'")
                print(f"   3. Copy the 16-character password")
                print(f"   4. Update SENDER_PASSWORD in your .env file (or GitHub Secrets)")
                print(f"   5. Make sure 2-Step Verification is enabled on your Google account")
            else:
                print(f"❌ Error sending email: {e}")
            return False
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return False
    
    def send_price_drop_alert(
        self,
        departure_date: str,
        return_date: str,
        current_price: float,
        previous_price: float,
        price_drop: float,
        currency: str,
        inbound_airport: str,
        outbound_airport: str,
        routing_description: str,
        flight_numbers: Optional[str] = None,
        airlines: Optional[str] = None,
        booking_url: Optional[str] = None
    ) -> bool:
        """Send price drop alert email."""
        msg = self.create_price_drop_email(
            departure_date=departure_date,
            return_date=return_date,
            current_price=current_price,
            previous_price=previous_price,
            price_drop=price_drop,
            currency=currency,
            inbound_airport=inbound_airport,
            outbound_airport=outbound_airport,
            routing_description=routing_description,
            flight_numbers=flight_numbers,
            airlines=airlines,
            booking_url=booking_url
        )
        
        return self.send_email(msg)
    
    def send_daily_report(
        self,
        date: str,
        best_price: float,
        currency: str,
        total_searches: int,
        alerts_count: int,
        price_history: List[Dict[str, Any]]
    ) -> bool:
        """Send daily summary report email."""
        msg = self.create_daily_report_email(
            date=date,
            best_price=best_price,
            currency=currency,
            total_searches=total_searches,
            alerts_count=alerts_count,
            price_history=price_history
        )
        
        return self.send_email(msg)
