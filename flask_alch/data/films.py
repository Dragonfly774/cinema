import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Films(SqlAlchemyBase):
    __tablename__ = 'films'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    actors = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    age = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    collapse = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    countries = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    directors = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    frames = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    genres = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    id_kinopoisk = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    link_img = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    premiere_word = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    producers = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    rating_imdb = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    rating_kinopoisk = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    time = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    timetable = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("time_table.id"))

    time_table = orm.relation('TimeTable')
    # user_id = sqlalchemy.Column(sqlalchemy.Integer,
    #                             sqlalchemy.ForeignKey("users.id"))
    # user = orm.relation('User')

    # categories = orm.relation("Category",
    #                           secondary="association",
    #                           backref="news")