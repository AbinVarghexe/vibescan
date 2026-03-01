# VibeScan - Quick Start Guide

Get started with VibeScan in under 5 minutes!

## 🚀 Installation

### For Python Projects

```bash
pip install vibescan
```

### For Node.js Projects

```bash
npm install -g vibescan-js
```

## 💡 Basic Usage

### Scan Your Current Project

Simply run in your project directory:

```bash
vibescan
```

VibeScan will automatically find and scan:
- `package.json` (for npm projects)
- `requirements.txt` (for Python projects)

### Scan a Specific Directory

```bash
vibescan /path/to/your/project
```

### Example Output

```
=========================================
              VibeScan
=========================================
Analyzing dependencies for AI hallucinations and slopsquatting...

Analyzing 25 dependencies...

✓ 23 Safe Dependencies

⚠ 1 Suspicious Dependencies (Review Recommended)
  - new-crypto-lib (npm) - Score: 45/100
    * Package is suspiciously new (Created 3 days ago)
    * Low download count (250 in last month)

❌ 1 Critical Risk Dependencies (Action Required!)
  - reqeusts (pypi) - Score: 100/100
    * Package does not exist in registry (Likely AI Hallucination/Slopsquat target)
    * Name is deceptively similar to popular package 'requests' (Typosquatting risk)

-----------------------------------------
VibeScan detected CRITICAL risks. Build failed.
```

## 🛠️ Common Use Cases

### 1. Pre-commit Check

Add to your `.pre-commit-config.yaml`:

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

Install pre-commit hooks:
```bash
pip install pre-commit
pre-commit install
```

### 2. CI/CD Integration (GitHub Actions)

Create `.github/workflows/vibescan.yml`:

```yaml
name: Security Scan
on: [push, pull_request]

jobs:
  vibescan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      - run: pip install vibescan
      - run: vibescan
```

### 3. Manual Code Review

Before merging a PR with dependency changes:

```bash
# Check the branch
git checkout feature-branch
vibescan

# Review any flagged dependencies
```

### 4. Web Interface

For teams or one-off checks, use the web interface:

```bash
# Start the web server
cd web
python app.py

# Open http://localhost:5000 in your browser
```

Upload your `package.json` or `requirements.txt` file or paste the content directly.

## 📊 Understanding Risk Scores

| Score | Severity | Action |
|-------|----------|--------|
| 0-9 | ✅ Safe | No action needed |
| 10-59 | ⚠️ Suspicious | Review and investigate |
| 60-100 | ❌ Critical | Remove or fix immediately |

### What Increases Risk Score?

- **+100**: Package doesn't exist (AI hallucination)
- **+60**: Name similar to popular package (typosquatting)
- **+40**: Package created <7 days ago
- **+20**: Very low downloads (<100/month)
- **+10**: Package created <30 days ago
- **+5**: Low downloads (<1000/month)

## 🔍 Real-World Examples

### Example 1: AI Hallucinated Package

```python
# requirements.txt
requests==2.28.0
crypto-secure-hasher-v2==1.0.0  # ❌ Doesn't exist!
```

VibeScan detects: `crypto-secure-hasher-v2 does not exist in registry`

### Example 2: Typosquatting

```json
{
  "dependencies": {
    "reactt": "^18.0.0"  // ❌ Should be "react"
  }
}
```

VibeScan detects: `reactt is deceptively similar to popular package 'react'`

### Example 3: Suspiciously New Package

A package created 2 days ago with 50 downloads triggers a warning, allowing you to investigate before adding it.

## 🎓 Best Practices

1. **Run VibeScan regularly**: Integrate into your workflow
2. **Review suspicious packages**: Don't ignore warnings
3. **Update VibeScan**: Keep the tool updated for latest patterns
4. **Check before copy-pasting**: AI-generated code may contain hallucinations
5. **Educate your team**: Share findings and train on risks

## 🐛 Troubleshooting

### "Command not found: vibescan"

**Solution**: Ensure installation path is in your PATH
```bash
# Python
pip install --user vibescan
# Add ~/.local/bin to PATH

# npm
npm install -g vibescan-js
# npm global bin should be in PATH
```

### "No package.json or requirements.txt found"

**Solution**: Navigate to your project directory or specify path
```bash
vibescan /path/to/project
```

### Network Errors

VibeScan needs internet access to check package registries. If behind a proxy:

```bash
export HTTP_PROXY=http://proxy:port
export HTTPS_PROXY=https://proxy:port
```

## 📚 More Resources

- [Full Documentation](README.md)
- [Deployment Guide](DEPLOYMENT.md)
- [Web Interface Guide](web/README.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Issue Tracker](https://github.com/yourusername/vibescan/issues)

## 💬 Getting Help

- **GitHub Issues**: Report bugs or request features
- **Documentation**: Check README.md for detailed info
- **Web Interface**: Try the visual tool at http://localhost:5000

---

**Stay safe in the AI coding era! 🛡️**