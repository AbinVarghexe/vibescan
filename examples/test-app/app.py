"""
Demo Flask Application with Intentional Security Issues
========================================================
This application demonstrates VibeScan's ability to detect:
1. Typosquatted dependencies
2. Hallucinated/non-existent packages
3. Security risks in project dependencies

WARNING: This app contains intentionally vulnerable dependencies!
DO NOT USE IN PRODUCTION!
"""

from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    """Main page displaying information about the vulnerable dependencies"""
    return render_template('index.html')

@app.route('/api/dependencies')
def get_dependencies():
    """API endpoint returning information about the dependencies"""
    dependencies = {
        'python': {
            'legitimate': ['Flask==3.0.0', 'requests==2.31.0'],
            'typosquatting': [
                'reqeusts==1.0.0 (typo of "requests")',
                'djago==2.0.0 (typo of "django")',
                'numpyy==1.0.0 (typo of "numpy")',
                'pandsa==0.5.0 (typo of "pandas")',
                'flsk==1.2.0 (typo of "flask")',
                'pythonrequest==1.0.0 (similar to "requests")'
            ],
            'hallucinated': [
                'flask-super-auth==1.0.0',
                'secure-web-framework==2.1.0',
                'ai-data-processor==3.0.0',
                'magic-database-connector==1.5.0',
                'ultra-fast-api==2.0.0',
                'quantum-validator==1.0.0',
                'neural-web-engine==0.9.0'
            ]
        },
        'javascript': {
            'legitimate': ['express', 'axios'],
            'typosquatting': [
                'expresss (typo of "express")',
                'recat (typo of "react")',
                'lodsh (typo of "lodash")',
                'momnet (typo of "moment")',
                'axois (typo of "axios")'
            ],
            'hallucinated': [
                'react-super-hooks',
                'express-quantum-router',
                'ai-frontend-framework',
                'neural-state-manager',
                'magic-http-client'
            ]
        }
    }
    return jsonify(dependencies)

@app.route('/api/scan-status')
def scan_status():
    """Endpoint to show scan status"""
    return jsonify({
        'status': 'vulnerable',
        'total_issues': 18,
        'critical': 13,
        'warning': 5,
        'safe': 2,
        'message': 'This application has intentional vulnerabilities for demonstration purposes'
    })

if __name__ == '__main__':
    print("=" * 80)
    print("VULNERABLE DEMO APPLICATION - FOR TESTING ONLY")
    print("=" * 80)
    print("\nThis application contains intentionally vulnerable dependencies:")
    print("- Typosquatted packages (similar names to popular packages)")
    print("- Hallucinated packages (non-existent packages)")
    print("\nUse VibeScan to detect these issues:")
    print("  vibescan test-app/")
    print("\n" + "=" * 80)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
