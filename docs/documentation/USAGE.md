# VibeScan Usage Guide

Complete guide on how to install, configure, and use VibeScan in your projects.

## Table of Contents

- [Installation](#installation)
  - [Install from Source](#install-from-source)
  - [Install via pip](#install-via-pip)
  - [Install via npm](#install-via-npm)
  - [Run with Docker](#run-with-docker)
- [Basic Usage](#basic-usage)
  - [Scan Current Directory](#scan-current-directory)
  - [Scan Specific Path](#scan-specific-path)
  - [Debug Mode](#debug-mode)
- [Configuration](#configuration)
  - [CLI Flags](#cli-flags)
  - [Risk Scoring Thresholds](#risk-scoring-thresholds)
  - [Supported Files](#supported-files)
- [CI/CD Integration](#cicd-integration)
  - [GitHub Actions](#github-actions)
  - [GitLab CI](#gitlab-ci)
  - [Pre-Commit Hooks](#pre-commit-hooks)
  - [Docker in CI](#docker-in-ci)
- [Understanding Output](#understanding-output)
- [Examples](#examples)

---

## Installation

### Install from Source

Clone the repository and install in development mode:

```bash
git clone https://github.com/AbinVarghexe/vibescan.git
cd vibescan
pip install -e .
```

**Requirements**: Python 3.7 or higher

### Install via pip

```bash
pip install vibescan
```

### Install via npm

```bash
npm install -g vibescan
```

### Run with Docker

Pull and run the Docker image:

```bash
docker pull vibescan/vibescan:latest
docker run --rm -v $(pwd):/app vibescan/vibescan:latest
```

---

## Basic Usage

### Scan Current Directory

Navigate to your project directory and run:

```bash
vibescan
```

VibeScan will automatically detect and scan:
- `package.json` (npm dependencies + devDependencies)
- `requirements.txt` (Python packages)

### Scan Specific Path

Scan a different directory:

```bash
vibescan /path/to/project
```

### Debug Mode

Enable verbose output for troubleshooting:

```bash
vibescan --debug
```

Debug mode shows:
- Files being parsed
- Individual package checks
- API response details
- Scoring calculations

---

## Configuration

### CLI Flags

| Flag | Description | Default |
|------|-------------|---------|
| `path` | Directory to scan | `.` (current directory) |
| `--debug` | Enable debug output | Off |

### Risk Scoring Thresholds

VibeScan categorizes dependencies into three levels:

| Category | Score Range | Exit Code | Action |
|----------|-------------|-----------|--------|
| **Safe** | 0 - 9 | 0 | No action needed |
| **Suspicious** | 10 - 59 | 0 | Review recommended |
| **Critical** | 60 - 100 | 1 | Blocks pipeline |

**Exit Code Behavior**: VibeScan exits with code `1` if **any** dependency scores ≥ 60, making it perfect for CI/CD gates.

### Scoring Factors

| Check | Score Impact | Reason |
|-------|--------------|--------|
| Package not in registry | +100 | AI hallucination / slopsquat target |
| Typosquat detected | +60 | Name similar to popular package |
| Created < 7 days ago | +40 | Suspiciously new |
| Created < 30 days ago | +10 | Relatively new |
| Downloads < 100/month | +20 | Very low popularity |
| Downloads < 1000/month | +5 | Low popularity |

**Maximum Score**: 100 (capped)

### Supported Files

| File | Ecosystem | Parsed Fields |
|------|-----------|---------------|
| `package.json` | npm | `dependencies`, `devDependencies` |
| `requirements.txt` | PyPI | All non-comment lines |

---

## CI/CD Integration

VibeScan is designed to run as a security gate in your deployment pipelines. Any critical finding causes the process to exit with code `1`, blocking the build.

### GitHub Actions

Create `.github/workflows/vibescan.yml`:

```yaml
name: VibeScan Security Check

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  vibescan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install VibeScan
        run: pip install vibescan
      
      - name: Scan dependencies
        run: vibescan check .
```

### GitLab CI

Add to `.gitlab-ci.yml`:

```yaml
vibescan:
  stage: test
  image: python:3.11-slim
  script:
    - pip install vibescan
    - vibescan check .
  only:
    - merge_requests
    - main
```

### Pre-Commit Hooks

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/AbinVarghexe/vibescan
    rev: v0.1.0
    hooks:
      - id: vibescan
        name: VibeScan dependency check
        entry: vibescan check .
        language: python
        pass_filenames: false
        stages: [commit, push]
```

Install the hook:

```bash
pre-commit install
```

### Docker in CI

Use Docker for any CI system:

```bash
docker run --rm -v $(pwd):/app vibescan/vibescan:latest
```

**Circle CI Example**:

```yaml
version: 2.1
jobs:
  vibescan:
    docker:
      - image: vibescan/vibescan:latest
    steps:
      - checkout
      - run: vibescan check .
```

---

## Understanding Output

### Terminal Output Example

```
=========================================
              VibeScan                   
=========================================
Analyzing dependencies for AI hallucinations and slopsquatting...

Analyzing 15 dependencies...

✓ OK 12 Safe Dependencies

!! 2 Suspicious Dependencies (Review Recommended)
  - chalk-extra (npm) - Score: 25/100
    → Package is relatively new (Created 20 days ago)
    → Low download count (450 in last month)
  
  - reqests (pypi) - Score: 65/100
    → Package does not exist in registry (Likely AI Hallucination/Slopsquat target)
    → Name is deceptively similar to popular package 'requests' (Typosquatting risk)

✗ CRITICAL 1 Critical Dependencies
  - hallucinated-lib (npm) - Score: 100/100
    → Package does not exist in registry (Likely AI Hallucination/Slopsquat target)

[!] Critical dependencies detected. Exiting with code 1.
```

### Color Coding

- **Green** (Safe): No issues found
- **Yellow** (Suspicious): Review recommended but not blocking
- **Red** (Critical): Blocks pipeline, requires immediate attention

---

## Examples

### Example 1: Scanning a Node.js Project

```bash
cd my-node-app
vibescan
```

Output:
```
Analyzing 25 dependencies...
✓ OK 25 Safe Dependencies
```

### Example 2: Detecting a Hallucinated Package

Given `requirements.txt`:
```
requests
pandas-extra  # hallucinated by AI
numpy
```

Running `vibescan` detects:
```
✗ CRITICAL 1 Critical Dependencies
  - pandas-extra (pypi) - Score: 100/100
    → Package does not exist in registry
```

### Example 3: Typosquat Detection

Given `package.json`:
```json
{
  "dependencies": {
    "react": "^18.0.0",
    "reqest": "^2.88.0"
  }
}
```

Running `vibescan` flags:
```
!! 1 Suspicious Dependencies
  - reqest (npm) - Score: 60/100
    → Name is deceptively similar to popular package 'request'
```

---

## Troubleshooting

### Issue: "No package.json or requirements.txt found"

**Solution**: Ensure you're in the correct directory, or specify the path explicitly:
```bash
vibescan /path/to/project
```

### Issue: Network errors during scan

**Solution**: VibeScan requires internet access to query npm and PyPI registries. Check your connection and firewall settings.

### Issue: False positives

**Solution**: VibeScan uses heuristics and may occasionally flag legitimate new packages. Always manually review suspicious results before blocking a build.

---

## Advanced Usage

### Custom Wrapper Scripts

Create a shell script to customize VibeScan behavior:

```bash
#!/bin/bash
# vibescan-wrapper.sh

echo "Running VibeScan..."
vibescan --debug > vibescan-report.log 2>&1

if [ $? -eq 1 ]; then
  echo "Critical issues found. See vibescan-report.log"
  exit 1
fi

echo "All dependencies are safe!"
```

### Combining with Other Security Tools

Chain VibeScan with other scanners:

```bash
# Run multiple security checks
npm audit && \
vibescan && \
snyk test
```

---

## Support

- **Issues**: [GitHub Issues](https://github.com/AbinVarghexe/vibescan/issues)
- **Discussions**: [GitHub Discussions](https://github.com/AbinVarghexe/vibescan/discussions)
- **Documentation**: [https://abinvarghexe.github.io/vibescan/](https://abinvarghexe.github.io/vibescan/)

---

**Last Updated**: March 2026  
**Version**: 0.1.0
