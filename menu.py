import os
import shutil
import time
from tiktok.functions import download_tiktok_video
from youtube.functions import download_youtube_video
from vimeo.functions import download_vimeo_video  # Funkcja do pobierania z Vimeo
from converter import conv60fps  # Import funkcji konwersji 60 FPS dla YouTube
from converter import h264format_conv  # Import funkcji konwersji H.264 dla TikTok
from yt_dlp import YoutubeDL
import re

def check_ffmpeg():
    """
    Checks if FFmpeg is installed and accessible from the command line.
    """
    if shutil.which("ffmpeg") is None:
        print("Error: FFmpeg is not installed or not added to the PATH.")
        print("Please install FFmpeg and ensure it is accessible from the command line.")
        time.sleep(5)
        exit(1)  # Exit the program

def detect_platform(url):
    """
    Detects the platform (YouTube, TikTok, or Vimeo) based on the URL.
    """
    if "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    elif "tiktok.com" in url:
        return "tiktok"
    elif "vimeo" in url:
        return "vimeo"
    else:
        return None  

def download_video(url):
    """
    Downloads a video based on the platform detected from the URL.
    """
    platform = detect_platform(url)
    
    
    output_path = './videos/%(title)s.%(ext)s'  

    if platform == "youtube":
        file_path, fps = download_youtube_video(url, output_path)
        if file_path:
            if fps and fps >= 60:
                print("Video is already 60 FPS. No conversion needed.")
            else:
                if input("Convert to 60 FPS? (y/n): ").strip().lower() == 'y':
                    converted = conv60fps(file_path)
                    if converted:
                        print(f"Saved as: {converted}")
                else:
                    print("Conversion skipped.")
        return file_path
    
    elif platform == "tiktok":
        final_file = download_tiktok_video(url, output_path)
        if final_file:
            print(f"Final video file is ready: {final_file}")
        else:
            print("Failed to process the video.")
        return final_file
    
    elif platform == "vimeo":
        final_file = download_vimeo_video(url, output_path) 
        if final_file:
            print(f"Final video file from Vimeo is ready: {final_file}")
        else:
            print("Failed to process the video.")
        return final_file
    
    else:
        print("Unsupported platform. Please provide a valid YouTube, TikTok, or Vimeo link.")
        return None

if __name__ == "__main__":
    
    check_ffmpeg()

    while True:
        url = input("\nEnter video URL (or type 'exit' to quit): ").strip()

        if url.lower() == 'exit':
            print("Exiting program. Goodbye!")
            break

        download_video(url)  
