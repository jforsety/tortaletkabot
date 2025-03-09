import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from aiogram import types
import os

# Импортируем тестируемую функцию и зависимости
from app_bot.main import cmd_admin, admin_message, admin_btn, logger


@pytest.mark.asyncio
async def test_admin_command_non_private_chat(monkeypatch):
    # Устанавливаем переменную окружения
    monkeypatch.setenv("ADMIN_ID", "12345")

    # Создаем мок-объекты
    message = MagicMock()
    message.chat.type = "group"  # Не приватный чат
    message.answer = AsyncMock()  # Мок асинхронного метода

    # Вызываем тестируемую функцию
    await cmd_admin(message)

    # Проверяем, что ответ не отправлен
    message.answer.assert_not_called()


@pytest.mark.asyncio
async def test_admin_command_private_chat_unauthorized(monkeypatch, mocker):
    # Устанавливаем переменную окружения
    monkeypatch.setenv("ADMIN_ID", "12345")

    # Мок для сообщения
    message = MagicMock()
    message.chat.type = "private"
    message.from_user.id = 99999  # Не совпадает с ADMIN_ID
    message.answer = AsyncMock()

    # Мокаем логгер
    mock_logger = mocker.patch.object(logger, 'info')

    # Вызываем функцию
    await cmd_admin(message)

    # Проверяем отсутствие ответа и запись в лог
    message.answer.assert_not_called()
    mock_logger.assert_called_once_with(
        "Попытка использовать команду admin без необходимых доступов: 99999"
    )


@pytest.mark.asyncio
async def test_admin_command_private_chat_authorized(monkeypatch):
    # Устанавливаем переменную окружения
    admin_id = "12345"
    monkeypatch.setenv("ADMIN_ID", admin_id)

    # Мок для сообщения
    message = MagicMock()
    message.chat.type = "private"
    message.from_user.id = int(admin_id)  # Совпадает с ADMIN_ID
    message.answer = AsyncMock()

    # Вызываем функцию
    await cmd_admin(message)

    # Проверяем отправку сообщения с правильными параметрами
    message.answer.assert_awaited_once_with(
        admin_message,
        reply_markup=admin_btn
    )