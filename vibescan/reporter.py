from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def print_banner():
    print(f"{Fore.CYAN}{Style.BRIGHT}=========================================")
    print(f"{Fore.CYAN}{Style.BRIGHT}              VibeScan                   ")
    print(f"{Fore.CYAN}{Style.BRIGHT}=========================================")
    print("Analyzing dependencies for AI hallucinations and slopsquatting...\n")

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

    print(f"{Fore.GREEN}{Style.BRIGHT}✓ {len(safe)} Safe Dependencies")
    
    if suspicious:
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}⚠ {len(suspicious)} Suspicious Dependencies (Review Recommended)")
        for s in suspicious:
            print(f"  - {Fore.YELLOW}{s['name']}{Style.RESET_ALL} ({s['ecosystem']}) - Score: {s['score']}/100")
            for r in s['reasons']:
                print(f"    * {r}")
                
    if critical:
        print(f"\n{Fore.RED}{Style.BRIGHT}❌ {len(critical)} Critical Risk Dependencies (Action Required!)")
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
