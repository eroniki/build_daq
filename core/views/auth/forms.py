from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email, Length
from core.models import User


class SignupForm(FlaskForm):
    name = StringField('Name',
                       validators=[
                           DataRequired(),
                           Length(min=1, max=64)
                       ])
    email = StringField('Email',
                        validators=[
                            DataRequired(),
                            Email(),
                            Length(min=1, max=64)
                        ])
    password = PasswordField('Password',
                             validators=[
                                 DataRequired(),
                                 Length(min=6, max=32)
                             ])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[
                                         DataRequired(),
                                         EqualTo('password')
                                     ])
    submit = SubmitField('Create account')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('The email address is already taken, please try again!')  # noqa


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[
                            DataRequired(),
                            Email()
                        ])
    password = PasswordField('Password',
                             validators=[
                                 DataRequired()
                             ])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')
