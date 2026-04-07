import os
import logging
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
from moviepy.video.fx.all import loop

def assemble_video(
    background_video_path: str, 
    audio_path: str, 
    words_info: list, 
    output_path: str = "final_output.mp4"
) -> str:
    """
    Assembles the final video by combining the background video, 
    voiceover audio, and dynamic text overlays.
    """
    if not os.path.exists(background_video_path) or not os.path.exists(audio_path):
        logging.error("Missing input files for video assembly.")
        return ""
        
    logging.info("Initializing Video Assembly...")
    try:
        # Load clips
        bg_clip = VideoFileClip(background_video_path)
        audio_clip = AudioFileClip(audio_path)
        
        # Ensure video is at least as long as audio, or loop it
        if bg_clip.duration < audio_clip.duration:
            logging.info("Background video is shorter than audio. Looping video...")
            bg_clip = loop(bg_clip, duration=audio_clip.duration)
        else:
            bg_clip = bg_clip.subclip(0, audio_clip.duration)

        # Set the audio of the background to the TTS audio
        video_with_audio = bg_clip.set_audio(audio_clip)

        # Generate subtitle clips
        subtitle_clips = []
        for word_info in words_info:
            word = word_info['word']
            start = word_info['start']
            end = word_info['end']
            
            # Create a TextClip for the word
            # Note: Requires ImageMagick installed on the system to use TextClip
            try:
                txt_clip = TextClip(
                    word, 
                    fontsize=80, 
                    color='white', 
                    font='Arial-Bold',
                    stroke_color='black',
                    stroke_width=3,
                    method='caption',
                    align='center',
                    size=(900, None)
                )
                
                # Set the position (center of the screen) and duration
                txt_clip = txt_clip.set_position(('center', 'center')).set_start(start).set_end(end)
                subtitle_clips.append(txt_clip)
            except Exception as e:
                logging.error(f"Failed to generate TextClip for word '{word}'. Is ImageMagick installed? Error: {e}")

        # Overlay subtitles onto the video
        logging.info("Overlaying dynamic subtitles...")
        final_video = CompositeVideoClip([video_with_audio] + subtitle_clips)

        # Render the final result
        logging.info(f"Rendering final video to {output_path}...")
        final_video.write_videofile(
            output_path, 
            fps=30, 
            codec="libx264", 
            audio_codec="aac",
            preset="ultrafast",     # Faster render for local automation scripts
            threads=4
        )
        
        # Cleanup memory
        bg_clip.close()
        audio_clip.close()
        final_video.close()
        
        logging.info("Video assembly complete.")
        return output_path

    except Exception as e:
        logging.error(f"Failed to assemble video: {e}")
        return ""

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Testing Video Assembler block...")
