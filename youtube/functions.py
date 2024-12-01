from yt_dlp import YoutubeDL

def download_youtube_video(url):
    """
    Downloads the best quality video with audio as MP4.
    """
    opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        'outtmpl': './%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
    }
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url)
        file_path = ydl.prepare_filename(info)
        fps = info.get('fps', None)
        return file_path, fps