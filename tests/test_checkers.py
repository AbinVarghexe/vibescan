import json
import responses
from datetime import datetime, timezone
from vibescan.checkers.registry_checker import check_npm_package, check_pypi_package
from vibescan.checkers.typosquat_checker import check_typosquatting

@responses.activate
def test_check_npm_package_exists():
    responses.add(
        responses.GET,
        "https://registry.npmjs.org/react",
        json={"time": {"created": "2013-05-29T16:11:41.056Z"}},
        status=200
    )
    res = check_npm_package("react")
    assert res['exists'] is True
    assert res['created'] is not None
    assert res['created'].year == 2013

@responses.activate
def test_check_npm_package_hallucinated():
    responses.add(
        responses.GET,
        "https://registry.npmjs.org/totally-fake-package12345",
        status=404
    )
    res = check_npm_package("totally-fake-package12345")
    assert res['exists'] is False
    assert res['created'] is None

@responses.activate
def test_check_pypi_package_exists():
    responses.add(
        responses.GET,
        "https://pypi.org/pypi/requests/json",
        json={"releases": {"0.2.0": [{"upload_time": "2011-02-14T03:31:07"}]}},
        status=200
    )
    res = check_pypi_package("requests")
    assert res['exists'] is True
    assert res['created'] is not None

def test_check_typosquatting_safe():
    res = check_typosquatting("react", "npm")
    assert res['is_typo'] is False

def test_check_typosquatting_typo():
    # reqeusts -> requests
    res = check_typosquatting("reqeusts", "pypi")
    assert res['is_typo'] is True
    assert res['similar_to'] == 'requests'
    
    # reactt -> react
    res = check_typosquatting("reactt", "npm")
    assert res['is_typo'] is True
    assert res['similar_to'] == 'react'