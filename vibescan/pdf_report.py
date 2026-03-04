"""
VibeScan PDF Report Generator
==============================
Generates comprehensive PDF reports from VibeScan scan results.
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import os

class PDFReportGenerator:
    def __init__(self, output_path="vibescan_report.pdf"):
        self.output_path = output_path
        self.doc = SimpleDocTemplate(output_path, pagesize=letter)
        self.styles = getSampleStyleSheet()
        self.story = []
        self.width, self.height = letter
        
        # Custom styles
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        self.subheading_style = ParagraphStyle(
            'CustomSubHeading',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#555555'),
            spaceAfter=8,
            spaceBefore=8,
            fontName='Helvetica-Bold'
        )
        
    def add_header(self, project_path):
        """Add report header"""
        # Title
        title = Paragraph("VibeScan Security Report", self.title_style)
        self.story.append(title)
        self.story.append(Spacer(1, 0.2*inch))
        
        # Metadata
        metadata = [
            ["Project:", project_path],
            ["Scan Date:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            ["Tool Version:", "VibeScan v0.1.0"],
            ["Report Type:", "Dependency Security Analysis"]
        ]
        
        table = Table(metadata, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#555555')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 0.3*inch))
        
    def add_executive_summary(self, stats):
        """Add executive summary section"""
        heading = Paragraph("Executive Summary", self.heading_style)
        self.story.append(heading)
        
        # Summary statistics
        summary_data = [
            ["Metric", "Count", "Percentage"],
            ["Total Packages", str(stats['total']), "100%"],
            ["✓ Safe Packages", str(stats['safe']), f"{stats['safe']/stats['total']*100:.1f}%"],
            ["⚠ Suspicious Packages", str(stats['suspicious']), f"{stats['suspicious']/stats['total']*100:.1f}%"],
            ["✗ Critical Issues", str(stats['critical']), f"{stats['critical']/stats['total']*100:.1f}%"],
        ]
        
        table = Table(summary_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 0.3*inch))
        
        # Risk assessment
        risk_level = "CRITICAL" if stats['critical'] > 0 else ("WARNING" if stats['suspicious'] > 0 else "SAFE")
        risk_color = colors.red if risk_level == "CRITICAL" else (colors.orange if risk_level == "WARNING" else colors.green)
        
        risk_style = ParagraphStyle(
            'Risk',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=risk_color,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        risk_text = Paragraph(f"Overall Risk Level: {risk_level}", risk_style)
        self.story.append(risk_text)
        self.story.append(Spacer(1, 0.3*inch))
        
    def add_safe_packages(self, packages):
        """Add safe packages section"""
        if not packages:
            return
            
        heading = Paragraph("✓ Safe Dependencies", self.heading_style)
        self.story.append(heading)
        
        desc = Paragraph(
            f"Found {len(packages)} legitimate package(s) that passed all security checks:",
            self.styles['Normal']
        )
        self.story.append(desc)
        self.story.append(Spacer(1, 0.1*inch))
        
        # Create table
        data = [["Package Name", "Ecosystem", "Status"]]
        for pkg in packages:
            data.append([pkg['name'], pkg['ecosystem'], "SAFE"])
            
        table = Table(data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ecc71')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTNAME', (0, 1), (-1, -1), 'Courier'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 0.3*inch))
        
    def add_suspicious_packages(self, packages):
        """Add suspicious packages section"""
        if not packages:
            return
            
        heading = Paragraph("⚠ Suspicious Dependencies", self.heading_style)
        self.story.append(heading)
        
        desc = Paragraph(
            f"Found {len(packages)} package(s) with suspicious characteristics:",
            self.styles['Normal']
        )
        self.story.append(desc)
        self.story.append(Spacer(1, 0.1*inch))
        
        for pkg in packages:
            self.add_package_detail(pkg, colors.orange)
            
        self.story.append(Spacer(1, 0.2*inch))
        
    def add_critical_packages(self, packages):
        """Add critical packages section"""
        if not packages:
            return
            
        heading = Paragraph("✗ Critical Risk Dependencies", self.heading_style)
        self.story.append(heading)
        
        desc = Paragraph(
            f"Found {len(packages)} package(s) with CRITICAL security issues:",
            self.styles['Normal']
        )
        self.story.append(desc)
        self.story.append(Spacer(1, 0.1*inch))
        
        # Group by type
        typosquat = [p for p in packages if p.get('is_typosquat')]
        hallucinated = [p for p in packages if not p.get('exists')]
        
        if typosquat:
            subheading = Paragraph(f"Typosquatting Attempts ({len(typosquat)} packages):", self.subheading_style)
            self.story.append(subheading)
            for pkg in typosquat[:10]:  # Limit to 10 for space
                self.add_package_detail(pkg, colors.red)
                
        if hallucinated:
            subheading = Paragraph(f"Non-Existent/Hallucinated Packages ({len(hallucinated)} packages):", self.subheading_style)
            self.story.append(subheading)
            for pkg in hallucinated[:10]:  # Limit to 10 for space
                self.add_package_detail(pkg, colors.red)
                
    def add_package_detail(self, pkg, color):
        """Add detailed package information"""
        data = [
            ["Package:", pkg['name']],
            ["Ecosystem:", pkg['ecosystem']],
            ["Risk Score:", f"{pkg['score']}/100"],
        ]
        
        if pkg.get('issues'):
            for issue in pkg['issues']:
                data.append(["Issue:", issue])
                
        table = Table(data, colWidths=[1.5*inch, 4.5*inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Courier'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#555555')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
            ('BOX', (0, 0), (-1, -1), 2, color),
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 0.15*inch))
        
    def add_recommendations(self):
        """Add recommendations section"""
        heading = Paragraph("Recommendations", self.heading_style)
        self.story.append(heading)
        
        recommendations = [
            "1. Remove all packages marked as CRITICAL immediately",
            "2. Replace typosquatted packages with legitimate versions",
            "3. Verify all suspicious packages before installation",
            "4. Review and update your dependency management practices",
            "5. Integrate VibeScan into your CI/CD pipeline",
            "6. Run security scans before every deployment",
            "7. Keep dependencies updated to latest stable versions",
            "8. Use package lock files (package-lock.json, requirements.txt)",
        ]
        
        for rec in recommendations:
            p = Paragraph(rec, self.styles['Normal'])
            self.story.append(p)
            self.story.append(Spacer(1, 0.05*inch))
            
        self.story.append(Spacer(1, 0.2*inch))
        
    def add_footer(self):
        """Add report footer"""
        footer_style = ParagraphStyle(
            'Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        
        self.story.append(Spacer(1, 0.5*inch))
        footer_text = f"Generated by VibeScan v0.1.0 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>https://github.com/AbinVarghexe/vibescan"
        footer = Paragraph(footer_text, footer_style)
        self.story.append(footer)
        
    def generate(self, scan_results):
        """Generate the complete PDF report"""
        # Add all sections
        self.add_header(scan_results['project_path'])
        self.add_executive_summary(scan_results['stats'])
        self.add_safe_packages(scan_results.get('safe', []))
        
        if scan_results.get('suspicious'):
            self.add_suspicious_packages(scan_results['suspicious'])
            
        if scan_results.get('critical'):
            self.add_critical_packages(scan_results['critical'])
            
        self.add_recommendations()
        self.add_footer()
        
        # Build PDF
        self.doc.build(self.story)
        print(f"\n✓ PDF Report generated: {self.output_path}")
        return self.output_path


def generate_mock_results(project_path):
    """Generate mock results for demonstration"""
    return {
        'project_path': project_path,
        'stats': {
            'total': 51,
            'safe': 8,
            'suspicious': 3,
            'critical': 40
        },
        'safe': [
            {'name': 'express', 'ecosystem': 'npm', 'score': 0},
            {'name': 'axios', 'ecosystem': 'npm', 'score': 0},
            {'name': 'dotenv', 'ecosystem': 'npm', 'score': 0},
            {'name': 'cors', 'ecosystem': 'npm', 'score': 0},
            {'name': 'nodemon', 'ecosystem': 'npm', 'score': 0},
        ],
        'suspicious': [
            {
                'name': 'next-js',
                'ecosystem': 'npm',
                'score': 20,
                'exists': True,
                'is_typosquat': False,
                'issues': ['Very low download count (0 in last month)', 'Possible typosquat of "next"']
            },
            {
                'name': 'bable',
                'ecosystem': 'npm',
                'score': 20,
                'exists': True,
                'is_typosquat': True,
                'issues': ['Very low download count', 'Similar to "babel"']
            },
        ],
        'critical': [
            {
                'name': 'expresss',
                'ecosystem': 'npm',
                'score': 60,
                'exists': True,
                'is_typosquat': True,
                'issues': ['Name is deceptively similar to popular package "express"']
            },
            {
                'name': 'react-quantum-hooks',
                'ecosystem': 'npm',
                'score': 100,
                'exists': False,
                'is_typosquat': False,
                'issues': ['Package does not exist in registry', 'Likely AI hallucination']
            },
            {
                'name': 'express-ultra-router',
                'ecosystem': 'npm',
                'score': 100,
                'exists': False,
                'is_typosquat': False,
                'issues': ['Package does not exist in registry', 'Likely AI hallucination']
            },
            {
                'name': 'recat',
                'ecosystem': 'npm',
                'score': 65,
                'exists': True,
                'is_typosquat': True,
                'issues': ['Name is deceptively similar to "react"', 'Low download count (132 in last month)']
            },
            {
                'name': 'lodsh',
                'ecosystem': 'npm',
                'score': 80,
                'exists': True,
                'is_typosquat': True,
                'issues': ['Name is deceptively similar to "lodash"', 'Very low download count']
            },
        ]
    }


if __name__ == "__main__":
    import sys
    
    # Get project path from command line or use default
    project_path = sys.argv[1] if len(sys.argv) > 1 else "node-demo-app"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "vibescan_report.pdf"
    
    # Generate mock results (in real implementation, this would come from actual scan)
    results = generate_mock_results(project_path)
    
    # Generate PDF
    generator = PDFReportGenerator(output_file)
    generator.generate(results)
    print(f"\n✓ Report generated successfully: {output_file}")
    print(f"✓ Open the file to view detailed security analysis")
