import time
from fuzzywuzzy import fuzz
import datetime

days_to_num = {
    'понедельник': 1,
    "вторник": 2,
    "среда": 3,
    "четверг": 4,
    "пятница": 5,
    "суббота": 6,
    "воскресенье": 7,
    "завтра":datetime.date.today().isoweekday()+1,
    "сегодня":datetime.date.today().isoweekday(),
    "послезавтра":datetime.date.today().isoweekday()+2
}

not_days = ["завтра","сегодня","послезавтра"]

predmeti = {
    "математика": ["математика", "матем"],
    "руссклит": ['руссклит', "русслит", "руслит"],
    "русскяз": ["русскяз", "руссяз", "русяз"],
    "беллит": ['беллит', "белит"],
    "беляз": ["беляз"],
    "общество": ['общество', "обществоведение"],
    "физика":["физика"],
    "география":["география","геогр"],
    "искусство":["искусство","искуство"],
    "англяз":["англяз"],
    "информатика":["информат","информатика"],
    "биология":["биология"],
    "историябел":["историябел"],
    "историявсем":["историявсем"],
    "химия":["химия"]
}
def check_date(date):
    try:
        time.strptime(date, '%d.%m.%Y')
    except Exception:
        return False



def check_predmet(predmet):
    for keys in predmeti:
        for i in predmeti[keys]:
            if fuzz.partial_ratio(predmet,i) == 100:
                return keys
    return False


def check_day(day):
    for key in days_to_num:
        if fuzz.ratio(key,day) >= 80:
            num = days_to_num[key]
            if num>7:
                return num%7
            return num
    raise Exception("Опа ошибочка")


def get_day(day):
    return check_day(day)

