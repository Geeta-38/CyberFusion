def calculate_risk(attack_type):

    scores = {
        "DDoS": 95,
        "Brute Force": 85,
        "Malware": 90,
        "Port Scan": 40,
        "Reconnaissance": 35,
        "Normal": 10
    }

    return scores.get(attack_type, 50)
