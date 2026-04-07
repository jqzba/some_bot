import google.generativeai as genai
import json
import logging
from config import GOOGLE_API_KEY

# Configure the API if the key is available
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
else:
    logging.warning("GOOGLE_API_KEY not found in environment.")

# Utilizing Gemini 1.5 Flash for rapid and cost-effective generation
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_video_script(topic: str) -> dict:
    """
    Generates a highly engaging short-form video script and visual prompt using Gemini.
    """
    prompt = f"""
    Create a highly engaging, 15-30 second short-form vertical video script about: {topic}
    You are an expert social media manager. The output must be valid JSON matching this schema:
    {{
        "title": "A catchy, viral-style title",
        "visual_prompt": "A highly detailed, visually striking description for a generative text-to-video AI (Nano Banana Video) to create the background (e.g., 'Cinematic 4k tracking shot of a glowing futuristic city'). Keep it to one scene.",
        "voiceover_script": "The exact words spoken by the TTS engine. Keep it punchy, enthusiastic, and under 60 words."
    }}
    """
    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json",
            )
        )
        return json.loads(response.text)
    except Exception as e:
        logging.error(f"Failed to generate script from Gemini: {e}")
        return {}

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Testing template generation...")
    # Cannot hit live without an API key, so we just run syntax checking basically.
