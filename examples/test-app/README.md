# VibeScan Demo Application

## ⚠️ WARNING: INTENTIONALLY VULNERABLE APPLICATION

This is a demo web application that contains **intentionally vulnerable dependencies** to demonstrate VibeScan's security analysis capabilities. 

**DO NOT USE IN PRODUCTION!**

## 🎯 Purpose

This application demonstrates VibeScan's ability to detect:

1. **Typosquatting Attacks**: Malicious packages with names similar to popular legitimate packages
2. **Hallucinated Dependencies**: Non-existent packages that might be suggested by AI coding assistants
3. **Security Risk Assessment**: Risk scoring and categorization of dependencies

## 📦 Intentional Vulnerabilities

### Python Dependencies (requirements.txt)

**Legitimate Packages:**
- `Flask==3.0.0`
- `requests==2.31.0`

**Typosquatting Attempts:**
- `reqeusts` (typo of "requests")
- `djago` (typo of "django")
- `numpyy` (typo of "numpy")
- `pandsa` (typo of "pandas")
- `flsk` (typo of "flask")
- `pythonrequest` (similar to "requests")

**Hallucinated Packages:**
- `flask-super-auth`
- `secure-web-framework`
- `ai-data-processor`
- `magic-database-connector`
- `ultra-fast-api`
- `quantum-validator`
- `neural-web-engine`

### JavaScript Dependencies (package.json)

**Legitimate Packages:**
- `express`
- `axios`

**Typosquatting Attempts:**
- `expresss` (typo of "express")
- `recat` (typo of "react")
- `lodsh` (typo of "lodash")
- `momnet` (typo of "moment")
- `axois` (typo of "axios")

**Hallucinated Packages:**
- `react-super-hooks`
- `express-quantum-router`
- `ai-frontend-framework`
- `neural-state-manager`
- `magic-http-client`

## 🔍 How to Test with VibeScan

### 1. Scan the Application

From the vibescan root directory, run:

```bash
vibescan test-app/
```

### 2. Expected Results

VibeScan should detect approximately:
- **13 Critical issues** (hallucinated/non-existent packages)
- **5 Warning issues** (typosquatting attempts)
- **2 Safe packages** (legitimate dependencies)

### 3. Run with Debug Output

For more detailed analysis:

```bash
vibescan test-app/ --debug
```

## 🚀 Running the Demo Application

### Install Only Legitimate Dependencies

Since the requirements.txt contains problematic packages, install only Flask and requests manually:

```bash
cd test-app
pip install Flask==3.0.0 requests==2.31.0
```

### Start the Web Application

```bash
python app.py
```

The application will be available at: http://localhost:5000

### Features

The web interface provides:
- Visual overview of all intentional vulnerabilities
- Statistics on issue types
- Information about each problematic dependency
- Instructions for running VibeScan

## 📊 Understanding the Issues

### Typosquatting

Typosquatting is when attackers create packages with names very similar to popular packages, hoping developers will install them by mistake. Examples:
- `reqeusts` instead of `requests`
- `numpyy` instead of `numpy`

**VibeScan Detection**: Uses similarity algorithms to identify packages that closely match popular package names.

### Hallucinated Dependencies

These are packages that don't exist in any registry. They might be:
- Suggested by AI coding assistants
- Misremembered package names
- Proposed future packages that don't exist yet

**VibeScan Detection**: Checks registries (PyPI, npm) to verify package existence.

## 🛡️ Security Best Practices

1. **Always verify package names** before adding them to your project
2. **Use VibeScan** before deploying dependencies
3. **Review AI-suggested packages** carefully
4. **Pin exact versions** in production
5. **Regular security audits** of dependencies

## 📁 Project Structure

```
test-app/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies (with intentional issues)
├── package.json          # Node.js dependencies (with intentional issues)
├── templates/
│   └── index.html        # Web interface
└── README.md             # This file
```

## 🧪 Testing Scenarios

### Scenario 1: Pre-deployment Security Check
```bash
# Before deploying, scan for vulnerabilities
vibescan test-app/
```

### Scenario 2: CI/CD Integration
```bash
# Use in CI/CD pipeline (will fail on critical issues)
vibescan test-app/ || exit 1
```

### Scenario 3: Debug Mode
```bash
# Get detailed information about each package
vibescan test-app/ --debug
```

## 📝 Expected VibeScan Output

VibeScan should report:

```
Scanning: test-app/

Found dependency files:
- requirements.txt (16 packages)
- package.json (12 packages)

Issues Detected:
[CRITICAL] flask-super-auth: Package not found in PyPI registry
[CRITICAL] secure-web-framework: Package not found in PyPI registry
[WARNING] reqeusts: Possible typosquatting of "requests"
[WARNING] djago: Possible typosquatting of "django"
... (more issues)

Summary:
- Total packages: 28
- Safe: 2
- Suspicious: 5
- Critical: 13

Risk Score: 85/100 (HIGH RISK)
```

## 🤝 Contributing

This demo application is part of the VibeScan project. To suggest improvements:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📄 License

This demo application is part of VibeScan and is licensed under the MIT License.

## ⚡ Disclaimer

This application is for educational and testing purposes only. The packages listed in requirements.txt and package.json should never be used in production environments.
