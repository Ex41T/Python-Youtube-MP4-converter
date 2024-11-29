import os
from yt_dlp import YoutubeDL
import subprocess

def download_youtube_video(url):
    """
    Downloads the best quality video with audio as MP4.
    Returns the file path and FPS if available.
    """
    opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        'outtmpl': './%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
    }
    try:
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url)
            file_path = ydl.prepare_filename(info)
            fps = info.get('fps', None)
            print(f"Downloaded: {file_path}")
            print(f"FPS: {fps or 'Unknown'}")
            return file_path, fps
    except Exception as e:
        print(f"Download error: {e}")
        return None, None

def convert_to_60fps(file_path):
    """
    Converts a video to 60 FPS using FFmpeg.
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None

    output_file = f"60fps_{os.path.basename(file_path)}"
    cmd = [
        "ffmpeg", "-i", file_path, "-filter:v", "fps=fps=60", "-c:a", "copy", output_file
    ]
    try:
        subprocess.run(cmd, check=True)
        print(f"Converted to 60 FPS: {output_file}")
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"Conversion error: {e}")
        return None
    except FileNotFoundError:
        print("FFmpeg not found. Ensure it is installed.")
        return None

def download_tiktok_video(url):
    """
    Downloads a TikTok video using yt-dlp (without watermark)
    and converts it to H.264 (MP4) format using FFmpeg.
    If conversion succeeds, the encoded file is deleted.
    """
    opts = {
        'format': 'mp4',  # save as mp4
        'outtmpl': './%(title)s.%(ext)s',  # Output filename
    }

    try:
        # Step 1: Download the video using yt-dlp
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            print(f"Video downloaded successfully: {file_path}")
        
        # Step 2: Convert to H.264 format if necessary
        converted_file = convert_to_h264(file_path)

        # Step 3: Remove original file if conversion succeeded
        if converted_file:
            os.remove(file_path)
            print(f"Original file removed: {file_path}")

        return converted_file or file_path

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def convert_to_h264(file_path):
    """
    Converts a video to H.264 (MP4) format using FFmpeg.
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None

    output_file = f"h264_{os.path.basename(file_path)}"
    cmd = [
        "ffmpeg", "-i", file_path, "-c:v", "libx264", "-c:a", "aac", "-strict", "experimental", output_file
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"Converted file saved as: {output_file}")
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg conversion error: {e}")
        return None
    except FileNotFoundError:
        print("FFmpeg not found. Please install FFmpeg and try again.")
        return None

if __name__ == "__main__":
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
                        converted = convert_to_60fps(file_path)
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
