import os
import google.generativeai as genai
from dotenv import load_dotenv
import re

load_dotenv()  # load .env file

# Configure Gemini with your API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def clean_text(text):
    # Remove Markdown symbols (*, #, etc.)
    return re.sub(r'[*#_`]+', '', text).strip()

def generate_itinerary_with_gemini(destination, days, budget, interests):
    prompt = f"""
    Generate a clear and structured travel itinerary for {destination}.
    Trip duration: {days} days.
    Budget: {budget}.
    Interests: {interests}.

    Formatting Rules:
    - Do NOT use *, #, or markdown styling.
    - Only plain text with numbered days.
    - Each day should start with "Day X:" followed by activities.
    - Keep sentences concise and easy to read.
    """

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    if response.candidates:
        return clean_text(response.candidates[0].content.parts[0].text)
    else:
        return "No response from Gemini"
