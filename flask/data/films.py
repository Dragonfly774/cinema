import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Films(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'films'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    genres = sqlalchemy.Column(sqlalchemy.String)
    id_kinopoisk = sqlalchemy.Column(sqlalchemy.Integer)
    link_img = sqlalchemy.Column(sqlalchemy.String)
    age = sqlalchemy.Column(sqlalchemy.String)

    timetable = orm.relation("TimeTable", back_populates='film')

    # categories = orm.relation("Category",
    #                           secondary="association",
    #                           backref="news")
