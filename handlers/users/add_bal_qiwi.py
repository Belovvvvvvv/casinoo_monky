from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from config import config
from data.functions.db import get_user, add_stat, select_buy_stat, update_balance, delete_stat
from keyboards.inline.other_keyboards import check_menu, back_to_main_menu, cabinet_keyboard
from loader import dp, bot
from states.states import balance_states
from texts import cabinet_text


@dp.callback_query_handler(text="back_to_personal_account", state="*")
async def back_to_personal_account(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(cabinet_text(get_user(call.from_user.id)),
                                 reply_markup=cabinet_keyboard())


@dp.callback_query_handler(regexp="^method_balance:\w$")
async def add_balance_qiwi_main(call: CallbackQuery):
    await call.message.edit_text("Напишите сумму, которую вы хотите пополнить."
                                 "\n❗️*Внимание*❗️\n`Минимальная сумма пополнения - 10₽`",
                                 parse_mode="MarkDown", reply_markup=back_to_main_menu)
    if call.data.split(":")[1] == 'q':
        await balance_states.BS1.set()
    elif call.data.split(":")[1] == 'p':
        await balance_states.BS2.set()


@dp.message_handler(state=balance_states.BS1)
async def add_balance_qiwi(message: Message, state: FSMContext):
    if float(message.text) >= 10:

        await bot.send_message(message.chat.id,
                               f"*Для того, чтобы пополнить свой баланс на" 
                               f" {round(float(message.text), 2)}руб вам нужно:*\n\n"
                               f"💰Перевести - `{round(float(message.text), 2)}₽`\n"
                               f"💳На кошелек - `+{config('QIWI_ADDRESS')}`\n"
                               f"📃С комментарием - `G{message.from_user.id}`",
                               parse_mode="MarkDown")
        
        await state.finish()
    else:
        await message.answer("Неверное количество, попробуйте еще раз :)")
        
        

@dp.message_handler(state=balance_states.BS2)
async def add_balance_payeer(message: Message, state: FSMContext):

    if float(message.text) >= 10:

        await bot.send_message(message.chat.id,
                               f"Для того, чтобы пополнить свой баланс на {round(float(message.text), 2)}руб вам нужно:\n\n"
                               f"💰Перевести - {round(float(message.text), 2)}₽\n"
                               f"💳На кошелек - <code>{config('payeer_account')}</code>\n📃С комментарием - <code>G{message.from_user.id}</code>\n\n❗️ <i>Время зачисления до 3 минут</i>")
        
        await state.finish()
    else:
        await message.answer("Неверное количество, попробуйте еще раз :)")