from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import (StringField, PasswordField,
                    SubmitField, BooleanField)
from wtforms.validators import (DataRequired,Length,
                                Email, EqualTo, ValidationError)
from flask_blog.models import User
from flask_login import current_user



class RegistrationForm(FlaskForm):
    username=StringField(label='Username',
                        validators=[DataRequired(), Length(min=3, max=20, message=None)])
    email=StringField(label='Email', validators=[DataRequired(), Email()])
    password=PasswordField(label='Password', validators=[DataRequired()])
    confirm_password=PasswordField(label='Confirm_Password',
                                    validators=[DataRequired(), EqualTo(fieldname='password')])
    submit=SubmitField(label='Sign Up')


    def validate_username(self,username):
        '''
        Function to validate whether the username so typed in the regitration form
        already exists in the flask database. If the username happens to be existing,
        already, then a validation error should be given.
        '''
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That Username is Taken.\
                                   Please choose a different username.")

    def validate_email(self,email):
        '''
        Function to validate whether the email so typed in the registration form
        already exists in the flask database. If the username happens to be existing,
        already, then a validation error should be given.
        '''
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That Email is Taken.\
                                   Please choose a different username.")

class LoginForm(FlaskForm):
    email=StringField(label='Email', validators=[DataRequired(), Email()])
    password=PasswordField(label='Password', validators=[DataRequired()])
    remember=BooleanField(label='Remember Me')
    submit=SubmitField(label='Login')

class UpdateAccountForm(FlaskForm):
    username=StringField(label='Username',
                        validators=[DataRequired(), Length(min=3, max=20, message=None)])
    email=StringField(label='Email', validators=[DataRequired(), Email()])
    picture=FileField(label='Update Profile Picture',
                   validators=[FileAllowed(upload_set=['jpeg','jpg','png'])])
    submit=SubmitField(label='Update')
    def validate_username(self,username):
        '''
        Function to validate whether the username so typed in the registration form
        already exists in the flask database. If the username happens to be existing,
        already, then a validation error should be given.
        '''
        if username.data==current_user.username:
            current_user.username=username.data
        else:
            user=User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("That Username is Taken.\
                                       Please choose a different username.")

    def validate_email(self,email):
        '''
        Function to validate whether the email so typed in the registration form
        already exists in the flask database. If the username happens to be existing,
        already, then a validation error should be given.
        '''
        if email.data==current_user.email:
            current_user.email=email.data
        else:
            user=User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("That Email is Taken.\
                                       Please choose a different email.")


class RequestResetForm(FlaskForm):
    email=StringField(label='Email', validators=[DataRequired(), Email()])
    submit=SubmitField(label='Request Password Reset')

    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("No Account Exists.\
                                   You must register First.")

class ResetPasswordForm(FlaskForm):
    password=PasswordField(label='Password', validators=[DataRequired()])
    confirm_password=PasswordField(label='Confirm_Password',
                                    validators=[DataRequired(), EqualTo(fieldname='password')])
    submit=SubmitField(label='Reset Password')
