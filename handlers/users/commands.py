from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from aiogram import types
from aiogram.dispatcher import FSMContext
from config import config
from data.functions.db import get_user, add_user_to_db, update_balance, add_members,get_members_user,get_fast,get_members,create_fast_kon, delete_other_game_chat, get_chat_dice_game_by_id
from filters.filters import IsPrivate, IsGroup, IsAdmin, IsReplyMessage
from keyboards.inline.admin_menu_keyboards import admin_menu_keyboard
from keyboards.inline.other_keyboards import fast_keyboard,fast_close_keyboard
from keyboards.reply.reply_keyboards import main_menu_keyboard
from keyboards.inline.callback_datas import fast_callback
from loader import dp, bot
import asyncio, re
from utils.payments import send_safe


@dp.message_handler(IsPrivate(), Command("start"))
async def answer_start(message: Message, state: FSMContext):
    await state.finish()
    if get_user(message.chat.id) == None:
        add_user_to_db(message.chat.id, message.get_args())
        if message.get_args() and get_user(int(message.get_args())):
          await send_safe(message.get_args(), 'У вас новый реферал!')
    await state.finish()
    await message.answer(text="Главное меню",
                        reply_markup=main_menu_keyboard())

@dp.message_handler(IsPrivate(), Command("admin"))
async def admin_menu(message: Message):
    if get_user(message.chat.id) != None:
        if str(message.chat.id) in str(config("admin_id")):
            await message.answer(text="<i>Админ меню</i>",
                                 reply_markup=admin_menu_keyboard())
            

@dp.message_handler(IsGroup(), IsReplyMessage(), commands=["del", "delete"])
async def del_chat_game(message: Message):
    game_id = int(re.findall("№([0-9]+)", message.reply_to_message.text)[0])
    print(f'del_game {game_id}')
    game = get_chat_dice_game_by_id(game_id)
    if game != None:
        if game[2] == message.from_user.id and game[4] == 0:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.reply_to_message.message_id)
            delete_other_game_chat(game_id)
            update_balance(game[2], game[9])
            await message.reply(f"🗑 Игра <code>{game[0]}</code> удалена.  Игроку <code>{game[2]}</code> возвращены <code>{game[9]}</code> RUB")



@dp.message_handler(IsAdmin(), commands="fast")
async def create_fast(message: Message):
    try:
        amount = message.get_args()
        if not amount.isdigit():
            await message.reply("❌ Аргумент должен быть числом.")
        else:
            create = await create_fast_kon(chat_id=message.chat.id, amount=amount)
            await message.answer(f'''
🎲 <b>ФАСТ</b> 🎲

🚀 <b>Быстрые</b> <code>{amount} RUB</code> 💸
🛹 <b>Для участия нажмите кнопку:</b> «<code>Участвовать</code> ✅»

<b>Только первые 6️⃣ человек</b>
🏆 <code>Победителя выберет кость</code>🏆
                ''',reply_markup=await fast_keyboard(message.chat.id, create))
    except Exception as err:
        print(f'Fast {err}')
                
                
@dp.callback_query_handler(fast_callback.filter(action="participate"))
async def participate(call: types.CallbackQuery, callback_data: dict):
    fast_id = int(callback_data["fast_id"])
    fast = await get_fast(fast_id)
    members_fast = await get_members(fast_id)
    if len(members_fast) < 6:
        user_fast = await get_members_user(fast_id, call.from_user.id)
        if not user_fast:
            await add_members(fast_id, call.from_user.id, call.from_user.first_name)
            await call.answer('✅ Участие в фасте успешно. Ожидай результатов!', show_alert=True)
            members_fast = await get_members(fast_id)
        else:
            await call.answer('🤨 Ты уже учавствуешь в фасте!', show_alert=True)

    members_fast = await get_members(fast_id)
    if len(members_fast) == 6:
        await call.message.edit_reply_markup(await fast_close_keyboard())
        text = f"🚀 Фаст №{fast_id} начинается, участвуют:\n\n"
        for i in range(6):
            num = i+1
            text += f"{num}. <a href='tg://user?id={members_fast[i][1]}'>{members_fast[i][2]}</a>\n"
        await call.message.reply(text, parse_mode="HTML")
        emoji = await call.message.answer_dice(emoji="🎲")
        await asyncio.sleep(3)
        win = emoji.dice.value - 1
        update_balance(members_fast[win][1], fast[2])
        await call.message.reply(f"🥳 Победил игрок №{emoji.dice.value}\n💎 Игрок <a href='tg://user?id={members_fast[win][1]}'>{members_fast[win][2]}</a> поздравляю тебя, ты выигрываешь <code>{fast[2]}</code> RUB!", parse_mode="HTML")
        

