import yaml

def load_scoring_config():
    with open("config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config.get("scoring", {"low": 0, "medium": 2, "high": 3})

def assign_risk_level(keywords_found, config=None):
    """
    Assign suspicion risk level based on keyword matches and thresholds from config.yaml
    """
    if not config:
        config = load_scoring_config()

    if not keywords_found:
        return "LOW"

    count = len(keywords_found.split(",")) if isinstance(keywords_found, str) and keywords_found else 0

    if count <= config["low"]:
        return "LOW"
    elif count <= config["medium"]:
        return "MEDIUM"
    else:
        return "HIGH"
