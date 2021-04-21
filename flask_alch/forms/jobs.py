from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField
from wtforms import BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    job = StringField('Job Title', validators=[DataRequired()])
    team_leader = IntegerField("Team Leader id", validators=[DataRequired()])
    work_size = IntegerField("Work Size")
    collaborators = StringField("Collaborators")
    is_finished = BooleanField("Is job finished?")

    submit = SubmitField('Submit')