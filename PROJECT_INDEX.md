# VibeScan - Complete Project Index & File Reference

Comprehensive guide to every file, module, and resource in the VibeScan project.

---

## 📋 Table of Contents

1. [Documentation Files](#documentation-files)
2. [Source Code](#source-code)
3. [Test Files](#test-files)
4. [Web Interfaces](#web-interfaces)
5. [Configuration Files](#configuration-files)
6. [Supporting Files](#supporting-files)

---

## 📚 Documentation Files

### For Students & Academic Use

| File | Purpose | When to Use |
|------|---------|-------------|
| [COLLEGE_PROJECT_README.md](COLLEGE_PROJECT_README.md) | Complete college project report | Submitting project report, explaining the project |
| [CODE_DOCUMENTATION.md](CODE_DOCUMENTATION.md) | Line-by-line code explanations | Understanding code, preparing for viva |
| [PRESENTATION_GUIDE.md](PRESENTATION_GUIDE.md) | Presentation scripts & viva Q&A | Preparing for presentations, viva voce |

### For Users & Developers

| File | Purpose | When to Use |
|------|---------|-------------|
| [README.md](README.md) | Main project documentation | First-time users, general overview |
| [QUICKSTART.md](QUICKSTART.md) | 5-minute quick start guide | Want to start using immediately |
| [PRD.md](PRD.md) | Product Requirements Document | Understanding project requirements |

### For Deployment

| File | Purpose | When to Use |
|------|---------|-------------|
| [DEPLOYMENT.md](DEPLOYMENT.md) | Production deployment guide | Deploying to servers, cloud platforms |
| [STREAMLIT_DEPLOY.md](STREAMLIT_DEPLOY.md) | Streamlit-specific deployment | Deploying the Streamlit interface |
| [AUTOMATION.md](AUTOMATION.md) | CI/CD automation setup | Setting up GitHub Actions, pre-commit hooks |

### Project Management

| File | Purpose | When to Use |
|------|---------|-------------|
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Implementation status & metrics | Checking project completion status |
| [CHANGELOG.md](CHANGELOG.md) | Version history & changes | Understanding what changed between versions |
| [INDEX.md](INDEX.md) | Original project index | Quick reference to deployment options |

### Additional Documentation

| File | Purpose | When to Use |
|------|---------|-------------|
| [docs/README.md](docs/README.md) | Documentation directory index | Finding the right documentation |
| [LICENSE](LICENSE) | MIT License | Understanding usage rights |

---

## 💻 Source Code

### Core Package (`vibescan/`)

#### Main Modules

| File | Lines | Purpose | Key Functions |
|------|-------|---------|---------------|
| [vibescan/__init__.py](vibescan/__init__.py) | ~10 | Package initialization | Package metadata |
| [vibescan/cli.py](vibescan/cli.py) | ~70 | Command-line interface | `main()` - Entry point |
| [vibescan/parsers.py](vibescan/parsers.py) | ~70 | Parse dependency files | `parse_package_json()`, `parse_requirements_txt()` |
| [vibescan/scorer.py](vibescan/scorer.py) | ~60 | Calculate risk scores | `calculate_risk()` |
| [vibescan/reporter.py](vibescan/reporter.py) | ~60 | Format & display results | `print_banner()`, `report_results()` |

#### Checker Modules (`vibescan/checkers/`)

| File | Lines | Purpose | Key Functions |
|------|-------|---------|---------------|
| [vibescan/checkers/__init__.py](vibescan/checkers/__init__.py) | ~5 | Module initialization | - |
| [vibescan/checkers/registry_checker.py](vibescan/checkers/registry_checker.py) | ~80 | Verify package existence | `check_npm_package()`, `check_pypi_package()` |
| [vibescan/checkers/typosquat_checker.py](vibescan/checkers/typosquat_checker.py) | ~40 | Detect typosquatting | `check_typosquatting()` |

**Total Core Code**: ~395 lines

---

## 🧪 Test Files (`tests/`)

| File | Tests | Purpose | Coverage |
|------|-------|---------|----------|
| [tests/test_parsers.py](tests/test_parsers.py) | 3 | Test parser functions | package.json, requirements.txt parsing |
| [tests/test_checkers.py](tests/test_checkers.py) | 5 | Test checker modules | Registry verification, typosquat detection |
| [tests/test_scorer.py](tests/test_scorer.py) | 4 | Test risk scoring | Risk calculation algorithm |

**Total Tests**: 12 tests (all passing ✅)

**Test Commands**:
```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_parsers.py -v

# Run with coverage
pytest tests/ --cov=vibescan
```

---

## 🌐 Web Interfaces

### Flask Web Interface (`web/`)

| File | Lines | Purpose |
|------|-------|---------|
| [web/app.py](web/app.py) | ~165 | Flask backend application |
| [web/templates/index.html](web/templates/index.html) | ~400 | Frontend HTML/CSS/JavaScript |
| [web/requirements.txt](web/requirements.txt) | ~5 | Flask dependencies |
| [web/README.md](web/README.md) | ~80 | Web interface documentation |

**How to Run**:
```bash
cd web
pip install -r requirements.txt
python app.py
# Visit http://localhost:5000
```

### Streamlit Interface

| File | Lines | Purpose |
|------|-------|---------|
| [streamlit_app.py](streamlit_app.py) | ~310 | Streamlit web application |

**How to Run**:
```bash
pip install streamlit
streamlit run streamlit_app.py
# Visit http://localhost:8501
```

### Node.js Wrapper (`js-wrapper/`)

| File | Lines | Purpose |
|------|-------|---------|
| [js-wrapper/index.js](js-wrapper/index.js) | ~80 | Node.js CLI wrapper |
| [js-wrapper/package.json](js-wrapper/package.json) | ~30 | npm package config |
| [js-wrapper/README.md](js-wrapper/README.md) | ~40 | npm wrapper docs |

**Total Web Code**: ~1,115 lines

---

## ⚙️ Configuration Files

### Python Package Configuration

| File | Purpose | Key Settings |
|------|---------|-------------|
| [setup.py](setup.py) | Package installation script | Version, dependencies, entry points |
| [pyproject.toml](pyproject.toml) | Build system config | Build backend, project metadata |
| [requirements.txt](requirements.txt) | Project dependencies | requests, colorama, flask, streamlit |
| [MANIFEST.in](MANIFEST.in) | Package manifest | Include/exclude files in distribution |

### Docker Configuration

| File | Purpose |
|------|---------|
| [Dockerfile](Dockerfile) | Container image definition |
| [docker-compose.yml](docker-compose.yml) | Multi-container setup |

**Docker Commands**:
```bash
# Build image
docker build -t vibescan .

# Run container
docker run -v $(pwd):/app vibescan

# Using docker-compose
docker-compose up
```

### CI/CD Configuration

| File | Purpose | Location |
|------|---------|----------|
| `.github/workflows/*.yml` | GitHub Actions | (If exists) |
| `.pre-commit-config.yaml` | Pre-commit hooks | (User-created) |

---

## 📦 Supporting Files

### Data & Test Files

| Directory | Purpose | Contents |
|-----------|---------|----------|
| [dummy_project/](dummy_project/) | Test project | Sample package.json, requirements.txt |
| [vibescan.egg-info/](vibescan.egg-info/) | Package metadata | Auto-generated by setuptools |

### Build Artifacts

| Directory | Purpose | Status |
|-----------|---------|--------|
| `__pycache__/` | Python bytecode | Generated (git-ignored) |
| `dist/` | Distribution packages | Generated (git-ignored) |
| `build/` | Build artifacts | Generated (git-ignored) |

### Utility Scripts

| File | Lines | Purpose |
|------|-------|---------|
| [fix_quotes.py](fix_quotes.py) | ~30 | Fix quote formatting in files |
| [verify.py](verify.py) | ~50 | Verify project setup |

### Output Files

| File | Purpose |
|------|---------|
| [pytest_out.txt](pytest_out.txt) | Test output log |

---

## 📊 Code Statistics

### By Component

| Component | Files | Lines | Tests |
|-----------|-------|-------|-------|
| **Core Engine** | 7 | ~395 | 12 |
| **Web Interfaces** | 5 | ~1,115 | - |
| **Tests** | 3 | ~200 | 12 |
| **Documentation** | 15+ | ~15,000 | - |
| **Configuration** | 8 | ~200 | - |
| **Total** | **38+** | **~16,910** | **12** |

### By Language

| Language | Lines | Percentage |
|----------|-------|------------|
| Python | ~1,860 | 65% |
| JavaScript | ~480 | 17% |
| HTML/CSS | ~400 | 14% |
| Markdown | ~15,000+ | Documentation |
| YAML/TOML | ~100 | 4% |

---

## 🔍 File Quick Reference

### Need to Understand...

| What | Read This File |
|------|---------------|
| How parsers work | [vibescan/parsers.py](vibescan/parsers.py) + [CODE_DOCUMENTATION.md](CODE_DOCUMENTATION.md#parsers) |
| How registry checking works | [vibescan/checkers/registry_checker.py](vibescan/checkers/registry_checker.py) |
| How typosquatting detection works | [vibescan/checkers/typosquat_checker.py](vibescan/checkers/typosquat_checker.py) |
| How risk scoring works | [vibescan/scorer.py](vibescan/scorer.py) |
| How CLI works | [vibescan/cli.py](vibescan/cli.py) |
| How web interface works | [web/app.py](web/app.py) |
| How Streamlit app works | [streamlit_app.py](streamlit_app.py) |

### Need to Modify...

| What | Edit This File |
|------|---------------|
| Add new package manager | [vibescan/parsers.py](vibescan/parsers.py) |
| Add new checker | Create new file in [vibescan/checkers/](vibescan/checkers/) |
| Change risk algorithm | [vibescan/scorer.py](vibescan/scorer.py) |
| Modify CLI output | [vibescan/reporter.py](vibescan/reporter.py) |
| Update web UI | [web/templates/index.html](web/templates/index.html) |
| Change dependencies | [requirements.txt](requirements.txt), [setup.py](setup.py) |

### Need to Deploy...

| Where | Read This |
|-------|-----------|
| PyPI | [DEPLOYMENT.md](DEPLOYMENT.md#pypi) |
| npm | [DEPLOYMENT.md](DEPLOYMENT.md#npm) |
| Docker | [Dockerfile](Dockerfile) + [DEPLOYMENT.md](DEPLOYMENT.md#docker) |
| AWS/Azure/GCP | [DEPLOYMENT.md](DEPLOYMENT.md) |
| Streamlit Cloud | [STREAMLIT_DEPLOY.md](STREAMLIT_DEPLOY.md) |

---

## 🎓 For College Project

### Essential Files to Study

1. **[COLLEGE_PROJECT_README.md](COLLEGE_PROJECT_README.md)** - Your main report (40+ pages)
2. **[CODE_DOCUMENTATION.md](CODE_DOCUMENTATION.md)** - Code explanations (45+ pages)
3. **[PRESENTATION_GUIDE.md](PRESENTATION_GUIDE.md)** - Presentation help (30+ pages)
4. **[vibescan/cli.py](vibescan/cli.py)** - Main entry point
5. **[vibescan/scorer.py](vibescan/scorer.py)** - Core algorithm

### For Viva Preparation

**Be ready to explain**:
1. How [parsers.py](vibescan/parsers.py) extracts dependencies
2. How [registry_checker.py](vibescan/checkers/registry_checker.py) verifies packages
3. How [typosquat_checker.py](vibescan/checkers/typosquat_checker.py) uses Levenshtein distance
4. How [scorer.py](vibescan/scorer.py) calculates risk
5. How all modules work together in [cli.py](vibescan/cli.py)

**Reference**: All viva questions answered in [PRESENTATION_GUIDE.md](PRESENTATION_GUIDE.md)

---

## 🔗 External Resources

### Package Repositories
- **PyPI**: https://pypi.org/project/vibescan/
- **npm**: https://www.npmjs.com/package/vibescan-js
- **GitHub**: https://github.com/AbinVarghexe/vibescan

### APIs Used
- **npm Registry**: https://registry.npmjs.org/
- **npm Downloads**: https://api.npmjs.org/downloads/
- **PyPI JSON API**: https://pypi.org/pypi/{package}/json

### Dependencies
- **Python**: requests, colorama, flask, streamlit
- **Node.js**: child_process, path

---

## 📝 Version Information

- **Current Version**: 1.0.0
- **Last Updated**: March 2, 2026
- **Python Version**: 3.8+
- **Node Version**: 14+

---

## 🎯 Quick Commands

```bash
# Install
pip install vibescan

# Run scan
vibescan

# Run tests
pytest tests/ -v

# Start web interface
cd web && python app.py

# Start Streamlit
streamlit run streamlit_app.py

# Build package
python setup.py sdist bdist_wheel

# Run Docker
docker-compose up
```

---

**This index provides a complete map of the VibeScan project. Use it as your reference guide!**

---

**Document Version**: 1.0  
**Last Updated**: March 2, 2026
