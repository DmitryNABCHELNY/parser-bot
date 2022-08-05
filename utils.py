from aiogram import types


def make_reply_keyboard(btns, row_width=1):
    kb = types.ReplyKeyboardMarkup(row_width=row_width, resize_keyboard=True)
    for row in btns:
        kb.add(*[types.KeyboardButton(b) for b in row])
    return kb


def make_inline_keyboard(btns, row_width=1):
    kb = types.InlineKeyboardMarkup(row_width=row_width)
    for row in btns:
        current_btns = []
        for btn in row:
            if btn[1].startswith('url_'):
                current_btns.append(types.InlineKeyboardButton(text=btn[0], url=btn[1][4:]))
            else:
                current_btns.append(types.InlineKeyboardButton(text=btn[0], callback_data=btn[1]))
        kb.add(*current_btns)
    return kb
