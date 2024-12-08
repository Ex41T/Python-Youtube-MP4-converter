from yt_dlp import YoutubeDL

def download_facebook_reels(url, output_path):
    """
    Downloads a Facebook reel video using yt-dlp.
    """
    opts = {
        'format': 'mp4',
        'outtmpl': output_path,
    }

    try:
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            print(f"Facebook reel downloaded successfully: {file_path}")
            return file_path
    except Exception as e:
        print(f"Error downloading Facebook reel: {e}")
        return None
