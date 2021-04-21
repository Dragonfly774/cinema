import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class TimeTable(SqlAlchemyBase):
    __tablename__ = 'time_table'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    time = sqlalchemy.Column(sqlalchemy.String)
    price = sqlalchemy.Column(sqlalchemy.String)
    hall = sqlalchemy.Column(sqlalchemy.Integer)
    date = sqlalchemy.Column(sqlalchemy.String)
    films = orm.relation("Films", back_populates='time_table')
