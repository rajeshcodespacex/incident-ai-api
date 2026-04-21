from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def get_ai_response(issue_description: str) -> dict:
    try:
        prompt = f"""You are an IT support expert for file transfer systems.

Incident: {issue_description}

Reply with:
1. Root Cause
2. Fix Steps
3. Severity: HIGH, MEDIUM, or LOW
4. Fix Time"""

        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=prompt
        )

        response_text = response.text
        severity = "MEDIUM"
        if "HIGH" in response_text.upper():
            severity = "HIGH"
        elif "LOW" in response_text.upper():
            severity = "LOW"

        return {
            "ai_response": response_text,
            "severity": severity
        }

    except Exception as e:
        return {
            "ai_response": f"AI service temporarily unavailable: {str(e)}",
            "severity": "MEDIUM"
        }