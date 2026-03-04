import json
import os
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def print_banner():
    """Print professional ASCII banner"""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}")
    print("="*80)
    print("""
    ██╗   ██╗██╗██████╗ ███████╗███████╗ ██████╗ █████╗ ███╗   ██╗
    ██║   ██║██║██╔══██╗██╔════╝██╔════╝██╔════╝██╔══██╗████╗  ██║
    ██║   ██║██║██████╔╝█████╗  ███████╗██║     ███████║██╔██╗ ██║
    ╚██╗ ██╔╝██║██╔══██╗██╔══╝  ╚════██║██║     ██╔══██║██║╚██╗██║
     ╚████╔╝ ██║██████╔╝███████╗███████║╚██████╗██║  ██║██║ ╚████║
      ╚═══╝  ╚═╝╚═════╝ ╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
    """)
    print(f"                   AI Dependency Risk Scanner v0.1.0")
    print("="*80)
    print(f"{Style.RESET_ALL}")

def report_results(results):
    """
    results: list of dicts with calculated risk:
    [{'name': 'pkg', 'version': '...', 'ecosystem': '...', 'score': 100, 'reasons': [...]}]
    """
    safe = []
    suspicious = []
    critical = []

    for res in results:
        score = res['score']
        if score >= 60:
            critical.append(res)
        elif score >= 10:
            suspicious.append(res)
        else:
            safe.append(res)

    print(f"{Fore.GREEN}{Style.BRIGHT}OK {len(safe)} Safe Dependencies")
    
    if suspicious:
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}!! {len(suspicious)} Suspicious Dependencies (Review Recommended)")
        for s in suspicious:
            print(f"  - {Fore.YELLOW}{s['name']}{Style.RESET_ALL} ({s['ecosystem']}) - Score: {s['score']}/100")
            for r in s['reasons']:
                print(f"    * {r}")
                
    if critical:
        print(f"\n{Fore.RED}{Style.BRIGHT}XX {len(critical)} Critical Risk Dependencies (Action Required!)")
        for c in critical:
            print(f"  - {Fore.RED}{c['name']}{Style.RESET_ALL} ({c['ecosystem']}) - Score: {c['score']}/100")
            for r in c['reasons']:
                print(f"    * {r}")

    print("\n-----------------------------------------")
    if critical:
        print(f"{Fore.RED}{Style.BRIGHT}VibeScan detected CRITICAL risks. Build failed.")
        return False
    elif suspicious:
        print(f"{Fore.YELLOW}{Style.BRIGHT}VibeScan detected suspicious packages but no critical risks. Proceed with caution.")
        return True
    else:
        print(f"{Fore.GREEN}{Style.BRIGHT}VibeScan passed. No critical or suspicious risks detected.")
        return True


def save_json_report(results, output_path, scan_path):
    """Save scan results as JSON"""
    safe = [r for r in results if r['score'] < 10]
    suspicious = [r for r in results if 10 <= r['score'] < 60]
    critical = [r for r in results if r['score'] >= 60]
    
    # Clean results for JSON serialization
    def clean_for_json(pkg):
        """Remove non-JSON-serializable objects"""
        return {
            'name': pkg['name'],
            'version': pkg.get('version', 'N/A'),
            'ecosystem': pkg['ecosystem'],
            'score': pkg['score'],
            'reasons': pkg['reasons']
        }
    
    report_data = {
        "scan_info": {
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "scan_path": scan_path,
            "vibescan_version": "0.1.0",
            "total_packages": len(results)
        },
        "summary": {
            "safe": len(safe),
            "suspicious": len(suspicious),
            "critical": len(critical),
            "risk_level": "CRITICAL" if critical else ("WARNING" if suspicious else "SAFE")
        },
        "packages": {
            "safe": [clean_for_json(p) for p in safe],
            "suspicious": [clean_for_json(p) for p in suspicious],
            "critical": [clean_for_json(p) for p in critical]
        }
    }
    
    with open(output_path, 'w') as f:
        json.dump(report_data, f, indent=2)


def generate_detailed_report(results, output_path, scan_path):
    """Generate detailed text report"""
    safe = [r for r in results if r['score'] < 10]
    suspicious = [r for r in results if 10 <= r['score'] < 60]
    critical = [r for r in results if r['score'] >= 60]
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("                    VIBESCAN SECURITY REPORT\n")
        f.write("="*80 + "\n\n")
        
        f.write(f"Scan Path: {scan_path}\n")
        f.write(f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"VibeScan Version: 0.1.0\n\n")
        
        f.write("="*80 + "\n")
        f.write("EXECUTIVE SUMMARY\n")
        f.write("="*80 + "\n\n")
        
        f.write(f"  Total Packages Analyzed:    {len(results)}\n")
        f.write(f"  ✓ Safe Packages:            {len(safe)} ({len(safe)/len(results)*100:.1f}%)\n")
        f.write(f"  ⚠ Suspicious Packages:      {len(suspicious)} ({len(suspicious)/len(results)*100:.1f}%)\n")
        f.write(f"  ✗ Critical Issues:          {len(critical)} ({len(critical)/len(results)*100:.1f}%)\n\n")
        
        if critical:
            f.write(f"  ⚠ OVERALL RISK LEVEL: CRITICAL\n\n")
        elif suspicious:
            f.write(f"  ⚠ OVERALL RISK LEVEL: WARNING\n\n")
        else:
            f.write(f"  ✓ OVERALL RISK LEVEL: SAFE\n\n")
        
        # Safe packages
        f.write("="*80 + "\n")
        f.write(f"✓ SAFE DEPENDENCIES ({len(safe)} packages)\n")
        f.write("="*80 + "\n\n")
        
        for pkg in safe:
            f.write(f"  ✓ {pkg['name']} ({pkg['ecosystem']})\n")
            f.write(f"    Version: {pkg.get('version', 'N/A')}\n")
            f.write(f"    Risk Score: {pkg['score']}/100\n")
            if pkg['reasons']:
                for reason in pkg['reasons']:
                    f.write(f"    • {reason}\n")
            f.write("\n")
        
        # Suspicious packages
        if suspicious:
            f.write("="*80 + "\n")
            f.write(f"⚠ SUSPICIOUS DEPENDENCIES ({len(suspicious)} packages)\n")
            f.write("="*80 + "\n\n")
            
            for pkg in suspicious:
                f.write(f"  ⚠ {pkg['name']} ({pkg['ecosystem']})\n")
                f.write(f"    Version: {pkg.get('version', 'N/A')}\n")
                f.write(f"    Risk Score: {pkg['score']}/100\n")
                for reason in pkg['reasons']:
                    f.write(f"    • {reason}\n")
                f.write("\n")
        
        # Critical packages
        if critical:
            f.write("="*80 + "\n")
            f.write(f"✗ CRITICAL ISSUES ({len(critical)} packages)\n")
            f.write("="*80 + "\n\n")
            
            for pkg in critical:
                f.write(f"  ✗ {pkg['name']} ({pkg['ecosystem']})\n")
                f.write(f"    Version: {pkg.get('version', 'N/A')}\n")
                f.write(f"    Risk Score: {pkg['score']}/100\n")
                for reason in pkg['reasons']:
                    f.write(f"    • {reason}\n")
                f.write("\n")
        
        # Recommendations
        f.write("="*80 + "\n")
        f.write("RECOMMENDATIONS\n")
        f.write("="*80 + "\n\n")
        
        if critical:
            f.write("1. ✗ REMOVE CRITICAL PACKAGES IMMEDIATELY\n")
            f.write("   These packages pose serious security risks and should be removed.\n\n")
        
        if suspicious:
            f.write("2. ⚠ REVIEW SUSPICIOUS PACKAGES\n")
            f.write("   Manually verify these packages before use.\n\n")
        
        f.write("3. ✓ INTEGRATE VIBESCAN INTO CI/CD\n")
        f.write("   Add VibeScan to your build pipeline to catch issues early.\n\n")
        
        f.write("4. 🔍 REGULAR SECURITY AUDITS\n")
        f.write("   Run VibeScan before every deployment.\n\n")
        
        f.write("="*80 + "\n")
        f.write(f"Report generated by VibeScan v0.1.0\n")
        f.write(f"Documentation: https://github.com/AbinVarghexe/vibescan\n")
        f.write("="*80 + "\n")


def generate_pdf_report(results, output_path, scan_path):
    """Generate PDF report using reportlab"""
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
    except ImportError:
        print(f"{Fore.YELLOW}reportlab not installed. Cannot generate PDF.{Style.RESET_ALL}")
        return
    
    safe = [r for r in results if r['score'] < 10]
    suspicious = [r for r in results if 10 <= r['score'] < 60]
    critical = [r for r in results if r['score'] >= 60]
    
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#0066cc'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    story.append(Paragraph("VibeScan Security Report", title_style))
    story.append(Spacer(1, 12))
    
    # Metadata
    story.append(Paragraph(f"<b>Scan Path:</b> {scan_path}", styles['Normal']))
    story.append(Paragraph(f"<b>Scan Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Paragraph(f"<b>VibeScan Version:</b> 0.1.0", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Executive Summary
    story.append(Paragraph("<b>Executive Summary</b>", styles['Heading2']))
    
    summary_data = [
        ['Metric', 'Count', 'Percentage'],
        ['Total Packages', str(len(results)), '100%'],
        ['✓ Safe Packages', str(len(safe)), f'{len(safe)/len(results)*100:.1f}%'],
        ['⚠ Suspicious Packages', str(len(suspicious)), f'{len(suspicious)/len(results)*100:.1f}%'],
        ['✗ Critical Issues', str(len(critical)), f'{len(critical)/len(results)*100:.1f}%'],
    ]
    
    summary_table = Table(summary_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    story.append(summary_table)
    story.append(Spacer(1, 20))
    
    # Risk Level
    if critical:
        risk_color = colors.red
        risk_text = "CRITICAL"
    elif suspicious:
        risk_color = colors.orange
        risk_text = "WARNING"
    else:
        risk_color = colors.green
        risk_text = "SAFE"
    
    risk_style = ParagraphStyle(
        'RiskLevel',
        parent=styles['Normal'],
        fontSize=16,
        textColor=risk_color,
        spaceAfter=20,
        alignment=TA_CENTER
    )
    story.append(Paragraph(f"<b>Overall Risk Level: {risk_text}</b>", risk_style))
    story.append(PageBreak())
    
    # Critical Issues
    if critical:
        story.append(Paragraph("<b>Critical Issues</b>", styles['Heading2']))
        for pkg in critical:
            story.append(Paragraph(f"<b>✗ {pkg['name']}</b> ({pkg['ecosystem']})", styles['Heading3']))
            story.append(Paragraph(f"Risk Score: {pkg['score']}/100", styles['Normal']))
            for reason in pkg['reasons']:
                story.append(Paragraph(f"• {reason}", styles['Normal']))
            story.append(Spacer(1, 12))
        story.append(PageBreak())
    
    # Suspicious Packages
    if suspicious:
        story.append(Paragraph("<b>Suspicious Packages</b>", styles['Heading2']))
        for pkg in suspicious:
            story.append(Paragraph(f"<b>⚠ {pkg['name']}</b> ({pkg['ecosystem']})", styles['Heading3']))
            story.append(Paragraph(f"Risk Score: {pkg['score']}/100", styles['Normal']))
            for reason in pkg['reasons']:
                story.append(Paragraph(f"• {reason}", styles['Normal']))
            story.append(Spacer(1, 12))
    
    # Build PDF
    doc.build(story)
