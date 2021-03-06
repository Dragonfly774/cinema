import datetime
import os
from random import randrange

from flask import Flask, render_template, redirect, request, make_response, abort, jsonify

from data.users import User
from data.films import Films
from data.booking import Booking
from data.time_table import TimeTable

from waitress import serve

from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from forms.loginform import LoginForm
from forms.user import RegisterForm
from forms.schedule import ScheduleForm
from forms.booking import BookingForm
from forms.films import FilmsForm

from data import db_session, films_api, films_resources
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

api = Api(app)

# для списка объектов
api.add_resource(films_resources.FilmsListResource, '/api/v2/films')
# для одного объекта
api.add_resource(films_resources.FilmsResource, '/api/v2/films/<int:films_id>')

#  инициализируем LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

"""пользователя будет перегидовать на форму регестрации, 
когда попытаеться перейти к обработчику доступному только для авторизованых"""
login_manager.login_view = '/register'


@login_manager.user_loader
def load_user(user_id):
    """
    Для верной работы flask-login
    у нас должна быть функция для
    получения пользователя, украшенная
    декоратором login_manager.user_loader
    :param user_id:
    :return: user
    """
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    """Обработчик формы регистрации"""
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data,
            age=form.age.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    обработчик формы авторизации
    :return: login.html форму авторизации
    """
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    """login_required Таким декоратором можно
    украшать обработчики страниц, на которые
    может попасть только авторизованный
    пользователь."""
    logout_user()
    return redirect("/")


@app.route("/")
@app.route("/index", methods=['GET', 'POST'])
def index():
    """
    Главная страница, где располагаются фильмы в прокате
    :return: главную страницу
    """
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
    # время покупки билетов отображается именно в тот день который указан
    day = f'{datetime.datetime.now().day}'
    day_month = f'{day} {months[datetime.datetime.now().month]}'
    time_now = f'{datetime.datetime.now().hour}:{datetime.datetime.now().minute}'

    db_sess = db_session.create_session()
    films = db_sess.query(Films)
    times = db_sess.query(TimeTable).filter(TimeTable.date == day_month)
    user = db_sess.query(User).first()
    return render_template("index.html", films=films, times=times, user=user, time_now=time_now)


@app.route("/booking/<int:id>/<int:idt>", methods=['GET', 'POST'])
@login_required
def booking(id, idt):
    """Обработчик формы бронирование билетов"""
    db_sess = db_session.create_session()
    films = db_sess.query(Films).filter(Films.id == id).first()
    times = db_sess.query(TimeTable)
    time_day = db_sess.query(TimeTable).filter(TimeTable.id == idt).first()

    time_booking_error = f"{time_day.date} в {time_day.time}"
    places = [int(i) for i in range(1, 16)]
    form = BookingForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        id_booking = int(randrange(99999))
        plase_and_row = db_sess.query(Booking).filter(Booking.place == request.form['place'],
                                                      Booking.roww == request.form['row'],
                                                      Booking.title == films.title,
                                                      Booking.time == time_booking_error).first()
        if plase_and_row:
            return render_template("booking.html", id=id, idt=idt, times=times, places=places, form=form,
                                   message="Это место уже забронированно")
        if request.method == 'POST':
            for time in times:
                if time.id == idt:
                    book = Booking(
                        id_booking=id_booking,
                        place=request.form['place'],
                        time=f"{time.date} в {time.time}",
                        title=time.film.title,
                        price=time_day.price,
                        roww=request.form['row'],
                        email=current_user.email,
                        number=form.number.data,
                        name=form.name.data
                    )
                    db_sess.add(book)
                    db_sess.commit()
                    return redirect('/my_booking')
    return render_template("booking.html", id=id, idt=idt, times=times, places=places, price=time_day.price, form=form)


@app.route("/my_booking", methods=['GET', 'POST'])
def my_booking():
    """
    Главная страница, где располагаются фильмы в прокате
    :return: главную страницу
    """
    db_sess = db_session.create_session()
    user = db_sess.query(User).first()
    if user == current_user:
        booking = db_sess.query(Booking)
    else:
        booking = db_sess.query(Booking).filter(Booking.email == current_user.email)

    return render_template("my_booking.html", booking=booking, user=user)


@app.route('/my_booking_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def my_booking_delete(id):
    """Обработчик удаления бронирования"""
    db_sess = db_session.create_session()
    book = db_sess.query(Booking).filter(Booking.id_booking == id).first()
                                         # Booking.email == current_user.email
    if book:
        db_sess.delete(book)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/my_booking')


@app.route('/schedule/<int:id>', methods=['GET', 'POST'])
@login_required
def schedule(id):
    """Обработчик формы добавления расписания"""
    form = ScheduleForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        time = TimeTable()
        if request.method == 'POST':
            date_month = request.form['class']
            time.date = f"{form.date_day.data} {date_month}"
            time.id_film = id
            time.time = form.time.data
            time.price = form.price.data
        db_sess.add(time)
        db_sess.commit()
        return redirect('/')
    return render_template('time_add.html', title='Добавление расписание к фильму',
                           form=form)


@app.route('/schedule_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def schedule_delete(id):
    """Обработчик удаления расписания"""
    db_sess = db_session.create_session()
    times = db_sess.query(TimeTable).filter(TimeTable.id_film == id).first()
    time = f"{times.date} в {times.time}"
    # print(time)
    # book = db_sess.query(Booking).filter(Booking.time == time).first()

    if times:
        db_sess.delete(times)
        # db_sess.delete(book)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/add_film', methods=['GET', 'POST'])
@login_required
def add_film():
    """Обработчик формы добавления фильма"""
    form = FilmsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        film = Films()
        film.title = form.title.data
        film.genres = form.genres.data
        film.link_img = form.img.data
        film.age = form.age.data
        db_sess.add(film)
        db_sess.commit()
        return redirect('/')
    return render_template('add_film.html', title='Добавления фильма',
                           form=form)


@app.route('/films_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def films_delete(id):
    """Обработчик удаления фильма"""
    db_sess = db_session.create_session()
    film = db_sess.query(Films).filter(Films.id == id).first()

    if film:
        db_sess.delete(film)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def main():
    db_session.global_init("db/blogs.sqlite")
    db_sess = db_session.create_session()

    # Api
    app.register_blueprint(films_api.blueprint)

    app.run(port=8080, host='127.0.0.1')
    # # с дефаултными значениями будет не более 4 потов
    # port = int(os.environ.get('PORT', 5000))
    # serve(app, port=port, host="0.0.0.0")


if __name__ == '__main__':
    main()

"""git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/Dragonfly774/flask_alch.git
git push -u origin main
"""
