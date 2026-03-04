# VibeScan Test Results

## Scan Summary

**Date:** March 4, 2026  
**Target:** test-app/  
**Command:** `vibescan test-app`

---

## 📊 Overall Statistics

| Category | Count | Percentage |
|----------|-------|------------|
| **Total Dependencies** | 29 | 100% |
| ✅ **Safe** | 2 | 6.9% |
| ⚠️ **Suspicious** | 2 | 6.9% |
| 🚨 **Critical** | 25 | 86.2% |

**Overall Risk Assessment:** 🔴 **CRITICAL - Build Failed**

---

## ✅ Safe Dependencies (2)

These packages passed all security checks:

### NPM Packages
- `express` - Popular web framework
- `axios` - HTTP client library

---

## ⚠️ Suspicious Dependencies (2)

These packages exist but have concerning metrics:

### NPM Packages
1. **react-super-hooks** - Score: 20/100
   - ⚠️ Very low download count (42 in last month)
   - Suspicious popularity for a React-related package

### PyPI Packages
1. **requests** - Score: 20/100
   - ⚠️ Very low download count (0 in last month)
   - Note: This might be a different package than the legitimate "requests" library

---

## 🚨 Critical Risk Dependencies (25)

### Non-Existent Packages (Hallucinations) - Score: 100/100

These packages do not exist in any registry and are likely AI hallucinations:

#### PyPI (Python)
1. **flask-super-auth**
   - 🚫 Package does not exist in PyPI registry
   - Likely AI hallucination

2. **secure-web-framework**
   - 🚫 Package does not exist in PyPI registry
   - Likely AI hallucination

3. **ai-data-processor**
   - 🚫 Package does not exist in PyPI registry
   - Likely AI hallucination

4. **magic-database-connector**
   - 🚫 Package does not exist in PyPI registry
   - Likely AI hallucination

5. **ultra-fast-api**
   - 🚫 Package does not exist in PyPI registry
   - Likely AI hallucination

6. **quantum-validator**
   - 🚫 Package does not exist in PyPI registry
   - Likely AI hallucination

7. **neural-web-engine**
   - 🚫 Package does not exist in PyPI registry
   - Likely AI hallucination

#### NPM (JavaScript)
8. **express-quantum-router**
   - 🚫 Package does not exist in npm registry
   - Likely AI hallucination

9. **ai-frontend-framework**
   - 🚫 Package does not exist in npm registry
   - Likely AI hallucination

10. **neural-state-manager**
    - 🚫 Package does not exist in npm registry
    - Likely AI hallucination

11. **magic-http-client**
    - 🚫 Package does not exist in npm registry
    - Likely AI hallucination

---

### Typosquatting Attempts

These packages have names deceptively similar to popular packages:

#### PyPI (Python)

1. **reqeusts** - Score: 100/100
   - 🎯 Typosquatting target: `requests`
   - 🚫 Does not exist in registry
   - **High Risk:** Intentional misspelling

2. **djago** - Score: 100/100
   - 🎯 Typosquatting target: `django`
   - 🚫 Does not exist in registry
   - **High Risk:** Intentional misspelling

3. **numpyy** - Score: 100/100
   - 🎯 Typosquatting target: `numpy`
   - 🚫 Does not exist in registry
   - **High Risk:** Extra letter

4. **pandsa** - Score: 100/100
   - 🎯 Typosquatting target: `pandas`
   - 🚫 Does not exist in registry
   - **High Risk:** Letter swap

5. **flsk** - Score: 100/100
   - 🎯 Typosquatting target: `flask`
   - 🚫 Does not exist in registry
   - **High Risk:** Missing vowel

6. **pythonrequest** - Score: 100/100
   - 🎯 Typosquatting target: `requests`
   - 🚫 Does not exist in registry
   - **High Risk:** Similar name pattern

7. **Flask** (capitalized) - Score: 80/100
   - 🎯 Typosquatting target: `flask`
   - ⚠️ Very low download count
   - **Risk:** Case variation

#### NPM (JavaScript)

1. **expresss** - Score: 60/100
   - 🎯 Typosquatting target: `express`
   - **Risk:** Extra letter

2. **recat** - Score: 65/100
   - 🎯 Typosquatting target: `react`
   - ⚠️ Low download count (132/month)
   - **Risk:** Letter swap

3. **lodsh** - Score: 80/100
   - 🎯 Typosquatting target: `lodash`
   - ⚠️ Very low download count (0/month)
   - **High Risk:** Missing letter

4. **momnet** - Score: 65/100
   - 🎯 Typosquatting target: `moment`
   - ⚠️ Low download count (107/month)
   - **Risk:** Letter swap

5. **axois** - Score: 60/100
   - 🎯 Typosquatting target: `axios`
   - **Risk:** Letter swap

---

## 🔍 Detailed Analysis

### Detection Methods

VibeScan successfully identified issues using:

1. **Registry Verification**
   - Checked PyPI (Python Package Index)
   - Checked npm (Node Package Manager)
   - Detected 18 non-existent packages

2. **Typosquatting Detection**
   - Used similarity algorithms (difflib)
   - Compared against popular package database
   - Detected 7 typosquatting attempts

3. **Popularity Analysis**
   - Analyzed download statistics
   - Flagged packages with suspiciously low downloads
   - Identified 2 suspicious packages

### Risk Scoring

Risk scores are calculated based on:
- **Package existence** (0-50 points)
- **Name similarity** to popular packages (0-30 points)
- **Download statistics** (0-10 points)
- **Package age** (0-10 points)

**Score Ranges:**
- 0-30: ✅ Safe
- 31-59: ⚠️ Suspicious
- 60-100: 🚨 Critical

---

## 🛡️ Remediation Steps

### Immediate Actions Required

1. **Remove all Critical packages** from requirements.txt and package.json

2. **Replace typosquatted packages** with legitimate versions:
   - `reqeusts` → `requests`
   - `djago` → `django`
   - `numpyy` → `numpy`
   - `pandsa` → `pandas`
   - `flsk` → `flask`
   - `expresss` → `express`
   - `recat` → `react`
   - `lodsh` → `lodash`
   - `momnet` → `moment`
   - `axois` → `axios`

3. **Remove hallucinated packages** - they don't exist:
   - All packages with "quantum", "magic", "neural", "ai-", "ultra-" prefixes

4. **Verify legitimate packages:**
   ```bash
   pip show requests
   npm show express
   ```

### Prevention Strategies

1. **Always use VibeScan** before installing new dependencies
2. **Double-check package names** in official registries
3. **Review AI-suggested packages** carefully
4. **Pin exact versions** in production
5. **Use lock files** (requirements.txt, package-lock.json)

---

## 📝 CI/CD Integration

VibeScan exits with failure code when critical issues are detected, making it perfect for CI/CD:

```yaml
# GitHub Actions Example
- name: Security Scan
  run: vibescan .
  
# GitLab CI Example
security_scan:
  script:
    - vibescan .
  allow_failure: false
```

---

## 🎯 Conclusion

VibeScan successfully detected:
- ✅ **7 typosquatting attempts** (packages with names similar to popular packages)
- ✅ **18 hallucinated packages** (non-existent packages)
- ✅ **2 suspicious packages** (low download counts)
- ✅ **2 safe packages** (legitimate dependencies)

**Result:** Build failed due to critical security risks

**Recommendation:** Clean up dependencies before deployment

---

## 📚 Additional Resources

- [VibeScan Documentation](https://abinvarghexe.github.io/vibescan/)
- [GitHub Repository](https://github.com/AbinVarghexe/vibescan)
- [PyPI Package Security Best Practices](https://packaging.python.org/guides/)
- [npm Security Best Practices](https://docs.npmjs.com/about-security-best-practices)
