# VibeScan Documentation

Welcome to the VibeScan documentation! This directory contains the project landing page and supplementary documentation.

## 📚 Available Documentation

### For Users

1. **[README.md](../README.md)**
   - Installation instructions
   - Usage examples
   - Feature overview

2. **[QUICKSTART.md](../QUICKSTART.md)**
   - Get started in 5 minutes
   - Basic usage examples

3. **[PRD.md](../PRD.md)**
   - Product Requirements Document
   - Feature specifications

### For Deployment

4. **[DEPLOYMENT.md](../DEPLOYMENT.md)**
   - PyPI and npm publish guide
   - Docker setup

5. **[STREAMLIT_DEPLOY.md](../STREAMLIT_DEPLOY.md)**
   - Deploying the Streamlit web interface
   - Streamlit Cloud setup

### Project History

6. **[CHANGELOG.md](../CHANGELOG.md)**
   - Version history
   - Feature additions and bug fixes

## 🚀 Quick Reference

### Installation
```bash
pip install vibescan
```

### Basic Usage
```bash
vibescan                    # Scan current directory
vibescan ./my-project       # Scan specific directory
vibescan --debug            # Debug mode
```

### Web Interface
```bash
streamlit run streamlit_app.py
# Visit http://localhost:8501
```

### Run Tests
```bash
pytest tests/ -v
```
