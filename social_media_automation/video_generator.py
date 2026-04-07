import os
import time
import requests
import logging
from config import NANO_BANANA_API_KEY, NANO_BANANA_URL

def generate_background_video(prompt: str, output_path: str = "background.mp4") -> str:
    """
    Calls the Nano Banana API to generate a video based on the Gemini prompt.
    Returns the path to the downloaded video file.
    """
    if not NANO_BANANA_API_KEY:
        logging.warning("NANO_BANANA_API_KEY not found. Skipping video generation.")
        return ""
    
    headers = {
        "Authorization": f"Bearer {NANO_BANANA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Send the generation request
    payload = {
        "prompt": prompt,
        "resolution": "1080x1920", # Vertical video format
        "duration": 30 # Up to 30 second background to cover typical short text
    }
    
    logging.info(f"Requesting Nano Banana Video for prompt: {prompt[:40]}...")
    try:
        response = requests.post(NANO_BANANA_URL, json=payload, headers=headers)
        response.raise_for_status()
        
        task_id = response.json().get("task_id")
        if not task_id:
            logging.error("No task ID returned from Nano Banana.")
            return ""
            
        logging.info(f"Video generation active. Task ID: {task_id}")
        
        # Poll the server until completion
        status_url = f"{NANO_BANANA_URL}/{task_id}/status"
        video_url = ""
        while True:
            status_resp = requests.get(status_url, headers=headers)
            status_data = status_resp.json()
            status = status_data.get("status")
            
            if status == "completed":
                video_url = status_data.get("output_url")
                break
            elif status == "failed":
                logging.error("Nano Banana generation failed remotely.")
                return ""
                
            logging.info("Waiting 10s for rendering...")
            time.sleep(10)
            
        # Download the resultant file
        logging.info("Rendering complete. Downloading video stream...")
        vid_resp = requests.get(video_url, stream=True)
        with open(output_path, "wb") as f:
            for chunk in vid_resp.iter_content(chunk_size=8192):
                f.write(chunk)
                
        logging.info(f"Background saved to {output_path}")
        return output_path

    except Exception as e:
        logging.error(f"Nano Banana API error: {e}")
        return ""

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Testing Nano Banana module skeleton...")
