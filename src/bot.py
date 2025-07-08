import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery
from aiogram.types.input_file import FSInputFile

from keyboard.inlineButtons import get_main_reply_keyboard, get_format_choice_keyboard
from handlers.tiktok import validate_tiktok_url
from handlers.youtube_shorts import validate_youtube_shorts_url
from handlers.instagram_reels import validate_instagram_reels_url
from handlers.pinterest import validate_pinterest_url
from handlers.x import validate_x_url

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set!")

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

user_platform = {}

@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.answer(
        "Салют! DownloaderShortsVideos - это бот для удобного скачивания видео из TikTok, Youtube Shorts, Instagram Reels, X(Twitter), Pinterest\n\n" \
        "Чтобы скачать видео, выбери платформу, с которой ты хочешь скачать видео, и отправь ссылку на видео.\n" \
        "Нажми на кнопку ниже, чтобы начать.",
        reply_markup=get_main_reply_keyboard()
    )

PLATFORM_BUTTONS = {
    "TikTok": "tiktok",
    "YouTube Shorts": "youtube",
    "Instagram Reels": "instagram",
    "Pinterest": "pinterest",
    "X (Twitter)": "x"
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
    
    is_valid = False
    if platform == "tiktok" and validate_tiktok_url(url):
        is_valid = True
    elif platform == "youtube" and validate_youtube_shorts_url(url):
        is_valid = True
    elif platform == "instagram" and validate_instagram_reels_url(url):
        is_valid = True
    elif platform == "pinterest" and validate_pinterest_url(url):
        is_valid = True
    elif platform == "x" and validate_x_url(url):
        is_valid = True
       
    if is_valid:
        await message.answer(
            "Выбери формат для скачивания:",
            reply_markup=get_format_choice_keyboard(url, platform)
        )
    else:
        await message.answer("Пожалуйста, пришли корректную ссылку на видео.")

@dp.callback_query(F.data.startswith(("video_", "audio_")))
async def handle_format_choice(callback: CallbackQuery):
    data_parts = callback.data.split("_", 2)
    format_type = data_parts[0]  
    platform = data_parts[1]     
    url = data_parts[2]          
    
    await callback.answer()
    
    if format_type == "video":
        if platform == "tiktok":
            await callback.message.answer("Скачиваю видео из TikTok...")
            from services.tiktok_downloader import download_tiktok_video
            video_path = download_tiktok_video(url)
            if video_path:
                input_file = FSInputFile(video_path)
                await callback.message.answer_video(video=input_file)
                os.remove(video_path)
            else:
                await callback.message.answer("Не могу скачать видео. Попробуй ещё раз.")
        
        elif platform == "youtube":
            await callback.message.answer("Скачиваю видео из Youtube Shorts...")
            from services.youtube_downloader import download_youtube_short
            import uuid
            video_path = f"youtube_{uuid.uuid4().hex}.mp4"
            result_path = download_youtube_short(url, video_path)
            if result_path and os.path.getsize(result_path) > 0:
                input_file = FSInputFile(result_path)
                await callback.message.answer_video(video=input_file)
                os.remove(result_path)
            else:
                await callback.message.answer("Не могу скачать видео. Попробуй ещё раз.")
                if result_path and os.path.exists(result_path):
                    os.remove(result_path)
        
        elif platform == "instagram":
            await callback.message.answer("Скачиваю видео из Instagram...")
            from services.instagram_downloader import download_instagram_reel
            video_path = download_instagram_reel(url)
            if video_path:
                input_file = FSInputFile(video_path)
                await callback.message.answer_video(video=input_file)
                os.remove(video_path)
            else:
                await callback.message.answer("Не могу скачать видео. Попробуй ещё раз.")

        elif platform == "pinterest":
            await callback.message.answer("Скачиваю видео из Pinterest...")
            from services.pinterest_downloader import download_pinterest_video
            video_path = download_pinterest_video(url)
            if video_path:
                input_file = FSInputFile(video_path)
                await callback.message.answer_video(video=input_file)
                os.remove(video_path)
            else:
                await callback.message.answer("Не могу скачать видео. Попробуй ещё раз.")

        elif platform == "x":
            await callback.message.answer("Скачиваю видео из X (Twitter)...")
            from services.x_downloader import download_x_video
            video_path = download_x_video(url)
            if video_path:
                input_file = FSInputFile(video_path)
                await callback.message.answer_video(video=input_file)
                os.remove(video_path)
            else:
                await callback.message.answer("Не могу скачать видео. Попробуй ещё раз.")
    
    elif format_type == "audio":
        if platform == "tiktok":
            await callback.message.answer("Скачиваю аудио из TikTok...")
            from services.tiktok_downloader import download_tiktok_audio
            audio_path = download_tiktok_audio(url)
            if audio_path:
                input_file = FSInputFile(audio_path)
                await callback.message.answer_audio(audio=input_file)
                os.remove(audio_path)
            else:
                await callback.message.answer("Не могу скачать аудио. Попробуй ещё раз.")
        
        elif platform == "youtube":
            await callback.message.answer("Скачиваю аудио из Youtube Shorts...")
            from services.youtube_downloader import download_youtube_short_audio
            audio_path = download_youtube_short_audio(url)
            if audio_path:
                input_file = FSInputFile(audio_path)
                await callback.message.answer_audio(audio=input_file)
                os.remove(audio_path)
            else:
                await callback.message.answer("Не могу скачать аудио. Попробуй ещё раз.")
        
        elif platform == "instagram":
            await callback.message.answer("Скачиваю аудио из Instagram...")
            from services.instagram_downloader import download_instagram_reel_audio
            audio_path = download_instagram_reel_audio(url)
            if audio_path:
                input_file = FSInputFile(audio_path)
                await callback.message.answer_audio(audio=input_file)
                os.remove(audio_path)
            else:
                await callback.message.answer("Не могу скачать аудио. Попробуй ещё раз.")

        elif platform == "pinterest":
            await callback.message.answer("Скачиваю аудио из Pinterest...")
            from services.pinterest_downloader import download_pinterest_audio
            audio_path = download_pinterest_audio(url)
            if audio_path:
                input_file = FSInputFile(audio_path)
                await callback.message.answer_audio(audio=input_file)
                os.remove(audio_path)
            else:
                await callback.message.answer("Не могу скачать аудио. Попробуй ещё раз.")

        elif platform == "x":
            await callback.message.answer("Скачиваю аудио из X (Twitter)...")
            from services.x_downloader import download_x_audio
            audio_path = download_x_audio(url)
            if audio_path:
                input_file = FSInputFile(audio_path)
                await callback.message.answer_audio(audio=input_file)
                os.remove(audio_path)
            else:
                await callback.message.answer("Не могу скачать аудио. Попробуй ещё раз.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())