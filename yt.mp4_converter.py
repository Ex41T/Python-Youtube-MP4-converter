import os
from yt_dlp import YoutubeDL
import subprocess


defdownload_func(url):


    
    """
    Downloads the best available quality video with audio from the provided YouTube URL.
    Ensures the file is saved as an MP4 in the current directory.
    The frame rate (FPS) is also retrieved if available.
    """


    
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',  
        'outtmpl': './%(title)s.%(ext)s',  
        'merge_output_format': 'mp4',  
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url)
            file_name = ydl.prepare_filename(info_dict)
            fps = info_dict.get('fps', None)  
            print(f"\nDownloaded file: {file_name}")
            print(f"Frame rate (FPS): {fps or 'Unknown'}")
            return file_name, fps
    except Exception as e:
        print(f"Error during download: {e}")
        return None, None


def convert_fps(file_path):

    """
    
    Converts a given video file to 60 frames per second (FPS) using FFmpeg. (optional)
    
    """



    try:
        if not os.path.exists(file_path):
            print(f"The file {file_path} does not exist!")
            return None

        print("Converting video to 60 FPS using FFmpeg...")
        output_file = f"60fps_{os.path.basename(file_path)}"

        command = [
            "ffmpeg", "-i", file_path, "-filter:v", "fps=fps=60", "-c:a", "copy", output_file
        ]
        subprocess.run(command, check=True)
        print(f"File saved as: {output_file}")
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"Error during 60 FPS conversion: {e}")
        return None
    except FileNotFoundError:
        print("FFmpeg not found. Ensure it is installed and available in the system PATH.")
        return None




if __name__ == "__main__":


    """
    Handles user input to download a YouTube video and ensures the best quality.
    If the video is below 60 FPS, it gives an option to convert it to 60 FPS.
    """

    url = input("Enter the YouTube video URL: ")
    downloaded_file, fps = download_func(url)

    if downloaded_file:
        if fps and fps >= 60:
            print("\nThe video already has 60 FPS. No conversion needed.")
        else:
            convert_choice = input("\nThe video does not have 60 FPS. Would you like to convert it to 60 FPS? (y/n): ").strip().lower()
            if convert_choice == 'y':
                converted_file = convert_fps(downloaded_file)
                if converted_file:
                    print(f"\nDone! The file has been saved as: {converted_file}")
            else:
                print("\nProcess completed without conversion.")
