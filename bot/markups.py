from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import URL_CHANNEL

btn_url_channel = InlineKeyboardButton(text="ПОДПИСАТЬСЯ", url=URL_CHANNEL)
inline_kb_list = [[btn_url_channel]]
check_sub_menu = InlineKeyboardMarkup(inline_keyboard=inline_kb_list)



