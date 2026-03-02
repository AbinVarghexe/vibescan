# Required GitHub Secrets for Automated Deployment

This document lists all GitHub Secrets needed for automated deployment workflows.

## 📦 Package Publishing

### PyPI
- `PYPI_API_TOKEN` - PyPI API token for publishing packages
  - Get from: https://pypi.org/manage/account/token/
  - Permissions: Upload packages

- `TEST_PYPI_API_TOKEN` - Test PyPI API token (optional, for testing)
  - Get from: https://test.pypi.org/manage/account/token/

### npm
- `NPM_TOKEN` - npm authentication token
  - Get from: https://www.npmjs.com/settings/YOUR_USERNAME/tokens
  - Type: Automation token

## 🐳 Docker

- `DOCKER_USERNAME` - Docker Hub username
- `DOCKER_TOKEN` - Docker Hub access token
  - Get from: https://hub.docker.com/settings/security

## 🚀 Hosting Platforms

### Heroku
- `HEROKU_API_KEY` - Heroku API key
  - Get from: Account Settings → API Key
- `HEROKU_APP_NAME` - Your Heroku app name
- `HEROKU_EMAIL` - Email associated with Heroku account

### Fly.io
- `FLY_API_TOKEN` - Fly.io API token
  - Run: `flyctl auth token`

### Railway
- `RAILWAY_TOKEN` - Railway API token
  - Get from: Account Settings → Tokens

### Render
- `RENDER_DEPLOY_HOOK` - Render deploy hook URL suffix
  - Get from: Dashboard → Settings → Deploy Hook

### Hugging Face
- `HF_TOKEN` - Hugging Face API token
  - Get from: Settings → Access Tokens
- `HF_SPACE_NAME` - Your Hugging Face Space name (e.g., username/vibescan)

## 📚 Documentation

### ReadTheDocs (Optional)
- `READTHEDOCS_TOKEN` - ReadTheDocs API token
- `READTHEDOCS_PROJECT` - Project slug on ReadTheDocs

## 🔒 Security Scanning

### Snyk (Optional)
- `SNYK_TOKEN` - Snyk API token
  - Get from: https://snyk.io/account

### Codecov (Optional)
- `CODECOV_TOKEN` - Codecov token
  - Get from: https://codecov.io/

## 📝 How to Add Secrets

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add name and value
5. Click **Add secret**

## 🎯 Minimum Required for Basic Deployment

For basic automated deployment, you need at minimum:
- `PYPI_API_TOKEN` (for Python package)
- `NPM_TOKEN` (for npm package)
- `DOCKER_USERNAME` and `DOCKER_TOKEN` (for Docker)

## ⚠️ Security Notes

- ✅ Never commit secrets to the repository
- ✅ Use repository secrets, not environment variables in code
- ✅ Rotate tokens periodically
- ✅ Use minimal permissions for each token
- ✅ Enable 2FA on all platforms

## 📖 Testing Deployment

You can test deployment workflows without secrets by:
1. Commenting out secret-dependent jobs
2. Using `workflow_dispatch` trigger
3. Testing locally with Docker

## 🆘 Troubleshooting

If deployment fails:
1. Check secret names match exactly
2. Verify tokens haven't expired
3. Check token permissions
4. Review workflow logs for specific errors
5. Test credentials manually using CLI tools

---

**Last Updated**: March 2, 2026