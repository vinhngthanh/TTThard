from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length

class AddPlayerForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email:', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Password:', validators=[DataRequired(), Length(min=8, max=30)])
    submit = SubmitField('Add User')

class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Password:', validators=[DataRequired(), Length(min=8, max=30)])
    submit = SubmitField('Login')

class DeletePlayerForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Password:', validators=[DataRequired(), Length(min=8, max=30)])
    submit = SubmitField("Delete User")