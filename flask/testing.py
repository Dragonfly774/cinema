from pprint import pprint

from data import db_session
from data.time_table import TimeTable
from data.booking import Booking
import datetime

months = {
    1: 'Январь',
    2: 'Февраль',
    3: 'Март',
    4: 'Апрель',
    5: 'Май',
    6: 'Июнь',
    7: 'Июль',
    8: 'Август',
    9: 'Сентябрь',
    10: 'Октябрь',
    11: 'Ноябрь',
    12: 'Декабрь'
}

day= f'{datetime.datetime.now().hour}'
p = "10:00 до 11:28"
day_month = f'{months[datetime.datetime.now().month]}'

print(p[:6])


db_session.global_init("db/blogs.sqlite")
db_sess = db_session.create_session()
time = db_sess.query(TimeTable).first()
# print(time.film.title)
# # # print(', '.join(time.time))
# # print(time.time[::])
# film = TimeTable()
# film.id_film = 2
# film.time = "20:00 до 22:03"
# film.price = "180"
# film.hall = 2
# film.date = "2021-04-24"
# db_sess.add(film)
# db_sess.commit()
# print(len('+79022879533'))
