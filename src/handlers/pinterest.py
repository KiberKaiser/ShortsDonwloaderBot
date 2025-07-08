import os
from aiogram import types
from aiogram.types.input_file import FSInputFile
from services.pinterest_downloader import download_pinterest_video

def validate_pinterest_url(url: str) -> bool:
   return url.startswith("https://www.pinterest.com/") or url.startswith("https://pin.it/")

async def handle_pinterest_download(message: types.Message):
    url = message.text.strip()
    if validate_pinterest_url(url):
        await message.answer("Скачиваю видео из Pinterest...")
        video_path = download_pinterest_video(url)
        if video_path:
            input_file = FSInputFile(video_path)
            await message.answer_video(video=input_file)
            os.remove(video_path)
        else:
            await message.answer("Не могу скачать видео. Попробуй ещё раз.")
