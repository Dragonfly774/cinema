import sqlalchemy
from sqlalchemy import orm, ARRAY

from .db_session import SqlAlchemyBase


class TimeTable(SqlAlchemyBase):
    __tablename__ = 'time_table'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_film = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("films.id"))
    date = sqlalchemy.Column(sqlalchemy.String)
    time = sqlalchemy.Column(sqlalchemy.String)
    price = sqlalchemy.Column(sqlalchemy.String)
    film = orm.relation('Films')

    booking = orm.relation("Booking", back_populates='price')
