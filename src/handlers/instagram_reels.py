import os
from aiogram import types
from aiogram.types.input_file import FSInputFile
from services.instagram_downloader import download_instagram_reel

def validate_instagram_reels_url(url: str) -> bool:
    return (
        url.startswith("https://www.instagram.com/reel/") or
        url.startswith("https://instagram.com/reel/")
    )

async def handle_instagram_reels_download(message: types.Message):
    url = message.text.strip()
    if validate_instagram_reels_url(url):
        await message.answer("Скачиваю видео из Instagram...")
        video_path = download_instagram_reel(url)
        if video_path:
            input_file = FSInputFile(video_path)
            await message.answer_video(video=input_file)
            os.remove(video_path)
        else:
            await message.answer("Не могу скачать видео. Попробуй ещё раз.")