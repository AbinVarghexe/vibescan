# 🚀 Complete Automation & Deployment Guide

This guide shows you how to fully automate VibeScan deployment with GitHub Actions and free hosting.

---

## 📋 Prerequisites

Before starting, create accounts on:
1. **GitHub** - https://github.com (Already have: AbinVarghexe/vibescan)
2. **PyPI** - https://pypi.org/account/register/
3. **npm** - https://www.npmjs.com/signup
4. **Streamlit Cloud** - https://share.streamlit.io/ (Sign in with GitHub)

---

## 🔑 Step 1: Configure GitHub Secrets

Go to your repository settings: `https://github.com/AbinVarghexe/vibescan/settings/secrets/actions`

Add these secrets:

### For PyPI Publishing
**Secret Name**: `PYPI_API_TOKEN`
**Value**: Your PyPI API token

How to get:
1. Log in to https://pypi.org/
2. Go to Account Settings → API tokens
3. Create a new token with scope: "Entire account"
4. Copy the token (starts with `pypi-`)

### For npm Publishing
**Secret Name**: `NPM_TOKEN`
**Value**: Your npm access token

How to get:
1. Log in to https://www.npmjs.com/
2. Click your profile → Access Tokens
3. Generate New Token → Classic Token
4. Select "Automation" type
5. Copy the token

---

## 🤖 Step 2: Automated Workflow

The repository already has `.github/workflows/publish.yml` configured!

### What it does automatically:

✅ **On every push to main**:
- Runs all tests
- Triggers Streamlit Cloud deployment

✅ **On version tags** (e.g., `v0.1.0`):
- Runs all tests
- Builds Python package
- Publishes to PyPI
- Publishes to npm

### To trigger a release:

```bash
# Tag a new version
git tag -a v0.1.0 -m "Release version 0.1.0"
git push origin v0.1.0
```

GitHub Actions will automatically:
1. Run tests
2. Build packages
3. Publish to PyPI
4. Publish to npm

---

## 🌐 Step 3: Deploy Streamlit App (100% FREE)

### Option A: Streamlit Cloud (Recommended - Easiest)

1. **Go to**: https://share.streamlit.io/

2. **Sign in** with your GitHub account (@AbinVarghexe)

3. **Click "New app"**

4. **Fill in**:
   - Repository: `AbinVarghexe/vibescan`
   - Branch: `main`
   - Main file path: `streamlit_app.py`
   - App URL: `vibescan` (or custom name)

5. **Click "Deploy"**

6. **Your app will be live at**:
   ```
   https://vibescen.streamlit.app
   ```

**Benefits**:
- ✅ Completely FREE
- ✅ Auto-deploys on every push to main
- ✅ SSL certificate included
- ✅ No configuration needed
- ✅ Custom domain support

### Option B: Render.com (Alternative FREE option)

1. Go to https://render.com/
2. Sign in with GitHub
3. Click "New +" → "Web Service"
4. Connect your repository
5. Configure:
   - Name: `vibescan`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run streamlit_app.py --server.port $PORT`
   - Instance Type: `Free`
6. Click "Create Web Service"

**Your app**: `https://vibescan.onrender.com`

### Option C: Railway.app (Another FREE option)

1. Go to https://railway.app/
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select `AbinVarghexe/vibescan`
5. Railway auto-detects Python and deploys
6. Click on the deployment to get your URL

**Your app**: `https://vibescan.up.railway.app`

---

## 📦 Step 4: Verify Everything Works

### Test PyPI Package:
```bash
pip install vibescan
vibescan --help
```

### Test npm Package:
```bash
npm install -g vibescan-js
vibescan --help
```

### Test Streamlit App:
Visit your deployed URL and test:
1. Upload a package.json file
2. Paste requirements.txt content
3. Verify scanning works

---

## 🔄 Continuous Deployment Flow

```
Developer pushes code to main
          ↓
GitHub Actions triggers
          ↓
    ┌─────┴─────┐
    ↓           ↓
Run Tests   Build Packages
    ↓           ↓
    ↓     If tagged version:
    ↓       - Publish to PyPI
    ↓       - Publish to npm
    ↓           ↓
    └─────┬─────┘
          ↓
Streamlit Cloud Auto-deploys
          ↓
Live within 2 minutes! 🎉
```

---

## 🎯 Quick Commands Reference

### Release a new version:
```bash
# Update version in setup.py, pyproject.toml, package.json
# Commit changes
git add .
git commit -m "Bump version to 0.2.0"
git push

# Create and push tag
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin v0.2.0

# GitHub Actions will handle the rest!
```

### Test locally:
```bash
# Python package
python -m vibescan.cli dummy_project

# Streamlit app
streamlit run streamlit_app.py

# Tests
pytest tests/ -v
```

### Force re-deploy Streamlit:
```bash
# Just push any change to main branch
git commit --allow-empty -m "Trigger redeploy"
git push
```

---

## 🌟 What You Get (All FREE!)

| Component | Service | URL | Status |
|-----------|---------|-----|--------|
| Python Package | PyPI | `pip install vibescan` | Auto-published on tags |
| Node Package | npm | `npm install vibescan-js` | Auto-published on tags |
| Web App | Streamlit Cloud | `*.streamlit.app` | Auto-deployed on push |
| Source Code | GitHub | github.com/AbinVarghexe/vibescan | Version controlled |
| CI/CD | GitHub Actions | Automated testing | Always running |

---

## 🐛 Troubleshooting

### PyPI upload fails:
- Check your `PYPI_API_TOKEN` secret is correct
- Ensure version number is incremented
- Package name might be taken (change in setup.py)

### npm publish fails:
- Verify `NPM_TOKEN` secret
- Package name might be taken (change in js-wrapper/package.json)
- Try scoped package: `@abinvarghexe/vibescan-js`

### Streamlit app not loading:
- Check `requirements.txt` has all dependencies
- Verify `streamlit_app.py` is in root directory
- Check Streamlit Cloud logs for errors

### GitHub Actions failing:
- Check Actions tab for detailed logs
- Ensure all secrets are configured
- Verify tests pass locally first

---

## 📊 Monitoring

### GitHub Actions:
https://github.com/AbinVarghexe/vibescan/actions

### PyPI Stats:
https://pypistats.org/packages/vibescan

### npm Stats:
https://www.npmjs.com/package/vibescan-js

### Streamlit App Analytics:
Available in Streamlit Cloud dashboard

---

## 🎓 Best Practices

1. **Always run tests locally** before pushing
2. **Use semantic versioning** (v0.1.0, v0.2.0, v1.0.0)
3. **Update CHANGELOG.md** for each release
4. **Monitor GitHub Actions** for failures
5. **Test deployed app** after each deployment

---

## 🚀 You're All Set!

Everything is configured and automated. Just:
1. ✅ Add GitHub secrets (PYPI_API_TOKEN, NPM_TOKEN)
2. ✅ Deploy Streamlit app to Streamlit Cloud
3. ✅ Push code to main branch
4. ✅ Create tags for releases

**The rest is automatic!** 🎉

---

## 📞 Need Help?

- **Issues**: https://github.com/AbinVarghexe/vibescan/issues
- **Streamlit Docs**: https://docs.streamlit.io/
- **GitHub Actions**: https://docs.github.com/actions

---

**Enjoy your fully automated deployment pipeline! 🚀**
