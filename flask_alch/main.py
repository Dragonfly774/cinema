import os
import datetime

from flask import Flask, render_template, redirect, request, make_response, session, abort, flash
from data import db_session

from data.users import User
from data.news import News
from data.jobs import Jobs
from data.films import Films
from data.time_table import TimeTable

from forms.user import RegisterForm
from waitress import serve

from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from forms.loginform import LoginForm
from forms.jobs import JobsForm
from forms.news import NewsForm
from forms.schedule import ScheduleForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

#  инициализируем LoginManager
login_manager = LoginManager()
login_manager.init_app(app)


def add_users(db):
    db_sess = db

    user = User()
    user.name = "Ridley"
    user.surname = "Scott"
    user.age = 21
    user.position = "captain"
    user.speciality = "research engineer"
    user.address = "module_1"
    user.email = "scott_chief@mars.org"
    db_sess.add(user)

    user2 = User()
    user2.name = "Ilon"
    user2.surname = "DontMask"
    user2.age = 45
    user2.position = "sailor"
    user2.speciality = "engineer"
    user2.address = "module_1"
    user2.email = "ilon_mars@mars.org"
    db_sess.add(user2)

    user3 = User()
    user3.name = "NoName"
    user3.surname = "NoName"
    user3.age = 19
    user3.position = "sailor"
    user3.speciality = "No"
    user3.address = "module_2"
    user3.email = "NoName@mars.org"
    db_sess.add(user3)

    user4 = User()
    user4.name = "Saimon"
    user4.surname = "Romanov"
    user4.age = 16
    user4.position = "chief assistant"
    user4.speciality = "robotics engineer"
    user4.address = "module_1"
    user4.email = "mars_bez_putina@mars.org"
    db_sess.add(user4)

    user5 = User()
    user5.name = "404"
    user5.surname = "404"
    user5.age = 404
    user5.position = "sailor"
    user5.speciality = "kettle"
    user5.address = "module_3"
    user5.email = "404_kettle@mars.org"
    db_sess.add(user5)

    db_sess.commit()


def add_films(db):
    db_sess = db

    # film = Films()
    # film.link_img = "https://img06.rl0.ru/kassa/c128x192q80i/kassa.rambler.ru/s/StaticContent/P/Aimg/2103/24/210324205026182.jpg"
    # film.title = "Отец"
    # db_sess.add(film)
    #
    # film = Films()
    # film.link_img = "https://img05.rl0.ru/kassa/c128x192q80i/kassa.rambler.ru/s/StaticContent/P/Aimg/2103/20/210320081016449.jpg"
    # film.title = "Чернобыль"
    # db_sess.add(film)
    #
    # film = Films()
    # film.link_img = "https://img09.rl0.ru/kassa/c128x192q80i/kassa.rambler.ru/s/StaticContent/P/Aimg/2103/20/210320081018655.jpg"
    # film.title = "Мортал Кобмат"
    # db_sess.add(film)

    film = Films()
    film.link_img = "https://img05.rl0.ru/kassa/c128x192q80i/kassa.rambler.ru/s/StaticContent/P/Aimg/2103/31/210331095026517.jpg"
    film.title = "Гнев человеческий"
    db_sess.add(film)

    film = Films()
    film.link_img = "https://img03.rl0.ru/kassa/c128x192q80i/kassa.rambler.ru/s/StaticContent/P/Aimg/2103/18/210318195031411.jpg"
    film.title = "Майор Гром: Чумной Доктор"
    db_sess.add(film)

    film = Films()
    film.link_img = "https://img01.rl0.ru/kassa/c128x192q80i/kassa.rambler.ru/s/StaticContent/P/Aimg/2104/09/210409051514277.jpg"
    film.title = "От винта 2"
    db_sess.add(film)

    film = Films()
    film.link_img = "https://img01.rl0.ru/kassa/c128x192q80i/kassa.rambler.ru/s/StaticContent/P/Aimg/2103/25/210325210045208.jpg"
    film.title = "100% Волк"
    db_sess.add(film)
    db_sess.commit()


@login_manager.user_loader
def load_user(user_id):
    """Для верной работы flask-login
    у нас должна быть функция для
    получения пользователя, украшенная
    декоратором login_manager.user_loader"""
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
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


@app.route('/booking/<int:id>', methods=['GET', 'POST'])
def booking(id):
    db_sess = db_session.create_session()
    film = db_sess.query(Films).filter(Films.id == id
                                       ).first()
    films = db_sess.query(Films)
    times = db_sess.query(TimeTable)
    user = db_sess.query(User).first()
    if film:
        pass
        # db_sess.delete(film)
        # db_sess.commit()
    else:
        abort(404)
    # return redirect('/')
    return render_template("3.html", films=films, times=times, user=user)


@app.route("/")
@app.route("/index", methods=['GET', 'POST'])
def index():
    """авторизованного пользователя отображались и его личные записи."""
    db_sess = db_session.create_session()
    films = db_sess.query(Films)
    times = db_sess.query(TimeTable)
    user = db_sess.query(User).first()
    buttons = [int(i) for i in range(1, 31)]
    column = [int(i) for i in range(1, 5)]
    # print(datetime.datetime.now())
    # day_standart = datetime.datetime.now().date()
    # day_month = (datetime.datetime.now().day, datetime.datetime.now().month)
    # а = request.form.get('checkbox-btn-group')
    # print(a)
    if request.method == 'POST':
        print(request.form.get('checkbox-btn-group'))
    # id = 0
    # if request.method == 'POST':
    #     id = request.form.get('checkbox-btn-group')
    #     print(request.form.get('checkbox-btn-group'))
    return render_template("2.html", films=films, times=times, user=user, buttons=buttons, column=column)


@app.route("/tt", methods=['GET', 'POST'])
def t():
    """авторизованного пользователя отображались и его личные записи."""
    db_sess = db_session.create_session()
    films = db_sess.query(Films)
    times = db_sess.query(TimeTable)
    user = db_sess.query(User).first()

    # day_standart = datetime.datetime.now().date()
    # day_month = (datetime.datetime.now().day, datetime.datetime.now().month)
    # а = request.form.get('checkbox-btn-group')
    # print(a)
    id = 0
    if request.method == 'POST':
        id = request.form.get('checkbox-btn-group')
    print(request.form.get('ac'))
        # return render_template("2.html", id=id)
    return render_template("2.html", id=id)


# @app.route("/admin")
# def admin():
#     """авторизованного пользователя отображались и его личные записи."""
#     form = LoginForm()
#     if form.validate_on_submit():
#         db_sess = db_session.create_session()
#         user = db_sess.query(User).filter(User.email == form.email.data).first()
#         if user and user.check_password(form.password.data):
#             login_user(user, remember=form.remember_me.data)
#             return redirect("/")
#         return render_template('admin.html',
#                                message="Неправильный логин или пароль",
#                                form=form)
#     return render_template('admin.html', form=form)

# @app.route("/")
# @app.route("/index")
# def index():
#     """авторизованного пользователя отображались и его личные записи."""
#     db_sess = db_session.create_session()
#     films = db_sess.query(Films)
#     times = db_sess.query(TimeTable)
#     user = db_sess.query(User).first()
#     print(datetime.datetime.now())
#     day_standart = datetime.datetime.now().date()
# day_month = datetime.datetime.now().day()
# if current_user.is_authenticated:
#     news = db_sess.query(News).filter(
#         (News.user == current_user) | (News.is_private != True))
# else:
#     news = db_sess.query(News).filter(News.is_private != True)
# # res = make_response(render_template("index.html", news=news))
# # res.set_cookie("visits_count", '1', max_age=60 * 60 * 24 * 365 * 2)
# return render_template("index.html", news=news, jobs=jobs)
# return render_template("2.html", films=films, times=times, user=user)

@app.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule():
    form = ScheduleForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        time = TimeTable()
        time.id_film = form.id_film.data
        time.time = form.time.data
        time.price = form.price.data
        time.hall = form.hall.data
        time.date = form.date.data
        db_sess.add(time)
        db_sess.commit()
        return redirect('/')
    return render_template('time_add.html', title='Добавление расписание к фильму',
                           form=form)


@app.route("/t")
@app.route("/jobs")
def table_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs)
    return render_template("table_jobs.html", jobs=jobs)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
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
        # return redirect('/t')
    return render_template('register.html', title='Регистрация', form=form)


# @app.route("/c")
# @app.route("/cookie_test")
# def cookie_test():
#     visits_count = int(request.cookies.get("visits_count", 0))
#     if visits_count:
#         res = make_response(
#             f"Вы пришли на эту страницу {visits_count + 1} раз")
#         res.set_cookie("visits_count", str(visits_count + 1),
#                        max_age=60 * 60 * 24 * 365 * 2)
#     else:
#         res = make_response(
#             "Вы пришли на эту страницу в первый раз за последние 2 года")
#         res.set_cookie("visits_count", '1',
#                        max_age=60 * 60 * 24 * 365 * 2)
#     return res

@app.route("/s")
@app.route("/session_test")
def session_test():
    """session.pop('visits_count', None) delete session"""
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")


def main():
    db_session.global_init("db/blogs.sqlite")
    db_sess = db_session.create_session()
    # add_users(db_sess)
    # add_films(db_sess)
    # add_jobs(db_sess)
    # add_news(db_sess)

    # news.categories.remove(category) Чтобы удалить категорию у новости, достаточно сделать:

    app.run(port=8080, host='127.0.0.1')

    # app.run(port=5000, host='0.0.0.0')

    # app.run(port=port, host="0.0.0.0")
    #
    # # с дефаултными значениями будет не более 4 потов
    # port = int(os.environ.get('PORT', 5000))
    # serve(app, port=port, host="0.0.0.0")


if __name__ == '__main__':
    main()

"""git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/Dragonfly774/flask_alch.git
git push -u origin main"""
