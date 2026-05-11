# theme/gemini_service.py
import os
import re
import logging
from dotenv import load_dotenv
from google import genai
from google.api_core import exceptions

load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Validate API key on startup
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    logger.error("GEMINI_API_KEY not found in environment variables")
    raise ValueError("GEMINI_API_KEY environment variable is required")

client = genai.Client(api_key=api_key)

def clean_text(text: str) -> str:
    """Remove markdown characters and strip whitespace."""
    if not text:
        return ""
    return re.sub(r'[*#_`]+', '', text).strip()

def generate_itinerary_with_gemini(destination, days, budget, interests):
    """
    Generate a travel itinerary using Gemini API.
    
    Args:
        destination (str): Travel destination
        days (int): Number of days for the trip
        budget (str): Budget for the trip (e.g., "Low", "Medium", "High")
        interests (str): Comma-separated interests (e.g., "hiking,food,culture")
    
    Returns:
        str: Generated itinerary text
        
    Raises:
        ValueError: If inputs are invalid
        Exception: If API call fails after retries
    """
    # Input validation
    if not destination or not isinstance(destination, str) or len(destination.strip()) == 0:
        raise ValueError("Destination must be a non-empty string")
    
    if not isinstance(days, (int, str)):
        raise ValueError("Days must be a number")
    try:
        days_int = int(days)
        if days_int <= 0 or days_int > 365:
            raise ValueError("Days must be between 1 and 365")
    except (ValueError, TypeError):
        raise ValueError("Days must be a valid positive number")
    
    if not budget or not isinstance(budget, str) or len(budget.strip()) == 0:
        raise ValueError("Budget must be a non-empty string")
    
    if not interests or not isinstance(interests, str) or len(interests.strip()) == 0:
        raise ValueError("Interests must be a non-empty string")
    
    # Sanitize inputs
    destination = destination.strip()
    budget = budget.strip()
    interests = interests.strip()
    
    prompt = f"""
Generate a clear and structured travel itinerary.

Destination: {destination}
Duration: {days_int} days
Budget: {budget}
Interests: {interests}

Rules:
- Plain text only
- No markdown
- Each day must start with "Day X:"
- Keep output concise and practical
"""
    
    try:
        logger.info(f"Generating itinerary for {destination} ({days_int} days)")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        # Validate response
        if not response or not hasattr(response, 'text'):
            logger.error("Invalid response from Gemini API")
            raise Exception("API returned an invalid response")
        
        if not response.text:
            logger.warning("Empty response from Gemini API")
            raise Exception("API returned empty content")
        
        cleaned = clean_text(response.text)
        logger.info("Itinerary generated successfully")
        return cleaned
    
    except exceptions.GoogleAPIError as e:
        logger.error(f"Gemini API error: {str(e)}")
        raise Exception(f"Failed to generate itinerary: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error generating itinerary: {str(e)}")
        raise
