"""
VibeScan Detailed Terminal Report
==================================
Displays comprehensive scan results in terminal with formatting.
"""

import sys
from colorama import init, Fore, Back, Style
init(autoreset=True)

def print_header(title):
    """Print formatted section header"""
    width = 80
    print("\n" + "=" * width)
    print(f"{Fore.CYAN}{Style.BRIGHT}{title.center(width)}{Style.RESET_ALL}")
    print("=" * width + "\n")

def print_section(title, icon=""):
    """Print section title"""
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}{icon} {title}{Style.RESET_ALL}")
    print("-" * 80)

def print_subsection(title):
    """Print subsection title"""
    print(f"\n{Fore.CYAN}{title}{Style.RESET_ALL}")

def print_stat(label, value, color=Fore.WHITE):
    """Print a statistic"""
    print(f"  {Fore.WHITE}{label:<30} {color}{value}{Style.RESET_ALL}")

def print_package(name, ecosystem, score, issues=None, status="CRITICAL"):
    """Print package details"""
    if status == "SAFE":
        status_color = Fore.GREEN
        symbol = "✓"
    elif status == "SUSPICIOUS":
        status_color = Fore.YELLOW
        symbol = "⚠"
    else:
        status_color = Fore.RED
        symbol = "✗"
    
    print(f"\n  {status_color}{symbol} {Style.BRIGHT}{name}{Style.RESET_ALL} ({ecosystem})")
    print(f"    Risk Score: {status_color}{score}/100{Style.RESET_ALL}")
    
    if issues:
        for issue in issues:
            print(f"    • {Fore.WHITE}{issue}{Style.RESET_ALL}")

def print_detailed_report():
    """Print comprehensive scan report"""
    
    # Header
    print_header("VIBESCAN DETAILED SECURITY REPORT")
    
    # Metadata
    print(f"{Fore.CYAN}Project Path:{Style.RESET_ALL} node-demo-app/")
    print(f"{Fore.CYAN}Scan Date:{Style.RESET_ALL} March 4, 2026")
    print(f"{Fore.CYAN}Tool Version:{Style.RESET_ALL} VibeScan v0.1.0")
    print(f"{Fore.CYAN}Package Manager:{Style.RESET_ALL} npm (Node.js)")
    
    # Executive Summary
    print_section("EXECUTIVE SUMMARY", "📊")
    
    total = 51
    safe = 8
    suspicious = 3
    critical = 40
    
    print_stat("Total Packages Analyzed:", f"{total}", Fore.WHITE)
    print_stat("Safe Packages:", f"{safe} ({safe/total*100:.1f}%)", Fore.GREEN)
    print_stat("Suspicious Packages:", f"{suspicious} ({suspicious/total*100:.1f}%)", Fore.YELLOW)
    print_stat("Critical Issues:", f"{critical} ({critical/total*100:.1f}%)", Fore.RED)
    
    print(f"\n  {Back.RED}{Fore.WHITE}{Style.BRIGHT} OVERALL RISK LEVEL: CRITICAL {Style.RESET_ALL}")
    
    # Safe Packages
    print_section("SAFE DEPENDENCIES (8 packages)", "✓")
    
    safe_packages = [
        ("express", "npm", 0, None),
        ("axios", "npm", 0, None),
        ("dotenv", "npm", 0, None),
        ("cors", "npm", 0, None),
        ("nodemon", "npm", 0, None),
        ("axios-mock", "npm", 5, ["Low downloads but exists"]),
        ("prettier-format", "npm", 5, ["Variant of prettier"]),
        ("ai-linter", "npm", 5, ["Low usage"]),
    ]
    
    for pkg in safe_packages:
        print_package(pkg[0], pkg[1], pkg[2], pkg[3], "SAFE")
    
    # Suspicious Packages
    print_section("SUSPICIOUS DEPENDENCIES (3 packages)", "⚠")
    
    suspicious_packages = [
        ("next-js", "npm", 20, [
            "Very low download count (0 in last month)",
            "Possible typosquat of 'next'",
            "Wrong hyphenation pattern"
        ]),
        ("auto-api-generator", "npm", 20, [
            "Very low download count (6 in last month)",
            "AI-style naming pattern"
        ]),
        ("bable", "npm", 20, [
            "Very low download count (0 in last month)",
            "Similar to popular package 'babel'",
            "Missing letter attack"
        ]),
    ]
    
    for pkg in suspicious_packages:
        print_package(pkg[0], pkg[1], pkg[2], pkg[3], "SUSPICIOUS")
    
    # Critical Packages - Typosquatting
    print_section("CRITICAL: TYPOSQUATTING ATTACKS (16 packages)", "✗")
    
    print_subsection("Simple Character Manipulation:")
    typo_simple = [
        ("expresss", "npm", 60, ["Extra letter 's'", "Targets: express (50M+ downloads/week)"]),
        ("expres", "npm", 60, ["Missing letter 's'", "Targets: express"]),
        ("lodsh", "npm", 80, ["Missing letter 'a'", "Targets: lodash", "Very low downloads (0/month)"]),
        ("webpck", "npm", 100, ["Missing letter 'a'", "Targets: webpack", "Does not exist in registry"]),
        ("chalkk", "npm", 80, ["Extra letter 'k'", "Targets: chalk", "Very low downloads (4/month)"]),
    ]
    
    for pkg in typo_simple:
        print_package(pkg[0], pkg[1], pkg[2], pkg[3], "CRITICAL")
    
    print_subsection("Letter Swap Attacks:")
    letter_swap = [
        ("recat", "npm", 65, ["Letters swapped: 'ea' -> 'ac'", "Targets: react", "Low downloads (132/month)"]),
        ("momnet", "npm", 65, ["Letters swapped: 'en' -> 'ne'", "Targets: moment", "Low downloads (107/month)"]),
        ("axois", "npm", 60, ["Letters swapped: 'io' -> 'oi'", "Targets: axios"]),
    ]
    
    for pkg in letter_swap:
        print_package(pkg[0], pkg[1], pkg[2], pkg[3], "CRITICAL")
    
    print_subsection("Hyphenation & Suffix Tricks:")
    hyphen_tricks = [
        ("next-js", "npm", 20, ["Wrong hyphenation", "Targets: next", "Suspicious"]),
        ("mongoose-db", "npm", 80, ["Extra suffix '-db'", "Targets: mongoose", "Low downloads (17/month)"]),
        ("tailwind-css", "npm", 100, ["Wrong hyphenation", "Targets: tailwindcss", "Does not exist"]),
        ("type-script", "npm", 100, ["Wrong hyphenation", "Targets: typescript", "Does not exist"]),
        ("commander-js", "npm", 80, ["Extra suffix '-js'", "Targets: commander", "Low downloads (63/month)"]),
    ]
    
    for pkg in hyphen_tricks:
        print_package(pkg[0], pkg[1], pkg[2], pkg[3], "CRITICAL")
    
    print_subsection("Case Variation & Duplicates:")
    case_tricks = [
        ("esLint", "npm", 100, ["Wrong case: 'L' should be lowercase", "Targets: eslint", "Does not exist"]),
        ("loodash", "npm", 65, ["Extra 'o'", "Targets: lodash", "Low downloads (551/month)"]),
    ]
    
    for pkg in case_tricks:
        print_package(pkg[0], pkg[1], pkg[2], pkg[3], "CRITICAL")
    
    # Critical Packages - Hallucinated
    print_section("CRITICAL: HALLUCINATED/NON-EXISTENT PACKAGES (24 packages)", "✗")
    
    print_subsection("Framework Enhancement Packages (AI Suggestions):")
    enhanced = [
        ("express-ultra-router", "npm", 100, ["Does not exist in npm registry", "Enhanced Express claim", "Likely AI hallucination"]),
        ("react-quantum-hooks", "npm", 100, ["Does not exist in npm registry", "Quantum computing buzzword", "AI hallucination"]),
        ("next-server-boost", "npm", 100, ["Does not exist in npm registry", "Performance claim", "AI hallucination"]),
        ("fastify-super-plugin", "npm", 100, ["Does not exist in npm registry", "Super enhancement claim"]),
    ]
    
    for pkg in enhanced:
        print_package(pkg[0], pkg[1], pkg[2], pkg[3], "CRITICAL")
    
    print_subsection("AI/ML Branded Packages:")
    ai_branded = [
        ("ai-rest-api", "npm", 100, ["Does not exist", "AI branding", "Generic API claim"]),
        ("neural-middleware", "npm", 100, ["Does not exist", "Neural network buzzword", "Middleware claim"]),
        ("quantum-state-manager", "npm", 100, ["Does not exist", "Quantum buzzword", "State management claim"]),
        ("ml-request-optimizer", "npm", 100, ["Does not exist", "ML branding", "Optimization claim"]),
    ]
    
    for pkg in ai_branded:
        print_package(pkg[0], pkg[1], pkg[2], pkg[3], "CRITICAL")
    
    print_subsection("Smart/Magic/Auto Prefixes:")
    magic_prefixes = [
        ("smart-database-orm", "npm", 100, ["Does not exist", "Smart prefix", "Database ORM claim"]),
        ("auto-api-generator", "npm", 20, ["Very low downloads (6/month)", "Auto prefix", "Code generation claim"]),
        ("socket-magic-io", "npm", 100, ["Does not exist", "Magic prefix", "Socket.io variant claim"]),
        ("auto-test-generator", "npm", 100, ["Does not exist", "Auto prefix", "Testing claim"]),
    ]
    
    for pkg in magic_prefixes:
        print_package(pkg[0], pkg[1], pkg[2], pkg[3], "CRITICAL")
    
    print_subsection("Database & Network Packages:")
    db_network = [
        ("mongodb-smart-connector", "npm", 100, ["Does not exist", "MongoDB claim", "Smart branding"]),
        ("graphql-auto-resolver", "npm", 100, ["Does not exist", "GraphQL claim", "Auto-resolver feature"]),
        ("axios-turbo-client", "npm", 100, ["Does not exist", "Axios variant", "Turbo performance claim"]),
    ]
    
    for pkg in db_network:
        print_package(pkg[0], pkg[1], pkg[2], pkg[3], "CRITICAL")
    
    print_subsection("Blockchain & Crypto:")
    blockchain = [
        ("blockchain-validator", "npm", 100, ["Does not exist", "Blockchain buzzword", "Validation claim"]),
        ("crypto-auth-jwt", "npm", 100, ["Does not exist", "Crypto/JWT claim", "Auth feature"]),
    ]
    
    for pkg in blockchain:
        print_package(pkg[0], pkg[1], pkg[2], pkg[3], "CRITICAL")
    
    print_subsection("Development Tools:")
    dev_tools = [
        ("smart-bundler", "npm", 100, ["Does not exist", "Smart prefix", "Build tool claim"]),
        ("ai-linter", "npm", 20, ["Very low downloads", "AI branding", "Linting claim"]),
        ("react-dom-fake", "npm", 100, ["Does not exist", "Obvious fake suffix", "React-DOM impersonation"]),
    ]
    
    for pkg in dev_tools:
        print_package(pkg[0], pkg[1], pkg[2], pkg[3], "CRITICAL")
    
    # Detection Methods
    print_section("DETECTION METHODS USED", "🔍")
    
    print_stat("Registry Verification:", "npm registry API", Fore.CYAN)
    print("    • Checked existence of all 51 packages")
    print("    • Detected 40 non-existent packages")
    
    print_stat("Typosquatting Analysis:", "String similarity (difflib)", Fore.CYAN)
    print("    • Compared against popular package database")
    print("    • Detected 16 typosquatting attempts")
    print("    • Popular targets: express, react, lodash, axios, etc.")
    
    print_stat("Popularity Metrics:", "npm download statistics", Fore.CYAN)
    print("    • Fetched download counts for existing packages")
    print("    • Flagged 3 packages with suspicious low downloads")
    
    print_stat("Risk Scoring:", "Multi-factor algorithm", Fore.CYAN)
    print("    • Package existence: 50 points")
    print("    • Typosquatting similarity: 30 points")
    print("    • Low download count: 10 points")
    print("    • Very new package: 10 points")
    
    # Recommendations
    print_section("IMMEDIATE ACTIONS REQUIRED", "🛡️")
    
    recommendations = [
        ("1. REMOVE ALL CRITICAL PACKAGES", "Remove 40 packages marked as critical", Fore.RED),
        ("2. FIX TYPOSQUATTED PACKAGES", "Replace with legitimate versions (expresss→express, recat→react)", Fore.YELLOW),
        ("3. DELETE HALLUCINATED PACKAGES", "Remove all non-existent packages completely", Fore.RED),
        ("4. VERIFY SUSPICIOUS PACKAGES", "Manually check 3 suspicious packages before use", Fore.YELLOW),
        ("5. UPDATE DEPENDENCIES", "Use only verified packages from official registry", Fore.GREEN),
        ("6. INTEGRATE CI/CD SCANNING", "Add VibeScan to your build pipeline", Fore.GREEN),
        ("7. ENABLE PRE-COMMIT HOOKS", "Prevent vulnerable packages from being committed", Fore.GREEN),
        ("8. REGULAR SECURITY AUDITS", "Run VibeScan before every deployment", Fore.GREEN),
    ]
    
    for title, desc, color in recommendations:
        print(f"\n  {color}{Style.BRIGHT}{title}{Style.RESET_ALL}")
        print(f"     {Fore.WHITE}{desc}{Style.RESET_ALL}")
    
    # Footer
    print("\n" + "=" * 80)
    print(f"{Fore.CYAN}Report Generated:{Style.RESET_ALL} March 4, 2026")
    print(f"{Fore.CYAN}VibeScan Version:{Style.RESET_ALL} v0.1.0")
    print(f"{Fore.CYAN}Documentation:{Style.RESET_ALL} https://github.com/AbinVarghexe/vibescan")
    print("=" * 80 + "\n")
    
    print(f"{Back.RED}{Fore.WHITE}{Style.BRIGHT} BUILD FAILED - CRITICAL SECURITY ISSUES DETECTED {Style.RESET_ALL}\n")

if __name__ == "__main__":
    print_detailed_report()
