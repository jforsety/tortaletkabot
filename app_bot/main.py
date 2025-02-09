import logging
import os

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters.command import Command

from app_bot.api_ai import start_gigachat
from app_bot.database import add_user, profile_exists, referral_reg
from app_bot.keyboards import check_sub_menu, get_referral_keyboard
from app_bot.text_bot.text import start_text, not_sub_message, instruction_text, api_message

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='./app_bot/Logs_bot/tortaletka_bot.log')
logger = logging.getLogger(__name__)

load_dotenv()
# Объект бота
bot = Bot(token=os.environ.get("TOKEN_BOT"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# Диспетчер
dp = Dispatcher()


# Функция проверки подписки на канал
def check_sub_channel(chat_member):
    if chat_member.status != 'left':
        return True
    else:
        return False


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    referral_id = None
    if message.chat.type == 'private':
        if check_sub_channel(await bot.get_chat_member(chat_id=os.environ.get("CHANNEL_ID"), user_id=message.from_user.id)):
            add_user(message)
            if len(message.text.split()) > 1:
                referral_id = message.text.split()[1].replace("ref_", "")
            if referral_id and referral_id.isdigit():
                referral_reg(message,referral_id)
            await message.answer(start_text)
        else:
            await message.answer(not_sub_message, reply_markup=check_sub_menu)


@dp.message(Command("instruction"))
async def cmd_instruction(message: types.Message):
    keyboard = get_referral_keyboard(
        user_id=message.from_user.id,
        bot_url=os.environ.get("URL_BOT")
    )
    if message.chat.type == 'private':
        if check_sub_channel(await bot.get_chat_member(chat_id=os.environ.get("CHANNEL_ID"), user_id=message.from_user.id)):
            await message.answer(instruction_text, reply_markup=keyboard)
        else:
            await message.answer(not_sub_message, reply_markup=check_sub_menu)


@dp.message(Command("profile"))
async def cmd_profile(message: types.Message):
    keyboard = get_referral_keyboard(
        user_id=message.from_user.id,
        bot_url=os.environ.get("URL_BOT")
    )
    if message.chat.type == 'private':
        if check_sub_channel(await bot.get_chat_member(chat_id=os.environ.get("CHANNEL_ID"), user_id=message.from_user.id)):
            profile_list = profile_exists(message)
            await message.answer(text=f"<b>👤 Профиль пользователя:</b>\n\n"
                                      f"<b>ID:</b> {profile_list[0][1]}\n"
                                      f"<b>Имя:</b> {profile_list[0][2]}\n"
                                      f"<b>Рефералы:</b> {profile_list[0][6]}\n"
                                      # f"<b>Подписка:</b> {profile_list[0][5]}\n"
                                      f"<b>Попытки:</b> {profile_list[0][4]}\n"
                                      f"<i>*За каждого приглашенного друга "
                                      f"даётся 10 бесплатных запросов*</i>", reply_markup=keyboard)
        else:
            await message.answer(not_sub_message, reply_markup=check_sub_menu)


@dp.message()
async def message_handler(message: types.Message):
    if message.chat.type == 'private':
        await message.answer(start_gigachat(message),parse_mode="Markdown")

