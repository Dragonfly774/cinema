from pprint import pprint

from data import db_session
from data.time_table import TimeTable
import datetime

# print(datetime.datetime.now().date())
db_session.global_init("db/blogs.sqlite")
db_sess = db_session.create_session()
# time = db_sess.query(TimeTable).first()
# # print(', '.join(time.time))
# print(time.time[::])
film = TimeTable()
film.id_film = 2
film.time = "20:00 до 22:03"
film.price = "180"
film.hall = 2
film.date = "2021-04-24"
db_sess.add(film)
db_sess.commit()
