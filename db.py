import sqlite3
from class_bd import Class_BD

class MainDB:
    def __init__(self):
       self.sq = sqlite3.connect('main.db')
       self.cursor = self.sq.cursor()
       self.cursor.execute("""CREATE TABLE IF NOT EXISTS main(chat_id BIGINT)""")
       self.sq.commit()

    def check_if_exists(self,chat_id):
        self.cursor.execute(f"""SELECT chat_id FROM main WHERE chat_id = {chat_id}""")
        res = self.cursor.fetchone()
        return res

    def add_class(self,name,chat_id):
        if self.check_if_exists(chat_id) == None:
            try:
                self.cursor.execute(fr"""INSERT INTO main(chat_id) VALUES ({chat_id})""")
                self.sq.commit()
                Class_BD(chat_id).create()
                return f"Класс {name} успешно добавлен в базу данных!"
            except Exception as ex:
                print(ex)
                return "Ошибка! Попробуйте ещё раз"
        else:
            return f"Класс {name} уже сохранен в базе, по chat-id!"

    def get_array(self):
        return self.cursor.execute("""SELECT * FROM main""").fetchall()