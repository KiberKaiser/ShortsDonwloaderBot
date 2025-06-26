from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

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