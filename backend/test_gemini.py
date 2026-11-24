
import os

from dotenv import load_dotenv
from google import genai


# Load environment variables
load_dotenv()

# Get API key securely
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")


# Initialize Gemini client
client = genai.Client(api_key=api_key)


# Send a test prompt
response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="Explain how AI works in three simple sentences."
)


# Display Gemini response
print("\nGemini Response:")
print(response.text)

print("\nGemini API connection successful!")
