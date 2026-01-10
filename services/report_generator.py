"""
Report Generator Service - PDF Export
Creates professional SEO audit reports
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import io
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-GUI backend

class ReportGenerator:
    """
    Generate professional PDF reports for SEO audits
    """
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Create custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#6366f1'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        # Subtitle
        self.styles.add(ParagraphStyle(
            name='Subtitle',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.grey,
            spaceAfter=20,
            alignment=TA_CENTER
        ))
        
        # Section header
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1f2937'),
            spaceAfter=12,
            spaceBefore=12
        ))
    
    def generate_report(self, scan_data, user_data, ai_report=None):
        """
        Generate complete PDF report
        
        Args:
            scan_data: Scan results from database
            user_data: User profile data
            ai_report: Optional AI-generated insights
        
        Returns:
            BytesIO object containing PDF
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch)
        
        # Build content
        story = []
        
        # Header
        story.extend(self._build_header(scan_data, user_data))
        
        # Executive Summary
        story.extend(self._build_executive_summary(scan_data))
        
        # Scores Section
        story.extend(self._build_scores_section(scan_data))
        
        # Issues Section
        story.extend(self._build_issues_section(scan_data))
        
        # Technical Details
        story.extend(self._build_technical_details(scan_data))
        
        # AI Insights (if available)
        if ai_report and not ai_report.get('is_demo'):
            story.append(PageBreak())
            story.extend(self._build_ai_section(ai_report))
        
        # Footer
        story.extend(self._build_footer())
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def _build_header(self, scan_data, user_data):
        """Build report header"""
        elements = []
        
        # Title
        title = Paragraph("🎯 Nexus SEO Intelligence", self.styles['CustomTitle'])
        elements.append(title)
        
        # Subtitle
        subtitle = Paragraph(
            f"SEO Audit Report for {scan_data.get('domain', 'Website')}", 
            self.styles['Subtitle']
        )
        elements.append(subtitle)
        
        # Metadata table
        metadata = [
            ['Report Date:', datetime.utcnow().strftime('%B %d, %Y')],
            ['Analyzed URL:', scan_data.get('url', 'N/A')],
            ['Report Type:', user_data.get('tier', 'demo').upper()],
            ['Generated For:', user_data.get('email', 'User')]
        ]
        
        table = Table(metadata, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#6366f1')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(Spacer(1, 0.3*inch))
        elements.append(table)
        elements.append(Spacer(1, 0.5*inch))
        
        return elements
    
    def _build_executive_summary(self, scan_data):
        """Build executive summary section"""
        elements = []
        
        elements.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        
        overall_score = scan_data.get('overall_score', 0)
        
        if overall_score >= 80:
            status = "Excellent"
            color_hex = '#10b981'
        elif overall_score >= 60:
            status = "Good"
            color_hex = '#3b82f6'
        elif overall_score >= 40:
            status = "Needs Improvement"
            color_hex = '#f59e0b'
        else:
            status = "Critical"
            color_hex = '#ef4444'
        
        summary_text = f"""
        Your website scored <font color="{color_hex}"><b>{overall_score}/100</b></font> ({status}). 
        We identified <b>{scan_data.get('critical_issues', 0)} critical issues</b> and 
        <b>{scan_data.get('high_issues', 0)} high-priority issues</b> that require immediate attention.
        """
        
        elements.append(Paragraph(summary_text, self.styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _build_scores_section(self, scan_data):
        """Build scores visualization section"""
        elements = []
        
        elements.append(Paragraph("SEO Performance Scores", self.styles['SectionHeader']))
        
        # Scores data
        scores = [
            ['Metric', 'Score', 'Status'],
            ['Overall SEO', f"{scan_data.get('overall_score', 0)}/100", self._get_status(scan_data.get('overall_score', 0))],
            ['Technical SEO', f"{scan_data.get('technical_score', 0)}/100", self._get_status(scan_data.get('technical_score', 0))],
            ['Content Quality', f"{scan_data.get('content_score', 0)}/100", self._get_status(scan_data.get('content_score', 0))],
            ['Performance', f"{scan_data.get('performance_score', 0)}/100", self._get_status(scan_data.get('performance_score', 0))],
        ]
        
        table = Table(scores, colWidths=[2*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6366f1')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 12),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica', 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.4*inch))
        
        return elements
    
    def _build_issues_section(self, scan_data):
        """Build issues breakdown section"""
        elements = []
        
        elements.append(Paragraph("Issues Identified", self.styles['SectionHeader']))
        
        issues_detail = scan_data.get('issues_detail', {})
        
        # Critical Issues
        if issues_detail.get('critical'):
            elements.append(Paragraph("<b>🔴 Critical Issues (Fix Immediately)</b>", self.styles['Normal']))
            for issue in issues_detail['critical']:
                elements.append(Paragraph(f"• {issue}", self.styles['Normal']))
            elements.append(Spacer(1, 0.2*inch))
        
        # High Priority
        if issues_detail.get('high'):
            elements.append(Paragraph("<b>🟡 High Priority Issues</b>", self.styles['Normal']))
            for issue in issues_detail['high']:
                elements.append(Paragraph(f"• {issue}", self.styles['Normal']))
            elements.append(Spacer(1, 0.2*inch))
        
        # Medium Priority
        if issues_detail.get('medium'):
            elements.append(Paragraph("<b>🟠 Medium Priority Issues</b>", self.styles['Normal']))
            for issue in issues_detail['medium']:
                elements.append(Paragraph(f"• {issue}", self.styles['Normal']))
            elements.append(Spacer(1, 0.2*inch))
        
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _build_technical_details(self, scan_data):
        """Build technical details section"""
        elements = []
        
        elements.append(Paragraph("Technical Details", self.styles['SectionHeader']))
        
        details = [
            ['Metric', 'Value'],
            ['Page Title', scan_data.get('title', 'N/A')[:60]],
            ['Word Count', str(scan_data.get('word_count', 0))],
            ['Load Time', f"{scan_data.get('load_time_ms', 0)}ms"],
            ['Page Size', f"{scan_data.get('page_size_kb', 0)}KB"],
            ['HTTPS', '✅ Yes' if scan_data.get('has_ssl') else '❌ No'],
            ['Mobile Friendly', '✅ Yes' if scan_data.get('is_mobile_friendly') else '❌ No'],
            ['Images', str(scan_data.get('image_count', 0))],
            ['Links', str(scan_data.get('link_count', 0))],
        ]
        
        table = Table(details, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
            ('FONT', (1, 0), (1, -1), 'Helvetica', 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.4*inch))
        
        return elements
    
    def _build_ai_section(self, ai_report):
        """Build AI insights section"""
        elements = []
        
        elements.append(Paragraph("🤖 AI-Powered Insights", self.styles['SectionHeader']))
        
        sections = ai_report.get('sections', {})
        
        for section_name, content in sections.items():
            if content and section_name != 'EXECUTIVE SUMMARY':
                elements.append(Paragraph(f"<b>{section_name}</b>", self.styles['Normal']))
                # Clean and format content
                paragraphs = content.split('\n\n')
                for para in paragraphs:
                    if para.strip():
                        elements.append(Paragraph(para.strip(), self.styles['Normal']))
                elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _build_footer(self):
        """Build report footer"""
        elements = []
        
        elements.append(Spacer(1, 0.5*inch))
        
        footer_style = ParagraphStyle(
            'Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        
        footer_text = """
        <br/><br/>
        Generated by Nexus SEO Intelligence | https://nexusseo.com<br/>
        © 2026 Nexus SEO. All rights reserved.<br/>
        This report is confidential and intended solely for the use of the individual or entity to whom it is addressed.
        """
        
        elements.append(Paragraph(footer_text, footer_style))
        
        return elements
    
    def _get_status(self, score):
        """Get status label for score"""
        if score >= 80:
            return "✅ Excellent"
        elif score >= 60:
            return "🟢 Good"
        elif score >= 40:
            return "🟡 Fair"
        else:
            return "🔴 Poor"