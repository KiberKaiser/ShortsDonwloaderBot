import yt_dlp
import uuid
import os
import subprocess
import shutil


def get_ffmpeg_path():
    if shutil.which('ffmpeg'):
        return 'ffmpeg'
    
    windows_paths = [
        r'D:\ffmpeg\bin\ffmpeg.exe',  
        r'C:\ffmpeg\bin\ffmpeg.exe',
        r'C:\Program Files\ffmpeg\bin\ffmpeg.exe',
        r'.\ffmpeg\bin\ffmpeg.exe',
        r'ffmpeg\bin\ffmpeg.exe'
    ]
    
    for path in windows_paths:
        if os.path.exists(path):
            return path
        
    linux_paths = [
        '/usr/bin/ffmpeg',
        '/usr/local/bin/ffmpeg',
        '/opt/ffmpeg/bin/ffmpeg'
    ]
    
    for path in linux_paths:
        if os.path.exists(path):
            return path
    
    return 'ffmpeg'  


def download_pinterest_video(url: str, output_path: str = None) -> str | None:
    if not output_path:
        output_path = f"pinterest_{uuid.uuid4().hex}.mp4"  

    ydl_opts = {
        'outtmpl': output_path,
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
        'format': 'bestvideo+bestaudio/best',  
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            ydl.download([url])
            final_filename = ydl.prepare_filename(info).rsplit('.', 1)[0] + ".mp4"
            
            if os.path.exists(final_filename):
                print(f"Видео с аудио сохранено: {final_filename}")
                return final_filename

    except Exception as e:
        print(f"Ошибка при загрузке: {e}")

    return None


def download_pinterest_audio(url: str) -> str | None:
    output_path = f"pinterest_audio_{uuid.uuid4().hex}.%(ext)s"
    
    formats = [
        'bestaudio[ext=m4a]',
        'bestaudio[ext=mp3]',
        'bestaudio',
        'best[ext=m4a]',
        'best[acodec!=none]', 
        'best'
    ]
    
    for fmt in formats:
        ydl_opts = {
            'outtmpl': output_path,
            'format': fmt,
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                final_filename = ydl.prepare_filename(info)
                ydl.download([url])
                
                if os.path.exists(final_filename):
                    return final_filename
                    
        except Exception as e:
            print(f"Аудио формат {fmt} не сработал: {e}")
            continue
    
    return None


def merge_audio_video(video_path: str, audio_path: str, output_path: str = None) -> str | None:

    if not output_path:
        output_path = f"pinterest_merged_{uuid.uuid4().hex}.mp4"
    
    if not os.path.exists(video_path):
        print(f"Видео файл не найден: {video_path}")
        return None
        
    if not os.path.exists(audio_path):
        print(f"Аудио файл не найден: {audio_path}")
        return None
    
    try:
        ffmpeg_path = get_ffmpeg_path()
        cmd = [
            ffmpeg_path,
            '-i', video_path,  
            '-i', audio_path,  
            '-c:v', 'copy',    
            '-c:a', 'aac',     
            '-strict', 'experimental',
            '-y',              
            output_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            if os.path.exists(output_path):
                print(f"Аудио и видео успешно объединены: {output_path}")
                try:
                    os.remove(video_path)
                    os.remove(audio_path)
                    print("Временные файлы удалены")
                except Exception as e:
                    print(f"Не удалось удалить временные файлы: {e}")
                
                return output_path
        else:
            print(f"Ошибка FFmpeg: {result.stderr}")
            
    except FileNotFoundError:
        print("FFmpeg не найден. Убедитесь, что FFmpeg установлен и добавлен в PATH")
    except Exception as e:
        print(f"Ошибка при объединении файлов: {e}")
    
    return None


def download_pinterest_separate_and_merge(url: str, output_path: str = None) -> str | None:

    if not output_path:
        output_path = f"pinterest_final_{uuid.uuid4().hex}.mp4"
    

    video_path = download_pinterest_video_only(url)
    if not video_path:
        print("Не удалось скачать видео")
        return None
    
    audio_path = download_pinterest_audio(url)
    if not audio_path:
        print("Не удалось скачать аудио")
        if os.path.exists(video_path):
            os.remove(video_path)
        return None
    
    return merge_audio_video(video_path, audio_path, output_path)


def download_pinterest_video_only(url: str, output_path: str = None) -> str | None:
 
    if not output_path:
        output_path = f"pinterest_video_{uuid.uuid4().hex}.%(ext)s"

    ydl_opts = {
        'outtmpl': output_path,
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
        'format': 'bestvideo[ext=mp4]',  
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            final_filename = ydl.prepare_filename(info)
            ydl.download([url])
            
            if os.path.exists(final_filename):
                print(f"Видео без аудио сохранено: {final_filename}")
                return final_filename

    except Exception as e:
        print(f"Ошибка при загрузке видео: {e}")

    return None