from data import db_session
from data.time_table import TimeTable
import datetime

# print(datetime.datetime.now().date())
db_session.global_init("db/blogs.sqlite")
db_sess = db_session.create_session()
film = TimeTable()
film.id_film = 1
film.time = '[["зал 1", ["10:10", "11:15", "12:10"]], ["зал 2", ["13:55", "14:50", "15:55", "16:35"]]]'
film.price = "от 150"
film.hall = 1
film.date = "2021-04-23"
db_sess.add(film)
db_sess.commit()
