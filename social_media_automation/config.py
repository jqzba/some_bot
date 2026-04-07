import os
from dotenv import load_dotenv

load_dotenv()

# Google Services
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") # Gemini API Key
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS") # GCP Service Account

# Nano Banana 
NANO_BANANA_API_KEY = os.getenv("NANO_BANANA_API_KEY")
NANO_BANANA_URL = "https://api.nano-banana.ai/v1/video/generate" # Hypothetical endpoint based on research

# Social APIs (YouTube, Instagram, TikTok)
YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID")
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
