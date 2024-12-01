import os
import subprocess

def h264format_conv(file_path):
    """
    Converts a TikTok video to H.264 (MP4) format using FFmpeg.
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




def conv60fps(file_path):
    """
    Converts a YouTube video to 60 FPS using FFmpeg.
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None

    output_file = f"converted {os.path.basename(file_path)}"
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
