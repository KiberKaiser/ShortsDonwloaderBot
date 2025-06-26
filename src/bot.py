import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery

from keyboard.inlineButtons import get_main_reply_keyboard
from handlers.tiktok import handle_tiktok_download, validate_tiktok_url
from handlers.youtube_shorts import handle_youtube_shorts_download, validate_youtube_shorts_url
from handlers.instagram_reels import handle_instagram_reels_download, validate_instagram_reels_url

TOKEN = ""  

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

user_platform = {}

@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.answer(
        "Салют! DownloaderShortsVideos - это бот для удобного скачивания видео из TikTok, Youtube Shorts, Instagram Reels\n\n" \
        "Чтобы скачать видео, выбери платформу, с которой ты хочешь скачать видео, и отправь ссылку на видео.\n" \
        "Нажми на кнопку ниже, чтобы начать.",
        reply_markup=get_main_reply_keyboard()
    )

PLATFORM_BUTTONS = {
    "TikTok": "tiktok",
    "YouTube Shorts": "youtube",
    "Instagram Reels": "instagram"
}

@dp.message(lambda message: message.text in PLATFORM_BUTTONS)
async def platform_chosen_text(message: types.Message):
    platform = PLATFORM_BUTTONS[message.text]
    user_platform[message.from_user.id] = platform
    await message.answer(f"Вы выбрали {message.text}. Отправь ссылку на видео.")

@dp.message()
async def universal_handler(message: types.Message):
    user_id = message.from_user.id
    url = message.text.strip()
    platform = user_platform.get(user_id)

    if not platform:
        await message.answer("Сначала выбери платформу:", reply_markup=get_main_reply_keyboard())
        return

    if platform == "tiktok" and validate_tiktok_url(url):
        await handle_tiktok_download(message)
    elif platform == "youtube" and validate_youtube_shorts_url(url):
        await handle_youtube_shorts_download(message)
    elif platform == "instagram" and validate_instagram_reels_url(url):
        await handle_instagram_reels_download(message)
    else:
        await message.answer("Пожалуйста, пришли корректную ссылку на видео.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())