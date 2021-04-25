import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Booking(SqlAlchemyBase):
    __tablename__ = 'booking'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_booking = sqlalchemy.Column(sqlalchemy.Integer)
    place = sqlalchemy.Column(sqlalchemy.Integer)
    price = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("time_table.id"))
    roww = sqlalchemy.Column(sqlalchemy.Integer)
    number = sqlalchemy.Column(sqlalchemy.String)
    time = sqlalchemy.Column(sqlalchemy.String)
    title = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.id"))
    name = sqlalchemy.Column(sqlalchemy.String)

    user = orm.relation('User')
    time_table = orm.relation('TimeTable')
