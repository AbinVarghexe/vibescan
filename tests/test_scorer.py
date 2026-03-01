from datetime import datetime, timedelta, timezone
from vibescan.scorer import calculate_risk

def test_calculate_risk_hallucinated():
    registry_data = {'exists': False, 'created': None}
    typo_data = {'is_typo': False, 'similar_to': None, 'score': 0.0}
    
    score, reasons = calculate_risk(registry_data, typo_data)
    assert score == 100
    assert "Likely AI Hallucination/Slopsquat target" in reasons[0]

def test_calculate_risk_typosquat_and_hallucinated():
    registry_data = {'exists': False, 'created': None}
    typo_data = {'is_typo': True, 'similar_to': 'react', 'score': 0.8}
    
    score, reasons = calculate_risk(registry_data, typo_data)
    assert score == 100 # Capped at 100 (100 + 60)
    assert len(reasons) == 2

def test_calculate_risk_new_package():
    # Package created 2 days ago
    two_days_ago = datetime.now(timezone.utc) - timedelta(days=2)
    registry_data = {'exists': True, 'created': two_days_ago, 'downloads': 5000}
    typo_data = {'is_typo': False, 'similar_to': None, 'score': 0.0}
    
    score, reasons = calculate_risk(registry_data, typo_data)
    assert score == 40
    assert "suspiciously new" in reasons[0]

def test_calculate_risk_safe():
    # Package created 5 years ago
    old_date = datetime.now(timezone.utc) - timedelta(days=5*365)
    registry_data = {'exists': True, 'created': old_date, 'downloads': 1000000}
    typo_data = {'is_typo': False, 'similar_to': None, 'score': 0.0}
    
    score, reasons = calculate_risk(registry_data, typo_data)
    assert score == 0
    assert len(reasons) == 0