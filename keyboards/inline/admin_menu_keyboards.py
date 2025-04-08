from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import other_games_info
from data.functions.db import get_other_games, get_blackjack_games, \
    get_bakkara_games
from keyboards.inline.callback_datas import admin_search_user_callback, \
    game_info_callback


def admin_menu_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton(text="✉ Рассылка",
                                   callback_data="admin:mailing_menu")
    button2 = InlineKeyboardButton(text="📊 Статистика",
                                   callback_data="admin:statistic")
    button3 = InlineKeyboardButton(text="⚙ Настройки",
                                   callback_data="admin:settings")
    button4 = InlineKeyboardButton(text="🔍 Найти пользователя",
                                   callback_data="admin:search_user")
    button5 = InlineKeyboardButton(text="🗑 Удаление игры",
                                   callback_data="admin:delete_game_choose")
    keyboard.add(button1)
    keyboard.row(button2, button3)
    keyboard.add(button4)
    keyboard.add(button5)
    return keyboard


def delete_choose_game():
    keyboard = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton(text="🃏21 очко🃏",
                                   callback_data="admin:delete_blackjack")
    button2 = InlineKeyboardButton(text="🎴Баккара🎴",
                                   callback_data="admin:delete_baccara")
    button3 = InlineKeyboardButton(text="🎳🎯Игры🎲🏀",
                                   callback_data="admin:delete_othergames")
    button4 = InlineKeyboardButton(text="⏪ Назад",
                                   callback_data="admin:back_to_main")
    keyboard.row(button1, button2)
    keyboard.add(button3)
    keyboard.add(button4)
    return keyboard


def delete_other_games_kb():
    games = get_other_games()
    keyboard = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton(text="♻ Обновить",
                                  callback_data="admin:delete_othergames")
    button = InlineKeyboardButton(text="⏪ Назад",
                                  callback_data="admin:delete_game_choose")
    for game in games:
        keyboard.row(
            InlineKeyboardButton(
                text=f"{other_games_info[game[-1]]['emoji']} #{game[0]} | {game[2]}₽",
                callback_data=game_info_callback.new(
                    game_name=game[3], action="delete_game",
                    game_id=f"{game[0]}"
                )))
    keyboard.add(button1)
    keyboard.add(button)
    return keyboard


def delete_blackjack_kb():
    games = get_blackjack_games()
    keyboard = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton(text="♻ Обновить",
                                  callback_data="admin:delete_blackjack")
    button = InlineKeyboardButton(text="⏪ Назад",
                                  callback_data="admin:delete_game_choose")
    for game in games:
        keyboard.row(
            InlineKeyboardButton(text=f"🔍 Game #{game[0]} | {game[-2]}₽",
                                 callback_data=game_info_callback.new(
                                     game_name='blackjack',
                                     action="delete_game",
                                     game_id=f"{game[0]}"
                                 )))
    keyboard.add(button1)
    keyboard.add(button)
    return keyboard


def delete_baccara_kb():
    games = get_bakkara_games()
    keyboard = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton(text="♻ Обновить",
                                  callback_data="admin:delete_baccara")
    button = InlineKeyboardButton(text="⏪ Назад",
                                  callback_data="admin:delete_game_choose")
    for game in games:
        keyboard.row(
            InlineKeyboardButton(text=f"🔍 Game #{game[0]} | {game[-2]}₽",
                                 callback_data=game_info_callback.new(
                                     game_name='baccara', action="delete_game",
                                     game_id=f"{game[0]}"
                                 )))
    keyboard.add(button1)
    keyboard.add(button)
    return keyboard


def admin_mailing_menu_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton(text="📷 Рассылка с картинкой",
                                   callback_data="admin:mailing_with_picture")
    button2 = InlineKeyboardButton(text="🧾 Рассылка без картинки",
                                   callback_data="admin:mailing_without_picture")
    button3 = InlineKeyboardButton(text="⏪ Назад",
                                   callback_data="admin:back_to_main")
    keyboard.add(button1, button2, button3)
    return keyboard


def admin_settings_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton(text="💵 Изменить процент комиссии",
                                   callback_data="admin:change_markup_percent")
    button2 = InlineKeyboardButton(text="⏪ Назад",
                                   callback_data="admin:back_to_main")
    keyboard.add(button1, button2)
    return keyboard


def admin_back_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton(text="⏪ Назад",
                                   callback_data="admin:back_to_main")
    keyboard.add(button1)
    return keyboard


def admin_search_user_keyboard(user_id):
    keyboard = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton(text="💳 Изменить баланс",
                                   callback_data=admin_search_user_callback.new(
                                       action="change_balance", user_id=user_id
                                   ))
    button2 = InlineKeyboardButton(text="🔒 Включить подкрутку",
                                   callback_data=admin_search_user_callback.new(
                                       action="on_spinup", user_id=user_id
                                   ))
    button3 = InlineKeyboardButton(text="🔓 Выключить подкрутку",
                                   callback_data=admin_search_user_callback.new(
                                       action="off_spinup", user_id=user_id
                                   ))
    button4 = InlineKeyboardButton(text="💢 Закрыть",
                                   callback_data="close"
                                   )
    keyboard.row(button1)
    keyboard.add(button2, button3)
    keyboard.row(button4)
    return keyboard
