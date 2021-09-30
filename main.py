import asyncio
from db_files.class_bd import Class_BD
from aiogram import Bot, executor, Dispatcher, types
from FrameWorks.config import TOKEN
from asyncio import get_event_loop
from db_files.db import MainDB
import sqlite3
import datetime
from FrameWorks.modules import get_day
from FrameWorks import keyboards
from Parsers import kinoParser
from FrameWorks import json_to_info


bot = Bot(token=TOKEN)
loop = get_event_loop()
dp = Dispatcher(bot, loop=loop)
db = MainDB()
admin = 1347781724


async def check_kino():
    while True:
        kinoParser.parser()
        await asyncio.sleep(3600)


async def check_date():
    print("Started!")
    while True:
        for i in db.get_array():
            sq = sqlite3.connect(f'c{i[0]}.db')
            cursor = sq.cursor()
            get = cursor.execute("""SELECT * FROM class""").fetchall()
            for k in get:
                if k[2] == datetime.date.today().strftime("%d.%m.%Y"):
                    cursor.execute(f"""DELETE FROM class WHERE dz=? AND date=?""",([k[1],k[2]]))
                    sq.commit()
        await asyncio.sleep(600)


async def asyncs_def():
    await check_kino()
    await check_date()


@dp.callback_query_handler(lambda c: c.data == 'amount')
async def get_all_groups(callback: types.CallbackQuery):
    await callback.answer(f"Бот использует {len(db.get_array())} групп.")


@dp.callback_query_handler(lambda c: c.data[0:1] == 'f')
async def get_films(call: types.CallbackQuery):
    dicts = json_to_info.get_info('files\\endless.json')
    day_dict = dicts[call.data[1:]]
    string = f"Фильмы на {call.data[1:]}:\n"
    array = []
    for key in day_dict:
        array.append((":".join(["g"+call.data[1:],key])))
    await bot.send_message(call.from_user.id,string,reply_markup=keyboards.keyboard_inline(array))

@dp.message_handler(commands='фильмы')
async def get_films(message: types.Message):
    dicts = json_to_info.get_info('files\\endless.json')
    await message.answer("******ФИЛЬМЫ******",reply_markup=keyboards.keyboard_inline(a_dict=dicts,rows=2))


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("*Привет я бот помощник!*\n"
                         "Для уточнения разного рода команд, напиши команду _/help_!\n"
                         "Production: Kirill Savchuk", parse_mode='Markdown')


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.answer("Вот мои команды:\n"
                         "_*Для начала работы нужно сохранить чат в Базу Данных!*_\n"
                         'Для этого нужно ввести "добавить класс" вместо класс нужно написать ваш класс.\n'
                         'Чтобы записать домашние задание нужно отправить сообщение такого вида: записать'
                         ' предмет дата(записывается в виде ДД.ММ.ГГГГ) домашнее задание.\n'
                         '_*!ВНИМАНИЕ!*_\n'
                         'Предмет должен быть написан без пробелов! Иначе бот вас не поймет, например:\n'
                         'Беларуский язык - беляз или бел.яз\nи т.п.'
                         '\nЧтобы просмотреть домашние задание нужно отправить сообщение такого вида:\n'
                         'посмотреть предмет\n'
                         '_*Для админов*_\n'
                         'Чтобы записать/изменить расписание нужно написать:\n установить расписание день '
                         '_*!ЧЕРЕЗ ПРОБЕЛ!*_ '
                         'предеметы \n Если два кабинета то указывать через запятую! Никаких пробелов!\n'
                         'Для просмотра расписания нужно написать сообщение такого рода:\n'
                         'посмотреть расписание день\n'
                         'Всё!', parse_mode='Markdown')


@dp.message_handler(commands=['admin'])
async def admin_panel(message: types.Message):
    if message.chat.id == admin:
        await message.answer("Что вы хотите сделать?", reply_markup=keyboards.get_admin_buttons())


@dp.message_handler(commands=['дз'])
async def send_dz(message: types.Message):
    print(message.get_args().split())
    predmet = message.get_args().split()[-1]
    await message.answer(Class_BD(
        message.chat.id).get_dz(
        predmet
    ))


@dp.message_handler(commands='расписание')
async def raspisanie(message: types.Message):
    day = message.get_args().split()[-1]
    await message.answer(Class_BD(message.chat.id).get_rasp(
        day
    ))


@dp.message_handler(commands='записать')
async def zapisat(message: types.Message):
    args = message.get_args().split()
    await message.answer(Class_BD(message.chat.id).write_dz(
        args[0], " ".join(args[2:]), args[1]
    ))


@dp.message_handler(commands='удалить')
async def delete(message: types.Message):
    get = message.get_args().split()
    await message.answer(Class_BD(message.chat.id).delete(get[0], get[1]))


@dp.message_handler(commands="добавить")
async def in_bd(message: types.Message):
    args = message.get_args().split()
    await db.add_class(args[-1],message.chat.id)


@dp.message_handler()
async def get_message(message: types.Message):
    if db.check_if_exists(message.chat.id):
        if message.text.lower() == "миша":
            await message.answer("Миша красавчик",parse_mode='')
        elif "установить расписание" == " ".join(message.text.lower().split()[0:2]):
            get = message.text.lower().split()[2:]
            day = get_day(get[0])
            await message.answer(Class_BD(message.chat.id).zapisat_rasp(day, get[1:]))

if __name__ == "__main__":
    loop.create_task(asyncs_def())
    executor.start_polling(dp,skip_updates=True)
