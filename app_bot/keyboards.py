import os

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv


load_dotenv()

# Клавиатура кнопки подписаться
btn_url_channel = InlineKeyboardButton(text="ПОДПИСАТЬСЯ", url=os.getenv('CHANNEL_URL'))
inline_start = [[btn_url_channel]]
check_sub_menu = InlineKeyboardMarkup(inline_keyboard=inline_start)

# Клавиатура админки в боте
btn_update_attempts = InlineKeyboardButton(text="ОБНОВИТЬ ПОПЫТКИ (ВСЕ)", callback_data="update_1")
btn_update_admin = InlineKeyboardButton(text="ОБНОВИТЬ ПОПЫТКИ (АДМ)", callback_data="update_2")
inline_admin = [[btn_update_attempts], [btn_update_admin]]
admin_btn = InlineKeyboardMarkup(inline_keyboard=inline_admin)


# Функция клавиатуры отправления реферальной ссылки
def get_referral_keyboard(user_id: int, bot_url: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📤Пригласить друга",
                                 url=f"https://t.me/share/url?url={bot_url}?start={user_id}")
        ]
    ])



