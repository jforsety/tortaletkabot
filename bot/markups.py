from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from config import URL_CHANNEL, URL_INVITE

btn_url_channel = InlineKeyboardButton(text="ПОДПИСАТЬСЯ", url=URL_CHANNEL)
inline_start = [[btn_url_channel]]
check_sub_menu = InlineKeyboardMarkup(inline_keyboard=inline_start)

btn_invite = InlineKeyboardButton(text="📤Пригласить друга", url=URL_INVITE)




