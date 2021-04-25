from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField
from wtforms.fields.html5 import EmailField, IntegerField
from wtforms.validators import DataRequired, Length


class FilmsForm(FlaskForm):
    title = StringField("Название", validators=[DataRequired()])
    img = StringField("Ссылка на постер", validators=[DataRequired()])
    genres = StringField("Жанры", validators=[DataRequired()])
    age = StringField("Возраст", validators=[DataRequired()])
    submit = SubmitField('Submit')