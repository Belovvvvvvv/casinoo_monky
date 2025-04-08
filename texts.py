from data.functions.db import get_all_users, get_all_games, get_all_slots_bets_sum, get_all_today_users, \
    get_all_today_games, get_all_bets_sum, get_all_slots_games, get_all_today_slots_games, get_all_today_slots_bets_sum, \
    get_all_today_bets_sum


def cabinet_text(user):
    text = \
        "💰 <i><b>PROFILE</b></i>\n" \
        f"<i><b>🆔 TG ID:</b></i> <code>{user[0]}</code>\n" \
        "<i><b>➖➖➖➖➖➖➖➖➖➖➖➖➖</b></i>\n" \
        f"💰 <b>Баланс: </b><i>{float(user[1])}₽</i>\n" \
        f"<i><b>➖➖➖➖➖➖➖➖➖➖➖➖➖</b></i>\n" \
        f"⌚️ Дата регистрации: <i>{user[4]}</i>"

    return text


def statistic_text(games_amount, win_amount, lose_amount, win, lose, profit):
    text = """
📜Всего игр: {}

📈Всего игр выиграно: {}
📉Всего игр проиграно: {}

▪ ️Выигрыш: {}₽
▪ ️Проигрыш: {}₽
〰 ️Профит: {}₽
    """.format(games_amount, win_amount, lose_amount, int(win), int(lose), int(profit))
    return text

def admin_search_user_text(user):
    text = """
<b>Информация о <a href='tg://user?id={}'>пользователе</a>:

🆔 Telegram ID: <code>{}</code>

💳 Баланс: {}₽

📅 Дата регистрации: {}

⚙ Подкрутка: {}</b>
    """.format(
        user[0],
        user[0],
        user[1],
        user[4],
        user[2],
    )
    return text


def admin_statistic_text():
    text = """
Статистика за все время:

Всего пользователей: {}
Всего игр: {}
Всего прокрутов в слотах: {}
Ставок на сумму: {} RUB
Прокрутов на сумму: {} RUB
    
Статистика за сегодня:

Новых пользователей за сегодня: {}
Игр за сегодня: {}
Прокрутов в слотах за сегодня: {}
Ставок за сегодня на сумму: {} RUB
Прокрутов за сегодня на сумму: {} RUB
Создатель данного скрипта @durov
    
    """.format(
        len(get_all_users()),
        len(get_all_games()),
        len(get_all_slots_games()),
        get_all_bets_sum(),
        get_all_slots_bets_sum() if get_all_slots_bets_sum() != None else 0,
        len(get_all_today_users()),
        len(get_all_today_games()),
        len(get_all_today_slots_games()),
        get_all_today_bets_sum() if get_all_today_bets_sum() != None else 0,
        get_all_today_slots_bets_sum() if get_all_today_slots_bets_sum() != None else 0)
    return text


def jackpot_statistic_text(win_amount, win):
    text = """
📊Всего побед: {}
📈️Выигрыш: {}₽
    """.format(win_amount,
               int(win) if win != None else 0
               )
    return text


def slots_statistic_text(games_amount, bet_sum, win_sim, lose_sum):
    text = """
➖ Количество игр: {}
➖ Сумма ставок: {}₽
〰 Выиграно: {}₽
〰 Проиграно: {}₽
    """.format(games_amount,
               bet_sum if win_sim != None else 0,
               win_sim if win_sim != None else 0,
               lose_sum if lose_sum != None else 0
               )
    return text