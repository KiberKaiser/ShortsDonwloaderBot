import os
from aiogram import types
from aiogram.types.input_file import FSInputFile
from services.tiktok_downloader import download_tiktok_video

def validate_tiktok_url(url: str) -> bool:
    return (
        url.startswith("https://www.tiktok.com/") or
        url.startswith("https://vm.tiktok.com/") or
        url.startswith("https://vt.tiktok.com/")
    )

async def handle_tiktok_download(message: types.Message):
    url = message.text.strip()
    if validate_tiktok_url(url):
        await message.answer("Скачиваю видео из TikTok...")
        video_path = download_tiktok_video(url)
        if video_path:
            input_file = FSInputFile(video_path)
            await message.answer_video(video=input_file)
            os.remove(video_path)
        else:
            await message.answer("Не могу скачать видео. Попробуй ещё раз.")
