from flask import Flask,render_template,redirect,url_for,request,session,abort,flash
from flask_login import login_required
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user,logout_user,LoginManager,login_required,logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import *
from flask_bcrypt import Bcrypt
import os
from models import *
from flask_mail import Mail,Message


app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_APP1_SECRET')
#configure Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER']= 'smtp.googlemail.com'
app.config['MAIL_PORT']= 587
app.config['MAIL_USE_TLS']= True
app.config['MAIL_USERNAME']= os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD']= os.environ.get('EMAIL_PASS')
db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
mail= Mail(app)
login_manager =LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category='info'


@login_manager.user_loader
def load_user(user_id):
    return visitor.query.get(user_id)


@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = registerForm()
    if form.validate_on_submit():
        #hashed_pwd = bcrypt.generate_password_hash(form.password.data)
        user = visitor(username=form.username.data, email=form.email.data,password=form.password.data)
        db.session.add(user)
        db.session.commit() 
        flash('Your account has been created','success')
        return redirect(url_for('login')) 
    return render_template('register.html',form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = loginForm()    
    if form.validate_on_submit():
        #verify the email
        user= visitor.query.filter_by(email=form.email.data).first()
        #verify password
        if user:
            if check_password_hash(user.password,form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
            #next_page = request.args.get('next')
            #return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        flash('Login unsuccessful,check your email or password','danger')    
    return render_template("login.html", form=form)
    
@app.route("/dashboard")
@login_required    
def dashboard():
    return render_template("dashboard.html")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
    
#Sending password reset email
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset request', sender='no-reply@milestone.com',
    recipients=[user.email])
    msg.body = f'''To reset your password click the following link:
    {url_for('reset_token',token=token, external=True)}
    Ignore the mail if you did not make any request'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user= visitor.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with reset Instructions','info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)  


@app.route("/reset_password/<token>",methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = visitor.verify_reset_token(token)
    if user is None:
        flash('Token Expired or Invalid Token','warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        #hashed_pwd = bcrypt.generate_password_hash(form.password.data)
        user.password = form.password.data
        db.session.commit() 
        flash('Your Password has been reset>you can now login','success')
        return redirect(url_for('login')) 
    return render_template('reset_token.html', title='Reset Password', form=form) 

if __name__== "__main__":
    app.run(debug=True)    
