from llm import analyze_alert

alert = {
    "attack_type": "Brute Force",
    "severity": "High",
    "risk_score": 85
}

result = analyze_alert(alert)

print(result)
