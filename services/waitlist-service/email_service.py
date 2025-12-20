"""
Email service for sending waitlist and invite emails via SMTP
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """SMTP email service"""
    
    def __init__(self):
        self.smtp_host = os.getenv('SMTP_HOST', 'localhost')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.smtp_user = os.getenv('SMTP_USER', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        self.from_email = os.getenv('FROM_EMAIL', 'noreply@vobee.ai')
        self.from_name = os.getenv('FROM_NAME', 'VoBee Team')
        
        # For local development, log emails instead of sending
        self.debug_mode = os.getenv('EMAIL_DEBUG_MODE', 'true').lower() == 'true'
        
        logger.info(f"Email service initialized (debug_mode={self.debug_mode})")
    
    def send_email(self, to_email: str, subject: str, html_body: str, text_body: str = None):
        """
        Send an email via SMTP
        
        Args:
            to_email: Recipient email
            subject: Email subject
            html_body: HTML email body
            text_body: Plain text fallback (optional)
        """
        try:
            if self.debug_mode:
                logger.info(f"[EMAIL DEBUG] To: {to_email}")
                logger.info(f"[EMAIL DEBUG] Subject: {subject}")
                logger.info(f"[EMAIL DEBUG] Body:\n{html_body}")
                return True
            
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            
            # Add text and HTML parts
            if text_body:
                part1 = MIMEText(text_body, 'plain')
                msg.attach(part1)
            
            part2 = MIMEText(html_body, 'html')
            msg.attach(part2)
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                if self.smtp_user and self.smtp_password:
                    server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Email sent to {to_email}: {subject}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False
    
    def send_waitlist_confirmation(self, email: str, position: int, total_waiting: int, estimated_wait: str):
        """Send waitlist confirmation email"""
        subject = f"You're on the VoBee waitlist (#{position})"
        
        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #ffc107; padding: 20px; text-align: center; }}
        .content {{ background: #f9f9f9; padding: 30px; }}
        .info-box {{ background: white; padding: 15px; margin: 20px 0; border-left: 4px solid #ffc107; }}
        .footer {{ text-align: center; color: #666; padding: 20px; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐝 VoBee</h1>
        </div>
        <div class="content">
            <h2>Jste na waitlistu VoBee / You're on the VoBee waitlist</h2>
            <p>Díky za zájem o VoBee early access.</p>
            <p>Thank you for your interest in VoBee early access.</p>
            
            <div class="info-box">
                <strong>Vaše pozice / Your position:</strong> #{position}<br>
                <strong>Celkem čekajících / Current waitlist:</strong> {total_waiting} lidí / people<br>
                <strong>Odhadovaný čas / Estimated invite:</strong> {estimated_wait}
            </div>
            
            <p>Spouštíme pomalu, aby kvalita zůstala vysoká. Až vás pozveme, dostanete:</p>
            <p>We're launching slowly to keep quality high. When we invite you, you'll get:</p>
            
            <ul>
                <li>14denní zkušební období zdarma (bez kreditní karty) / 14-day free trial (no credit card)</li>
                <li>3 pozvánkové kódy ke sdílení / 3 invite codes to share</li>
                <li>Prioritní podpora / Priority support</li>
            </ul>
            
            <p>Pošleme email, až na vás přijde řada.</p>
            <p>We'll email when it's your turn.</p>
            
            <p><strong>– VoBee Team</strong></p>
        </div>
        <div class="footer">
            <p>© 2025 VoBee AI Assistant</p>
        </div>
    </div>
</body>
</html>
"""
        
        text_body = f"""
VoBee Waitlist Confirmation

Hi,

You're confirmed for VoBee early access.

Your position: #{position}
Current waitlist: {total_waiting} people
Estimated invite: {estimated_wait}

We're launching slowly to keep quality high. When we invite you, you'll get:
- 14-day free trial (no credit card)
- 3 invite codes to share
- Priority support

We'll email when it's your turn.

– VoBee Team
"""
        
        return self.send_email(email, subject, html_body, text_body)
    
    def send_invite_ready(self, email: str, code: str, expiration_date: str):
        """Send invite code ready email"""
        subject = "Your VoBee invite code is ready"
        
        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #ffc107; padding: 20px; text-align: center; }}
        .content {{ background: #f9f9f9; padding: 30px; }}
        .code-box {{ background: white; padding: 20px; margin: 20px 0; border: 2px solid #ffc107; text-align: center; font-size: 24px; font-weight: bold; letter-spacing: 2px; }}
        .button {{ display: inline-block; background: #ffc107; color: #1a1a2e; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
        .footer {{ text-align: center; color: #666; padding: 20px; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐝 VoBee</h1>
        </div>
        <div class="content">
            <h2>Váš VoBee přístup je připraven / Your VoBee early access is ready</h2>
            <p>Váš pozvánkový kód VoBee je připraven k použití.</p>
            <p>Your VoBee invite code is ready to use.</p>
            
            <div class="code-box">
                {code}
            </div>
            
            <p><strong>Co dál / What happens next:</strong></p>
            <ol>
                <li>Jděte na vobee.ai/redeem / Go to vobee.ai/redeem</li>
                <li>Zadejte kód + vytvořte heslo / Enter code + create password</li>
                <li>Začněte 14denní zkušební období / Start 14-day free trial</li>
            </ol>
            
            <p style="text-align: center;">
                <a href="https://vobee.ai/redeem" class="button">Aktivovat účet / Activate Account</a>
            </p>
            
            <p><strong>Kód vyprší / Code expires:</strong> {expiration_date}</p>
            
            <p>Po 14 dnech používání dostanete 3 pozvánkové kódy ke sdílení.</p>
            <p>After 14 days of usage, you'll get 3 invite codes to share.</p>
            
            <p><strong>– VoBee Team</strong></p>
        </div>
        <div class="footer">
            <p>© 2025 VoBee AI Assistant</p>
        </div>
    </div>
</body>
</html>
"""
        
        text_body = f"""
VoBee Invite Code Ready

Hi,

Your VoBee early access is ready.

Your invite code: {code}

What happens next:
1. Go to vobee.ai/redeem
2. Enter code + create password
3. Start 14-day free trial

Code expires: {expiration_date}

After 14 days of usage, you'll get 3 invite codes to share.

– VoBee Team
"""
        
        return self.send_email(email, subject, html_body, text_body)
