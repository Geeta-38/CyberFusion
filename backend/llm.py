import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def analyze_alert(alert):

    prompt = f"""
    Analyze this cybersecurity alert:

    Attack Type: {alert['attack_type']}
    Severity: {alert['severity']}
    Risk Score: {alert['risk_score']}

    Provide:
    1. Threat description
    2. Potential impact
    3. Recommended mitigation
    """

    response = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=prompt
    )

    return response.text
