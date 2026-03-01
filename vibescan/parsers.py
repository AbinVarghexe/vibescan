import json
import os
import re

def parse_package_json(path):
    """
    Parses a package.json file and returns a list of dependencies.
    Returns: list of dicts [{'name': 'react', 'version': '^18.0.0', 'ecosystem': 'npm'}, ...]
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        deps = []
        # Check both dependencies and devDependencies
        for key in ['dependencies', 'devDependencies']:
            if key in data:
                for name, version in data[key].items():
                    deps.append({
                        'name': name,
                        'version': version,
                        'ecosystem': 'npm'
                    })
        return deps
    except Exception as e:
        print(f"Error parsing {path}: {e}")
        return []

def parse_requirements_txt(path):
    """
    Parses a requirements.txt file.
    Returns: list of dicts [{'name': 'requests', 'version': '==2.25.0', 'ecosystem': 'pypi'}, ...]
    """
    deps = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Basic matching for standard formats (e.g., package==1.0, package>=1.0, package)
                # Ignore git URLs and file paths for now as they are harder to verify against registry without context
                if 'git+' in line or line.startswith('-e') or '://' in line:
                    continue
                    
                match = re.split(r'[=><!~]+', line, maxsplit=1)
                name = match[0].strip()
                version = match[1].strip() if len(match) > 1 else 'latest'
                
                # Remove extras like package[security]
                name = re.sub(r'\[.*?\]', '', name)
                
                if name:
                    deps.append({
                        'name': name,
                        'version': version,
                        'ecosystem': 'pypi'
                    })
        return deps
    except Exception as e:
        print(f"Error parsing {path}: {e}")
        return []