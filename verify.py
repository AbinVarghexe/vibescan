#!/usr/bin/env python3
"""
VibeScan - Verification Script
Checks that all components are working correctly
"""

import sys
import subprocess
import os
from pathlib import Path

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def check_mark(success):
    return "✅" if success else "❌"

def run_check(name, command, cwd=None):
    """Run a check and return success status"""
    print(f"Checking {name}... ", end="", flush=True)
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd,
            capture_output=True, 
            text=True,
            timeout=30
        )
        success = result.returncode == 0
        print(f"{check_mark(success)}")
        if not success and result.stderr:
            print(f"  Error: {result.stderr[:200]}")
        return success
    except Exception as e:
        print(f"❌ \n  Error: {str(e)}")
        return False

def check_file_exists(name, path):
    """Check if a file exists"""
    print(f"Checking {name}... ", end="", flush=True)
    exists = Path(path).exists()
    print(f"{check_mark(exists)}")
    return exists

def main():
    print_header("VibeScan Verification")
    
    all_checks = []
    
    # 1. File Structure Checks
    print_header("1. File Structure")
    files_to_check = [
        ("README.md", "README.md"),
        ("LICENSE", "LICENSE"),
        ("setup.py", "setup.py"),
        ("pyproject.toml", "pyproject.toml"),
        ("DEPLOYMENT.md", "DEPLOYMENT.md"),
        ("Dockerfile", "Dockerfile"),
        ("CLI module", "vibescan/cli.py"),
        ("Parsers module", "vibescan/parsers.py"),
        ("Registry checker", "vibescan/checkers/registry_checker.py"),
        ("Typosquat checker", "vibescan/checkers/typosquat_checker.py"),
        ("Web app", "web/app.py"),
        ("Web template", "web/templates/index.html"),
        ("JS wrapper", "js-wrapper/index.js"),
    ]
    
    for name, path in files_to_check:
        all_checks.append(check_file_exists(name, path))
    
    # 2. Python Package Checks
    print_header("2. Python Package")
    all_checks.append(run_check("Python imports", "python -c \"import vibescan\""))
    all_checks.append(run_check("CLI module", "python -c \"from vibescan.cli import main\""))
    
    # 3. Test Suite
    print_header("3. Test Suite")
    all_checks.append(run_check("Pytest", "pytest tests/ -v"))
    
    # 4. Build Checks
    print_header("4. Build Artifacts")
    all_checks.append(check_file_exists("Wheel package", "dist/vibescan-0.1.0-py3-none-any.whl"))
    all_checks.append(check_file_exists("Source distribution", "dist/vibescan-0.1.0.tar.gz"))
    
    # 5. CLI Functionality
    print_header("5. CLI Functionality")
    all_checks.append(run_check("CLI execution", "python -m vibescan.cli --help"))
    # Dummy project scan exits with code 1 when risks found (expected behavior)
    print(f"Checking Dummy project scan... ", end="", flush=True)
    try:
        result = subprocess.run(
            "python -m vibescan.cli dummy_project",
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        # Expected to fail (exit code 1) because dummy has risky packages
        if result.returncode == 1 and "CRITICAL risks" in result.stdout:
            print("✅ (Correctly detected risks)")
            all_checks.append(True)
        else:
            print("❌")
            all_checks.append(False)
    except Exception as e:
        print(f"❌ \n  Error: {str(e)}")
        all_checks.append(False)
    
    # Summary
    print_header("Summary")
    passed = sum(all_checks)
    total = len(all_checks)
    percentage = (passed / total) * 100 if total > 0 else 0
    
    print(f"Checks passed: {passed}/{total} ({percentage:.1f}%)")
    print()
    
    if passed == total:
        print("🎉 All checks passed! VibeScan is ready for deployment.")
        return 0
    else:
        print("⚠️  Some checks failed. Please review the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())