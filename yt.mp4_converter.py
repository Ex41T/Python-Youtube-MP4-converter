import os
from yt_dlp import YoutubeDL
import subprocess


def download_highest_quality(url):


    
    """
    Downloads the highest quality video available with audio.

    Args:
        url (str): The URL of the YouTube video.

    Returns:
        tuple: A tuple containing the file name of the downloaded video and its frame rate (FPS), 
               or (None, None) if the download fails.
    """



    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',  # Select best video+audio
        'outtmpl': './%(title)s.%(ext)s',  # Save in the current directory with the title as the filename
        'merge_output_format': 'mp4',  # Merge video and audio into MP4 format
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url)
            file_name = ydl.prepare_filename(info_dict)
            fps = info_dict.get('fps', None)  # Retrieve FPS if available
            print(f"\nDownloaded file: {file_name}")
            print(f"Frame rate (FPS): {fps or 'Unknown'}")
            return file_name, fps
    except Exception as e:
        print(f"Error during download: {e}")
        return None, None


def convert_to_60fps(file_path):

    """
    Converts a video file to 60 FPS using FFmpeg.

    Args:
        file_path (str): The path to the video file to be converted.

    Returns:
        str: The path to the converted video file, or None if the conversion fails.
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
    Main program logic:
    1. Prompt the user for a YouTube URL.
    2. Download the highest quality video with audio.
    3. If the video has less than 60 FPS, ask the user if they want to convert it to 60 FPS.
    """


    url = input("Enter the YouTube video URL: ")
    downloaded_file, fps = download_highest_quality(url)

    if downloaded_file:
        if fps and fps >= 60:
            print("\nThe video already has 60 FPS. No conversion needed.")
        else:
            convert_choice = input("\nThe video does not have 60 FPS. Would you like to convert it to 60 FPS? (y/n): ").strip().lower()
            if convert_choice == 'y':
                converted_file = convert_to_60fps(downloaded_file)
                if converted_file:
                    print(f"\nDone! The file has been saved as: {converted_file}")
            else:
                print("\nProcess completed without conversion.")
