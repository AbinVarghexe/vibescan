import argparse
import os
import sys

from .parsers import parse_package_json, parse_requirements_txt
from .checkers.registry_checker import check_npm_package, check_pypi_package
from .checkers.typosquat_checker import check_typosquatting
from .scorer import calculate_risk
from .reporter import print_banner, report_results

def main():
    parser = argparse.ArgumentParser(description="VibeScan - AI Dependency Risk Scanner")
    parser.add_argument('path', nargs='?', default='.', help="Path to the directory to scan")
    parser.add_argument('--debug', action='store_true', help="Enable debug output")
    
    args = parser.parse_args()
    scan_path = args.path
    
    print_banner()
    
    deps = []
    
    # Check package.json
    pkg_json = os.path.join(scan_path, 'package.json')
    if os.path.exists(pkg_json):
        if args.debug: print(f"Found package.json at {pkg_json}")
        deps.extend(parse_package_json(pkg_json))
        
    # Check requirements.txt
    req_txt = os.path.join(scan_path, 'requirements.txt')
    if os.path.exists(req_txt):
        if args.debug: print(f"Found requirements.txt at {req_txt}")
        deps.extend(parse_requirements_txt(req_txt))
        
    if not deps:
        print("No package.json or requirements.txt found in the specified path.")
        sys.exit(0)
        
    print(f"Analyzing {len(deps)} dependencies...\n")
    
    results = []
    for dep in deps:
        registry_data = {}
        typo_data = {}
        
        name = dep['name']
        eco = dep['ecosystem']
        
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
        results.append(dep)
        
    success = report_results(results)
    
    if not success:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == '__main__':
    main()
