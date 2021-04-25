from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField, IntegerField
from wtforms.validators import DataRequired, Length


class BookingForm(FlaskForm):
    # row = StringField('Номер(а) ряда(ов) (через пробел)', validators=[DataRequired()])
    # place = StringField("Номер(а) мест(а) (через пробел)", validators=[DataRequired()])
    # count = IntegerField('Количество билетов', validators=[DataRequired()])
    number = StringField('Номер телефона', validators=[DataRequired(), Length(min=10, max=13)])
    name = StringField("Имя", validators=[DataRequired()])
    # email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Готово')
