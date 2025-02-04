import logging
import os

from dotenv import load_dotenv

from pythonjsonlogger import jsonlogger
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters.command import Command

from app_bot.config import CHANNEL_ID, TOKEN_BOT
from app_bot.database import add_user
from app_bot.markups import check_sub_menu, instruction_btn
from app_bot.text_bot.text import start_text, not_sub_message, instruction_text

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
# настроем логирование в файл в формате JSON
logHandler = logging.FileHandler('./app_bot/Logs_bot/tortaletka_bot.log')
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(message)s')
logHandler.setFormatter(formatter)

load_dotenv()
# Объект бота
bot = Bot(token=os.environ.get("TOKEN_BOT"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# Диспетчер
dp = Dispatcher()


#Функция проверки подписки на канал
def check_sub_channel(chat_member):
    if chat_member.status != 'left':
        return True
    else:
        return False


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if message.chat.type == 'private':
        if check_sub_channel(await bot.get_chat_member(chat_id=os.environ.get("CHANNEL_ID"), user_id=message.from_user.id)):
            add_user(message)
            await message.answer(start_text)
        else:
            await message.answer(not_sub_message, reply_markup=check_sub_menu)


# Хэндлер на команду /instruction
@dp.message(Command("instruction"))
async def cmd_instruction(message: types.Message):
    if message.chat.type == 'private':
        if check_sub_channel(await bot.get_chat_member(chat_id=os.environ.get("CHANNEL_ID"), user_id=message.from_user.id)):
            await message.answer(instruction_text, reply_markup=instruction_btn)
        else:
            await message.answer(not_sub_message, reply_markup=check_sub_menu)


# @dp.message(Command("get_chat_id"))
# async def get_chat_id(message: types.Message):
#     await message.answer(text=f"ID: {message.chat.id}")
