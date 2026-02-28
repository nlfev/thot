#!/usr/bin/env python3
"""
Test email configuration and send a test email.

Usage:
    python scripts/test_email.py [recipient_email]

If no recipient email is provided, sends to SMTP_USER email.
"""

import sys
import os
from pathlib import Path

# Add backend root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
from config import config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load .env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

def test_email_config():
    """Test SMTP configuration."""
    print("=" * 60)
    print("EMAIL CONFIGURATION TEST")
    print("=" * 60)
    
    print(f"\n📧 SMTP Server: {config.SMTP_SERVER}")
    print(f"📧 SMTP Port: {config.SMTP_PORT}")
    print(f"📧 SMTP User: {config.SMTP_USER}")
    print(f"📧 From Email: {config.SMTP_FROM_EMAIL}")
    print(f"📧 From Name: {config.SMTP_FROM_NAME}")
    
    if not config.SMTP_USER or not hasattr(config, 'SMTP_PASSWORD'):
        print("\n❌ ERROR: SMTP_USER or SMTP_PASSWORD not configured in .env")
        return False
    
    if config.SMTP_USER == "your-email@gmail.com":
        print("\n⚠️  WARNING: SMTP credentials appear to be default/placeholder values")
        print("   Please configure SMTP_USER and SMTP_PASSWORD in .env")
        return False
    
    return True


def test_smtp_connection():
    """Test SMTP connection."""
    print("\n" + "=" * 60)
    print("TESTING SMTP CONNECTION")
    print("=" * 60)
    
    try:
        print(f"\n⏳ Connecting to {config.SMTP_SERVER}:{config.SMTP_PORT}...")
        
        if config.SMTP_PORT == 587:
            # TLS connection
            server = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT, timeout=10)
            server.starttls()
            print("✅ TLS connection established")
        elif config.SMTP_PORT == 465:
            # SSL connection
            server = smtplib.SMTP_SSL(config.SMTP_SERVER, config.SMTP_PORT, timeout=10)
            print("✅ SSL connection established")
        else:
            # Regular SMTP
            server = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT, timeout=10)
            print(f"✅ SMTP connection established on port {config.SMTP_PORT}")
        
        print(f"\n⏳ Authenticating as {config.SMTP_USER}...")
        server.login(config.SMTP_USER, config.SMTP_PASSWORD)
        print("✅ Authentication successful")
        
        server.quit()
        print("\n✅ SMTP connection test PASSED")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"\n❌ AUTH FAILED: {e}")
        print("   Check your SMTP_USER and SMTP_PASSWORD in .env")
        return False
    except smtplib.SMTPException as e:
        print(f"\n❌ SMTP ERROR: {e}")
        return False
    except Exception as e:
        print(f"\n❌ CONNECTION ERROR: {e}")
        print("   Check SMTP_SERVER and SMTP_PORT in .env")
        return False


def send_test_email(recipient: str = None):
    """Send a test email."""
    if recipient is None:
        recipient = config.SMTP_USER
    
    print("\n" + "=" * 60)
    print("SENDING TEST EMAIL")
    print("=" * 60)
    
    try:
        print(f"\n⏳ Sending test email to {recipient}...")
        
        # Create message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "NLF Database - Email Configuration Test"
        msg["From"] = f"{config.SMTP_FROM_NAME} <{config.SMTP_FROM_EMAIL}>"
        msg["To"] = recipient
        
        # Text version
        text = f"""
Hello,

This is a test email from the NLF Database application.

If you received this email, your SMTP configuration is working correctly!

Configuration Details:
- SMTP Server: {config.SMTP_SERVER}:{config.SMTP_PORT}
- From: {config.SMTP_FROM_EMAIL}
- Recipient: {recipient}
- Environment: {os.getenv('ENVIRONMENT', 'development')}

Best regards,
NLF Database System
        """
        
        # HTML version
        html = f"""
<html>
  <body>
    <h2>NLF Database - Email Configuration Test</h2>
    <p>Hello,</p>
    <p>This is a test email from the NLF Database application.</p>
    <p><strong>If you received this email, your SMTP configuration is working correctly!</strong></p>
    
    <h3>Configuration Details:</h3>
    <ul>
      <li>SMTP Server: {config.SMTP_SERVER}:{config.SMTP_PORT}</li>
      <li>From: {config.SMTP_FROM_EMAIL}</li>
      <li>Recipient: {recipient}</li>
      <li>Environment: {os.getenv('ENVIRONMENT', 'development')}</li>
    </ul>
    
    <p>Best regards,<br/>NLF Database System</p>
  </body>
</html>
        """
        
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        msg.attach(part1)
        msg.attach(part2)
        
        # Send email
        if config.SMTP_PORT == 587:
            server = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT, timeout=10)
            server.starttls()
        elif config.SMTP_PORT == 465:
            server = smtplib.SMTP_SSL(config.SMTP_SERVER, config.SMTP_PORT, timeout=10)
        else:
            server = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT, timeout=10)
        
        server.login(config.SMTP_USER, config.SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Test email sent successfully to {recipient}")
        return True
        
    except Exception as e:
        print(f"❌ ERROR sending email: {e}")
        return False


def main():
    """Run all tests."""
    print("\n")
    
    # Test configuration
    if not test_email_config():
        print("\n❌ Configuration test failed")
        return 1
    
    # Test connection
    if not test_smtp_connection():
        print("\n❌ Connection test failed")
        return 1
    
    # Send test email
    recipient = sys.argv[1] if len(sys.argv) > 1 else None
    if not send_test_email(recipient):
        print("\n❌ Email send test failed")
        return 1
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED - Email configuration is working!")
    print("=" * 60)
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
