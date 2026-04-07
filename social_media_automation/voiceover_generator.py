import os
import logging
from google.cloud import texttospeech

def generate_voiceover(text: str, output_path: str = "voiceover.mp3") -> str:
    """
    Synthesizes speech from the given text using Google Cloud TTS.
    Returns the path to the generated audio file.
    """
    logging.info("Initializing Google Cloud TTS Client...")
    try:
        client = texttospeech.TextToSpeechClient()

        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Build the voice request, select the language code and the ssml voice gender
        # Using a Journey voice for energetic delivery (often high quality in GCP)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Journey-D" # Typically an energetic male voice
        )

        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=1.1, # Slightly sped up for short-form video style
            pitch=2.0      # Slightly higher pitch adds energy
        )

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # The response's audio_content is binary.
        with open(output_path, "wb") as out:
            out.write(response.audio_content)
            logging.info(f"Audio content written to file '{output_path}'")
        
        return output_path
    
    except Exception as e:
        logging.error(f"Failed to generate voiceover: {e}")
        return ""

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Testing TTS generation block...")
