import difflib

# A simplified list of highly popular packages to check for typosquatting.
# In a full production version, this would be a dynamic/larger database.
POPULAR_NPM_PACKAGES = [
    "react", "react-dom", "express", "lodash", "chalk", "commander", 
    "request", "axios", "moment", "eslint", "prettier", "typescript", 
    "next", "mongoose", "tailwindcss", "dotenv"
]

POPULAR_PYPI_PACKAGES = [
    "requests", "boto3", "urllib3", "botocore", "setuptools", "certifi", 
    "python-dateutil", "pandas", "numpy", "typing-extensions", "pytest",
    "flask", "django", "sqlalchemy", "pydantic", "fastapi"
]

def check_typosquatting(name, ecosystem):
    """
    Returns a dict containing typosquatting analysis.
    """
    targets = POPULAR_NPM_PACKAGES if ecosystem == 'npm' else POPULAR_PYPI_PACKAGES
    
    # Exact match means it's the real package, not a typo.
    if name in targets:
        return {'is_typo': False, 'similar_to': None, 'score': 0.0}
        
    # Find close matches. Cutoff 0.8 is generally a good threshold.
    matches = difflib.get_close_matches(name, targets, n=1, cutoff=0.75)
    
    if matches:
        # We found a similar package
        similar_to = matches[0]
        # Calculate ratio
        ratio = difflib.SequenceMatcher(None, name, similar_to).ratio()
        return {'is_typo': True, 'similar_to': similar_to, 'score': ratio}
        
    return {'is_typo': False, 'similar_to': None, 'score': 0.0}