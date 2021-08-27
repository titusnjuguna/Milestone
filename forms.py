from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField
from wtforms.fields.core import BooleanField
from wtforms.validators import DataRequired, InputRequired, Length , EqualTo, ValidationError
from models import visitor



class registerForm(FlaskForm):
    username = StringField('username_label',validators=[InputRequired(message="Username is required"),
               Length(min=5, max=30,message="Username must be between 5 and 29 characters")])
    email =  StringField('email_label',
            validators=[InputRequired(message="Email is required"),
            Length(min=20, max=70,message="Email must be between 20 and 69 characters")])
    password = PasswordField('password_label',
                validators=[InputRequired(message="Password is required"),
                Length(min=5, max=30,message="Password must be between 5 and 29 characters")])
    confirm_password = PasswordField('password_field',
                        validators=[InputRequired(message="Password is required"),
                        EqualTo('password',message="password must match")])
    submit_button = SubmitField("Create Account")
   
    def validate_username(self, username):
        user = visitor.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken')
    def validate_email(self, email):
        user = visitor.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already taken')            
        




class loginForm(FlaskForm):
    email =  StringField('email_label',validators=[InputRequired(message="Email is required"),
            Length(min=20, max=70,message="Email must be between 20 and 69 characters")])
    password = PasswordField('password_label', validators=[InputRequired(message="Password is required")]) 
    submit_button = SubmitField("login")
    Remember_Me = BooleanField()

class RequestResetForm(FlaskForm):
    email =  StringField('email_label',validators=[InputRequired(message="Email is required"),
            Length(min=20, max=70,message="Email must be between 20 and 69 characters")])
    submit_button = SubmitField("Request Password Reset")   

    def validate_email(self, email):
        user = visitor.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Email doesnt Exist') 

class ResetPasswordForm(FlaskForm):
    password = PasswordField('password_label',
                validators=[InputRequired(message="Password is required"),
                Length(min=5, max=30,message="Password must be between 5 and 29 characters")])
    confirm_password = PasswordField('password_field',
                        validators=[InputRequired(message="Password is required"),
                        EqualTo('password',message="password must match")])
    submit_button = SubmitField("Reset Password ")                    
