import nest_asyncio
nest_asyncio.apply()
from aiogram import Bot, types
from aiogram import Dispatcher
from aiogram.utils import executor
import asyncio
import sqlite3
import random
import time
import asyncio
from contextlib import suppress

TOKEN = '6949332925:AAH8EKD8rCV3z_fRg_U9Ggm_BkK7cC0CGkQ'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
connection = sqlite3.connect('history.db', check_same_thread=False)
cursor = connection.cursor()
data_base = {}
global waiting_reply
waiting_reply = 0

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    global waiting_reply
    waiting_reply = 0
    await message.reply("Welcome to Notes! \nif you need help send '/help'")

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    global waiting_reply
    waiting_reply = 0
    await message.reply("This Notes bot helps you keep record of your notes. you can:\
    \n1. add a note using /add then the note in the same message.\
    \n2. delete a note using /delete then its number in the same message.\
    \n3. change a note using /edit then the number of the note in the same message.\
    \n4. see your notes using /show.\
    \n5. delete all your notes using /stopservice")

@dp.message_handler(commands=['show'])
async def process_show_command(message: types.Message):
    id_user = message.from_user.id
    global waiting_reply
    waiting_reply = 0
    if id_user not in data_base:
      await bot.send_message(id_user, "you have no notes! \nwhat do you want me to show?! 0o0")
    elif len(data_base[id_user]) == 0:
      await bot.send_message(id_user, "you have no notes! \nwhat do you want me to show?! 0o0")
    else:
      text = ""
      for i in range(1, len(data_base[id_user]) + 1):
        text += str(i) +". " + data_base[id_user][i-1] + "\n"
      await bot.send_message(id_user, text)

@dp.message_handler(commands=['add'])
async def process_add_command(msg: types.Message):
    id_user = msg.from_user.id
    global waiting_reply
    waiting_reply = 0
    answer = msg.text[4:]
    if id_user not in data_base:
      data_base.update({id_user : []})
    if len(answer) == 0:
      await bot.send_message(id_user, "send the note in the same message :)")
    else:
      data_base[id_user].append(answer)
      await bot.send_message(id_user, "saved!")

@dp.message_handler(commands=['delete'])
async def process_delete_command(msg: types.Message):
    id_user = msg.from_user.id
    global waiting_reply
    waiting_reply = 0
    if id_user not in data_base:
      await bot.send_message(id_user, " you have no notes to delete -_-\ndo you want me to delete myself?")
    elif len(data_base[id_user]) == 0:
      await bot.send_message(id_user, " you have no notes to delete -_-\nam I a joke to you?")
    elif len(msg.text) == 7:
      await bot.send_message(id_user, "send the number of the note in the same message :)")
    else:
      answer = int(msg.text[7:])
      if answer > len(data_base[id_user]):
        await bot.send_message(id_user, " you don't have that many notes now, do you? ;)")
      elif answer < 1:
        await bot.send_message(id_user, " unvalid number, right? '-'")
      else:
        data_base[id_user].pop(answer - 1)
        await bot.send_message(id_user, "note deleted successfully (I hope it wasn't the wrong one tho x_x)")

@dp.message_handler(commands=['stopservice'])
async def process_stop_command(msg: types.Message):
  id_user = msg.from_user.id
  global waiting_reply
  waiting_reply = 0
  if id_user in data_base:
    await bot.send_message(id_user, "send 'I swear I am sure' to delete all of your notes")
    waiting_reply = -1
  else:
    await bot.send_message(id_user, "you are not in the database -_-")

@dp.message_handler(commands=['edit'])
async def process_edit_command(msg: types.Message):
    id_user = msg.from_user.id
    global waiting_reply
    waiting_reply = 0
    if id_user not in data_base:
      await bot.send_message(id_user, " you have no notes to edit\nand I don't read minds -_-")
    elif len(data_base[id_user]) == 0:
      await bot.send_message(id_user, " you have no notes to edit\nand I don't read minds -_-")
    elif len(msg.text) == 5:
      await bot.send_message(id_user, "send the number of the note you want to edit in the same message :)")
    else:
      answer = int(msg.text[5:])
      if answer > len(data_base[id_user]):
        await bot.send_message(id_user, " you don't have that many notes now, do you? ;)")
      elif answer < 1:
        await bot.send_message(id_user, " unvalid number, right? '-'")
      else:
        waiting_reply = answer
        await bot.send_message(id_user, "now send the new note ^.^")


@dp.message_handler()
async def process_without_command(msg: types.Message):
  id_user = msg.from_user.id
  global waiting_reply
  if waiting_reply == -1:
    if msg.text == "I swear I am sure":
      data_base.pop(id_user)
      await bot.send_message(id_user, "you are no longer my friend v_v")
    else:
      await bot.send_message(id_user, "you either had a typo or you changed your mind, both ways it's nice to have you back ^-^")  
    waiting_reply = 0
  
  elif waiting_reply > 0:
    data_base[id_user][waiting_reply - 1] = msg.text
    await bot.send_message(id_user, "note changed successfully!")
    waiting_reply = 0
  elif waiting_reply == 0:
    await bot.send_message(id_user, "undefined command, please use our /help for info about using the bot")

if __name__ == '__main__':
    connection.commit()
    executor.start_polling(dp)
    connection.close()
