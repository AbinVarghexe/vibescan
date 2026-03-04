# VibeScan Node.js Demo Application

## ⚠️ WARNING: INTENTIONALLY VULNERABLE NODE.JS APPLICATION

This is a pure Node.js/Express demo application with **42 intentionally vulnerable dependencies** to test VibeScan's npm package security analysis.

**DO NOT USE IN PRODUCTION!**

---

## 🎯 Purpose

Demonstrate VibeScan's ability to detect security issues in Node.js projects:

1. **Typosquatting Attacks** - 16 packages with names similar to popular npm packages
2. **Hallucinated Dependencies** - 26 non-existent packages (AI suggestions)
3. **Risk Assessment** - Comprehensive security scoring

---

## 📦 Package Vulnerabilities

### ✅ Legitimate Packages (5)

**Production Dependencies:**
- `express` ^4.18.2
- `axios` ^1.6.0
- `dotenv` ^16.3.1
- `cors` ^2.8.5

**Development Dependencies:**
- `nodemon` ^3.0.1

---

### ⚠️ Typosquatting Attempts (16)

Common typos and variations of popular packages:

| Malicious Package | Target Package | Attack Type |
|------------------|----------------|-------------|
| `expresss` | `express` | Extra letter |
| `expres` | `express` | Missing letter |
| `recat` | `react` | Letter swap |
| `lodsh` | `lodash` | Missing letter |
| `loodash` | `lodash` | Extra letter |
| `momnet` | `moment` | Letter swap |
| `axois` | `axios` | Letter swap |
| `chalkk` | `chalk` | Extra letter |
| `next-js` | `next` | Wrong hyphenation |
| `mongoose-db` | `mongoose` | Extra suffix |
| `tailwind-css` | `tailwindcss` | Wrong hyphenation |
| `prettier-format` | `prettier` | Extra suffix |
| `type-script` | `typescript` | Wrong hyphenation |
| `commander-js` | `commander` | Extra suffix |
| `esLint` | `eslint` | Wrong case |
| `webpck` | `webpack` | Missing letter |

---

### 🚫 Hallucinated Packages (26)

Non-existent packages that might be suggested by AI:

**Production Dependencies:**
- `express-ultra-router`
- `react-quantum-hooks`
- `next-server-boost`
- `axios-turbo-client`
- `fastify-super-plugin`
- `socket-magic-io`
- `graphql-auto-resolver`
- `mongodb-smart-connector`
- `ai-rest-api`
- `neural-middleware`
- `quantum-state-manager`
- `auto-api-generator`
- `smart-database-orm`
- `ml-request-optimizer`
- `blockchain-validator`
- `crypto-auth-jwt`
- `axios-mock`
- `react-dom-fake`

**Development Dependencies:**
- `auto-test-generator`
- `smart-bundler`
- `ai-linter`

---

## 🔍 Testing with VibeScan

### Basic Scan

From the vibescan root directory:

```bash
vibescan node-demo-app/
```

### Debug Mode

For detailed analysis:

```bash
vibescan node-demo-app/ --debug
```

---

## 📊 Expected Results

VibeScan should detect:

| Category | Count | Percentage |
|----------|-------|------------|
| **Total Packages** | 47 | 100% |
| 🚨 **Critical Issues** | 42 | 89.4% |
| ✅ **Safe Packages** | 5 | 10.6% |

**Breakdown:**
- **Typosquatting:** 16 packages
- **Hallucinated:** 26 packages
- **Risk Score:** 92/100 (CRITICAL)

---

## 🚀 Running the Demo Server

### Prerequisites

Only install legitimate dependencies:

```bash
cd node-demo-app
npm install express axios dotenv cors
npm install --save-dev nodemon
```

### Start the Server

```bash
npm start
```

Or with auto-reload:

```bash
npm run dev
```

### Access the Application

Open your browser to: **http://localhost:3000**

The web interface displays:
- Real-time vulnerability statistics
- List of all vulnerable packages
- Typosquatting examples
- Hallucinated package details
- Instructions for running VibeScan

---

## 🔥 API Endpoints

### GET /
Main dashboard with vulnerability visualization

### GET /api/stats
Returns vulnerability statistics:
```json
{
  "total_dependencies": 47,
  "safe": 5,
  "critical": 42,
  "breakdown": {
    "typosquatting": 16,
    "hallucinated": 26
  },
  "risk_score": 92
}
```

### GET /api/vulnerabilities
Returns detailed vulnerability information

### POST /api/scan
Simulates VibeScan execution

### GET /health
Health check endpoint

---

## 🛡️ Security Issues Demonstrated

### 1. Typosquatting Attack Vector

**Scenario:** Developer makes a typo when installing a package

```bash
npm install expresss  # Wrong!
# Should be: npm install express
```

**VibeScan Detection:**
```
XX expresss: Name is deceptively similar to popular package 'express'
```

### 2. AI Hallucination Vector

**Scenario:** AI assistant suggests a non-existent package

```javascript
// AI suggests:
import { useQuantumHooks } from 'react-quantum-hooks';
```

**VibeScan Detection:**
```
XX react-quantum-hooks: Package does not exist in registry
```

### 3. Sophisticated Naming Attacks

**Scenario:** Malicious packages with plausible-sounding names

```json
{
  "dependencies": {
    "express-ultra-router": "2.0.0",  // Sounds legitimate!
    "axios-turbo-client": "2.5.0"     // But doesn't exist
  }
}
```

---

## 📁 Project Structure

```
node-demo-app/
├── server.js          # Express server with API endpoints
├── package.json       # Dependencies with intentional issues
├── public/
│   └── index.html    # Web dashboard
└── README.md         # This file
```

---

## 🧪 Testing Scenarios

### Scenario 1: Pre-Installation Check

Before running `npm install`, scan the project:

```bash
vibescan node-demo-app/
```

Result: **Build fails** with 42 critical issues detected

### Scenario 2: CI/CD Pipeline

Add to your CI/CD workflow:

```yaml
# GitHub Actions
- name: Security Scan
  run: |
    npm install -g vibescan
    vibescan . || exit 1
```

### Scenario 3: Code Review

Run VibeScan during code review to catch malicious dependencies before merge.

---

## 📝 VibeScan Output Example

```
=========================================
              VibeScan
=========================================
Analyzing dependencies...

Found package.json at node-demo-app/package.json

Analyzing 47 dependencies...

OK 5 Safe Dependencies

XX 42 Critical Risk Dependencies (Action Required!)
  - expresss (npm) - Score: 60/100
    * Name is deceptively similar to 'express'
  
  - react-quantum-hooks (npm) - Score: 100/100
    * Package does not exist in registry
  
  ... (40 more critical issues)

-----------------------------------------
VibeScan detected CRITICAL risks. Build failed.
Exit Code: 1
```

---

## 🔧 Remediation Guide

### Step 1: Remove All Critical Packages

Delete all typosquatted and hallucinated packages from package.json

### Step 2: Fix Typos

Replace typosquatted packages with legitimate versions:
- `expresss` → `express`
- `recat` → `react`
- `lodsh` → `lodash`

### Step 3: Remove Hallucinated Packages

Delete non-existent packages entirely:
- `react-quantum-hooks` ❌
- `express-ultra-router` ❌
- `ai-rest-api` ❌

### Step 4: Verify Installation

```bash
npm install
vibescan .
```

Should report: ✅ All dependencies safe

---

## 🎓 Key Takeaways

1. **Always verify package names** before installation
2. **Be skeptical of AI suggestions** - they can hallucinate
3. **Use VibeScan** as a pre-commit hook
4. **Watch for typos** in package names
5. **Check npm registry** for unfamiliar packages

---

## 🌐 Integration Examples

### Pre-commit Hook

```bash
#!/bin/sh
# .git/hooks/pre-commit
vibescan . || exit 1
```

### NPM Script

```json
{
  "scripts": {
    "presecurity": "vibescan .",
    "preinstall": "vibescan ."
  }
}
```

### Docker Build

```dockerfile
RUN npm install -g vibescan && \
    vibescan /app || exit 1
```

---

## 📚 Additional Resources

- [VibeScan Documentation](https://abinvarghexe.github.io/vibescan/)
- [npm Security Best Practices](https://docs.npmjs.com/about-security-best-practices)
- [Typosquatting Explained](https://en.wikipedia.org/wiki/Typosquatting)

---

## ⚡ Quick Commands

```bash
# Scan the application
vibescan node-demo-app/

# Start the demo server
cd node-demo-app
npm start

# View web dashboard
open http://localhost:3000
```

---

**⚠️ Disclaimer:** This is a security testing application. The vulnerable dependencies are intentional and should never be used in production environments.
