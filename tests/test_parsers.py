import os
import json
import pytest
from vibescan.parsers import parse_package_json, parse_requirements_txt

def test_parse_package_json(tmpdir):
    # Create a temporary package.json
    p = tmpdir.join("package.json")
    data = {
        "dependencies": {
            "react": "^18.0.0",
            "lodash": "4.17.21"
        },
        "devDependencies": {
            "jest": "^27.0.0"
        }
    }
    p.write(json.dumps(data))
    
    deps = parse_package_json(str(p))
    
    assert len(deps) == 3
    names = [d['name'] for d in deps]
    assert 'react' in names
    assert 'lodash' in names
    assert 'jest' in names
    
    # Check ecosystem
    assert all(d['ecosystem'] == 'npm' for d in deps)

def test_parse_requirements_txt(tmpdir):
    p = tmpdir.join("requirements.txt")
    p.write("""
requests==2.25.0
pandas>=1.0.0
numpy
flask[security]
# comment
-e git+https://github.com/test/repo.git#egg=test
""")
    
    deps = parse_requirements_txt(str(p))
    
    assert len(deps) == 4
    names = [d['name'] for d in deps]
    assert 'requests' in names
    assert 'pandas' in names
    assert 'numpy' in names
    assert 'flask' in names
    
    assert all(d['ecosystem'] == 'pypi' for d in deps)

def test_parse_missing_file():
    assert parse_package_json("non_existent_package.json") == []
    assert parse_requirements_txt("non_existent_requirements.txt") == []
