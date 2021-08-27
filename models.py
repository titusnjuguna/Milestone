#Import required packages
from flask import Flask,render_template,redirect,url_for,request,session,abort,flash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    UserMixin, login_user,LoginManager,login_required,logout_user,current_user)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import *
import os
import app

app = Flask(__name__)
#configure Database
app.config['SQLALCHEMY_DATABASE_URI'] = " postgresql://tito:208251001@localhost:5432/Wira_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)

#create model
class visitor(db.Model,UserMixin):
    __tablename__="visitors"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(30))
    email = db.Column(db.String(20))
    password = db.Column(db.String())
    def __init__(self,username,email,password):
        self.username= username
        self.email = email
        self.password = generate_password_hash(password)
    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.password}')"  
    #decrypt password during login in
    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd) 
    def get_reset_token(self,expires_sec=2400):
        s = Serializer(app.config['SECRET_KEY'],expires_sec) 
        return s.dumps({'user_id':self.id}).decode('utf-8')  
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return visitor.query.get(user_id)         


    
   


       