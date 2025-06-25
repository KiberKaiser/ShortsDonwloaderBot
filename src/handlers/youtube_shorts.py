from aiogram import types
from services.youtube_downloader import download_youtube_short

async def handle_youtube_short_download(message: types.Message):
    url = message.text.strip()
    
    if validate_youtube_short_url(url):
        await message.answer("Downloading your YouTube Short...")
        video_path = await download_youtube_short(url)
        
        if video_path:
            await message.answer_video(video=open(video_path, 'rb'))
        else:
            await message.answer("Failed to download the video. Please try again.")
    else:
        await message.answer("Invalid YouTube Short URL. Please provide a valid link.")

def validate_youtube_short_url(url: str) -> bool:
    return "youtube.com/shorts/" in url or "youtu.be/" in url