from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField
from wtforms import BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length


class Booking(FlaskForm):
    rov = IntegerField('Номер(а) ряда(ов)', validators=[DataRequired()])
    place = StringField("Номер(а) мест(а)", validators=[DataRequired()])
    count = IntegerField('количество билетов', validators=[DataRequired()])
    submit = SubmitField('Готово')
