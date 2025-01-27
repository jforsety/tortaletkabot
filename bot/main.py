import asyncio
import logging

from pythonjsonlogger import jsonlogger
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters.command import Command

from bot.config import TOKEN_BOT, CHANNEL_ID
from bot.markups import check_sub_menu
from bot.text_bot.text import start_text, not_sub_message, manual_text

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
# настроем логирование в файл в формате JSON
logHandler = logging.FileHandler('Logs_bot/tortaletka_bot.log')
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(message)s')
logHandler.setFormatter(formatter)
# Объект бота
bot = Bot(TOKEN_BOT, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

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
        if check_sub_channel(await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)):
            await message.answer(start_text)
        else:
            await message.answer(not_sub_message, reply_markup=check_sub_menu)


# Хэндлер на команду /manual
@dp.message(Command("manual"))
async def cmd_manual(message: types.Message):
    if message.chat.type == 'private':
        if check_sub_channel(await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)):
            await message.answer(manual_text)
        else:
            await message.answer(not_sub_message, reply_markup=check_sub_menu)


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())