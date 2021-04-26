import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class TimeTable(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'time_table'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    # id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_film = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("films.id"))
    date = sqlalchemy.Column(sqlalchemy.String)
    time = sqlalchemy.Column(sqlalchemy.String)
    price = sqlalchemy.Column(sqlalchemy.String)
    film = orm.relation('Films')
