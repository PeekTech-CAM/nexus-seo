from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO
from datetime import datetime

class PDFGenerator:
    """Generate PDF reports from scan results"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        # Heading styles
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12
        ))
        
        # Score style
        self.styles.add(ParagraphStyle(
            name='ScoreStyle',
            parent=self.styles['Normal'],
            fontSize=48,
            textColor=colors.HexColor('#27ae60'),
            alignment=TA_CENTER,
            spaceAfter=20
        ))
    
    def generate(self, results):
        """Generate PDF from scan results"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        
        # Title
        title = Paragraph("SEO Audit Report", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 0.2*inch))
        
        # Basic Info
        info_data = [
            ['URL:', results.get('url', 'N/A')],
            ['Scan Date:', results.get('scan_date', datetime.now().isoformat())],
            ['Status:', 'Success' if 'score' in results else 'Failed']
        ]
        
        info_table = Table(info_data, colWidths=[1.5*inch, 5*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Check if scan was successful
        if 'error' in results:
            error_text = Paragraph(f"<b>Error:</b> {results['error']}", self.styles['Normal'])
            story.append(error_text)
            doc.build(story)
            buffer.seek(0)
            return buffer.getvalue()
        
        # Overall Score
        score = results.get('score', 0)
        score_text = Paragraph(f"{score}/100", self.styles['ScoreStyle'])
        story.append(score_text)
        
        score_desc = self._get_score_description(score)
        score_desc_para = Paragraph(score_desc, self.styles['Normal'])
        story.append(score_desc_para)
        story.append(Spacer(1, 0.3*inch))
        
        # Meta Tags Section
        story.append(Paragraph("Meta Tags Analysis", self.styles['CustomHeading']))
        meta_data = [
            ['Element', 'Status', 'Content/Details'],
            ['Title', 
             '✓' if results['meta_tags']['title'] else '✗',
             results['meta_tags']['title'][:50] + '...' if len(results['meta_tags']['title']) > 50 else results['meta_tags']['title']],
            ['Description',
             '✓' if results['meta_tags']['description'] else '✗',
             results['meta_tags']['description'][:50] + '...' if len(results['meta_tags']['description']) > 50 else results['meta_tags']['description']],
            ['Canonical',
             '✓' if results['meta_tags']['canonical'] else '✗',
             'Set' if results['meta_tags']['canonical'] else 'Not set'],
            ['Open Graph',
             '✓' if results['meta_tags']['og_tags'] else '✗',
             f"{len(results['meta_tags']['og_tags'])} tags"],
        ]
        
        meta_table = Table(meta_data, colWidths=[1.5*inch, 0.7*inch, 4.3*inch])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')])
        ]))
        
        story.append(meta_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Headings Section
        story.append(Paragraph("Heading Structure", self.styles['CustomHeading']))
        heading_data = [
            ['Heading Level', 'Count', 'Status'],
            ['H1', len(results['headings']['h1']), '✓' if len(results['headings']['h1']) == 1 else '⚠' if len(results['headings']['h1']) > 0 else '✗'],
            ['H2', len(results['headings']['h2']), '✓' if len(results['headings']['h2']) > 0 else '-'],
            ['H3', len(results['headings']['h3']), '✓' if len(results['headings']['h3']) > 0 else '-'],
            ['H4', len(results['headings']['h4']), '-'],
            ['H5', len(results['headings']['h5']), '-'],
            ['H6', len(results['headings']['h6']), '-'],
        ]
        
        heading_table = Table(heading_data, colWidths=[2*inch, 2*inch, 2.5*inch])
        heading_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')])
        ]))
        
        story.append(heading_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Images Section
        story.append(Paragraph("Image Optimization", self.styles['CustomHeading']))
        image_data = [
            ['Metric', 'Value'],
            ['Total Images', str(results['images']['total'])],
            ['Images without ALT', str(results['images']['without_alt'])],
            ['Images without TITLE', str(results['images']['without_title'])],
            ['Optimization Rate', f"{((results['images']['total'] - results['images']['without_alt']) / results['images']['total'] * 100):.1f}%" if results['images']['total'] > 0 else 'N/A']
        ]
        
        image_table = Table(image_data, colWidths=[3*inch, 3.5*inch])
        image_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')])
        ]))
        
        story.append(image_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Links Section
        story.append(Paragraph("Link Analysis", self.styles['CustomHeading']))
        link_data = [
            ['Metric', 'Value'],
            ['Total Links', str(results['links']['total'])],
            ['Internal Links', str(results['links']['internal'])],
            ['External Links', str(results['links']['external'])],
            ['Nofollow Links', str(results['links']['nofollow'])]
        ]
        
        link_table = Table(link_data, colWidths=[3*inch, 3.5*inch])
        link_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')])
        ]))
        
        story.append(link_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Technical SEO
        story.append(Paragraph("Technical SEO", self.styles['CustomHeading']))
        tech_data = [
            ['Check', 'Status'],
            ['HTTPS/SSL', '✓ Enabled' if results['technical']['has_ssl'] else '✗ Not enabled'],
            ['Sitemap', '✓ Found' if results['technical']['has_sitemap'] else '✗ Not found'],
            ['Robots.txt', '✓ Found' if results['technical']['has_robots_txt'] else '✗ Not found'],
            ['Mobile Friendly', '✓ Yes' if results['technical']['is_mobile_friendly'] else '✗ No'],
            ['Response Time', f"{results['performance']['response_time']:.2f}s"],
            ['Page Size', f"{results['performance']['content_size'] / 1024:.2f} KB"]
        ]
        
        tech_table = Table(tech_data, colWidths=[3*inch, 3.5*inch])
        tech_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')])
        ]))
        
        story.append(tech_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Recommendations
        story.append(Paragraph("Top Recommendations", self.styles['CustomHeading']))
        recommendations = self._generate_recommendations(results)
        for rec in recommendations[:5]:  # Top 5 recommendations
            rec_para = Paragraph(f"• {rec}", self.styles['Normal'])
            story.append(rec_para)
            story.append(Spacer(1, 0.1*inch))
        
        # Footer
        story.append(Spacer(1, 0.3*inch))
        footer = Paragraph(
            "<i>Report generated by Nexus SEO Intelligence</i>",
            self.styles['Normal']
        )
        story.append(footer)
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    
    def _get_score_description(self, score):
        """Get description based on score"""
        if score >= 90:
            return "<b>Excellent!</b> Your website has strong SEO optimization."
        elif score >= 70:
            return "<b>Good!</b> Your website has solid SEO, with some room for improvement."
        elif score >= 50:
            return "<b>Fair.</b> Your website needs several SEO improvements."
        else:
            return "<b>Poor.</b> Your website requires significant SEO work."
    
    def _generate_recommendations(self, results):
        """Generate prioritized recommendations"""
        recommendations = []
        
        if not results['meta_tags']['title']:
            recommendations.append("Add a title tag to your page")
        
        if not results['meta_tags']['description']:
            recommendations.append("Add a meta description")
        
        if not results['technical']['has_ssl']:
            recommendations.append("Enable HTTPS/SSL certificate")
        
        if not results['headings']['h1']:
            recommendations.append("Add an H1 heading to your page")
        
        if results['images']['without_alt'] > 0:
            recommendations.append(f"Add ALT text to {results['images']['without_alt']} images")
        
        if not results['technical']['is_mobile_friendly']:
            recommendations.append("Add viewport meta tag for mobile optimization")
        
        if not results['technical']['has_sitemap']:
            recommendations.append("Create and submit an XML sitemap")
        
        if results['content']['word_count'] < 300:
            recommendations.append("Increase page content to at least 300 words")
        
        if not results['content']['has_structured_data']:
            recommendations.append("Add structured data (Schema.org) markup")
        
        if not results['meta_tags']['og_tags']:
            recommendations.append("Add Open Graph tags for social media sharing")
        
        return recommendations if recommendations else ["Great job! No major issues detected."]