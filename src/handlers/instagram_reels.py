import os
from aiogram import types
from services.instagram_downloader import download_instagram_reel

async def handle_instagram_reel_download(message: types.Message):
    url = message.text.strip()
    
    if validate_instagram_url(url):
        await message.answer("Downloading your Instagram Reel...")
        video_path = await download_instagram_reel(url)
        
        if video_path:
            await message.answer_video(video=open(video_path, 'rb'))
            os.remove(video_path)  
        else:
            await message.answer("Failed to download the video. Please try again.")
    else:
        await message.answer("Invalid Instagram URL. Please provide a valid link.")

def validate_instagram_url(url: str) -> bool:
    return url.startswith("https://www.instagram.com/reel/") or url.startswith("https://instagram.com/reel/")