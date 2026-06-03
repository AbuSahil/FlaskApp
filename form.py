from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField , TextAreaField
from wtforms.validators import DataRequired, Email

class MyForm(FlaskForm):
    
    name = StringField("Name of the Candidate", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email(message="Invalid email address")])
    bio = TextAreaField("Bio", validators=[DataRequired()])
    submit = SubmitField("Submit")