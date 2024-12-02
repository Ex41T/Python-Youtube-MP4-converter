import os
from yt_dlp import YoutubeDL
import subprocess
from converter import h264format_conv

def download_tiktok_video(url, output_path):
    """
    Downloads a TikTok video using yt-dlp without watermark
    and converts it to H.264 (MP4) format using FFmpeg.
    If conversion succeeds, the encoded file is deleted.
    """
    

    opts = {
        'format': 'mp4',  
        'outtmpl': output_path,  
    }

    try:
        # Step 1: Download the video using yt-dlp
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            print(f"Video downloaded successfully: {file_path}")
        
        # Step 2: Convert to H.264 format 
        converted_file = h264format_conv(file_path)

        # Step 3: Remove original file if conversion succeeded
        if converted_file:
            os.remove(file_path)
            print(f"Original file removed: {file_path}")

        return converted_file or file_path

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
