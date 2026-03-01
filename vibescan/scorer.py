from datetime import datetime, timezone

def calculate_risk(registry_data, typo_data):
    """
    Calculates a risk score from 0 to 100 based on the registry and typosquatting data.
    Returns: (score, list_of_reasons)
    """
    score = 0
    reasons = []

    # 1. Hallucination Check
    if registry_data.get('exists') is False:
        score += 100
        reasons.append("Package does not exist in registry (Likely AI Hallucination/Slopsquat target)")
    elif registry_data.get('exists') is None:
        reasons.append("Could not verify package existence due to network error.")
        # We don't penalize score for network errors, but we warn

    # 2. Typosquat Check
    if typo_data.get('is_typo'):
        # If it's a typo AND doesn't exist, it's a huge risk for slopsquatting
        score += 60
        target = typo_data['similar_to']
        reasons.append(f"Name is deceptively similar to popular package '{target}' (Typosquatting risk)")

    # 3. New Package Check
    created = registry_data.get('created')
    if created:
        now = datetime.now(timezone.utc)
        if created.tzinfo is None:
            # Assuming UTC if naive
            created = created.replace(tzinfo=timezone.utc)
            
        age_days = (now - created).days
        if age_days < 7:
            score += 40
            reasons.append(f"Package is suspiciously new (Created {age_days} days ago)")
        elif age_days < 30:
            score += 10
            reasons.append(f"Package is relatively new (Created {age_days} days ago)")

    # Cap at 100
    score = min(score, 100)
    
    return score, reasons
