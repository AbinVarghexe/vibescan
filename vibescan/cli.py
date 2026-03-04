import argparse
import os
import sys
import time
from datetime import datetime
from colorama import Fore, Style, init

from .parsers import parse_package_json, parse_requirements_txt
from .checkers.registry_checker import check_npm_package, check_pypi_package
from .checkers.typosquat_checker import check_typosquatting
from .scorer import calculate_risk
from .reporter import print_banner, report_results, generate_detailed_report, save_json_report

init(autoreset=True)

def print_progress_bar(current, total, prefix='', suffix='', length=50):
    """Print a progress bar to the terminal"""
    percent = ("{0:.1f}").format(100 * (current / float(total)))
    filled = int(length * current // total)
    bar = '█' * filled + '░' * (length - filled)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    if current == total:
        print()

def main():
    parser = argparse.ArgumentParser(
        description="VibeScan - AI Dependency Risk Scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  vibescan                    # Scan current directory
  vibescan ./my-project       # Scan specific project
  vibescan . --no-report      # Skip report generation
  vibescan . --json-only      # Generate JSON report only
        """
    )
    parser.add_argument('path', nargs='?', default='.', help="Path to the directory to scan")
    parser.add_argument('--debug', action='store_true', help="Enable debug output")
    parser.add_argument('--no-report', action='store_true', help="Skip automatic report generation")
    parser.add_argument('--json-only', action='store_true', help="Generate JSON report only (no PDF)")
    parser.add_argument('--output-dir', default='vibescan-reports', help="Directory to save reports (default: vibescan-reports)")
    
    args = parser.parse_args()
    scan_path = os.path.abspath(args.path)
    
    print_banner()
    
    # Detect dependency files
    print(f"{Fore.CYAN}📁 Scanning directory:{Style.RESET_ALL} {scan_path}")
    deps = []
    detected_files = []
    
    # Check package.json
    pkg_json = os.path.join(scan_path, 'package.json')
    if os.path.exists(pkg_json):
        detected_files.append('package.json')
        deps.extend(parse_package_json(pkg_json))
        
    # Check requirements.txt
    req_txt = os.path.join(scan_path, 'requirements.txt')
    if os.path.exists(req_txt):
        detected_files.append('requirements.txt')
        deps.extend(parse_requirements_txt(req_txt))
        
    if not deps:
        print(f"\n{Fore.RED}✗ No package.json or requirements.txt found in the specified path.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  Searched in: {scan_path}{Style.RESET_ALL}")
        sys.exit(0)
    
    print(f"{Fore.GREEN}✓ Detected files:{Style.RESET_ALL} {', '.join(detected_files)}")
    print(f"{Fore.CYAN}📦 Total dependencies:{Style.RESET_ALL} {len(deps)}\n")
    
    # Analysis phase
    print(f"{Fore.CYAN}{Style.BRIGHT}🔍 Starting security analysis...{Style.RESET_ALL}\n")
    
    results = []
    start_time = time.time()
    
    for idx, dep in enumerate(deps, 1):
        registry_data = {}
        typo_data = {}
        
        name = dep['name']
        eco = dep['ecosystem']
        
        # Progress indicator
        print_progress_bar(idx - 1, len(deps), 
                          prefix=f'{Fore.CYAN}Analyzing{Style.RESET_ALL}',
                          suffix=f'{name[:30]:<30}')
        
        # Check Typosquat
        typo_data = check_typosquatting(name, eco)
        
        # Check Registry
        if eco == 'npm':
            registry_data = check_npm_package(name)
        elif eco == 'pypi':
            registry_data = check_pypi_package(name)
            
        score, reasons = calculate_risk(registry_data, typo_data)
        
        dep['score'] = score
        dep['reasons'] = reasons
        dep['registry_data'] = registry_data
        dep['typo_data'] = typo_data
        results.append(dep)
    
    # Final progress update
    print_progress_bar(len(deps), len(deps), 
                      prefix=f'{Fore.GREEN}Complete{Style.RESET_ALL}',
                      suffix=f'Analyzed {len(deps)} packages')
    
    elapsed_time = time.time() - start_time
    print(f"\n{Fore.GREEN}✓ Analysis completed in {elapsed_time:.2f}s{Style.RESET_ALL}\n")
    
    # Display results
    print(f"{Fore.CYAN}{Style.BRIGHT}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{Style.BRIGHT}                         SECURITY SCAN RESULTS{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{Style.BRIGHT}{'='*80}{Style.RESET_ALL}\n")
    
    success = report_results(results)
    
    # Generate reports
    if not args.no_report:
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*80}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{Style.BRIGHT}                         GENERATING REPORTS{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{Style.BRIGHT}{'='*80}{Style.RESET_ALL}\n")
        
        # Create reports directory
        report_dir = os.path.join(scan_path, args.output_dir)
        os.makedirs(report_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        project_name = os.path.basename(scan_path)
        
        # Generate JSON report
        json_path = os.path.join(report_dir, f'vibescan_report_{timestamp}.json')
        print(f"{Fore.CYAN}📄 Generating JSON report...{Style.RESET_ALL}")
        save_json_report(results, json_path, scan_path)
        print(f"{Fore.GREEN}✓ JSON report saved:{Style.RESET_ALL} {json_path}")
        
        # Generate detailed text report
        txt_path = os.path.join(report_dir, f'vibescan_report_{timestamp}.txt')
        print(f"\n{Fore.CYAN}📄 Generating detailed report...{Style.RESET_ALL}")
        generate_detailed_report(results, txt_path, scan_path)
        print(f"{Fore.GREEN}✓ Detailed report saved:{Style.RESET_ALL} {txt_path}")
        
        # Generate PDF report if not json-only
        if not args.json_only:
            try:
                from reportlab.lib.pagesizes import letter
                from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
                from reportlab.lib.styles import getSampleStyleSheet
                from reportlab.lib import colors
                
                pdf_path = os.path.join(report_dir, f'vibescan_report_{timestamp}.pdf')
                print(f"\n{Fore.CYAN}📄 Generating PDF report...{Style.RESET_ALL}")
                
                # Create PDF
                from .reporter import generate_pdf_report
                generate_pdf_report(results, pdf_path, scan_path)
                print(f"{Fore.GREEN}✓ PDF report saved:{Style.RESET_ALL} {pdf_path}")
            except ImportError:
                print(f"\n{Fore.YELLOW}⚠ reportlab not installed. Skipping PDF generation.{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}  Install with: pip install reportlab{Style.RESET_ALL}")
        
        # Summary
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*80}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{Style.BRIGHT}✓ Reports saved to:{Style.RESET_ALL} {report_dir}")
        print(f"{Fore.CYAN}{Style.BRIGHT}{'='*80}{Style.RESET_ALL}\n")
    
    if not success:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == '__main__':
    main()