import asyncio
import logging
import os
from datetime import datetime

from aiogram.exceptions import TelegramAPIError
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

from aiogram.types import CallbackQuery
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters.command import Command

from app_bot.api_ai import start_gigachat
from app_bot.database import add_user, profile_exists, referral_reg, update_attempts, update_attempts_admin, \
    get_users_id
from app_bot.keyboards import check_sub_menu, get_referral_keyboard, admin_btn
from app_bot.text_bot.text import start_text, not_sub_message, instruction_text, admin_message, attempts_text


logger = logging.getLogger(__name__)

load_dotenv()
# Объект бота
bot = Bot(token=os.environ.get("TOKEN_BOT"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# Диспетчер
dp = Dispatcher()

# Константа для задержки между отправками (в секундах)
SEND_DELAY = 0.8  # Можно регулировать по необходимости


# Функция проверки подписки на канал
def check_sub_channel(chat_member):
    if chat_member.status != 'left':
        return True
    else:
        return False


# Инициализация планировщика
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")


# Функция регистрации задач
def setup_scheduler():
    scheduler.add_job(
        update_attempts,
        "cron",
        hour=0,
        minute=1,
        start_date=datetime.now()
    )


# Вызов регистрации задач (при импорте модуля)
setup_scheduler()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    referral_id = None
    if message.chat.type == 'private':
        if check_sub_channel(
                await bot.get_chat_member(chat_id=os.environ.get("CHANNEL_ID"), user_id=message.from_user.id)):
            add_user(message)
            if len(message.text.split()) > 1:
                referral_id = message.text.split()[1].replace("ref_", "")
            if referral_id and referral_id.isdigit():
                referral_reg(message, referral_id)
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
        if check_sub_channel(
                await bot.get_chat_member(chat_id=os.environ.get("CHANNEL_ID"), user_id=message.from_user.id)):
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
        if check_sub_channel(
                await bot.get_chat_member(chat_id=os.environ.get("CHANNEL_ID"), user_id=message.from_user.id)):
            profile_list = profile_exists(message)
            await message.answer(text=f"<b>👤 Профиль пользователя:</b>\n\n"
                                      f"<b>ID:</b> {profile_list[0][1]}\n"
                                      f"<b>Имя:</b> {profile_list[0][2]}\n"
                                      f"<b>Рефералы:</b> {profile_list[0][6]}\n"
                                    # f"<b>Подписка:</b> {profile_list[0][5]}\n"
                                      f"<b>Попытки:</b> {profile_list[0][5]}\n"
                                      f"<i>*За каждого приглашенного друга "
                                      f"даётся 10 бесплатных запросов*</i>", reply_markup=keyboard)
        else:
            await message.answer(not_sub_message, reply_markup=check_sub_menu)


@dp.message(Command("admin"))
async def cmd_admin(message: types.Message):
    if message.chat.type == 'private':
        if message.from_user.id == int(os.environ.get("ADMIN_ID")):
            logger.info(f"Использование команды admin - {message.from_user.id}")
            await message.answer(admin_message, reply_markup=admin_btn)
        else:
            logger.info(f"Попытка использовать команду admin без необходимых доступов: {message.from_user.id}")


# Обработчик кнопки "ОБНОВИТЬ ПОПЫТКИ (ВСЕ)"
@dp.callback_query(F.data == "update_1")
async def start_update_attempts(call: types.CallbackQuery):
    await update_attempts()
    await call.message.answer(attempts_text)


# Обработчик кнопки "ОБНОВИТЬ ПОПЫТКИ (АДМ)"
@dp.callback_query(F.data == "update_2")
async def start_update_admin(call: types.CallbackQuery):
    update_attempts_admin()
    await call.message.answer(attempts_text)


class SendMessagesState(StatesGroup):
    waiting_for_content = State()


# Обработчик кнопки "ОТПРАВКА СООБЩЕНИЯ (ВСЕ)"
@dp.callback_query(F.data == "send_messages")
async def start_send_messages(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Отправьте изображение с текстом для рассылки")
    await state.set_state(SendMessagesState.waiting_for_content)


# Обработчик контента
@dp.message(SendMessagesState.waiting_for_content, F.photo | F.text)
async def process_content(message: types.Message, state: FSMContext, bot: Bot):
    try:
        if not message.photo:
            await message.answer("Нужно отправить изображение с текстом!")
            return

        photo_id = message.photo[-1].file_id
        caption = message.caption if message.caption else ""

        users = get_users_id()
        success = 0
        failed = 0
        total_users = len(users)

        for index, user in enumerate(users):
            try:
                await bot.send_photo(
                    chat_id=user[0],
                    photo=photo_id,
                    caption=caption
                )
                success += 1
            except TelegramAPIError as e:
                logger.error(f"Произошла ошибка при отправке сообщения пользователю {user[0]}: {e}")
                failed += 1
            except Exception as e:
                logger.error(f"Неизвестная ошибка: {e}")
                failed += 1

            # Добавляем задержку после каждой итерации, кроме последней
            if index < total_users - 1:
                await asyncio.sleep(SEND_DELAY)

        await message.answer(
            f"Рассылка завершена!\n"
            f"Успешно: {success}\n"
            f"Не удалось: {failed}"
        )

    except Exception as e:
        logger.error(f"Произошла ошибка при отправке сообщений: {str(e)}")
        await message.answer(f"Произошла ошибка: {str(e)}")
    finally:
        await state.clear()


# Обработчик для некорректного ввода
@dp.message(SendMessagesState.waiting_for_content)
async def invalid_content(message: types.Message):
    await message.answer("Пожалуйста, отправьте изображение с текстом!")


@dp.message()
async def message_handler(message: types.Message):
    if message.chat.type == 'private':
        if check_sub_channel(
                await bot.get_chat_member(chat_id=os.environ.get("CHANNEL_ID"), user_id=message.from_user.id)):
            await message.answer(start_gigachat(message), parse_mode="Markdown")
        else:
            await message.answer(not_sub_message, reply_markup=check_sub_menu)
