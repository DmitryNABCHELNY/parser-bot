from utils import make_reply_keyboard, make_inline_keyboard
from aiogram.types import CallbackQuery, Message,\
    ReplyKeyboardMarkup,ReplyKeyboardRemove,     \
    InlineKeyboardButton, InlineKeyboardMarkup   \

btnns = [['🥊Перчатки', '🔫Пистолеты', '👌Пистолеты-пулемёты', '🔪Ножи', '❗️Винтовки', '🔭Снайперские Винтовки', '🎯дробовики']]
accept_guns = make_reply_keyboard(btnns,  row_width=2)

switch = [['Настройки⚙️', 'Поиск🚀']]
switch_but = make_reply_keyboard(switch, row_width=1)

p_m = [['Минимальный процент скидки💸', 'Цена(ОТ-ДО)', 'Назад']]
pmkey = make_reply_keyboard(p_m, row_width=1) 