from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app_bot.config import URL_CHANNEL, URL_INVITE


btn_url_channel = InlineKeyboardButton(text="ПОДПИСАТЬСЯ", url=URL_CHANNEL)
inline_start = [[btn_url_channel]]
check_sub_menu = InlineKeyboardMarkup(inline_keyboard=inline_start)


def get_referral_keyboard(user_id: int, bot_url: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📤Пригласить друга",
                                 url=f"https://t.me/share/url?url={bot_url}?start={user_id}")
        ]
    ])



