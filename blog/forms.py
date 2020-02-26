from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from blog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confim Password', validators = [DataRequired(), EqualTo('password')])
    register = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This Username Is Already Taken')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('This Email Is Already Taken')


class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators = [DataRequired()])
    remember = BooleanField('Remember Me')
    login = SubmitField('Log In')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=10, max=200)])
    content = TextAreaField('Content', validators=[DataRequired()])
    file = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    post = SubmitField('Post')

class CommentForm(FlaskForm):
    comment = StringField('Comment', validators=[DataRequired(), Length(min=1, max=100)])
    submit = SubmitField('Submit')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators = [DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    update = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This Username Is Already Taken')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('This Email Is Already Taken')

class RequestResetForm(FlaskForm):
    email = StringField('Email',validators = [DataRequired(), Email()])
    submit = SubmitField('Request Password Reset ')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is None:
            raise ValidationError('There is no account with that email. Yot mest register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confim Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

