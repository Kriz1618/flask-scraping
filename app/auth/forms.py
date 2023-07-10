from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.auth.models import User


def email_exist(form, field):
    email = User.query.filter_by(user_email=field.data).first()
    if email:
        raise ValidationError("Email already exists!!")
    

class RegistrationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(4,16, message="Between 4 and 16 characters")])
    email = StringField("Email", validators=[DataRequired(), Email(), email_exist])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo("confirm", message="Password must match")])
    confirm = PasswordField("confirm", validators=[DataRequired()])
    submit = SubmitField("Register", render_kw={"class": "btn btn-primary"})


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    stay_loggedin = BooleanField("Remember Me")
    submit = SubmitField("Login", render_kw={"class": "btn btn-primary"})

class ScrapyForm(FlaskForm):
    search_article = StringField("Article", validators=[DataRequired()])
    submit = SubmitField("Search Article", render_kw={"class": "btn btn-success"})
