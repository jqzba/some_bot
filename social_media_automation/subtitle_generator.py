import os
import io
import logging
from google.cloud import speech

def generate_subtitle_timings(audio_path: str) -> list:
    """
    Transcribes the audio file and extracts word-level timings using 
    Google Cloud Speech-to-Text API.
    Returns a list of dictionaries containing word text, start_time, and end_time.
    """
    if not os.path.exists(audio_path):
        logging.error(f"Audio file {audio_path} not found.")
        return []

    logging.info("Initializing Google Cloud Speech Client...")
    try:
        client = speech.SpeechClient()

        # Read the audio file
        with io.open(audio_path, "rb") as audio_file:
            content = audio_file.read()

        audio = speech.RecognitionAudio(content=content)

        # Configure the request to return word-level timestamps
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.MP3,
            sample_rate_hertz=24000,
            language_code="en-US",
            enable_word_time_offsets=True, # Critical for per-word dynamic captions
            model="video" # Optimized model for video narration type audio
        )

        logging.info("Sending audio configuration to Speech-to-Text API...")
        # Short videos under 1m can use standard recognize
        response = client.recognize(config=config, audio=audio)

        words_info = []
        for result in response.results:
            alternative = result.alternatives[0]
            for word_info in alternative.words:
                word = word_info.word
                start_time = word_info.start_time
                end_time = word_info.end_time
                
                # Convert protobuf Duration to seconds (float)
                start_sec = start_time.seconds + start_time.microseconds * 1e-6
                end_sec = end_time.seconds + end_time.microseconds * 1e-6
                
                words_info.append({
                    "word": word,
                    "start": start_sec,
                    "end": end_sec
                })

        logging.info(f"Extracted {len(words_info)} words with precise timings.")
        return words_info

    except Exception as e:
        logging.error(f"Failed to generate subtitle timings: {e}")
        return []

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Testing Speech-to-Text block...")
