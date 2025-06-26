import yt_dlp
import uuid
import os

def download_instagram_reel(url: str) -> str | None:
    output_path = f"instagram_{uuid.uuid4().hex}.mp4"
    ydl_opts = {
        'outtmpl': output_path,
        'format': 'mp4',
        'quiet': True,
        'noplaylist': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return output_path if os.path.exists(output_path) else None
    except Exception as e:
        print(f"Ошибка скачивания видео из Instagram: {e}")
        return None