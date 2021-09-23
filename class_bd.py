import sqlite3 as sq
from modules import check_predmet,check_date,check_day,\
    predmeti,days_to_num as dic,not_days


class Class_BD:
    def __init__(self,chat_id):
        self.sq = sq.connect(f'c{chat_id}.db')
        self.cursor = self.sq.cursor()

    def create(self):
        self.cursor.execute(f"""
CREATE TABLE IF NOT EXISTS class(learn STRING, dz STRING, date DATE)""")
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS rasp(day INTEGER, predmet STRING)""")
        self.sq.commit()

    def write_dz(self,predmet, dz, date):
        predmet_get = check_predmet(predmet)
        if predmet_get == False:
            return "Некорректно введен предмет!"
        if check_date(date) == False:
            return "Некорректно введена дата!"
        self.cursor.execute(f"""SELECT * FROM class WHERE date=? AND learn=?""", [date, predmet_get])
        get = self.cursor.fetchone()
        if get == None:
            self.cursor.execute("""INSERT INTO class(learn,dz,date) VALUES(?,?,?)""", (predmet_get, dz, date))
            self.sq.commit()
            return "Домашнее задание записано"
        elif get[0] == predmet_get:
            return "Домашнее задание на эту дату уже присутствует!"

    def get_dz(self,predmet):
        predmet_get = check_predmet(predmet)
        if predmet_get == False:
            return "Некорректно введен предмет!"
        self.cursor.execute("""SELECT * FROM class WHERE learn=?""", ([predmet_get]))
        get = self.cursor.fetchone()
        if get == None:
            return "Дз на этот предмет не записано!"
        return f"{get[0]} на {get[2]}\n{get[1]}"

    def zapisat_rasp(self,day, arr_of_predmet):
        if self.cursor.execute(f"SELECT * FROM rasp WHERE day=?", ([day])).fetchone() is None:
            self.cursor.execute(f"""INSERT INTO rasp(day,predmet) 
            VALUES(?,?)""",([day," ".join(arr_of_predmet)]))
            self.sq.commit()
        else:
            self.cursor.execute("""UPDATE rasp SET predmet=? WHERE day=?""",([" ".join(arr_of_predmet),day]))
            self.sq.commit()
        return "Рассписание записано!"

    def get_rasp(self,day):
        try:
            self.cursor.execute("""SELECT predmet FROM rasp WHERE day=?""",([day]))
            ras = self.cursor.fetchone()[0].split(" ")
            word_day = "".join([i for i in dic if dic[i] == day and not (i in not_days)])
            rasp = "".join([f"{i}. {val}\n" for i,val in enumerate(ras,start=1)])
            return f"********{word_day.upper()}********\n{rasp}"
        except:
            return "Походу повезло... В этот день уроков нету!"
    def delete(self,predmet,date):
        predmet = check_predmet(predmet)
        if predmet == False:
            return "Некорректно введен предмет!"
        try:
            self.cursor.execute(f"DELETE FROM class WHERE learn=? AND date =?",(predmet,date))
            self.sq.commit()
            return "Удаление прошло успешно"
        except Exception as ex:
            print(ex)
            return "Такое дз отсутствует!"
