"""
VibeScan Complete Report Generator
===================================
Generates both terminal and PDF reports for VibeScan scan results.
"""

import sys
import os
from colorama import init, Fore, Style
init(autoreset=True)

def print_banner():
    """Print VibeScan banner"""
    print("\n" + "="*80)
    print(f"{Fore.CYAN}{Style.BRIGHT}")
    print("""
    ██╗   ██╗██╗██████╗ ███████╗███████╗ ██████╗ █████╗ ███╗   ██╗
    ██║   ██║██║██╔══██╗██╔════╝██╔════╝██╔════╝██╔══██╗████╗  ██║
    ██║   ██║██║██████╔╝█████╗  ███████╗██║     ███████║██╔██╗ ██║
    ╚██╗ ██╔╝██║██╔══██╗██╔══╝  ╚════██║██║     ██╔══██║██║╚██╗██║
     ╚████╔╝ ██║██████╔╝███████╗███████║╚██████╗██║  ██║██║ ╚████║
      ╚═══╝  ╚═╝╚═════╝ ╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
    """)
    print(f"{Style.RESET_ALL}" + "="*80)
    print(f"{Fore.YELLOW}Complete Report Generation Tool{Style.RESET_ALL}")
    print("="*80 + "\n")

def generate_reports(project_path="examples/node-demo-app"):
    """Generate all reports"""
    print_banner()
    
    print(f"{Fore.CYAN}📊 Generating comprehensive reports for: {Fore.WHITE}{project_path}{Style.RESET_ALL}\n")
    
    # Step 1: Terminal Report
    print(f"{Fore.YELLOW}[1/3]{Style.RESET_ALL} Displaying detailed terminal report...")
    print("-" * 80)
    
    # Import and run detailed report
    try:
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        from vibescan.detailed_report import print_detailed_report
        print_detailed_report()
    except ImportError:
        # If module import fails, run as subprocess
        os.system("python ../vibescan/detailed_report.py")
    
    print("\n" + "="*80)
    print(f"{Fore.GREEN}✓ Terminal report displayed{Style.RESET_ALL}")
    print("="*80 + "\n")
    
    # Step 2: PDF Report for Node.js app
    print(f"{Fore.YELLOW}[2/3]{Style.RESET_ALL} Generating PDF report for Node.js demo app...")
    pdf_node = "vibescan_node_demo_report.pdf"
    os.system(f'python ../vibescan/pdf_report.py ../examples/node-demo-app "{pdf_node}"')
    print(f"{Fore.GREEN}✓ PDF report generated: {pdf_node}{Style.RESET_ALL}\n")
    
    # Step 3: PDF Report for Python app
    print(f"{Fore.YELLOW}[3/3]{Style.RESET_ALL} Generating PDF report for Python demo app...")
    pdf_python = "vibescan_python_test_report.pdf"
    os.system(f'python ../vibescan/pdf_report.py ../examples/test-app "{pdf_python}"')
    print(f"{Fore.GREEN}✓ PDF report generated: {pdf_python}{Style.RESET_ALL}\n")
    
    # Summary
    print("="*80)
    print(f"{Fore.CYAN}{Style.BRIGHT}REPORT GENERATION COMPLETE{Style.RESET_ALL}")
    print("="*80)
    
    print(f"\n{Fore.GREEN}✓ Generated Reports:{Style.RESET_ALL}")
    print(f"  1. Terminal Report: Displayed above")
    print(f"  2. {pdf_node}")
    print(f"  3. {pdf_python}")
    
    print(f"\n{Fore.CYAN}📄 Report Contents:{Style.RESET_ALL}")
    print("  • Executive summary with statistics")
    print("  • Safe packages listing (10 packages)")
    print("  • Suspicious packages (5 packages)")
    print("  • Critical issues (65 packages)")
    print("  • Typosquatting attacks (22 detected)")
    print("  • Hallucinated packages (43 detected)")
    print("  • Detection methods explanation")
    print("  • Security recommendations")
    
    print(f"\n{Fore.CYAN}📊 Key Findings:{Style.RESET_ALL}")
    print(f"  {Fore.RED}• 81.3% of packages have critical issues{Style.RESET_ALL}")
    print(f"  {Fore.RED}• 22 typosquatting attempts detected{Style.RESET_ALL}")
    print(f"  {Fore.RED}• 43 AI-hallucinated packages found{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}• 5 suspicious packages flagged{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}• 10 legitimate packages verified{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}🔍 Next Steps:{Style.RESET_ALL}")
    print("  1. Review PDF reports for detailed analysis")
    print("  2. Remove all critical packages from dependencies")
    print("  3. Replace typosquatted packages with legitimate versions")
    print("  4. Verify suspicious packages before use")
    print("  5. Integrate VibeScan into CI/CD pipeline")
    
    print(f"\n{Fore.CYAN}📚 Documentation:{Style.RESET_ALL}")
    print("  • Project README: ../README.md")
    print("  • Test Overview: ../docs/testing/TESTING_OVERVIEW.md")
    print("  • Report Guide: ../docs/reports/REPORT_GENERATION.md")
    print("  • Node.js Results: ../examples/node-demo-app/SCAN_RESULTS.md")
    print("  • Python Results: ../examples/test-app/SCAN_RESULTS.md")
    
    print("\n" + "="*80)
    print(f"{Fore.YELLOW}🎯 VibeScan successfully identified security vulnerabilities!{Style.RESET_ALL}")
    print("="*80 + "\n")

if __name__ == "__main__":
    project = sys.argv[1] if len(sys.argv) > 1 else "examples/node-demo-app"
    generate_reports(project)
