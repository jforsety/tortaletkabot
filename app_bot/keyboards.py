
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


btn_url_channel = InlineKeyboardButton(text="ПОДПИСАТЬСЯ", url="https://t.me/testtesttestttee4")
inline_start = [[btn_url_channel]]
check_sub_menu = InlineKeyboardMarkup(inline_keyboard=inline_start)


def get_referral_keyboard(user_id: int, bot_url: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📤Пригласить друга",
                                 url=f"https://t.me/share/url?url={bot_url}?start={user_id}")
        ]
    ])



