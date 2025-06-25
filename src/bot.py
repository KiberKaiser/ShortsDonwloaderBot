import os 
import aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio

from handlers.tiktok import handle_tiktok_download, validate_tiktok_url
from handlers.youtube_shorts import handle_youtube_short_download, validate_youtube_short_url
from handlers.instagram_reels import handle_instagram_reel_download, validate_instagram_url

TOKEN = ""  

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.answer("Welcome to the Video Downloader Bot! Send me a TikTok, YouTube Shorts, or Instagram Reels link.")

@dp.message()
async def universal_handler(message: types.Message):
    url = message.text.strip()
    if validate_tiktok_url(url):
        await handle_tiktok_download(message)
    elif validate_youtube_short_url(url):
        await handle_youtube_short_download(message)
    elif validate_instagram_url(url):
        await handle_instagram_reel_download(message)
    else:
        await message.answer("Please send a valid TikTok, YouTube Shorts, or Instagram Reels link.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())