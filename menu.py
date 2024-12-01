import os
import shutil
import time
from tiktok.functions import download_tiktok_video
from youtube.functions import download_youtube_video
from converter import conv60fps  # Import funkcji konwersji 60 FPS dla YouTube
from converter import h264format_conv  # Import funkcji konwersji H.264 dla TikTok
from yt_dlp import YoutubeDL

def check_ffmpeg():
    """
    Checks if FFmpeg is installed and accessible from the command line.
    """
    if shutil.which("ffmpeg") is None:
        print("Error: FFmpeg is not installed or not added to the PATH.")
        print("Please install FFmpeg and ensure it is accessible from the command line.")
        time.sleep(5)
        exit(1)  # Exit the program

if __name__ == "__main__":
    # Check if FFmpeg is installed before running the script
    check_ffmpeg()

    while True:
        print("\nMenu:")
        print("1. Download YouTube video")
        print("2. Download TikTok video")
        print("3. Exit")
        
        choice = input("Enter your choice (1/2/3): ").strip()
        
        if choice == "1":
            url = input("Enter YouTube URL: ").strip()
            file_path, fps = download_youtube_video(url)
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
        elif choice == "2":
            url = input("Enter TikTok URL: ").strip()
            final_file = download_tiktok_video(url)
            if final_file:
                print(f"Final video file is ready: {final_file}")
            else:
                print("Failed to process the video.")
        elif choice == "3":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")
