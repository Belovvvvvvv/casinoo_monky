from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_datas import fast_callback
from config import config


def cabinet_keyboard():
    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(text="🔥 Пополнить", callback_data="deposit")
    button2 = InlineKeyboardButton(text="💰 Вывести", callback_data="output")
    button3 = InlineKeyboardButton(text="🔑 Реферальная система", callback_data="partners_menu")

    keyboard.row(button1, button2)
    keyboard.row(button3)
    return keyboard


def deposit_keyboard():
    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(text="🥝Qiwi", callback_data="method_balance:q")
    button2 = InlineKeyboardButton(text="🅿️ PAYEER", callback_data="method_balance:p")
    button3 = InlineKeyboardButton(
        text="💳Visa/Master Card", url=f"https://t.me/{config('support_username')}")
    button4 = InlineKeyboardButton(text="CryptoBot🤖", callback_data="deposit:banker")
    keyboard.row(button1,button2)
    keyboard.row(button3,button4)

    return keyboard


def output_keyboard():
    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(text="🥝Qiwi", callback_data="output:qiwi")
    button2 = InlineKeyboardButton(text="CryptoBot🤖", callback_data="output:banker")
    button3 = InlineKeyboardButton(text="🔙 Назад", callback_data="output:cancel")
    keyboard.row(button1, button2)
    keyboard.row(button3)

    return keyboard


def p2p_deposit_keyboard(bill_id, url):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text='💸 Оплатить 💸', url=url))
    keyboard.add(
        InlineKeyboardButton(text='🔁 Проверить платёж', callback_data=f'check_p2p_deposit:{bill_id}'),
        InlineKeyboardButton(text='❌ Отменить', callback_data=f'reject_p2p_payment')
        )
    return keyboard


async def check_menu(cost, user_id):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="↗️Перейти к оплате", url=f"https://qiwi.com/payment/form/99?"
                                                                    f"extra%5B%27account%27%5D="
                                                                    f"{config('QIWI_ADDRESS')}&amountInteger="
                                                                    f"{cost}&amountFraction=0&"
                                                                    f"extra%5B%27comment%27%5D="
                                                                    f"{user_id}&currency=643&blocked[0]=account&"
                                                                    f"blocked[1]=comment&blocked[2]=sum")
            ],
            [
                InlineKeyboardButton(text="✅Проверить оплату", callback_data="check")
            ],
            [
                InlineKeyboardButton(text="⬅️Назад", callback_data="back_to_main_menu")
            ]
        ]
    )
    return markup


back_to_main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️Назад", callback_data="back_to_personal_account")
        ]
    ]
)

rate_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🤩Отзывы🤩", url="https://t.me/ozibiFFM")
        ]
    ]
)

support_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🧑‍💻 Админ", url="https://t.me/nonzun")
        ]
    ]
)

chat_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="💬 CHAT 💬", url="https://t.me/MonkeCasino_chat")
        ]
    ]
)


async def fast_keyboard(chat_id: int, fast_id: int):
    keyboard = InlineKeyboardMarkup(row_width=2).row(
        InlineKeyboardButton(text="Участвовать ✅", callback_data=fast_callback.new(chat_id=chat_id, fast_id=fast_id, action="participate"))
    )
    return keyboard
    

async def fast_close_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2).row(
        InlineKeyboardButton(text="Закрыто ❌", callback_data="close")
    )
    return keyboard