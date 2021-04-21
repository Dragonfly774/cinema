import requests
from pprint import pprint
from data import db_session
from data.films import Films

db_session.global_init("db/blogs.sqlite")
db_sess = db_session.create_session()
# data = {
#     'actors': data_film['actors'],
#     'age': data_film['age'],
#     'collapse': data_film['collapse'],
#     'countries': data_film['countries'],
#     'description': data_film['description'],
#     'directors': data_film['directors'],
#     'frames': data_film['frames'],
#     'genres': data_film['genres'],
#     'id': data_film['id'],
#     'id_kinopoisk': data_film['id_kinopoisk'],
#     'poster': data_film['poster'],
#     'premiere_world': data_film['premiere_world'],
#     'rating_imdb': data_film['rating_imdb'],
#     'rating_kinopoisk': data_film['rating_kinopoisk'],
#     'title': data_film['title'],
#     'year': data_film['year'],
#     'time': data_film['collapse']['duration'],
#     'producers': data_film['producers']
#
# }
# "1249198", "1109271", "8062", "1262160", "1239328", "1236795",
film = [ "1445243", "1309596", "688609"]
for i in film:
    response = requests.get(f"https://api.kinopoisk.cloud/movies/{i}/token/0d12aad940f6c3a4cdd54cfce1d9e1b9")
    # pprint(response.json())
    data_film = response.json()
    # print(data_film)
    # actors = data_film['actors']
    # print(data_film['age'])

    film = Films()
    film.link_img = data_film['poster']
    film.title = data_film['title']
    # film.actors = actors
    film.age = data_film['age']
    # film.collapse = data_film['collapse']
    film.countries = ", ".join(data_film['countries'])
    film.description = data_film['description']
    film.directors = ", ".join(data_film['directors'])
    # film.frames = ", ".join(data_film['frames'])
    film.genres = ", ".join(data_film['genres'])
    film.id_kinopoisk = data_film['id_kinopoisk']
    film.premiere_world = data_film['premiere_world']
    film.rating_imdb = data_film['rating_imdb']
    film.rating_kinopoisk = data_film['rating_kinopoisk']
    film.year = data_film['year']
    film.time = data_film['collapse']['duration']
    film.producers = ", ".join(data_film['producers'])

    db_sess.add(film)
    db_sess.commit()
