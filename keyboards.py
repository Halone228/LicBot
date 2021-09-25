from aiogram.types.inline_keyboard import InlineKeyboardMarkup,InlineKeyboardButton

def get_admin_buttons():
    kb_mk = InlineKeyboardMarkup()
    kb1 = InlineKeyboardButton(text="Рассылка!",callback_data='rasilka',)
    kb2 = InlineKeyboardButton(text="Узнать кол-во пользователей!",callback_data="amount")
    return kb_mk.row(kb1,kb2)