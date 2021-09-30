from aiogram.types.inline_keyboard import InlineKeyboardMarkup,InlineKeyboardButton


def get_admin_buttons():
    kb_mk = InlineKeyboardMarkup()
    kb1 = InlineKeyboardButton(text="Рассылка!",callback_data='rasilka',)
    kb2 = InlineKeyboardButton(text="Узнать кол-во пользователей!",callback_data="amount")
    return kb_mk.row(kb1,kb2)


def get_keyboard(array,rows=3):
    kb = InlineKeyboardMarkup(row_width=rows)
    for index,button in enumerate(array):
        kb.insert(button)
    return kb


def keyboard_inline(a_dict=None,url=False,callback=False,*args,**kwargs):
    """
    Принимает либо словарь с нужными ключами, либо массивы(кортежи) с информацией.
    В массиввах(кортежах) первым идёт колдата, потом текст.
    Если нужно указать url, передайте переменную url cо значением True. В этом случае значение передаються
    в анологии с колдатой.
    :param a_dict:
    :param args:
    :return InlineKeyboardMarkup:
    """
    array = []
    try:
        rows = kwargs['rows']
    except:
        rows = 3
    for i in args:
        if type(i) == tuple or type(i) == list:
            continue
        else:
            raise ValueError("In params not tuple or list!")
    if a_dict:
        for key in a_dict:
            array.append(InlineKeyboardButton(text=str(key),callback_data=a_dict[key]['callback_data']))
    for i in args:
        print(i)
        try:
            if url:
                button = InlineKeyboardButton(text=i[1],url=i[0])
                array.append(button)
            else:
                button = InlineKeyboardButton(text=i[1], callback_data=i[0])
                array.append(button)
        except Exception as ex_:
            raise ex_
    return get_keyboard(array,rows=rows)