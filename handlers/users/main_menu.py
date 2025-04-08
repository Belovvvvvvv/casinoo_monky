from aiogram.types import Message, CallbackQuery, InputFile

from config import config
from data.functions.db import get_user
from aiogram.dispatcher import FSMContext
from filters.filters import IsPrivate, IsPrivateCall
from keyboards.inline.other_keyboards import  cabinet_keyboard, chat_button
from keyboards.inline.games_keyboard import game_menu_keyboard
from loader import dp, bot
from texts import cabinet_text


@dp.message_handler(IsPrivate(), text="💰 PROFILE")
async def game_menu(message: Message):
    if get_user(message.chat.id) != None:
        await message.answer(cabinet_text(get_user(message.chat.id)),
                             reply_markup=cabinet_keyboard())


@dp.message_handler(IsPrivate(), text="💬 CHAT 💬")
async def chat(message: Message):
    await message.answer("<b><i>Игровой чат с участниками бота🤖</i></b>", reply_markup=chat_button)


@dp.callback_query_handler(IsPrivateCall(), text="partners_menu")
async def partners_handler(call: CallbackQuery):

    me = await bot.get_me()
    await call.message.answer(
        f"👥 <b>Приглашайте своих друзей и знакомых и получайте{config('ref_percent')}%"
        " от суммы всех их пополнений</b>\n\n📢 Ваша реферальная ссылка ⬇"
        f"\nhttps://t.me/{me.username}?start={call.from_user.id}",
        parse_mode="HTML")


@dp.message_handler(IsPrivate(), text="🎲 GAMES")
@dp.callback_query_handler(IsPrivateCall(), text="games_main_menu")
async def game_main_handler(message: Message, state: FSMContext):
    await state.finish()
    if not isinstance(message, Message):
      await message.message.edit_caption(
        caption="""<b>🎲 Список игр:</b>""",
        reply_markup=game_menu_keyboard())
    else:
      await message.answer_photo(
            photo=InputFile('filaro.jpg'),
            caption="""<b>🎲 Список игр:</b>""",
            reply_markup=game_menu_keyboard(),
            parse_mode="HTML")


@dp.callback_query_handler(IsPrivateCall(), text="games_back_menu", state='*')
async def game_main_handler(c: CallbackQuery, state: FSMContext):
    await state.finish()
    await c.message.delete()
    await c.message.answer_photo(
            photo=InputFile('filaro.jpg'),
            caption="""<b>🎲 Список игр:</b>""",
            reply_markup=game_menu_keyboard(),
            parse_mode="HTML")