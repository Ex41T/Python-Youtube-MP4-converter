import shutil

def check_ffmpeg():
    """
    Checks if FFmpeg is installed and accessible from the command line.
    """
    if shutil.which("ffmpeg") is None:
        raise EnvironmentError("FFmpeg is not installed or not added to the PATH.")
