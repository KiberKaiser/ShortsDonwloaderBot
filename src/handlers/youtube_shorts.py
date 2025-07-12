import os
import uuid
from aiogram import types
from aiogram.types.input_file import FSInputFile
from services.youtube_downloader import download_youtube_short

def validate_youtube_shorts_url(url: str) -> bool:
    return (
        url.startswith("https://youtube.com/shorts/") or
        url.startswith("https://www.youtube.com/shorts/") or
        url.startswith("https://m.youtube.com/shorts/") or
        url.startswith("https://youtu.be/")
    )

async def handle_youtube_shorts_download(message: types.Message):
    url = message.text.strip()
    if validate_youtube_shorts_url(url):
        await message.answer("Скачиваю видео из Youtube Shorts..")
        video_path = f"youtube_{uuid.uuid4().hex}.mp4"
        result_path = download_youtube_short(url, video_path)
        if result_path and os.path.getsize(result_path) > 0:
            input_file = FSInputFile(result_path)
            await message.answer_video(video=input_file)
            os.remove(result_path)
        else:
            await message.answer("Не могу скачать видео. Попробуй ещё раз.")
            if result_path and os.path.exists(result_path):
                os.remove(result_path)
    else:
        await message.answer("Invalid YouTube Shorts URL. Please send a valid link.")
