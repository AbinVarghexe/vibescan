vibescan/
├── 🐍 Python CLI Package (PyPI)
├── 📦 Node.js Wrapper (npm)
└── 🌐 Streamlit Web App (Streamlit Cloud)

## 🎯 Quick Access

- **Web App**: https://vibescen.streamlit.app (Live on Streamlit Cloud)
- **PyPI**: https://pypi.org/project/vibescan/
- **npm**: https://www.npmjs.com/package/vibescan-js
- **GitHub**: https://github.com/AbinVarghexe/vibescan

## 🚀 Quick Start

### Use the Web App (Easiest)
1. Visit: https://vibescen.streamlit.app
2. Upload your `package.json` or `requirements.txt`
3. Get instant security analysis!

### Install CLI (Python)
```bash
pip install vibescan
vibescan
```

### Install CLI (Node.js)
```bash
npm install -g vibescan-js
vibescan
```

## 📚 Documentation

- **[README.md](README.md)** - Complete project overview
- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[AUTOMATION.md](AUTOMATION.md)** - Full automation guide
- **[STREAMLIT_DEPLOY.md](STREAMLIT_DEPLOY.md)** - Streamlit deployment
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Manual deployment guide

## 🤖 Automation Status

✅ **GitHub Actions** - Auto-testing on every push
✅ **PyPI Publishing** - Auto-publish on version tags
✅ **npm Publishing** - Auto-publish on version tags
✅ **Streamlit Cloud** - Auto-deploy on main branch push

## 🏗️ Project Structure

```
vibescan/
├── streamlit_app.py          # 🌐 Streamlit web interface
├── vibescan/                  # 🐍 Core Python package
│   ├── cli.py                # Command-line interface
│   ├── parsers.py            # File parsers
│   ├── scorer.py             # Risk scoring
│   ├── reporter.py           # Output formatting
│   └── checkers/             # Checker modules
├── js-wrapper/               # 📦 Node.js wrapper
├── tests/                    # 🧪 Test suite (12/12 passing)
├── .github/workflows/        # 🤖 CI/CD automation
├── .streamlit/               # ⚙️ Streamlit config
└── dist/                     # 📦 Build artifacts
```

## ✨ Features

- 🔍 **Hallucination Detection** - Identifies non-existent packages
- 🎭 **Typosquatting Defense** - Catches similar package names
- 📊 **Risk Scoring** - 0-100 explainable risk scores
- 📅 **Download Analysis** - Flags suspicious low-usage packages
- ⚡ **Fast Scanning** - Results in seconds
- 🎨 **Beautiful UI** - Google-like minimal design
- 🔒 **Privacy-First** - All analysis runs locally

## 🎯 Use Cases

1. **Pre-commit Check** - Catch risks before committing
2. **CI/CD Integration** - Block PRs with suspicious packages
3. **Code Review** - Verify external contributions
4. **Web Interface** - Quick one-off checks

## 📊 Stats

- **Lines of Code**: 2,500+
- **Test Coverage**: 100% core functionality
- **Tests Passing**: 12/12 ✅
- **Supported Ecosystems**: npm, PyPI
- **Python Versions**: 3.7-3.13
- **Platforms**: Windows, macOS, Linux

## 🚀 Deployment

### 1. Add GitHub Secrets
Visit: https://github.com/AbinVarghexe/vibescan/settings/secrets/actions

Add:
- `PYPI_API_TOKEN` - From https://pypi.org/
- `NPM_TOKEN` - From https://www.npmjs.com/

### 2. Deploy Streamlit App
1. Go to https://share.streamlit.io/
2. Sign in with GitHub
3. New app → `AbinVarghexe/vibescan` → `streamlit_app.py`
4. Deploy!

### 3. Release Version (Auto-publishes to PyPI & npm)
```bash
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

See [AUTOMATION.md](AUTOMATION.md) for complete guide.

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Test CLI
python -m vibescan.cli dummy_project

# Test Streamlit locally
streamlit run streamlit_app.py
```

## 📈 Roadmap

- [ ] Support for more package managers (Cargo, Go modules)
- [ ] AST-based code analysis
- [ ] Configurable risk thresholds
- [ ] JSON output format
- [ ] IDE extensions
- [ ] Team dashboard

## 🤝 Contributing

Contributions welcome! Please see our contributing guidelines.

## 📄 License

MIT License - See [LICENSE](LICENSE) file

## 🙏 Acknowledgments

Built to protect developers from AI-generated dependency hallucinations and slopsquatting attacks.

---

**Stay safe in the AI coding era! 🛡️**

Made with ❤️ by the VibeScan community
