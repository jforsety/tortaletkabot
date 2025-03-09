import datetime
import os
import sqlite3
from pathlib import Path

import aiosqlite

database = sqlite3.connect("db.sqlite3")
cursor = database.cursor()


def add_user(message):
    """Регистрация пользователя"""
    cursor.execute("SELECT external_id FROM app_tortaletka_client WHERE external_id=?", (message.from_user.id,))
    user = cursor.fetchone()
    if not user:
        cursor.execute("INSERT INTO app_tortaletka_client (external_id, first_name, last_name, attempt, "
                       "premium_status, referrals, date_registration, last_date, username) VALUES(?,?,?,?,?,?,?,?,"
                       "?)", (message.from_user.id,
                              message.from_user.first_name,
                              message.from_user.last_name,
                              20, 0, 0,
                              datetime.datetime.now(),
                              datetime.datetime.now(),
                              message.from_user.username))
    else:
        cursor.execute("UPDATE app_tortaletka_client SET last_date=? WHERE external_id=?",
                       (datetime.datetime.now(), user[0]))
    database.commit()


def profile_exists(message):
    """Получение информации по профилю"""
    result = cursor.execute("SELECT * FROM `app_tortaletka_client` WHERE `external_id` = ?",
                            (message.from_user.id,)).fetchall()
    return result


def profile_attempts(message):
    """Получение попыток пользователя"""
    result = cursor.execute("SELECT `attempt` FROM `app_tortaletka_client` WHERE `external_id` = ?",
                            (message.from_user.id,)).fetchone()
    return result


def referral_reg(message,referral_id: int):
    """Добавление информации о регистрации реферала и добавление попыток"""
    cursor.execute("UPDATE app_tortaletka_client SET attempt=attempt + 10, referrals=referrals + 1 WHERE external_id=?",(referral_id,))
    database.commit()


def edit_attempts(message):
    """Изменение попыток пользователя"""
    cursor.execute("UPDATE app_tortaletka_client SET attempt=attempt - 1 WHERE external_id=?",
                            (message.from_user.id,))
    database.commit()


# def update_attempts():
#     """Синхронное обновление попыток пользователей"""
#     users_id = cursor.execute("SELECT `external_id` FROM `app_tortaletka_client`").fetchall()
#     for id in users_id:
#         cursor.execute("UPDATE `app_tortaletka_client` SET attempt = 20 WHERE external_id = ?", (id))
#         database.commit()


async def update_attempts():
    """Асинхронное обновление попыток пользователей"""
    db_path = Path(__file__).parent.parent / "db.sqlite3"
    async with aiosqlite.connect(db_path) as database:
        cursor = await database.cursor()
        # Получаем все external_id
        await cursor.execute("SELECT external_id FROM app_tortaletka_client")
        users_id = await cursor.fetchall()
        # Обновляем попытки для каждого пользователя
        for id_tuple in users_id:
            user_id = id_tuple[0]  # Извлекаем значение из кортежа
            await cursor.execute(
                "UPDATE `app_tortaletka_client` SET attempt = 20 WHERE external_id = ?",
                (user_id,)
            )
        # Коммитим все изменения одной транзакцией
        await database.commit()


def update_attempts_admin():
    """Обновление попыток администратора"""
    admin_id = os.environ.get("ADMIN_ID")
    cursor.execute("UPDATE `app_tortaletka_client` SET attempt = 100 WHERE external_id = ?", (admin_id,))
    database.commit()


