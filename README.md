# VibeScan 🔍

**VibeScan** is a cross-platform, pre-publish security analysis tool built for the modern AI-assisted development era. It detects **hallucinated dependencies**, typosquatting ("slopsquatting"), and risky packages before they enter your codebase.

## 🎯 Why VibeScan?

As developers increasingly rely on LLM code generators, the risk of introducing non-existent or malicious packages has skyrocketed. VibeScan acts as your first line of defense, catching AI hallucinations and slopsquatting attempts before they reach production.

## ✨ Features

- **🔎 Hallucination Detection**: Verifies packages exist in npm and PyPI registries
- **🎭 Typosquatting Defense**: Detects names similar to popular packages
- **📊 Risk Scoring**: Assigns explainable risk scores (0-100) to each dependency
- **⚡ Fast & Local**: Runs in seconds without sending source code to remote servers
- **🔄 Cross-Ecosystem**: Supports both Python and Node.js projects
- **🎨 Beautiful Output**: Color-coded results with clear explanations

## 🌐 Live Web App

**Try it now**: https://vibescen.streamlit.app/

No installation needed - just upload your `package.json` or `requirements.txt`!

## 📦 Installation

### Python (PyPI)

```bash
pip install vibescan
```

### Node.js (npm)

```bash
npm install -g vibescan-js
```

## 🚀 Usage

### Command Line

Scan your current project:

```bash
vibescan
```

Scan a specific directory:

```bash
vibescan ./my-project
```

Enable debug output:

```bash
vibescan --debug
```

### Pre-commit Hook

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
        always_run: true
```

### CI/CD Integration

#### GitHub Actions

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
      - name: Install VibeScan
        run: pip install vibescan
      - name: Run VibeScan
        run: vibescan
```

#### GitLab CI

```yaml
vibescan:
  image: python:3.11
  script:
    - pip install vibescan
    - vibescan
  only:
    - merge_requests
```

## 📊 Risk Scoring

VibeScan assigns risk scores based on multiple factors:

| Score | Severity | Description |
|-------|----------|-------------|
| 0-9   | ✅ Safe | No risks detected |
| 10-59 | ⚠️ Suspicious | Review recommended |
| 60-100 | ❌ Critical | Action required |

### Risk Factors

- **Package doesn't exist**: +100 (likely AI hallucination)
- **Typosquatting detected**: +60 (similar to popular package)
- **Suspiciously new** (<7 days): +40
- **Relatively new** (<30 days): +10

## 🔍 What It Checks

### Supported Files

- `package.json` (npm dependencies & devDependencies)
- `requirements.txt` (Python packages)

### Detection Capabilities

1. **Registry Verification**: Checks if packages exist on npm/PyPI
2. **Typosquatting**: Detects names similar to popular packages:
   - `reactt` → Similar to `react`
   - `reqeusts` → Similar to `requests`
3. **Age Analysis**: Flags newly created packages
4. **Popularity Heuristics**: Identifies suspicious low-usage packages

## 📝 Example Output

```
=========================================
              VibeScan                   
=========================================
Analyzing dependencies for AI hallucinations and slopsquatting...

Analyzing 5 dependencies...

✓ 3 Safe Dependencies

⚠ 1 Suspicious Dependencies (Review Recommended)
  - new-package (npm) - Score: 40/100
    * Package is suspiciously new (Created 2 days ago)

❌ 1 Critical Risk Dependencies (Action Required!)
  - crypto-secure-hash-v2-hallucinated (npm) - Score: 100/100
    * Package does not exist in registry (Likely AI Hallucination/Slopsquat target)

-----------------------------------------
VibeScan detected CRITICAL risks. Build failed.
```

## 🧪 Development

### Project Structure

```
vibescan/
├── vibescan/
│   ├── cli.py              # Command-line interface
│   ├── parsers.py          # Package file parsers
│   ├── scorer.py           # Risk scoring logic
│   ├── reporter.py         # Output formatting
│   └── checkers/
│       ├── registry_checker.py   # Registry verification
│       └── typosquat_checker.py  # Typosquatting detection
├── js-wrapper/            # Node.js wrapper
└── setup.py               # Python package config
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - see LICENSE file for details

## 🔒 Privacy

VibeScan respects your privacy:
- Analyzes code locally
- Only sends package names to public registries for verification
- No proprietary code is transmitted

## 🎯 Roadmap

- [ ] Support for more package managers (Cargo, Go modules)
- [ ] Static code analysis (AST) for unusual imports
- [ ] Configurable risk thresholds
- [ ] JSON output format
- [ ] Web dashboard for team visibility
- [ ] Integration with popular IDEs

## 💡 Use Cases

- **Pre-commit**: Catch risky dependencies before committing
- **CI/CD**: Block PRs with suspicious packages
- **Code Review**: Verify external contributions
- **Security Audit**: Scan existing projects for risks

## 🙏 Acknowledgments

Built to address the emerging threat of "slopsquatting" - malicious packages targeting AI-generated code suggestions.

---

**Stay safe in the AI coding era! 🛡️**
