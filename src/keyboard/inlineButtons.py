from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="TikTok"),
                KeyboardButton(text="YouTube Shorts"),
                KeyboardButton(text="Instagram Reels"),
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

def get_format_choice_keyboard(url: str, platform: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📹 Видео", callback_data=f"video_{platform}_{url}"),
                InlineKeyboardButton(text="🎵 Аудио", callback_data=f"audio_{platform}_{url}")
            ]
        ]
    )
    return keyboard