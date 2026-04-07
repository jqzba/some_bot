import logging
import os
from config import *

# Module Imports
from script_generator import generate_video_script
from voiceover_generator import generate_voiceover
from video_generator import generate_background_video
from subtitle_generator import generate_subtitle_timings
from video_assembler import assemble_video
from publisher import publish_video

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_automation_pipeline(topic: str = "3 reasons why AI is changing software development"):
    """
    Executes the fully automated end-to-end video pipeline.
    """
    logging.info(f"Starting Social Media Video Automation Pipeline for topic: '{topic}'")
    
    # 1. Generate Script (Gemini)
    logging.info("=== Step 1: Generating Script ===")
    script_data = generate_video_script(topic)
    if not script_data:
        logging.error("Pipeline blocked: Failed to generate script.")
        return
        
    title = script_data.get('title', 'Unknown Title')
    visual_prompt = script_data.get('visual_prompt', '')
    voiceover_text = script_data.get('voiceover_script', '')
    
    # 2. Generate Voiceover (Google Cloud TTS)
    logging.info("=== Step 2: Generating Voiceover ===")
    audio_path = "temp_voiceover.mp3"
    audio_path = generate_voiceover(voiceover_text, audio_path)
    if not audio_path:
        logging.error("Pipeline blocked: Failed to generate audio.")
        return
    
    # 3. Generate Background Visuals (Nano Banana Video API)
    logging.info("=== Step 3: Generating Visuals (Nano Banana) ===")
    bg_video_path = "temp_background.mp4"
    bg_video_path = generate_background_video(visual_prompt, bg_video_path)
    if not bg_video_path:
        logging.warning("Visuals generation skipped or failed. Fallback needed to proceed.")
        return
    
    # 4. Generate Subtitles (Google Cloud Speech-to-Text)
    logging.info("=== Step 4: Extracting Subtitle Timings ===")
    words_info = generate_subtitle_timings(audio_path)
    if not words_info:
        logging.warning("No words extracted. Subtitles will be empty.")
    
    # 5. Assemble Video (MoviePy)
    logging.info("=== Step 5: Assembling Video ===")
    final_output_path = "final_output.mp4"
    final_output_path = assemble_video(bg_video_path, audio_path, words_info, final_output_path)
    if not final_output_path:
        logging.error("Pipeline blocked: Video assembly failed.")
        return
    
    # 6. Publish
    logging.info("=== Step 6: Publishing to Social Media ===")
    # Add trending hashtags to description
    description = f"{title}\n\n#tech #automation #software #viral #foryou"
    publish_video(final_output_path, title, description)
    
    logging.info("=== Pipeline Complete! ===")
    
    # Cleanup temp files
    try:
        if os.path.exists(audio_path): os.remove(audio_path)
        if os.path.exists(bg_video_path): os.remove(bg_video_path)
    except Exception as e:
        logging.warning(f"Cleanup error: {e}")

if __name__ == "__main__":
    # Example execution trigger
    run_automation_pipeline()
