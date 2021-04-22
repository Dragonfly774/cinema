from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField
from wtforms import BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class ScheduleForm(FlaskForm):
    id_film = IntegerField('Id Фильма', validators=[DataRequired()])
    time = StringField("Время начало и конца фильма", validators=[DataRequired()])
    price = StringField("Цена билета", validators=[DataRequired()])
    hall = StringField("Номер зала", validators=[DataRequired()])
    date = StringField("Дата", validators=[DataRequired()])

    submit = SubmitField('Сохранить')