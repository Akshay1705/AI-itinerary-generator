# theme/gemini_service.py
import os
import re
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def clean_text(text: str) -> str:
    return re.sub(r'[*#_`]+', '', text).strip()

def generate_itinerary_with_gemini(destination, days, budget, interests):
    prompt = f"""
Generate a clear and structured travel itinerary.

Destination: {destination}
Duration: {days} days
Budget: {budget}
Interests: {interests}

Rules:
- Plain text only
- No markdown
- Each day must start with "Day X:"
- Keep output concise and practical
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return clean_text(response.text)
