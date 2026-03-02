# VibeScan Code Explanation

Deep technical walkthrough of VibeScan's architecture, modules, and implementation details.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Data Flow](#data-flow)
- [Project Structure](#project-structure)
- [Module Reference](#module-reference)
  - [cli.py - Entry Point](#clipy---entry-point)
  - [parsers.py - Dependency Extraction](#parserspy---dependency-extraction)
  - [checkers/ - Verification Modules](#checkers---verification-modules)
  - [scorer.py - Risk Calculation](#scorerpy---risk-calculation)
  - [reporter.py - Output Formatting](#reporterpy---output-formatting)
- [Risk Scoring Algorithm](#risk-scoring-algorithm)
- [External API Integration](#external-api-integration)
- [Extension Guide](#extension-guide)

---

## Architecture Overview

VibeScan follows a **modular pipeline architecture** where each stage transforms and enriches the data:

```
Input Files → Parser → Checker → Scorer → Reporter → Exit
(package.json,   ↓        ↓        ↓         ↓         ↓
requirements.txt) ↓        ↓        ↓         ↓         ↓
                List of Registry Risk      Color-coded Exit code
                Dependencies Data   Score  Terminal    (0 or 1)
```

### Pipeline Stages

1. **Parser**: Extracts dependency names from manifest files
2. **Checker**: Queries external registries and analyzes package metadata
3. **Scorer**: Calculates risk score (0-100) based on heuristics
4. **Reporter**: Formats results with color coding and exits with appropriate code

### Design Principles

- **Modularity**: Each stage is independently testable and replaceable
- **Extensibility**: New parsers, checkers, or scoring rules can be added without modifying existing code
- **Fail-fast**: Critical findings immediately block the pipeline (exit code 1)
- **Transparency**: Debug mode shows all intermediate steps

---

## Data Flow

### Step-by-Step Execution

```python
# 1. CLI receives path argument
$ vibescan /path/to/project

# 2. Parser discovers manifest files and extracts dependencies
[
  {'name': 'react', 'version': '^18.0.0', 'ecosystem': 'npm'},
  {'name': 'requests', 'version': '==2.25.0', 'ecosystem': 'pypi'},
  {'name': 'hallucinated-lib', 'version': '1.0.0', 'ecosystem': 'npm'}
]

# 3. Checker queries registries for each package
{
  'react': {'exists': True, 'created': datetime(2013, 5, 24), 'downloads': 18000000},
  'requests': {'exists': True, 'created': datetime(2011, 2, 13), 'downloads': 50000000},
  'hallucinated-lib': {'exists': False, 'created': None, 'downloads': 0}
}

# 4. Scorer calculates risk
[
  {'name': 'react', 'score': 0, 'reasons': []},
  {'name': 'requests', 'score': 0, 'reasons': []},
  {'name': 'hallucinated-lib', 'score': 100, 'reasons': ['Package does not exist in registry']}
]

# 5. Reporter categorizes and displays
✓ OK 2 Safe Dependencies
✗ CRITICAL 1 Critical Dependencies
  - hallucinated-lib (npm) - Score: 100/100
    * Package does not exist in registry (Likely AI Hallucination/Slopsquat target)

[!] Critical dependencies detected. Exiting with code 1.
```

---

## Project Structure

```
vibescan/
├── vibescan/               # Main package directory
│   ├── __init__.py         # Package initialization
│   ├── cli.py              # Entry point & orchestration
│   ├── parsers.py          # Dependency file parsers
│   ├── scorer.py           # Risk calculation logic
│   ├── reporter.py         # Terminal output formatting
│   └── checkers/           # Verification modules
│       ├── __init__.py
│       ├── registry_checker.py    # npm/PyPI API calls
│       └── typosquat_checker.py   # String similarity detection
│
├── docs/                   # Documentation website
│   ├── index.html          # Landing page
│   ├── get-started.html    # User guide
│   ├── styles.css          # Unified stylesheet
│   ├── assets/             # Images and static files
│   └── documentation/      # Markdown documentation
│       ├── README.md
│       ├── USAGE.md
│       └── CODE_EXPLANATION.md (this file)
│
├── pyproject.toml          # Build system requirements
├── setup.py                # Package metadata
├── requirements.txt        # Runtime dependencies
├── Dockerfile              # Container image
├── docker-compose.yml      # Multi-container setup
└── README.md               # Project overview
```

---

## Module Reference

### cli.py - Entry Point

**Purpose**: Command-line interface and orchestration of the scanning pipeline.

**Key Functions**:

```python
def main():
    # 1. Parse CLI arguments
    parser = argparse.ArgumentParser(description="VibeScan - AI Dependency Risk Scanner")
    parser.add_argument('path', nargs='?', default='.', help="Path to the directory to scan")
    parser.add_argument('--debug', action='store_true', help="Enable debug output")
    args = parser.parse_args()
    
    # 2. Discover and parse manifest files
    deps = []
    if os.path.exists('package.json'):
        deps.extend(parse_package_json('package.json'))
    if os.path.exists('requirements.txt'):
        deps.extend(parse_requirements_txt('requirements.txt'))
    
    # 3. Run checkers for each dependency
    for dep in deps:
        typo_data = check_typosquatting(dep['name'], dep['ecosystem'])
        
        if dep['ecosystem'] == 'npm':
            registry_data = check_npm_package(dep['name'])
        elif dep['ecosystem'] == 'pypi':
            registry_data = check_pypi_package(dep['name'])
        
        # 4. Calculate risk score
        score, reasons = calculate_risk(registry_data, typo_data)
        dep['score'] = score
        dep['reasons'] = reasons
    
    # 5. Display results and exit
    success = report_results(deps)
    sys.exit(0 if success else 1)
```

**Flow Control**:
- Exits with code `0` if no critical findings (score < 60)
- Exits with code `1` if any dependency scores ≥ 60 (blocks CI pipeline)

---

### parsers.py - Dependency Extraction

**Purpose**: Read manifest files and extract dependency information.

#### `parse_package_json(path)`

```python
def parse_package_json(path):
    """
    Parses a package.json file and returns a list of dependencies.
    """
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    deps = []
    for key in ['dependencies', 'devDependencies']:
        if key in data:
            for name, version in data[key].items():
                deps.append({
                    'name': name,
                    'version': version,
                    'ecosystem': 'npm'
                })
    return deps
```

**Parsing Logic**:
- Reads both `dependencies` and `devDependencies` sections
- Extracts package name and version specifier
- Tags each dependency with `ecosystem: 'npm'`

#### `parse_requirements_txt(path)`

```python
def parse_requirements_txt(path):
    """
    Parses a requirements.txt file.
    """
    deps = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue  # Skip comments and empty lines
            
            # Ignore git URLs, file paths, editable installs
            if 'git+' in line or line.startswith('-e') or '://' in line:
                continue
            
            # Split on version operators (==, >=, <=, !=, ~=)
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
```

**Parsing Logic**:
- Ignores comments (`#`), empty lines, git URLs, editable installs
- Splits on version operators: `==`, `>=`, `<=`, `!=`, `~=`
- Removes extras like `requests[security]` → `requests`
- Tags each dependency with `ecosystem: 'pypi'`

---

### checkers/ - Verification Modules

#### registry_checker.py

**Purpose**: Query npm and PyPI registries to verify package existence and metadata.

##### `check_npm_package(name)`

```python
def check_npm_package(name):
    """
    Queries the npm registry for package metadata.
    Returns: {'exists': True/False, 'created': datetime, 'downloads': int}
    """
    url = f"https://registry.npmjs.org/{name}"
    resp = requests.get(url, timeout=5)
    
    if resp.status_code == 404:
        return {'exists': False, 'created': None, 'downloads': 0}
    
    elif resp.status_code == 200:
        data = resp.json()
        
        # Extract creation date from time.created field
        created_str = data.get('time', {}).get('created')
        created = datetime.fromisoformat(created_str.replace('Z', '+00:00'))
        
        # Fetch download statistics from npmjs.org API
        downloads_url = f"https://api.npmjs.org/downloads/point/last-month/{name}"
        downloads_resp = requests.get(downloads_url, timeout=5)
        downloads = downloads_resp.json().get('downloads', 0)
        
        return {'exists': True, 'created': created, 'downloads': downloads}
```

**API Endpoints**:
- **Package metadata**: `https://registry.npmjs.org/{name}`
- **Download stats**: `https://api.npmjs.org/downloads/point/last-month/{name}`

**Response Handling**:
- `404` → Package does not exist (potential hallucination)
- `200` → Package exists, extract metadata
- Network errors → Return `{'exists': None}` (neutral score)

##### `check_pypi_package(name)`

```python
def check_pypi_package(name):
    """
    Queries PyPI registry.
    Returns: {'exists': True/False, 'created': datetime, 'downloads': int}
    """
    url = f"https://pypi.org/pypi/{name}/json"
    resp = requests.get(url, timeout=5)
    
    if resp.status_code == 404:
        return {'exists': False, 'created': None, 'downloads': 0}
    
    elif resp.status_code == 200:
        data = resp.json()
        
        # Find earliest release upload time
        releases = data.get('releases', {})
        earliest_time = None
        for ver, files in releases.items():
            for f in files:
                upload_time = datetime.fromisoformat(f['upload_time'])
                if not earliest_time or upload_time < earliest_time:
                    earliest_time = upload_time
        
        return {'exists': True, 'created': earliest_time, 'downloads': 0}
```

**API Endpoint**:
- **Package metadata**: `https://pypi.org/pypi/{name}/json`

**Note**: PyPI's public API does not provide easy download statistics. A future enhancement could integrate with the `pypistats` API.

#### typosquat_checker.py

**Purpose**: Detect intentional misspellings of popular packages (typosquatting attacks).

```python
POPULAR_NPM_PACKAGES = [
    "react", "react-dom", "express", "lodash", "chalk", "commander", 
    "request", "axios", "moment", "eslint", "prettier", "typescript"
]

POPULAR_PYPI_PACKAGES = [
    "requests", "boto3", "urllib3", "pandas", "numpy", "pytest",
    "flask", "django", "sqlalchemy", "pydantic", "fastapi"
]

def check_typosquatting(name, ecosystem):
    """
    Returns typosquatting analysis using string similarity.
    """
    targets = POPULAR_NPM_PACKAGES if ecosystem == 'npm' else POPULAR_PYPI_PACKAGES
    
    # Exact match → legitimate package
    if name in targets:
        return {'is_typo': False, 'similar_to': None, 'score': 0.0}
    
    # Find similar names with cutoff 0.75 (75% similarity)
    matches = difflib.get_close_matches(name, targets, n=1, cutoff=0.75)
    
    if matches:
        similar_to = matches[0]
        ratio = difflib.SequenceMatcher(None, name, similar_to).ratio()
        return {'is_typo': True, 'similar_to': similar_to, 'score': ratio}
    
    return {'is_typo': False, 'similar_to': None, 'score': 0.0}
```

**Algorithm**: Uses Python's `difflib.SequenceMatcher` to calculate string similarity ratio (0.0 to 1.0).

**Examples**:
- `"reqests"` vs `"requests"` → 87.5% similarity → Typosquat detected
- `"react-native"` vs `"react"` → 54% similarity → Not flagged (below 75% threshold)

**Extension**: The popular package lists are currently hardcoded. A production version could:
1. Fetch from curated databases (npm top 1000, PyPI stats)
2. Use edit distance algorithms (Levenshtein) for more accuracy
3. Check for common typos (swapped characters, missing letters)

---

### scorer.py - Risk Calculation

**Purpose**: Calculate a risk score (0-100) based on registry data and typosquat detection.

```python
def calculate_risk(registry_data, typo_data):
    """
    Calculates a risk score from 0 to 100.
    Returns: (score, list_of_reasons)
    """
    score = 0
    reasons = []
    
    # 1. Hallucination Check (most critical)
    if registry_data.get('exists') is False:
        score += 100
        reasons.append("Package does not exist in registry (Likely AI Hallucination/Slopsquat target)")
    
    # 2. Typosquat Check
    if typo_data.get('is_typo'):
        score += 60
        target = typo_data['similar_to']
        reasons.append(f"Name is deceptively similar to popular package '{target}' (Typosquatting risk)")
    
    # 3. New Package Check
    created = registry_data.get('created')
    if created:
        age_days = (datetime.now(timezone.utc) - created).days
        if age_days < 7:
            score += 40
            reasons.append(f"Package is suspiciously new (Created {age_days} days ago)")
        elif age_days < 30:
            score += 10
            reasons.append(f"Package is relatively new (Created {age_days} days ago)")
    
    # 4. Low Download Count Check
    downloads = registry_data.get('downloads', 0)
    if registry_data.get('exists') is True and downloads < 100:
        score += 20
        reasons.append(f"Very low download count ({downloads} in last month)")
    elif downloads > 0 and downloads < 1000:
        score += 5
        reasons.append(f"Low download count ({downloads} in last month)")
    
    # Cap at 100
    score = min(score, 100)
    
    return score, reasons
```

#### Scoring Rules

| Condition | Score Impact | Reason |
|-----------|--------------|--------|
| Package does not exist | +100 | Definitive hallucination/slopsquat |
| Typosquat detected | +60 | High malicious intent likelihood |
| Package < 7 days old | +40 | Suspicious freshness |
| Package < 30 days old | +10 | Moderately new |
| Downloads < 100/month | +20 | Very low adoption |
| Downloads < 1000/month | +5 | Low adoption |

**Cumulative Scoring**: Multiple red flags add up (e.g., non-existent + typosquat = 100 capped).

**Network Errors**: If `registry_data['exists']` is `None` (network error), no penalty is applied, but a warning is logged.

---

### reporter.py - Output Formatting

**Purpose**: Color-coded terminal output and exit code determination.

```python
from colorama import Fore, Style, init
init(autoreset=True)

def report_results(results):
    """
    Categorizes dependencies and prints color-coded results.
    Returns: True if safe to proceed, False if critical risk found
    """
    safe = []
    suspicious = []
    critical = []
    
    for res in results:
        score = res['score']
        if score >= 60:
            critical.append(res)
        elif score >= 10:
            suspicious.append(res)
        else:
            safe.append(res)
    
    # Print safe packages
    print(f"{Fore.GREEN}{Style.BRIGHT}✓ OK {len(safe)} Safe Dependencies")
    
    # Print suspicious packages (yellow)
    if suspicious:
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}!! {len(suspicious)} Suspicious Dependencies (Review Recommended)")
        for s in suspicious:
            print(f"  - {Fore.YELLOW}{s['name']}{Style.RESET_ALL} ({s['ecosystem']}) - Score: {s['score']}/100")
            for r in s['reasons']:
                print(f"    * {r}")
    
    # Print critical packages (red)
    if critical:
        print(f"\n{Fore.RED}{Style.BRIGHT}✗ CRITICAL {len(critical)} Critical Dependencies")
        for c in critical:
            print(f"  - {Fore.RED}{c['name']}{Style.RESET_ALL} ({c['ecosystem']}) - Score: {c['score']}/100")
            for r in c['reasons']:
                print(f"    * {r}")
    
    # Return success/failure
    if critical:
        print(f"{Fore.RED}{Style.BRIGHT}[!] Critical dependencies detected. Exiting with code 1.")
        return False
    else:
        print(f"{Fore.GREEN}{Style.BRIGHT}All dependencies passed security checks.")
        return True
```

**Color Coding**:
- **Green** (`Fore.GREEN`): Safe (score 0-9)
- **Yellow** (`Fore.YELLOW`): Suspicious (score 10-59)
- **Red** (`Fore.RED`): Critical (score 60-100)

**Exit Code Logic**:
- Returns `False` if any critical dependency → `cli.py` exits with code 1
- Returns `True` otherwise → `cli.py` exits with code 0

---

## Risk Scoring Algorithm

### Mathematical Model

```python
risk_score = min(
    hallucination_penalty +
    typosquat_penalty +
    age_penalty +
    popularity_penalty,
    100  # Maximum cap
)
```

### Penalty Breakdown

#### 1. Hallucination Penalty
```python
if package_not_in_registry:
    score += 100  # Instant critical status
```

**Justification**: Non-existent packages are the most dangerous. They indicate:
- AI model hallucinated a plausible-sounding name
- Attacker pre-registered a slopsquat target name
- Typo in dependency specification

#### 2. Typosquat Penalty
```python
if similar_to_popular_package(name, threshold=0.75):
    score += 60  # High risk
```

**Justification**: Intentional misspellings exploit human error:
- `reqests` instead of `requests`
- `expres` instead of `express`

**Threshold Calibration**: 75% similarity catches common typos while avoiding false positives on legitimately similar names.

#### 3. Age Penalty
```python
if age < 7_days:
    score += 40
elif age < 30_days:
    score += 10
```

**Justification**: Brand-new packages warrant extra scrutiny:
- Attackers often create packages just before targeting campaigns
- Legitimate packages usually have long histories

#### 4. Popularity Penalty
```python
if downloads < 100:
    score += 20
elif downloads < 1000:
    score += 5
```

**Justification**: Low adoption correlates with:
- Abandoned or experimental packages
- Malicious packages with few victims so far
- Targeted attacks (low-profile distribution)

### Score Interpretation

| Range | Category | CI Behavior | Recommendation |
|-------|----------|-------------|----------------|
| 0-9 | Safe | ✅ Pass | No action needed |
| 10-59 | Suspicious | ✅ Pass | Manual review recommended |
| 60-100 | Critical | ❌ Fail | Block deployment |

---

## External API Integration

### npm Registry API

**Base URL**: `https://registry.npmjs.org/`

**Endpoint**: `GET /{package_name}`

**Example Request**:
```bash
curl https://registry.npmjs.org/react
```

**Response Fields Used**:
```json
{
  "name": "react",
  "time": {
    "created": "2011-10-26T17:46:21.942Z",
    "modified": "2024-03-15T10:00:00.000Z"
  }
}
```

**Download Stats API**:
```bash
curl https://api.npmjs.org/downloads/point/last-month/react
```

**Response**:
```json
{
  "downloads": 18234567,
  "start": "2024-02-15",
  "end": "2024-03-15",
  "package": "react"
}
```

### PyPI API

**Base URL**: `https://pypi.org/pypi/`

**Endpoint**: `GET /{package_name}/json`

**Example Request**:
```bash
curl https://pypi.org/pypi/requests/json
```

**Response Fields Used**:
```json
{
  "info": {
    "name": "requests",
    "version": "2.31.0"
  },
  "releases": {
    "2.31.0": [
      {
        "filename": "requests-2.31.0.tar.gz",
        "upload_time": "2023-05-22T14:56:12",
        "upload_time_iso_8601": "2023-05-22T14:56:12.345678Z"
      }
    ]
  }
}
```

### Rate Limiting

Both APIs are public and do not require authentication for basic queries, but have rate limits:

- **npm**: ~1000 requests/IP/hour
- **PyPI**: No documented limit, but use respectful request rates

**Mitigation Strategy**: VibeScan makes 1-2 requests per dependency, well within typical limits for small projects. For large monorepos with hundreds of dependencies, consider:
1. Implementing request caching (Redis/memcached)
2. Batching requests with delays
3. Using authenticated API access for higher limits

---

## Extension Guide

### Adding a New Parser

To support additional manifest formats (e.g., `Gemfile`, `Cargo.toml`):

1. **Create parser function** in `parsers.py`:

```python
def parse_gemfile(path):
    """
    Parses a Gemfile and extracts Ruby gem dependencies.
    """
    deps = []
    with open(path, 'r') as f:
        for line in f:
            match = re.match(r"gem ['\"](.+?)['\"]", line)
            if match:
                deps.append({
                    'name': match.group(1),
                    'version': 'latest',
                    'ecosystem': 'rubygems'
                })
    return deps
```

2. **Add registry checker** in `checkers/registry_checker.py`:

```python
def check_rubygems_package(name):
    """
    Queries rubygems.org API.
    """
    url = f"https://rubygems.org/api/v1/gems/{name}.json"
    resp = requests.get(url, timeout=5)
    if resp.status_code == 404:
        return {'exists': False, 'created': None, 'downloads': 0}
    elif resp.status_code == 200:
        data = resp.json()
        downloads = data.get('downloads', 0)
        return {'exists': True, 'created': None, 'downloads': downloads}
```

3. **Update `cli.py`** to call new parser:

```python
gemfile = os.path.join(scan_path, 'Gemfile')
if os.path.exists(gemfile):
    deps.extend(parse_gemfile(gemfile))
```

4. **Update typosquat checker** with popular Ruby packages:

```python
POPULAR_RUBYGEMS_PACKAGES = ['rails', 'rake', 'bundler', 'rspec', ...]
```

### Adding Custom Scoring Rules

To add new risk factors:

1. **Modify `scorer.py`**:

```python
def calculate_risk(registry_data, typo_data):
    # ... existing checks ...
    
    # New rule: Check for suspicious maintainer
    maintainer = registry_data.get('maintainer')
    if maintainer and maintainer in SUSPICIOUS_MAINTAINERS:
        score += 50
        reasons.append(f"Package maintained by flagged user: {maintainer}")
    
    return score, reasons
```

2. **Update documentation** to reflect new scoring rules.

### Adding New Checkers

To add new verification modules (e.g., CVE database check):

1. **Create `checkers/cve_checker.py`**:

```python
import requests

def check_cve(name, version):
    """
    Queries CVE database for known vulnerabilities.
    """
    url = f"https://cve.circl.lu/api/search/{name}/{version}"
    resp = requests.get(url, timeout=5)
    if resp.status_code == 200:
        vulns = resp.json()
        return {'vulnerable': len(vulns) > 0, 'count': len(vulns)}
    return {'vulnerable': False, 'count': 0}
```

2. **Integrate in `cli.py`**:

```python
from .checkers.cve_checker import check_cve

cve_data = check_cve(dep['name'], dep['version'])
if cve_data['vulnerable']:
    score += 30
    reasons.append(f"Known vulnerabilities: {cve_data['count']} CVEs found")
```

---

## Development Workflow

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run unit tests
pytest tests/

# Run with coverage
pytest --cov=vibescan tests/
```

### Local Development

```bash
# Install in editable mode
pip install -e .

# Make changes to source code

# Test immediately without reinstalling
vibescan
```

### Debugging

Enable debug mode to see internal state:

```bash
vibescan --debug
```

**Output**:
```
Found package.json at /path/to/package.json
Parsing dependencies: ['react', 'axios', 'lodash']
Checking npm package: react
  - Registry response: 200 OK
  - Created: 2013-05-24
  - Downloads: 18000000
  - Risk score: 0
Checking npm package: axios
  ...
```

---

## Performance Considerations

### Bottlenecks

1. **Network I/O**: Registry API calls are synchronous and blocking
2. **Large Dependency Lists**: Projects with 100+ dependencies take ~30-60 seconds

### Optimization Strategies

#### 1. Concurrent Requests

Replace sequential checks with async/await:

```python
import asyncio
import aiohttp

async def check_npm_package_async(session, name):
    url = f"https://registry.npmjs.org/{name}"
    async with session.get(url) as resp:
        if resp.status == 200:
            data = await resp.json()
            return parse_npm_response(data)
        return {'exists': False}

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [check_npm_package_async(session, dep['name']) for dep in deps]
        results = await asyncio.gather(*tasks)
```

**Speedup**: 10x faster for 50+ dependencies

#### 2. Caching

Cache registry responses to avoid redundant API calls:

```python
import redis
cache = redis.Redis(host='localhost', port=6379, db=0)

def check_npm_package_cached(name):
    cached = cache.get(f"npm:{name}")
    if cached:
        return json.loads(cached)
    
    result = check_npm_package(name)
    cache.setex(f"npm:{name}", 3600, json.dumps(result))  # Cache for 1 hour
    return result
```

**Speedup**: Near-instant for repeated scans

#### 3. Partial Scanning

Only scan production dependencies:

```python
# In parsers.py
def parse_package_json(path, dev=False):
    keys = ['dependencies']
    if dev:
        keys.append('devDependencies')
    # ... rest of logic
```

**Speedup**: 2x faster by skipping devDependencies

---

## Security Considerations

### API Authentication

Current implementation uses public APIs without authentication. For production:

1. **Obtain API tokens** from npm and PyPI
2. **Add authentication headers**:

```python
headers = {'Authorization': f'Bearer {NPM_TOKEN}'}
resp = requests.get(url, headers=headers, timeout=5)
```

### Error Handling

Always handle network errors gracefully:

```python
try:
    resp = requests.get(url, timeout=5)
    resp.raise_for_status()
except requests.RequestException as e:
    return {'exists': None, 'error': str(e)}
```

### Input Validation

Sanitize package names to prevent injection attacks:

```python
import re

def sanitize_package_name(name):
    # Only allow alphanumeric, hyphens, underscores, dots
    if not re.match(r'^[a-zA-Z0-9._-]+$', name):
        raise ValueError(f"Invalid package name: {name}")
    return name
```

---

## Future Enhancements

### Planned Features

1. **Machine Learning**: Train a model on historical malicious package data
2. **Blockchain Verification**: Check package signatures against immutable ledgers
3. **Community Reports**: Integrate with security databases (Snyk, npm Advisory)
4. **Auto-Remediation**: Suggest safe alternatives for flagged packages
5. **GitHub Integration**: Automatic PR comments with scan results
6. **Web Dashboard**: Visualize risk trends over time

### Contributing

To contribute to VibeScan:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Implement your changes with tests
4. Submit a pull request with detailed description

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'colorama'"

**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

### Issue: Network timeouts

**Solution**: Increase timeout in registry checkers:
```python
resp = requests.get(url, timeout=10)  # Increase from 5 to 10 seconds
```

### Issue: False positive for legitimate package

**Solution**: VibeScan uses heuristics that may occasionally flag safe packages. Review reasons manually and consider:
1. Checking package on npmjs.com or pypi.org directly
2. Searching for security reports or CVEs
3. Verifying maintainer identity on GitHub

---

## License

VibeScan is licensed under the MIT License. See [LICENSE](../../LICENSE) for details.

---

## Support

- **GitHub Issues**: [https://github.com/AbinVarghexe/vibescan/issues](https://github.com/AbinVarghexe/vibescan/issues)
- **Documentation**: [https://abinvarghexe.github.io/vibescan/](https://abinvarghexe.github.io/vibescan/)
- **Email**: support@vibescan.io

---

**Last Updated**: March 2026  
**Version**: 0.1.0
