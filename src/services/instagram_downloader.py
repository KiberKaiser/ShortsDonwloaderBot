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

def download_instagram_reel_audio(url: str) -> str | None:
    output_path = "instagram_audio"
    ydl_opts = {
        'outtmpl': output_path,
        'format': 'bestaudio[ext=m4a]/bestaudio/best[ext=m4a]/best',
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            final_filename = ydl.prepare_filename(info)
            
            ydl.download([url])
            
            return final_filename if os.path.exists(final_filename) else None
    except Exception as e:
        print(f"Ошибка скачивания аудио из Instagram: {e}")
        return None