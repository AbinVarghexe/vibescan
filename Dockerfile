FROM python:3.11-slim

LABEL maintainer="VibeScan Contributors"
LABEL description="VibeScan Web Interface - AI Dependency Security Scanner"

WORKDIR /app

# Install vibescan Python package
COPY setup.py pyproject.toml README.md LICENSE MANIFEST.in ./
COPY vibescan ./vibescan
RUN pip install --no-cache-dir -e .

# Install web dependencies
COPY web/requirements.txt ./web/
RUN pip install --no-cache-dir -r web/requirements.txt gunicorn

# Copy web application
COPY web ./web

WORKDIR /app/web

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:5000')"

# Run with gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--access-logfile", "-", "--error-logfile", "-", "app:app"]