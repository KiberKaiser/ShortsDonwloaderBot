import yt_dlp
import uuid
import os

def download_youtube_short(url: str, output_path: str = None) -> str | None:
    if not output_path:
        output_path = f"youtube_{uuid.uuid4().hex}.%(ext)s"
    
    ydl_opts = {
        'outtmpl': output_path,
        'format': 'best[height<=720][ext=mp4]/best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
        'extract_flat': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            final_filename = ydl.prepare_filename(info)
            ydl.download([url])
            
            return final_filename if os.path.exists(final_filename) else None
    except Exception as e:
        print(f"Ошибка скачивания видео из YouTube Shorts: {e}")
        return None

def download_youtube_short_audio(url: str) -> str | None:
    output_path = "youtube_audio"
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
        print(f"Ошибка скачивания аудио из Youtube: {e}")
        return None