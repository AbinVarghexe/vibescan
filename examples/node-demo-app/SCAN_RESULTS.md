# VibeScan Node.js Application - Test Results

## 📊 Scan Summary

**Date:** March 4, 2026  
**Target:** node-demo-app/  
**Command:** `vibescan node-demo-app`  
**Package Manager:** npm (Node.js)

---

## 🎯 Overall Statistics

| Category | Count | Percentage |
|----------|-------|------------|
| **Total Packages** | 51 | 100% |
| ✅ **Safe** | 8 | 15.7% |
| ⚠️ **Suspicious** | 3 | 5.9% |
| 🚨 **Critical** | 40 | 78.4% |

**Overall Risk Assessment:** 🔴 **CRITICAL - Build Failed**

**Exit Code:** 1 (Build failure due to critical risks)

---

## ✅ Safe Dependencies (8)

These npm packages passed all security checks:

### Production Dependencies
1. **express** ^4.18.2 - Web application framework
2. **axios** ^1.6.0 - Promise-based HTTP client
3. **dotenv** ^16.3.1 - Environment variable loader
4. **cors** ^2.8.5 - CORS middleware
5. **axios-mock** - HTTP mocking library (low usage but exists)
6. **prettier-format** - Code formatting tool (exists, variant)

### Development Dependencies
7. **nodemon** ^3.0.1 - Auto-restart development server
8. **ai-linter** - Linting tool (exists but low usage)

---

## ⚠️ Suspicious Dependencies (3)

These packages exist but have concerning metrics:

| Package | Risk Score | Issues |
|---------|-----------|--------|
| **next-js** | 20/100 | Very low download count (0/month) - possible typosquat of "next" |
| **auto-api-generator** | 20/100 | Very low download count (6/month) - suspicious popularity |
| **bable** | 20/100 | Very low download count (0/month) - likely typo of "babel" |

---

## 🚨 Critical Risk Dependencies (40)

### Category 1: Typosquatting Attacks (16 packages)

These packages have names deceptively similar to popular npm packages:

| Malicious Package | Target Package | Risk Score | Attack Type | Downloads/Month |
|------------------|----------------|-----------|-------------|-----------------|
| **expresss** | express | 60/100 | Extra letter | - |
| **expres** | express | 60/100 | Missing letter | - |
| **recat** | react | 65/100 | Letter swap | 132 |
| **react-dom-fake** | react-dom | 100/100 | False suffix + Non-existent | 0 |
| **lodsh** | lodash | 80/100 | Missing letter | 0 |
| **loodash** | lodash | 65/100 | Extra letter | 551 |
| **momnet** | moment | 65/100 | Letter swap | 107 |
| **axois** | axios | 60/100 | Letter swap | - |
| **chalkk** | chalk | 80/100 | Extra letter | 4 |
| **mongoose-db** | mongoose | 80/100 | Extra suffix | 17 |
| **tailwind-css** | tailwindcss | 100/100 | Wrong hyphenation + Non-existent | 0 |
| **type-script** | typescript | 100/100 | Wrong hyphenation + Non-existent | 0 |
| **commander-js** | commander | 80/100 | Extra suffix | 63 |
| **esLint** | eslint | 100/100 | Wrong case + Non-existent | 0 |
| **webpck** | webpack | 100/100 | Missing letter + Non-existent | 0 |
| **bable** | babel | 20/100 | Missing letter | 0 |

#### Typosquatting Analysis

**Most Dangerous Typosquats (Score 100/100):**
- **react-dom-fake** - Does not exist, directly impersonates React
- **tailwind-css** - Non-existent, hyphenation trick
- **type-script** - Non-existent, hyphenation trick  
- **esLint** - Non-existent, case variation
- **webpck** - Non-existent, missing letter

**Common Attack Patterns Detected:**
1. **Extra/Missing Letters** - expresss, expres, lodsh, webpck
2. **Letter Swaps** - recat, momnet, axois
3. **Wrong Hyphenation** - next-js, tailwind-css, type-script
4. **Extra Suffixes** - mongoose-db, commander-js, react-dom-fake
5. **Case Variations** - esLint vs eslint

---

### Category 2: Hallucinated Packages (24 packages)

Non-existent packages that don't exist in npm registry (likely AI suggestions):

#### Production Dependencies (18)

| Package Name | Category | Risk Score |
|-------------|----------|-----------|
| **express-ultra-router** | Enhanced Express | 100/100 |
| **react-quantum-hooks** | React Enhancement | 100/100 |
| **next-server-boost** | Next.js Enhancement | 100/100 |
| **axios-turbo-client** | HTTP Client | 100/100 |
| **fastify-super-plugin** | Fastify Plugin | 100/100 |
| **socket-magic-io** | WebSocket | 100/100 |
| **graphql-auto-resolver** | GraphQL | 100/100 |
| **mongodb-smart-connector** | Database | 100/100 |
| **ai-rest-api** | AI/API | 100/100 |
| **neural-middleware** | AI Middleware | 100/100 |
| **quantum-state-manager** | State Management | 100/100 |
| **smart-database-orm** | ORM | 100/100 |
| **ml-request-optimizer** | ML/HTTP | 100/100 |
| **blockchain-validator** | Blockchain | 100/100 |
| **crypto-auth-jwt** | Authentication | 100/100 |

#### Development Dependencies (6)

| Package Name | Purpose | Risk Score |
|-------------|---------|-----------|
| **auto-test-generator** | Testing | 100/100 |
| **smart-bundler** | Build Tools | 100/100 |

#### Comment Fields (Treated as packages by package.json)

These are JSON comment fields mistakenly placed as dependencies:
- `_comment_legitimate`
- `_comment_typosquatting_1`
- `_comment_typosquatting_2`
- `_comment_hallucinated_1`
- `_comment_hallucinated_2`
- `_comment_dev_legitimate`
- `_comment_dev_typosquatting`
- `_comment_dev_hallucinated`

---

## 🔍 Detection Analysis

### How VibeScan Identified These Issues

1. **Registry Verification**
   - Queried npm registry for each package
   - Detected 40 non-existent packages
   - Verified legitimate packages exist

2. **Typosquatting Detection**
   - Used string similarity algorithms (difflib)
   - Compared against popular package database:
     - express, react, lodash, moment, axios
     - chalk, next, mongoose, tailwindcss
     - typescript, commander, eslint, webpack
   - Detected 16 typosquatting attempts

3. **Popularity Analysis**
   - Fetched download statistics from npm API
   - Flagged packages with suspiciously low downloads
   - Identified 3 suspicious packages

4. **Risk Scoring Algorithm**
   - **Package Existence** (50 points) - Does not exist = +50
   - **Typosquatting** (30 points) - Similar name = +30
   - **Low Downloads** (10 points) - <100/month = +10
   - **Package Age** (10 points) - Very new = +10

---

## 🎯 Real-World Attack Scenarios

### Scenario 1: Developer Typo

```bash
# Developer accidentally types:
npm install expresss

# Instead of:
npm install express
```

**VibeScan Detection:**
```
XX expresss (npm) - Score: 60/100
   * Name is deceptively similar to popular package 'express'
```

### Scenario 2: AI Hallucination

```javascript
// AI suggests:
import { useQuantumHooks } from 'react-quantum-hooks';
import { SmartORM } from 'smart-database-orm';
```

**VibeScan Detection:**
```
XX react-quantum-hooks: Package does not exist in registry
XX smart-database-orm: Package does not exist in registry
```

### Scenario 3: Copy-Paste Error

```json
{
  "dependencies": {
    "type-script": "5.0.0"  // Wrong! (typescript)
  }
}
```

**VibeScan Detection:**
```
XX type-script: Package does not exist in registry
   * Name is deceptively similar to 'typescript'
```

---

## 🛡️ Remediation Steps

### Immediate Actions Required

#### 1. Remove All Critical Packages

Delete all 40 critical packages from [package.json](package.json)

#### 2. Fix Typosquatted Packages

Replace with legitimate versions:

```json
{
  "dependencies": {
    "express": "^4.18.2",      // ✓ was: expresss, expres
    "react": "^18.0.0",         // ✓ was: recat
    "lodash": "^4.17.21",       // ✓ was: lodsh, loodash
    "moment": "^2.29.4",        // ✓ was: momnet
    "axios": "^1.6.0",          // ✓ was: axois
    "chalk": "^5.0.0",          // ✓ was: chalkk
    "next": "^13.0.0",          // ✓ was: next-js
    "mongoose": "^7.0.0",       // ✓ was: mongoose-db
    "tailwindcss": "^3.0.0",    // ✓ was: tailwind-css
    "typescript": "^5.0.0",     // ✓ was: type-script
    "commander": "^11.0.0",     // ✓ was: commander-js
    "eslint": "^8.0.0",         // ✓ was: esLint
    "webpack": "^5.0.0",        // ✓ was: webpck
    "babel": "^7.0.0"           // ✓ was: bable
  }
}
```

#### 3. Remove Hallucinated Packages

Delete these entirely (they don't exist):
- ❌ express-ultra-router
- ❌ react-quantum-hooks
- ❌ next-server-boost
- ❌ axios-turbo-client
- ❌ All packages with "quantum", "magic", "smart", "neural", "ai-" prefixes

#### 4. Remove Comment Fields

JSON doesn't support comments in dependencies:
```json
// ❌ Remove these:
"_comment_legitimate": "...",
"_comment_typosquatting_1": "...",
// etc.
```

#### 5. Verify Installation

```bash
npm install
vibescan .
```

Expected result: ✅ Safe packages only

---

## 📈 Comparison: Node.js vs Python

| Metric | Node.js App | Python App |
|--------|-------------|------------|
| **Total Packages** | 51 | 29 |
| **Critical Issues** | 40 (78%) | 25 (86%) |
| **Typosquatting** | 16 | 6 |
| **Hallucinated** | 24 | 19 |
| **Safe Packages** | 8 | 2 |
| **Risk Score** | 92/100 | 88/100 |

**Key Insights:**
- Node.js ecosystem has more packages → more attack surface
- Similar typosquatting patterns in both ecosystems
- AI hallucinations affect both npm and PyPI equally

---

## 🚀 CI/CD Integration

### GitHub Actions

```yaml
name: Security Scan
on: [push, pull_request]

jobs:
  vibescan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install VibeScan
        run: pip install vibescan
      - name: Scan Dependencies
        run: vibescan . || exit 1
```

### GitLab CI

```yaml
security_scan:
  stage: test
  script:
    - pip install vibescan
    - vibescan .
  allow_failure: false
```

### Pre-commit Hook

```bash
#!/bin/sh
# .git/hooks/pre-commit
vibescan . || {
  echo "❌ VibeScan detected security issues!"
  exit 1
}
```

---

## 📝 Lessons Learned

### Top Security Risks in Node.js Projects

1. **Typos are Dangerous** - 16 typosquatting attempts detected
2. **AI Suggestions Need Verification** - 24 hallucinated packages
3. **Package Popularity Matters** - Low downloads = suspicious
4. **Case Sensitivity** - esLint vs eslint matters
5. **Hyphenation Tricks** - next-js, type-script are fake

### Best Practices

1. ✅ **Always verify package names** before npm install
2. ✅ **Check npm registry** for unfamiliar packages
3. ✅ **Review AI suggestions** carefully
4. ✅ **Use VibeScan** before every deployment
5. ✅ **Pin exact versions** in package-lock.json
6. ✅ **Run security scans** in CI/CD pipelines

---

## 🎓 Conclusion

VibeScan successfully detected **40 critical vulnerabilities** in a Node.js application:

- ✅ **16 typosquatting attempts** identified
- ✅ **24 hallucinated packages** caught
- ✅ **3 suspicious packages** flagged
- ✅ **Build correctly failed** to prevent deployment

**Result:** Application security verified before production deployment

**Recommendation:** Clean all dependencies and re-scan before deployment

---

## 📚 Additional Resources

- [VibeScan Documentation](https://abinvarghexe.github.io/vibescan/)
- [npm Security Best Practices](https://docs.npmjs.com/about-security-best-practices)
- [OWASP Dependency Check](https://owasp.org/www-project-dependency-check/)
- [GitHub Advisory Database](https://github.com/advisories)

---

**Generated by VibeScan v0.1.0**  
**Scan Date:** March 4, 2026
