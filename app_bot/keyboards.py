import os

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()

btn_url_channel = InlineKeyboardButton(text="ПОДПИСАТЬСЯ", url=os.getenv('CHANNEL_URL'))
inline_start = [[btn_url_channel]]
check_sub_menu = InlineKeyboardMarkup(inline_keyboard=inline_start)


def get_referral_keyboard(user_id: int, bot_url: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📤Пригласить друга",
                                 url=f"https://t.me/share/url?url={bot_url}?start={user_id}")
        ]
    ])



