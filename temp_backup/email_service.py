"""
Email Service for Nexus SEO Intelligence
Sends SEO reports via email
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime
import os


class EmailService:
    """Handle email sending for reports"""
    
    def __init__(self, smtp_host=None, smtp_port=None, smtp_user=None, smtp_password=None):
        """
        Initialize email service
        
        For production, use environment variables:
        - SMTP_HOST (e.g., smtp.gmail.com)
        - SMTP_PORT (e.g., 587)
        - SMTP_USER (your email)
        - SMTP_PASSWORD (app password)
        """
        self.smtp_host = smtp_host or os.getenv('SMTP_HOST', 'smtp.gmail.com')
        self.smtp_port = int(smtp_port or os.getenv('SMTP_PORT', 587))
        self.smtp_user = smtp_user or os.getenv('SMTP_USER')
        self.smtp_password = smtp_password or os.getenv('SMTP_PASSWORD')
        
        if not self.smtp_user or not self.smtp_password:
            raise ValueError("SMTP credentials not configured. Set SMTP_USER and SMTP_PASSWORD environment variables.")
    
    def send_report(self, recipient_email, recipient_name, scan_url, pdf_buffer, scan_score):
        """
        Send SEO report via email
        
        Args:
            recipient_email: Email address to send to
            recipient_name: Recipient's name
            scan_url: URL that was scanned
            pdf_buffer: BytesIO buffer containing PDF
            scan_score: Overall SEO score
            
        Returns:
            bool: True if sent successfully
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = f"Nexus SEO Intelligence <{self.smtp_user}>"
            msg['To'] = recipient_email
            msg['Subject'] = f"SEO Audit Report for {scan_url}"
            
            # Email body
            html_body = self._create_email_body(recipient_name, scan_url, scan_score)
            msg.attach(MIMEText(html_body, 'html'))
            
            # Attach PDF
            pdf_buffer.seek(0)
            pdf_attachment = MIMEApplication(pdf_buffer.read(), _subtype='pdf')
            pdf_attachment.add_header(
                'Content-Disposition',
                'attachment',
                filename=f'SEO_Report_{scan_url.replace("https://", "").replace("http://", "").replace("/", "_")[:50]}.pdf'
            )
            msg.attach(pdf_attachment)
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False
    
    def _create_email_body(self, recipient_name, scan_url, scan_score):
        """Create HTML email body"""
        
        # Score color
        if scan_score >= 80:
            score_color = '#22c55e'
            status = 'Excellent'
        elif scan_score >= 60:
            score_color = '#eab308'
            status = 'Good'
        elif scan_score >= 40:
            score_color = '#f97316'
            status = 'Needs Improvement'
        else:
            score_color = '#ef4444'
            status = 'Critical'
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
            
            <!-- Header -->
            <div style="background: linear-gradient(135deg, #6366f1, #8b5cf6); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="color: white; margin: 0; font-size: 28px;">🎯 Nexus SEO Intelligence</h1>
                <p style="color: #e0e7ff; margin: 10px 0 0 0;">Your SEO Audit is Ready</p>
            </div>
            
            <!-- Content -->
            <div style="background: #ffffff; padding: 30px; border: 1px solid #e5e7eb; border-top: none; border-radius: 0 0 10px 10px;">
                
                <p style="font-size: 16px; margin-bottom: 20px;">
                    Hello {recipient_name},
                </p>
                
                <p style="font-size: 16px; margin-bottom: 25px;">
                    We've completed the comprehensive SEO audit for <strong>{scan_url}</strong>. 
                    Your detailed report is attached to this email.
                </p>
                
                <!-- Score Box -->
                <div style="background: #f8fafc; border: 2px solid {score_color}; border-radius: 10px; padding: 25px; text-align: center; margin: 30px 0;">
                    <h2 style="color: #1e293b; margin: 0 0 15px 0; font-size: 18px;">Overall SEO Score</h2>
                    <div style="font-size: 48px; font-weight: bold; color: {score_color}; margin: 15px 0;">
                        {scan_score}/100
                    </div>
                    <p style="color: #64748b; margin: 10px 0 0 0; font-size: 16px;">
                        Status: <strong style="color: {score_color};">{status}</strong>
                    </p>
                </div>
                
                <!-- Report Includes -->
                <div style="margin: 30px 0;">
                    <h3 style="color: #1e293b; font-size: 18px; margin-bottom: 15px;">📋 Your Report Includes:</h3>
                    <ul style="color: #475569; font-size: 15px; line-height: 2;">
                        <li>✅ Comprehensive SEO score breakdown</li>
                        <li>✅ Technical, content, and performance analysis</li>
                        <li>✅ Prioritized list of issues to fix</li>
                        <li>✅ AI-powered recommendations</li>
                        <li>✅ Actionable next steps</li>
                    </ul>
                </div>
                
                <!-- CTA Button -->
                <div style="text-align: center; margin: 35px 0;">
                    <a href="https://nexus-seo-fobcg4apinvom9hzpjnfyb.streamlit.app" 
                       style="display: inline-block; background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; 
                              padding: 15px 40px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px;">
                        View Full Dashboard
                    </a>
                </div>
                
                <!-- Next Steps -->
                <div style="background: #eff6ff; border-left: 4px solid #3b82f6; padding: 20px; margin: 30px 0; border-radius: 5px;">
                    <h4 style="color: #1e40af; margin: 0 0 10px 0;">💡 Next Steps:</h4>
                    <p style="color: #1e40af; margin: 5px 0; font-size: 14px;">
                        1. Review the attached PDF report<br>
                        2. Prioritize high-impact issues<br>
                        3. Implement recommended fixes<br>
                        4. Run a follow-up scan to track progress
                    </p>
                </div>
                
                <!-- Support -->
                <div style="margin-top: 35px; padding-top: 25px; border-top: 2px solid #e5e7eb;">
                    <p style="font-size: 14px; color: #64748b; margin: 10px 0;">
                        Questions or need help implementing these recommendations?
                    </p>
                    <p style="font-size: 14px; color: #64748b; margin: 5px 0;">
                        Reply to this email or visit our 
                        <a href="https://nexus-seo-fobcg4apinvom9hzpjnfyb.streamlit.app" style="color: #6366f1; text-decoration: none;">
                            support center
                        </a>
                    </p>
                </div>
                
            </div>
            
            <!-- Footer -->
            <div style="text-align: center; padding: 25px 0; color: #94a3b8; font-size: 13px;">
                <p style="margin: 5px 0;">
                    This report was generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
                </p>
                <p style="margin: 5px 0;">
                    © 2026 Nexus SEO Intelligence. All rights reserved.
                </p>
                <p style="margin: 15px 0 5px 0;">
                    <a href="#" style="color: #94a3b8; text-decoration: none; margin: 0 10px;">Privacy Policy</a>
                    <a href="#" style="color: #94a3b8; text-decoration: none; margin: 0 10px;">Terms of Service</a>
                </p>
            </div>
            
        </body>
        </html>
        """
        
        return html


# Convenience function
def send_seo_report_email(recipient_email, recipient_name, scan_url, pdf_buffer, scan_score):
    """
    Send SEO report via email
    
    Args:
        recipient_email: Email to send to
        recipient_name: Recipient's name
        scan_url: URL that was scanned
        pdf_buffer: PDF report buffer
        scan_score: Overall score
        
    Returns:
        bool: Success status
    """
    try:
        service = EmailService()
        return service.send_report(recipient_email, recipient_name, scan_url, pdf_buffer, scan_score)
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False