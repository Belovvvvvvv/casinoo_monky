﻿import asyncio

from keyboards.inline.games_keyboard import dice_chat_game_keyboard
from aiogram import types
from filters.filters import IsPrivate, IsPrivateCall, IsGroup
from loader import dp, bot
from config import config
from data.functions.db import get_chat_dice_game_by_id, chat_dice_game_add_player, \
                              get_chat_by_msg_id_dice_game, chat_dice_game_add_score, \
                              chat_dice_game_close, get_user, update_balance, list_all_dice_game



@dp.callback_query_handler(~IsPrivateCall(), regexp='^join_dice_chat:\d*$')
async def join_dice_game_chat_handler(c: types.CallbackQuery):
    game_id = int(c.data.split(':')[1])
    game = get_chat_dice_game_by_id(game_id=game_id)
    user = get_user(c.from_user.id)
    
    if user:
      
      if c.from_user.username:
        player_p2 = f'@{c.from_user.username}'
      else:
        player_p2 = f'<a href="tg://user?id={c.from_user.id}">{c.from_user.id}</a>'
        
      if game:

        if user[1] >= game[-3]:

          if game[-1]:

            try:

              if game[3]:
                
                username1 = f'{game[3]}'
              else:
                username1 = f'<a href="tg://user?id={game[2]}">{game[2]}</a>'

              if game[2] != c.from_user.id:
               
                if game[4] == 0:
                  win_sum = round((game[-3] * 2) - (game[-3] * 2 *  (int(config("chat_dice_percent")) / 100)), 2)
                  msg = await c.message.answer(
                    f'{game[-4]} GAME №{game_id}\n\n👥 Игроки:\n1️⃣ - {username1}\n2️⃣ - ' \
                    f'{player_p2}\n\n — Отправьте <code>{game[-4]}</code> в ответ на это сообщение\n' \
                    f'\n💰 Ставка: {win_sum} ₽')
                  update_balance(c.from_user.id, -game[-3])
                  chat_dice_game_add_player(
                    message_id=msg.message_id,
                    player_2_id=c.from_user.id,
                    player_2_name=player_p2,
                    game_id=game_id)

                else:
                  await c.answer('❌ В данной игре мест нет!', show_alert=True)
               
              else:  
                await c.answer('❌ Вы не можете присоединиться к данной игре', show_alert=True)
                
              
            except Exception as e:
              print(e)

          else:
            await c.answer('❌ Игра уже завершена!', show_alert=True) 
            
        else:
          await c.answer('❌ Недостаточно денег!', show_alert=True)
          
      else:
        await c.answer('❌ Игра не найдена!', show_alert=True)
        
    else:
      await c.answer('❌ Вы не являетесь пользователем нашего бота!', show_alert=True)
      
      
@dp.message_handler(~IsPrivate(), is_reply=True,  chat_type='supergroup', content_types='dice')
async def result_dice_game_chat_handler(m: types.Message):
    print(m.dice.emoji)
    game = get_chat_by_msg_id_dice_game(chat_id=m.chat.id, message_id=m.reply_to_message.message_id)
    if game:
      
      if m.dice.emoji == game[-4]:
 
        if game[-1]:

            if m.from_user.id not in [game[-5], game[-6]]:
              
              if game[2] == m.from_user.id and not game[6]:
                chat_dice_game_add_score(game[-0], m.dice.value, "score_1")
              
              if game[4] == m.from_user.id and not game[7]:
                chat_dice_game_add_score(game[-0], m.dice.value, "score_2")
              
              game = get_chat_by_msg_id_dice_game(chat_id=m.chat.id, message_id=m.reply_to_message.message_id)
              if game[6] != 0 and  game[-5] != 0:

                win_sum = round((game[-3] * 2) - (game[-3] * 2 *  (int(config("chat_dice_percent")) / 100)), 2)
                if game[3]:
                  username1 = f'{game[3]}'
                else:
                  username1 = f'<a href="tg://user?id={game[2]}">{game[2]}</a>'

                if game[5]:
                  username2 = f'{game[5]}'
                else:
                  username2 = f'<a href="tg://user?id={game[4]}">{game[4]}</a>'
                
                await asyncio.sleep(5)
                if game[-5] == game[-6]:
                  
                  text = \
                    f'{game[-4]} GAME №{game[0]}\n<a href="https://t.me/{config("chat")}">' \
                    f'📎 Наш чат</a>\n\n💰 Ставки возвращены: {game[-3]} ₽\n\n👥 Игроки: ' \
                    f'\n1️⃣ - {username1} [{game[-6]}]\n2️⃣ - {username2} [{game[-5]}]'
                    
                  update_balance(game[4], game[-3])
                  update_balance(game[2], game[-3])

                elif game[-5] > game[-6]:
                  
                  text = \
                    f'{game[-4]} GAME №{game[0]}\n<a href="https://t.me/{config("chat")}">' \
                    f'📎 Наш чат</a>\n\n💰 Выигрыш: {win_sum} ₽\n\n👥 Игроки:\n1️⃣ -' \
                    f' {username1} [{game[-6]}]\n2️⃣ - {username2} [{game[-5]}]\n\n' \
                    f'🥳 Победитель: {username2}'
                    
                  update_balance(game[4], win_sum)
                  
                else:
                  
                  text = \
                    f'{game[-4]} GAME №{game[0]}\n<a href="https://t.me/{config("chat")}">' \
                    f'📎 Наш чат</a>\n\n💰 Выигрыш: {win_sum} ₽\n\n👥 Игроки:\n1️⃣ - {username1}' \
                    f' [{game[-6]}]\n2️⃣ - {username2} [{game[-5]}]\n\n' \
                    f'🥳 Победитель:  {username1}'
                    
                  update_balance(game[2], win_sum)
                  
                chat_dice_game_close(game[0])
                await m.answer(text, disable_web_page_preview=True)
                
            else:
              msg = await m.reply_to_message.reply('❌ Игра уже началась, вы не участвуете в данной игре')
              await asyncio.sleep(10)
              await msg.delete()
            
        else:
          msg = await m.reply_to_message.reply('❌ Игра уже завершена!')
          await asyncio.sleep(10)
          await msg.delete()
          
          
@dp.message_handler(~IsPrivate(), is_reply=False,  chat_type='supergroup', commands=["all"])
async def list_dice_games_chat_handler(m: types.Message):
    
    all_games = list_all_dice_game(m.chat.id)
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    if len(all_games):

      for x in all_games:

        keyboard.add(types.InlineKeyboardButton(
          text=f'{x[-4]} #{x[0]} | {x[-3]} ₽',  callback_data=f'join_dice_chat:{x[0]}'.replace("#", "")))

      await m.answer('Все игры чата:', reply_markup=keyboard)
        
    else:
      await m.reply('В данном чате нет активных игр!')


@dp.message_handler(IsGroup(), commands=["баланс", "бал", "bal", "balance"])
async def add_chat_handler(m: types.Message):
    user = get_user(m.from_user.id)
    await m.reply(f"Ваш баланс {round(user[1], 2)}")

@dp.message_handler(IsGroup(), commands=["pay", "перевести"])
async def pay(m: types.Message):
  user_id, amount = m.get_args().split(" ")
  if not user_id.isdigit():
    await m.answer("ID не найден")
  elif not amount.isdigit():
    await m.answer("Сумма перевода должна быть целая")
  else:
    user_id = int(user_id)
    amount = int(amount)
    if user_id == m.from_user.id:
      await m.answe("Самому себе переводить нельзя")
    else:
      if get_user(m.from_user.id) == None:
        await m.answer("Ошибка")
      elif get_user(user_id) == None:
        await m.answer("Пользователя не существует")
      else:
        user = get_user(m.from_user.id)
        if user[1] < amount:
          await m.answer("Недостаточно средств")
        else:
          update_balance(m.from_user.id, -amount)
          update_balance(user_id, +amount)
          await m.answer(f"Перевод на {amount} был успешно осуществлен")

