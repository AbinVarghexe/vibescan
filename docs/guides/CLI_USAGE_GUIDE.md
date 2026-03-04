# VibeScan CLI Usage Guide

## Enhanced Terminal-Friendly Interface

VibeScan now features a modern, terminal-friendly CLI interface with:
- ✨ Professional ASCII art banner
- 📊 Real-time progress bars
- 🎨 Color-coded output
- 📄 Automatic report generation
- ⚡ Fast security scanning

## Quick Start

### Basic Scan
Scan the current directory:
```bash
vibescan
```

### Scan Specific Project
```bash
vibescan ./my-project
```

### Scan with Options
```bash
# Skip automatic report generation
vibescan ./my-project --no-report

# Generate JSON report only (skip PDF)
vibescan ./my-project --json-only

# Custom output directory
vibescan ./my-project --output-dir custom-reports

# Enable debug mode
vibescan ./my-project --debug
```

## Command-Line Options

| Option | Description |
|--------|-------------|
| `path` | Path to the directory to scan (default: `.`) |
| `--no-report` | Skip automatic report generation |
| `--json-only` | Generate JSON and TXT reports only (skip PDF) |
| `--output-dir DIR` | Directory to save reports (default: `vibescan-reports`) |
| `--debug` | Enable debug output |
| `--help` | Show help message |

## Output Format

### Terminal Output

The CLI displays:
1. **Banner** - VibeScan ASCII art logo
2. **Detection** - Files detected (package.json, requirements.txt)
3. **Progress Bar** - Real-time package analysis progress
4. **Results Summary** - Color-coded security findings:
   - 🟢 **Green** - Safe dependencies
   - 🟡 **Yellow** - Suspicious packages (review recommended)
   - 🔴 **Red** - Critical issues (action required)
5. **Report Paths** - Full paths to generated reports

### Example Output

```
================================================================================

    ██╗   ██╗██╗██████╗ ███████╗███████╗ ██████╗ █████╗ ███╗   ██╗
    ██║   ██║██║██╔══██╗██╔════╝██╔════╝██╔════╝██╔══██╗████╗  ██║
    ██║   ██║██║██████╔╝█████╗  ███████╗██║     ███████║██╔██╗ ██║
    ╚██╗ ██╔╝██║██╔══██╗██╔══╝  ╚════██║██║     ██╔══██║██║╚██╗██║
     ╚████╔╝ ██║██████╔╝███████╗███████║╚██████╗██║  ██║██║ ╚████║
      ╚═══╝  ╚═╝╚═════╝ ╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝

                   AI Dependency Risk Scanner v0.1.0
================================================================================

📁 Scanning directory: /path/to/project
✓ Detected files: package.json, requirements.txt
📦 Total dependencies: 29

🔍 Starting security analysis...

Complete |██████████████████████████████████████████████████| 100.0% Analyzed 29 packages
✓ Analysis completed in 30.84s

================================================================================
                         SECURITY SCAN RESULTS
================================================================================

OK 2 Safe Dependencies

!! 2 Suspicious Dependencies (Review Recommended)
  - react-super-hooks (npm) - Score: 20/100
    * Very low download count (42 in last month) - suspicious popularity

XX 25 Critical Risk Dependencies (Action Required!)
  - expresss (npm) - Score: 60/100
    * Name is deceptively similar to popular package 'express' (Typosquatting risk)

================================================================================
                         GENERATING REPORTS
================================================================================

📄 Generating JSON report...
✓ JSON report saved: /path/to/project/vibescan-reports/vibescan_report_20260304_004228.json

📄 Generating detailed report...
✓ Detailed report saved: /path/to/project/vibescan-reports/vibescan_report_20260304_004228.txt

📄 Generating PDF report...
✓ PDF report saved: /path/to/project/vibescan-reports/vibescan_report_20260304_004228.pdf

================================================================================
✓ Reports saved to: /path/to/project/vibescan-reports
================================================================================
```

## Generated Reports

VibeScan automatically generates three types of reports:

### 1. JSON Report (`vibescan_report_TIMESTAMP.json`)
- Structured data format
- Easy to parse programmatically
- Perfect for CI/CD integration
- Contains:
  - Scan metadata (timestamp, path, version)
  - Summary statistics
  - Categorized packages (safe, suspicious, critical)

### 2. Detailed Text Report (`vibescan_report_TIMESTAMP.txt`)
- Human-readable format
- Complete security analysis
- Package-by-package breakdown
- Risk scores and detection reasons
- Security recommendations

### 3. PDF Report (`vibescan_report_TIMESTAMP.pdf`)
- Professional presentation format
- Executive summary with tables
- Color-coded risk indicators
- Ready for sharing with stakeholders
- Requires `reportlab` (auto-installed)

## Report Location

Reports are saved in the project directory:
```
your-project/
├── package.json
├── requirements.txt
└── vibescan-reports/
    ├── vibescan_report_20260304_123456.json
    ├── vibescan_report_20260304_123456.txt
    └── vibescan_report_20260304_123456.pdf
```

Each report filename includes a timestamp (`YYYYMMDD_HHMMSS`) to prevent overwrites.

## Exit Codes

VibeScan uses standard exit codes for CI/CD integration:

- **0** - Success (no critical issues found)
- **1** - Failure (critical security issues detected)

## CI/CD Integration

### GitHub Actions

```yaml
name: VibeScan Security Check

on: [push, pull_request]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      - name: Install VibeScan
        run: pip install vibescan
      - name: Run VibeScan
        run: vibescan .
      - name: Upload Reports
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: vibescan-reports
          path: vibescan-reports/
```

### GitLab CI

```yaml
vibescan:
  image: python:3.11
  script:
    - pip install vibescan
    - vibescan .
  artifacts:
    when: always
    paths:
      - vibescan-reports/
```

### Pre-commit Hook

Add to `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: local
    hooks:
      - id: vibescan
        name: VibeScan Security Check
        entry: vibescan
        language: system
        pass_filenames: false
```

## Understanding Risk Scores

| Score Range | Category | Meaning | Action |
|-------------|----------|---------|--------|
| 0-9 | Safe | Legitimate package | ✅ Safe to use |
| 10-59 | Suspicious | Requires review | ⚠️ Verify before use |
| 60-100 | Critical | High security risk | ❌ Remove immediately |

## Risk Detection Methods

VibeScan checks for:

1. **Typosquatting** - Packages with names similar to popular libraries
   - Character substitution (axois → axios)
   - Missing letters (expres → express)
   - Extra letters (reactt → react)
   - Letter swapping (recat → react)

2. **AI Hallucinations** - Non-existent packages suggested by AI
   - Package doesn't exist in registry
   - Generic/AI-sounding names
   - Unrealistic capabilities

3. **Suspicious Popularity** - Legitimate-looking but suspicious
   - Very low download counts
   - Recent creation date
   - Minimal maintenance

## Best Practices

1. **Run before installation** - Scan dependencies before `npm install` or `pip install`
2. **Integrate into CI/CD** - Fail builds on critical issues
3. **Review suspicious packages** - Don't ignore yellow warnings
4. **Keep VibeScan updated** - Get latest detection patterns
5. **Share reports** - Use PDF reports for security audits
6. **Regular scans** - Scan projects periodically, not just once

## Troubleshooting

### No dependency files found
```
✗ No package.json or requirements.txt found
```
**Solution:** Ensure you're in the correct directory with dependency files.

### PDF generation skipped
```
⚠ reportlab not installed. Skipping PDF generation.
```
**Solution:** Install reportlab: `pip install reportlab`

### Slow scanning
**Tip:** Use `--json-only` to skip PDF generation for faster scans.

## Advanced Usage

### Scan multiple projects
```bash
for dir in project1 project2 project3; do
  vibescan $dir
done
```

### Custom report directory
```bash
vibescan . --output-dir ../security-reports
```

### JSON-only for CI/CD
```bash
vibescan . --json-only --output-dir reports
```

### Parse JSON reports
```python
import json
with open('vibescan-reports/vibescan_report_TIMESTAMP.json') as f:
    report = json.load(f)
    if report['summary']['risk_level'] == 'CRITICAL':
        print("Security issues detected!")
        exit(1)
```

## Getting Help

```bash
vibescan --help
```

For more information:
- GitHub: https://github.com/AbinVarghexe/vibescan
- Issues: https://github.com/AbinVarghexe/vibescan/issues
- Documentation: https://github.com/AbinVarghexe/vibescan/docs

---

**VibeScan** - Protecting your dependencies from AI hallucinations and typosquatting attacks.
