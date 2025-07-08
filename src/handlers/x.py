import os
from aiogram import types
from aiogram.types.input_file import FSInputFile
from services.x_downloader import download_x_video

def validate_x_url(url: str) -> bool:
    return (
        url.startswith(("https://twitter.com/", "https://x.com/"))
    )

async def handle_x_download(message: types.Message):
    url = message.text.strip()
    if validate_x_url(url):
        await message.answer("Скачиваю видео из X...")
        video_path = download_x_video(url)
        if video_path:
            input_file = FSInputFile(video_path)
            await message.answer_video(video=input_file)
            os.remove(video_path)
        else:
            await message.answer("Не могу скачать видео. Попробуй ещё раз.")