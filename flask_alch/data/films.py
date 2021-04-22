import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.dialects import sqlite

from .db_session import SqlAlchemyBase


class Films(SqlAlchemyBase):
    __tablename__ = 'films'
    s = sqlite
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    actors = sqlalchemy.Column(sqlalchemy.String())
    age = sqlalchemy.Column(sqlalchemy.String)
    genres = sqlalchemy.Column(sqlalchemy.String())
    id_kinopoisk = sqlalchemy.Column(sqlalchemy.Integer)
    link_img = sqlalchemy.Column(sqlalchemy.String)
    rating_imdb = sqlalchemy.Column(sqlalchemy.Integer)
    rating_kinopoisk = sqlalchemy.Column(sqlalchemy.Integer)
    time = sqlalchemy.Column(sqlalchemy.String())


    timetable = orm.relation("TimeTable", back_populates='film')
    # user_id = sqlalchemy.Column(sqlalchemy.Integer,
    #                             sqlalchemy.ForeignKey("users.id"))
    # user = orm.relation('User')

    # categories = orm.relation("Category",
    #                           secondary="association",
    #                           backref="news")