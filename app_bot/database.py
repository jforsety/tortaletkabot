import datetime
import sqlite3

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
                              30, 0, 0,
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
    """Получение попыток профиля"""
    result = cursor.execute("SELECT `attempt` FROM `app_tortaletka_client` WHERE `external_id` = ?",
                            (message.from_user.id,)).fetchone()
    return result


def referral_reg(message,referral_id: int):
    """Добавление информации о регистрации реферала и добавление попыток"""
    cursor.execute("UPDATE app_tortaletka_client SET attempt=attempt + 5, referrals=referrals + 1 WHERE external_id=?",(referral_id,))
    database.commit()
