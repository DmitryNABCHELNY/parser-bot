#Бота писал для себя, позже на продажу, поэтому логика работает только под 1 пользователя 

from os import stat
from aiogram.types import message
import aiogram.utils.executor
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keyboards import *
from workparser import *
from aiogram.utils.markdown import hbold, hlink
from states import New_user, Settings1
import asyncio
import json
import time

BOT_TOKEN = '5521468053:AAHawyRSK6HeNOscywNN0A_iNp5_Q__VCMc'
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
ADMINS = [5196608348]

global searcher
searcher = []
global waiters
waiters = []


async def is_searcher(id):
    global searcher
    global waiters
    if len(searcher) == 0:
        searcher.append(waiters[0])
        waiters.pop(0)
        if id in searcher:
            return
        else:
            await asyncio.sleep(60)
            is_searcher(waiters, searcher, id)
    else:
        await asyncio.sleep(60)
        is_searcher(waiters, searcher, id)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    cl = 0
    if message.from_user.id == 5196608348:
        await bot.send_message(message.from_user.id, 'Добро пожаловать', reply_markup=switch_but)
        cl = 1               
    #if message.from_user.id in ADMINS:
    #    await bot.send_message(message.from_user.id, 'Добро пожаловать')
    #elif cl == 1:
    #    pass
    else:
        await bot.send_message(message.from_user.id, 'Вас нет в базе пользователей.')

# @dp.message_handler(commands=['new_user'], state='*')
# async def start(message: types.Message, state: FSMContext):
#     await state.set_state(New_user.user)
#     if message.from_user.id in ADMINS:
#         await bot.send_message(message.from_user.id, 'Вводи:')
#     else:
#         pass

# @dp.message_handler(state=New_user.user)
# async def help(message: types.Message, state: FSMContext):
#     await state.finish()
#     g = open('lst_of.txt', 'a+')
#     g.write('\n' + message.text)
#     g.close()
#     await bot.send_message(message.from_user.id, f'Вы добавили юзера с id:{message.text}')
#     new_p = open(f'{str(message.text)}.json', 'w+')
#     with open(f'{message.text}.json', 'w', encoding='utf-8') as file1:
#         result = {}
#         json.dump(result, file1, indent=4, ensure_ascii=False)
#     with open('user_settings.json', 'r', encoding='utf-8') as set1:
#         user = json.load(set1)
#         with open('user_settings.json', 'w', encoding='utf-8') as set1:
#             user[message.text] = {'procent':'15', 'price_from': '10', 'price_to':'5000'}
            # json.dump(user, ensure_ascii=False, indent=4, fp=set1)


@dp.message_handler(state=Settings1.procent)
async def procent(message: types.Message, state: FSMContext):
    await state.finish()
    with open('user_settings.json', encoding='utf-8') as set:
        result1 = json.load(set)
        try:
            int(message.text.split()[0])
            with open('user_settings.json', 'w', encoding='utf-8') as set:
                result1[str(message.from_user.id)]['procent'] = message.text
                json.dump(result1, ensure_ascii=False, indent=4, fp=set)
                await message.answer(f'Вы успешно заменили процент на {message.text}%')
        except:
            await message.answer(f'Вы ввели неверный формат данных')
    
@dp.message_handler(state=Settings1.money_from)
async def procent(message: types.Message, state: FSMContext):
    await state.finish()
    with open('user_settings.json', encoding='utf-8') as set:
        result1 = json.load(set)
        try:
            int(message.text.split()[0])
            with open('user_settings.json', 'w', encoding='utf-8') as set:
                result1[str(message.from_user.id)]['price_from'] = str(message.text.split()[0])
                result1[str(message.from_user.id)]['price_to'] = str(message.text.split()[1])
                json.dump(result1, ensure_ascii=False, indent=4, fp=set)
                await message.answer(f'Вы успешно заменили цену от-до на {message.text.split()[0]}$-{message.text.split()[1]}$')
        except:
            await message.answer(f'Вы ввели неверный формат данных')
    

@dp.message_handler(state='*')
async def help(message: types.Message, state: FSMContext):
    global waiters
    global searcher
    with open('user_settings.json', encoding='utf-8') as set:
        resu1t = json.load(set)
        proc = resu1t[str(message.from_user.id)]['procent']
        money_from1 = resu1t[str(message.from_user.id)]['price_from']
        money_to1 = resu1t[str(message.from_user.id)]['price_to']
    if message.text == btnns[0][0]:
        await message.answer(f'❗️Начался поиск по вашему запросу❗️\nПримерное время ожидания:12 минут')
        await collect_data('13', user_id= message.from_user.id, procent = proc, money_from=money_from1, money_to= money_to1)
        with open(f'{str(message.from_user.id)}.json', encoding='utf-8') as file:
            data = json.load(file)
        for index, item in enumerate(data):
            card = f'{hlink(item.get("full_name"), item.get("3d"))}\n' \
                f'{hbold("Скидка: ")}{item.get("overprice")}%\n' \
                f'{hbold("Цена: ")}${item.get("item_price")}🔥'
        
        
        if index%20 == 0:
            await asyncio.sleep(3)
            
        await message.answer(card, parse_mode='HTML')
        searcher.clear
    elif message.text == btnns[0][1]:
        await message.answer(f'❗️Начался поиск по вашему запросу❗️\nПримерное время ожидания:12 минут')
        await collect_data('5', user_id= message.from_user.id, procent = proc, money_from=money_from1, money_to= money_to1)
        with open(f'{str(message.from_user.id)}.json', encoding='utf-8') as file:
            data = json.load(file)
        for index, item in enumerate(data):
            card = f'{hlink(item.get("full_name"), item.get("3d"))}\n' \
                f'{hbold("Скидка: ")}{item.get("overprice")}%\n' \
                f'{hbold("Цена: ")}${item.get("item_price")}🔥'
        
        
            if index%20 == 0:
                await asyncio.sleep(3)
                
            await message.answer(card, parse_mode='HTML')
            searcher.clear
    elif message.text == btnns[0][2]:
        
        await message.answer(f'❗️Начался поиск по вашему запросу❗️\nПримерное время ожидания: минут')
        await collect_data('6', user_id= message.from_user.id, procent = proc, money_from=money_from1, money_to= money_to1)
        with open(f'{str(message.from_user.id)}.json', encoding='utf-8') as file:
            data = json.load(file)
        for index, item in enumerate(data):
            card = f'{hlink(item.get("full_name"), item.get("3d"))}\n' \
                f'{hbold("Скидка: ")}{item.get("overprice")}%\n' \
                f'{hbold("Цена: ")}${item.get("item_price")}🔥'
        
        
            if index%20 == 0:
                await asyncio.sleep(3)
                
            await message.answer(card, parse_mode='HTML')
            searcher.clear
    elif message.text == btnns[0][3]:
        
        await message.answer(f'❗️Начался поиск по вашему запросу❗️\nПримерное время ожидания:11 минут')
        await collect_data('2', user_id= message.from_user.id, procent = proc, money_from=money_from1, money_to= money_to1)
        with open(f'{str(message.from_user.id)}.json', encoding='utf-8') as file:
            data = json.load(file)
        for index, item in enumerate(data):
            card = f'{hlink(item.get("full_name"), item.get("3d"))}\n' \
                f'{hbold("Скидка: ")}{item.get("overprice")}%\n' \
                f'{hbold("Цена: ")}${item.get("item_price")}🔥'
        
        
            if index%20 == 0:
                await asyncio.sleep(3)
                
            await message.answer(card, parse_mode='HTML')
            searcher.clear
    elif message.text == btnns[0][4]:
        
        await message.answer(f'❗️Начался поиск по вашему запросу❗️\nПримерное время ожидания:12 минут')
        await collect_data('3', user_id= message.from_user.id, procent = proc, money_from=money_from1, money_to= money_to1)
        with open(f'{str(message.from_user.id)}.json', encoding='utf-8') as file:
            data = json.load(file)
        for index, item in enumerate(data):
            card = f'{hlink(item.get("full_name"), item.get("3d"))}\n' \
                f'{hbold("Скидка: ")}{item.get("overprice")}%\n' \
                f'{hbold("Цена: ")}${item.get("item_price")}🔥'
        
        
            if index%20 == 0:
                await asyncio.sleep(3)
                
            await message.answer(card, parse_mode='HTML')
            searcher.clear
    elif message.text == btnns[0][5]:
        
        await message.answer(f'❗️Начался поиск по вашему запросу❗️\nПримерное время ожидания:10 минут')
        await collect_data('4', user_id= message.from_user.id, procent = proc, money_from=money_from1, money_to= money_to1)
        with open(f'{str(message.from_user.id)}.json', encoding='utf-8') as file:
            data = json.load(file)
        for index, item in enumerate(data):
            card = f'{hlink(item.get("full_name"), item.get("3d"))}\n' \
                f'{hbold("Скидка: ")}{item.get("overprice")}%\n' \
                f'{hbold("Цена: ")}${item.get("item_price")}🔥'
        
        
            if index%20 == 0:
                await asyncio.sleep(3)
                
            await message.answer(card, parse_mode='HTML')
            searcher.clear
    elif message.text == btnns[0][6]:
        
        await message.answer(f'❗️Начался поиск по вашему запросу❗️\nПримерное время ожидания:3 минуты')
        await collect_data('7', user_id= message.from_user.id, procent = proc, money_from=money_from1, money_to= money_to1)
        with open(f'{str(message.from_user.id)}.json', encoding='utf-8') as file:
            data = json.load(file)
        for index, item in enumerate(data):
            card = f'{hlink(item.get("full_name"), item.get("3d"))}\n' \
                f'{hbold("Скидка: ")}{item.get("overprice")}%\n' \
                f'{hbold("Цена: ")}${item.get("item_price")}🔥'
        
        
            if index%20 == 0:
                await asyncio.sleep(3)
                
            await message.answer(card, parse_mode='HTML')
            searcher.clear
    elif message.text == switch[0][0]:
        await message.answer('Настройки:', reply_markup=pmkey)
    elif message.text == switch[0][1]:
        await message.answer('Начните поиск предметов прямой сейчас:', reply_markup=accept_guns)
    elif message.text == p_m[0][0]:
        await state.set_state(Settings1.procent)
        with open('user_settings.json', 'r', encoding='utf-8') as setka:
            user = json.load(setka)
            abcd = user[str(message.from_user.id)]['procent']
        await message.answer(f'Минимальный процент скидки на данный момент:{abcd}%\nВведите новый процент скидки без значка"%"')
    elif message.text == p_m[0][1]:
        await state.set_state(Settings1.money_from)
        with open('user_settings.json', 'r', encoding='utf-8') as setka:
            user = json.load(setka)
            abcd = user[str(message.from_user.id)]['price_from']
            abcd1 = user[str(message.from_user.id)]['price_to']
        await message.answer(f'Цены от-до данный момент:{abcd}$-{abcd1}$\nВведите новую цену от-до в $, через пробел.\nНапример:10 100')
    elif message.text == p_m[0][2]:
        await message.answer('Вы вернулись назад', reply_markup=switch_but)


if __name__ == '__main__':
    executor.start_polling(dp)