import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os

class EmailService:
    """Service for sending emails"""
    
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.from_email = os.getenv("FROM_EMAIL", self.smtp_username)
    
    def send_email(self, to_email, subject, body, html_body=None, attachment=None):
        """
        Send an email
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Plain text email body
            html_body: HTML email body (optional)
            attachment: File attachment as bytes (optional)
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add plain text part
            text_part = MIMEText(body, 'plain')
            msg.attach(text_part)
            
            # Add HTML part if provided
            if html_body:
                html_part = MIMEText(html_body, 'html')
                msg.attach(html_part)
            
            # Add attachment if provided
            if attachment:
                att = MIMEApplication(attachment, _subtype="pdf")
                att.add_header('Content-Disposition', 'attachment', filename='seo_report.pdf')
                msg.attach(att)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False
    
    def send_welcome_email(self, to_email, username):
        """Send welcome email to new users"""
        subject = "Welcome to Nexus SEO Intelligence!"
        
        body = f"""
Hello {username},

Welcome to Nexus SEO Intelligence!

We're excited to have you on board. With Nexus SEO, you can:
- Perform comprehensive SEO audits
- Generate detailed reports
- Track your website's performance
- Optimize your search engine rankings

To get started, log in to your account and run your first SEO scan.

If you have any questions, feel free to reach out to our support team.

Best regards,
The Nexus SEO Team
"""
        
        html_body = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <h2 style="color: #1f77b4;">Welcome to Nexus SEO Intelligence!</h2>
    
    <p>Hello <strong>{username}</strong>,</p>
    
    <p>We're excited to have you on board. With Nexus SEO, you can:</p>
    
    <ul>
        <li>Perform comprehensive SEO audits</li>
        <li>Generate detailed reports</li>
        <li>Track your website's performance</li>
        <li>Optimize your search engine rankings</li>
    </ul>
    
    <p>To get started, log in to your account and run your first SEO scan.</p>
    
    <p>If you have any questions, feel free to reach out to our support team.</p>
    
    <p>Best regards,<br>
    <strong>The Nexus SEO Team</strong></p>
</body>
</html>
"""
        
        return self.send_email(to_email, subject, body, html_body)
    
    def send_scan_report(self, to_email, username, url, pdf_attachment=None):
        """Send scan report to user"""
        subject = f"SEO Report for {url}"
        
        body = f"""
Hello {username},

Your SEO scan for {url} is complete!

The detailed report is attached to this email. You can also view it anytime in your Nexus SEO dashboard.

Key features of your report:
- Overall SEO score
- Meta tags analysis
- Content optimization suggestions
- Technical SEO recommendations
- Performance metrics

If you have any questions about the report, please don't hesitate to contact us.

Best regards,
The Nexus SEO Team
"""
        
        html_body = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <h2 style="color: #1f77b4;">SEO Report Ready!</h2>
    
    <p>Hello <strong>{username}</strong>,</p>
    
    <p>Your SEO scan for <strong>{url}</strong> is complete!</p>
    
    <p>The detailed report is attached to this email. You can also view it anytime in your Nexus SEO dashboard.</p>
    
    <h3>Key features of your report:</h3>
    <ul>
        <li>Overall SEO score</li>
        <li>Meta tags analysis</li>
        <li>Content optimization suggestions</li>
        <li>Technical SEO recommendations</li>
        <li>Performance metrics</li>
    </ul>
    
    <p>If you have any questions about the report, please don't hesitate to contact us.</p>
    
    <p>Best regards,<br>
    <strong>The Nexus SEO Team</strong></p>
</body>
</html>
"""
        
        return self.send_email(to_email, subject, body, html_body, pdf_attachment)
    
    def send_subscription_confirmation(self, to_email, username, plan_type):
        """Send subscription confirmation email"""
        subject = f"Subscription Confirmed - {plan_type.title()} Plan"
        
        body = f"""
Hello {username},

Thank you for subscribing to the {plan_type.title()} plan!

Your subscription is now active and you can start enjoying all the features included in your plan.

If you have any questions about your subscription, please contact our support team.

Best regards,
The Nexus SEO Team
"""
        
        html_body = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <h2 style="color: #27ae60;">Subscription Confirmed!</h2>
    
    <p>Hello <strong>{username}</strong>,</p>
    
    <p>Thank you for subscribing to the <strong>{plan_type.title()} plan</strong>!</p>
    
    <p>Your subscription is now active and you can start enjoying all the features included in your plan.</p>
    
    <p>If you have any questions about your subscription, please contact our support team.</p>
    
    <p>Best regards,<br>
    <strong>The Nexus SEO Team</strong></p>
</body>
</html>
"""
        
        return self.send_email(to_email, subject, body, html_body)