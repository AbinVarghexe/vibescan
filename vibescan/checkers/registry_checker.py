import requests
from datetime import datetime
import json

def check_npm_package(name):
    """
    Queries the npm registry for package metadata.
    Returns dict: {'exists': True/False, 'created': datetime or None, 'downloads': int}
    """
    url = f"https://registry.npmjs.org/{name}"
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 404:
            return {'exists': False, 'created': None, 'downloads': 0}
        elif resp.status_code == 200:
            data = resp.json()
            created_str = data.get('time', {}).get('created')
            created = None
            if created_str:
                try:
                    # npm returns ISO 8601 like "2011-10-26T17:46:21.942Z"
                    created_str = created_str.replace('Z', '+00:00')
                    created = datetime.fromisoformat(created_str)
                except Exception:
                    pass
            
            # Fetch download statistics
            downloads = 0
            try:
                # Get last month's download count
                downloads_url = f"https://api.npmjs.org/downloads/point/last-month/{name}"
                downloads_resp = requests.get(downloads_url, timeout=5)
                if downloads_resp.status_code == 200:
                    downloads_data = downloads_resp.json()
                    downloads = downloads_data.get('downloads', 0)
            except Exception:
                pass
            
            return {'exists': True, 'created': created, 'downloads': downloads}
        else:
            return {'exists': None, 'created': None, 'downloads': 0, 'error': f"HTTP {resp.status_code}"}
    except requests.RequestException:
        return {'exists': None, 'created': None, 'downloads': 0, 'error': "Network Error"}

def check_pypi_package(name):
    """
    Queries PyPI registry.
    """
    url = f"https://pypi.org/pypi/{name}/json"
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 404:
            return {'exists': False, 'created': None, 'downloads': 0}
        elif resp.status_code == 200:
            data = resp.json()
            # Try to get creation time of first release
            releases = data.get('releases', {})
            created = None
            if releases:
                # Get the earliest release upload time
                earliest_time = None
                for ver, files in releases.items():
                    for f in files:
                        upload_time_str = f.get('upload_time')
                        if upload_time_str:
                            try:
                                upload_time = datetime.fromisoformat(upload_time_str)
                                if not earliest_time or upload_time < earliest_time:
                                    earliest_time = upload_time
                            except Exception:
                                pass
                created = earliest_time
            
            # PyPI doesn't provide easy download stats in the main API
            # We'll use 0 for now, or could integrate with pypistats API separately
            downloads = 0
            
            return {'exists': True, 'created': created, 'downloads': downloads}
        else:
            return {'exists': None, 'created': None, 'downloads': 0, 'error': f"HTTP {resp.status_code}"}
    except requests.RequestException:
        return {'exists': None, 'created': None, 'downloads': 0, 'error': "Network Error"}