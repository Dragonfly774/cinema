from data import db_session
from data.time_table import TimeTable

db_session.global_init("db/blogs.sqlite")
db_sess = db_session.create_session()
film = TimeTable()
film.time = ("10:10", "11:15", "12:10", "13:55", "14:50", "15:55", "16:35")
film.price = "от 150"
film.hall = 1, 2
film.date = "20 апреля"
db_sess.add(film)
db_sess.commit()
