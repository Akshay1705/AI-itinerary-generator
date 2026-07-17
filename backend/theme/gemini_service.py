import os
import re
import logging
import requests

from dotenv import load_dotenv
from google import genai
from google.api_core import exceptions

load_dotenv()

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)


def clean_text(text):
    if not text:
        return ""

    return re.sub(r'[*#_`]+', '', text).strip()


def build_prompt(destination, days, budget, interests):

    return f"""
Generate a detailed travel itinerary.

Destination: {destination}
Duration: {days} days
Budget: {budget}
Interests: {interests}

Rules:
- Plain text only
- No markdown
- Start every section with Day X:
- Practical and realistic plans
- Include local experiences
- Match budget level
"""


def generate_with_openrouter(prompt):

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "Voyager AI"
    }

    payload = {
        "model": "meta-llama/llama-3.2-3b-instruct:free",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=60
    )

    print("STATUS:", response.status_code)
    print("BODY:", response.text)

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"]


def generate_itinerary_with_gemini(destination, days, budget, interests):

    prompt = build_prompt(
        destination,
        days,
        budget,
        interests
    )

    try:

        logger.info("Trying Gemini API...")

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return clean_text(response.text)

    except Exception as gemini_error:

        logger.warning(
            f"Gemini failed: {str(gemini_error)}"
        )

        error_text = str(gemini_error)

        if "429" in error_text or "503" in error_text:

            logger.info(
                "Switching to OpenRouter fallback..."
            )

            try:

                result = generate_with_openrouter(prompt)

                return clean_text(result)

            except Exception as openrouter_error:

                logger.error(
                    f"OpenRouter failed: {str(openrouter_error)}"
                )

                return (
                    "AI services are currently unavailable. "
                    "Please try again later."
                )

        raise