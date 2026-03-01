"""
VibeScan Web Interface
A Flask-based web application for scanning dependencies
"""
from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import tempfile
import json
from vibescan.parsers import parse_package_json, parse_requirements_txt
from vibescan.checkers.registry_checker import check_npm_package, check_pypi_package
from vibescan.checkers.typosquat_checker import check_typosquatting
from vibescan.scorer import calculate_risk

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB max file size

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/scan', methods=['POST'])
def scan():
    """API endpoint to scan uploaded file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Determine file type
        filename = file.filename.lower()
        deps = []
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='w+', suffix=filename, delete=False, encoding='utf-8') as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name
        
        try:
            if filename == 'package.json':
                deps = parse_package_json(tmp_path)
            elif filename == 'requirements.txt':
                deps = parse_requirements_txt(tmp_path)
            else:
                return jsonify({'error': 'Only package.json and requirements.txt are supported'}), 400
        finally:
            os.unlink(tmp_path)
        
        if not deps:
            return jsonify({'error': 'No dependencies found in file'}), 400
        
        # Scan dependencies
        results = []
        for dep in deps:
            registry_data = {}
            typo_data = {}
            
            name = dep['name']
            eco = dep['ecosystem']
            
            # Check Typosquat
            typo_data = check_typosquatting(name, eco)
            
            # Check Registry
            if eco == 'npm':
                registry_data = check_npm_package(name)
            elif eco == 'pypi':
                registry_data = check_pypi_package(name)
            
            score, reasons = calculate_risk(registry_data, typo_data)
            
            dep['score'] = score
            dep['reasons'] = reasons
            results.append(dep)
        
        # Categorize results
        safe = [r for r in results if r['score'] < 10]
        suspicious = [r for r in results if 10 <= r['score'] < 60]
        critical = [r for r in results if r['score'] >= 60]
        
        return jsonify({
            'total': len(results),
            'safe': safe,
            'suspicious': suspicious,
            'critical': critical,
            'status': 'critical' if critical else ('suspicious' if suspicious else 'safe')
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/scan-text', methods=['POST'])
def scan_text():
    """API endpoint to scan text content"""
    try:
        data = request.get_json()
        if not data or 'content' not in data or 'type' not in data:
            return jsonify({'error': 'Missing content or type'}), 400
        
        content = data['content']
        file_type = data['type']
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='w+', suffix=f'.{file_type}', delete=False, encoding='utf-8') as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        
        deps = []
        try:
            if file_type == 'package.json':
                deps = parse_package_json(tmp_path)
            elif file_type == 'requirements.txt':
                deps = parse_requirements_txt(tmp_path)
            else:
                return jsonify({'error': 'Invalid file type'}), 400
        finally:
            os.unlink(tmp_path)
        
        if not deps:
            return jsonify({'error': 'No dependencies found'}), 400
        
        # Scan dependencies (same logic as scan endpoint)
        results = []
        for dep in deps:
            registry_data = {}
            typo_data = {}
            
            name = dep['name']
            eco = dep['ecosystem']
            
            typo_data = check_typosquatting(name, eco)
            
            if eco == 'npm':
                registry_data = check_npm_package(name)
            elif eco == 'pypi':
                registry_data = check_pypi_package(name)
            
            score, reasons = calculate_risk(registry_data, typo_data)
            
            dep['score'] = score
            dep['reasons'] = reasons
            results.append(dep)
        
        safe = [r for r in results if r['score'] < 10]
        suspicious = [r for r in results if 10 <= r['score'] < 60]
        critical = [r for r in results if r['score'] >= 60]
        
        return jsonify({
            'total': len(results),
            'safe': safe,
            'suspicious': suspicious,
            'critical': critical,
            'status': 'critical' if critical else ('suspicious' if suspicious else 'safe')
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)