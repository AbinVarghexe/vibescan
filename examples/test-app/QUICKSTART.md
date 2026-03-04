# VibeScan Demo - Quick Start Guide

## 🚀 Quick Demo

This demo showcases VibeScan's ability to detect security vulnerabilities in project dependencies.

### Step 1: View the Vulnerable Dependencies

**Python Dependencies** ([requirements.txt](requirements.txt)):
```txt
Flask==3.0.0          # ✅ Legitimate
requests==2.31.0      # ✅ Legitimate

reqeusts==1.0.0       # ⚠️ Typosquatting "requests"
djago==2.0.0          # ⚠️ Typosquatting "django"
numpyy==1.0.0         # ⚠️ Typosquatting "numpy"

flask-super-auth==1.0.0           # 🚫 Hallucinated
ai-data-processor==3.0.0          # 🚫 Hallucinated
quantum-validator==1.0.0          # 🚫 Hallucinated
```

**JavaScript Dependencies** ([package.json](package.json)):
```json
"express": "^4.18.0"   // ✅ Legitimate
"axios": "^1.6.0"      // ✅ Legitimate

"expresss": "1.0.0"    // ⚠️ Typosquatting "express"
"recat": "18.0.0"      // ⚠️ Typosquatting "react"
"lodsh": "4.17.0"      // ⚠️ Typosquatting "lodash"

"react-super-hooks": "3.0.0"      // 🚫 Hallucinated
"neural-state-manager": "4.0.0"   // 🚫 Hallucinated
```

### Step 2: Run VibeScan

From the vibescan root directory:

```bash
vibescan test-app
```

**Expected Output:**
```
=========================================
              VibeScan
=========================================
Analyzing dependencies for AI hallucinations and slopsquatting...

Analyzing 29 dependencies...

OK 2 Safe Dependencies

!! 2 Suspicious Dependencies (Review Recommended)

XX 25 Critical Risk Dependencies (Action Required!)

-----------------------------------------
VibeScan detected CRITICAL risks. Build failed.
```

### Step 3: View Detailed Results

Run with debug flag for more details:

```bash
vibescan test-app --debug
```

Or check the [detailed results document](SCAN_RESULTS.md).

### Step 4: Run the Web Application (Optional)

To see the vulnerabilities visualized in a web interface:

1. Install only legitimate dependencies:
```bash
cd test-app
pip install Flask==3.0.0 requests==2.31.0
```

2. Start the web app:
```bash
python app.py
```

3. Open browser to: http://localhost:5000

---

## 📊 What VibeScan Detects

### 1. Typosquatting (7 instances)
Malicious packages with names similar to popular packages:
- `reqeusts` vs `requests`
- `djago` vs `django`
- `numpyy` vs `numpy`
- `expresss` vs `express`
- `recat` vs `react`

### 2. Hallucinated Dependencies (18 instances)
Non-existent packages that don't exist in any registry:
- `flask-super-auth`
- `ai-data-processor`
- `quantum-validator`
- `neural-state-manager`
- `magic-http-client`

### 3. Suspicious Packages (2 instances)
Real packages with concerning metrics:
- Very low download counts
- Unusual naming patterns

---

## 🎯 Real-World Scenarios

### Scenario 1: AI Generated Code
AI coding assistants sometimes suggest packages that don't exist. VibeScan catches these before you try to install them.

**Example:**
```python
# AI suggests
from quantum_validator import validate_data

# VibeScan warns
XX quantum-validator: Package does not exist in registry
```

### Scenario 2: Typo in Package Name
Easy to make typos when typing package names. VibeScan detects similar names.

**Example:**
```bash
# Developer types
pip install reqeusts

# VibeScan warns
XX reqeusts: Similar to popular package 'requests'
```

### Scenario 3: Pre-Deployment Check
Run VibeScan before deploying to production to catch security issues.

```bash
vibescan . || exit 1  # Fail build on critical issues
```

---

## 📁 Demo Files

- **[app.py](app.py)** - Flask web application
- **[requirements.txt](requirements.txt)** - Python dependencies with issues
- **[package.json](package.json)** - JavaScript dependencies with issues
- **[templates/index.html](templates/index.html)** - Web interface
- **[SCAN_RESULTS.md](SCAN_RESULTS.md)** - Detailed VibeScan results
- **[README.md](README.md)** - Full documentation

---

## 🛡️ Security Tips

1. ✅ **Always scan before installing** new dependencies
2. ✅ **Verify package names** in official registries
3. ✅ **Review AI suggestions** carefully
4. ✅ **Use exact version pinning** in production
5. ✅ **Run VibeScan in CI/CD** pipelines

---

## 📞 Support

- GitHub: https://github.com/AbinVarghexe/vibescan
- Documentation: https://abinvarghexe.github.io/vibescan/
- Issues: https://github.com/AbinVarghexe/vibescan/issues

---

**⚠️ Remember:** This is a demo application with intentional vulnerabilities. Never use these packages in production!
