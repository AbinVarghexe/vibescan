# Deployment Guide

This guide covers deploying VibeScan to PyPI, npm, and setting up the web interface.

## Prerequisites

1. **PyPI Account**: Create an account at https://pypi.org/
2. **npm Account**: Create an account at https://www.npmjs.com/
3. **API Tokens**: Generate API tokens for both platforms

## Deploying to PyPI (Python Package)

### 1. Install Build Tools

```bash
pip install build twine
```

### 2. Build the Package

```bash
python -m build
```

This creates distribution files in `dist/`:
- `vibescan-0.1.0-py3-none-any.whl`
- `vibescan-0.1.0.tar.gz`

### 3. Test Upload (TestPyPI - Recommended First)

```bash
python -m twine upload --repository testpypi dist/*
```

Username: `__token__`
Password: Your TestPyPI API token

Test installation:
```bash
pip install --index-url https://test.pypi.org/simple/ vibescan
```

### 4. Upload to PyPI (Production)

```bash
python -m twine upload dist/*
```

Username: `__token__`
Password: Your PyPI API token

### 5. Verify Installation

```bash
pip install vibescan
vibescan --help
```

## Deploying to npm (Node.js Wrapper)

### 1. Navigate to js-wrapper

```bash
cd js-wrapper
```

### 2. Test Package Locally

```bash
npm link
vibescan --help
```

### 3. Login to npm

```bash
npm login
```

### 4. Publish to npm

```bash
npm publish
```

For scoped packages:
```bash
npm publish --access public
```

### 5. Verify Installation

```bash
npm install -g vibescan-js
vibescan --help
```

## Deploying the Web Interface

### Option 1: Traditional Server (with gunicorn)

```bash
cd web
pip install gunicorn

# Production server
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Option 2: Docker

Create `web/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install vibescan
RUN pip install vibescan

# Copy web app
COPY . /app/web

WORKDIR /app/web
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:

```bash
docker build -t vibescan-web .
docker run -p 5000:5000 vibescan-web
```

### Option 3: Cloud Platforms

#### Heroku

Create `Procfile`:
```
web: gunicorn app:app
```

Deploy:
```bash
heroku create vibescan-web
git push heroku main
```

#### AWS Elastic Beanstalk

```bash
eb init -p python-3.11 vibescan-web
eb create vibescan-web-env
eb deploy
```

#### Google Cloud Run

```bash
gcloud run deploy vibescan-web --source . --platform managed
```

## CI/CD Automation

### GitHub Actions - Auto-publish

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI and npm

on:
  release:
    types: [published]

jobs:
  publish-pypi:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.x'
      - name: Build package
        run: |
          pip install build
          python -m build
      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_API_TOKEN }}

  publish-npm:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '18.x'
          registry-url: 'https://registry.npmjs.org'
      - name: Publish to npm
        run: |
          cd js-wrapper
          npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

Add secrets to GitHub repository:
- `PYPI_API_TOKEN`: Your PyPI API token
- `NPM_TOKEN`: Your npm access token

## Version Management

### Updating Version Numbers

Update version in these files:
1. `setup.py` - Python package version
2. `pyproject.toml` - Python package version
3. `js-wrapper/package.json` - npm package version
4. `CHANGELOG.md` - Add new version entry

### Creating a Release

```bash
# Tag the release
git tag -a v0.1.0 -m "Release version 0.1.0"
git push origin v0.1.0

# GitHub Actions will automatically publish (if configured)
```

## Post-Deployment Checklist

- [ ] Test PyPI installation: `pip install vibescan`
- [ ] Test npm installation: `npm install -g vibescan-js`
- [ ] Verify CLI works: `vibescan --help`
- [ ] Test with sample projects
- [ ] Update documentation with installation commands
- [ ] Announce on social media/blog
- [ ] Monitor for issues

## Troubleshooting

### PyPI Upload Failed

- Check package name availability
- Verify API token is correct
- Ensure version number is incremented
- Check for build errors

### npm Publish Failed

- Package name might be taken
- Try scoped package: `@yourusername/vibescan-js`
- Verify npm authentication
- Check package.json for errors

### Web App Not Starting

- Check all dependencies installed
- Verify Python path is correct
- Check port availability
- Review application logs

## Support

For deployment issues, please open an issue at: https://github.com/yourusername/vibescan/issues