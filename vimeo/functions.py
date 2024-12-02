from yt_dlp import YoutubeDL

def download_vimeo_video(url, output_path):
    """
    Downloads a video from Vimeo using yt-dlp.
    """
    opts = {
        'format': 'bestvideo+bestaudio/best',  
        'outtmpl': output_path,  
        'postprocessors': [{ 
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',  
        }],
        'merge_output_format': 'mp4',  
    }

    with YoutubeDL(opts) as ydl:
        ydl.download([url])

    print(f"Vimeo video downloaded successfully to {output_path}")
