import os
import datetime
from random import randrange

from flask import Flask, render_template, redirect, request, make_response, session, abort, flash
from data import db_session

from data.users import User
from data.news import News
from data.jobs import Jobs
from data.films import Films
from data.booking import Booking
from data.time_table import TimeTable

from forms.user import RegisterForm
from waitress import serve

from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from forms.loginform import LoginForm
from forms.jobs import JobsForm
from forms.news import NewsForm
from forms.schedule import ScheduleForm
from forms.booking import BookingForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

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


@app.route('/news', methods=['GET', 'POST'])
@login_required
def add_news():
    """Добавление новостей"""
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('news.html', title='Добавление новости',
                           form=form)


@app.route('/addjob', methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = Jobs()
        jobs.job = form.job.data
        jobs.team_leader = form.team_leader.data
        jobs.work_size = form.work_size.data
        jobs.collaborators = form.collaborators.data
        jobs.is_finished = form.is_finished.data
        current_user.jobs.append(jobs)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/t')
    return render_template('jobs.html', title='Adding a Job',
                           form=form)


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    """редактирование новостей"""
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news.html',
                           title='Редактирование новости',
                           form=form
                           )


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id,
                                      News.user == current_user
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


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

    db_sess = db_session.create_session()
    films = db_sess.query(Films)
    times = db_sess.query(TimeTable).filter(TimeTable.date == day_month)
    user = db_sess.query(User).first()
    return render_template("2.html", films=films, times=times, user=user)


@app.route("/booking/<int:id>", methods=['GET', 'POST'])
@login_required
def booking(id):
    """Обработчик формы бронирование билетов"""
    db_sess = db_session.create_session()
    films = db_sess.query(Films)
    times = db_sess.query(TimeTable)
    user = db_sess.query(User).first()
    buttons = [int(i) for i in range(1, 31)]
    column = [int(i) for i in range(1, 5)]
    form = BookingForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        id_booking = int(randrange(99999))
        book = Booking(
            id_booking=id_booking,
            place=form.place.data,
            count=form.count.data,
            roww=form.rov.data,
            number=form.number.data,
            name=form.name.data
        )
        db_sess.add(book)
        db_sess.commit()
        print(1)
        return redirect('/')
    print(form.validate_on_submit())
    return render_template("3.html", id=id, times=times, user=user, buttons=buttons, column=column,
                           form=form)


@app.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule():
    """Обработчик формы добавления расписания"""
    form = ScheduleForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        time = TimeTable()
        # time.hall = form.hall.data
        if request.method == 'POST':
            date_month = request.form['class']
            time.date = f"{form.date_day.data} {date_month}"
            time.id_film = form.id_film.data
            time.time = form.time.data
            time.price = form.price.data
        db_sess.add(time)
        db_sess.commit()
        return redirect('/')
    return render_template('time_add.html', title='Добавление расписание к фильму',
                           form=form)


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


def main():
    db_session.global_init("db/blogs.sqlite")
    db_sess = db_session.create_session()
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
