import google.generativeai as genai
from PIL import Image
import io
import os
import logging
from typing import Final

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY: Final = os.getenv('GENAI_API_KEY')

"""Generates a response to the given question using the Gemini model."""
def generateResponse(question):
    logger.debug("start : generateResponse function.")
    # Set your API key
    genai.configure(api_key=f"{API_KEY}")
    # Initialize the model
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(question)
    return response.candidates[0].content.parts[0].text[0:500]

"""Analyzes the given file using the Gemini model."""
def analyse_file(filepath):
    logger.debug(f"start: analyse_file {filepath}")
    # Set your API key
    genai.configure(api_key=f"{API_KEY}")
    # Initialize the model

    model = genai.GenerativeModel("gemini-1.5-flash")
    
    image = Image.open(filepath).convert("RGB")
    response = model.generate_content(["Tell me about this image", image])
    
    return response.text
    
