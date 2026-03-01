# VibeScan Web Interface

A web-based interface for VibeScan that allows users to upload or paste dependency files for analysis.

## Running the Web Interface

### Install Dependencies

```bash
cd web
pip install -r requirements.txt
pip install -e ..  # Install vibescan package
```

### Start the Server

```bash
python app.py
```

The web interface will be available at `http://localhost:5000`

## Features

- **File Upload**: Drag and drop or click to upload package.json or requirements.txt files
- **Text Paste**: Paste file contents directly for quick scanning
- **Real-time Analysis**: Get instant feedback on dependency risks
- **Beautiful UI**: Modern, responsive design with color-coded results
- **Detailed Reports**: View risk scores and explanations for each dependency

## API Endpoints

### POST /api/scan
Upload a file for scanning
- **Content-Type**: multipart/form-data
- **Body**: file (package.json or requirements.txt)
- **Response**: JSON with scan results

### POST /api/scan-text
Scan pasted text content
- **Content-Type**: application/json
- **Body**: `{"content": "...", "type": "package.json" | "requirements.txt"}`
- **Response**: JSON with scan results

## Deployment

For production deployment, use a WSGI server like gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Or use Docker (see Dockerfile in the web directory).