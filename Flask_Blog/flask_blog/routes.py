from flask import render_template, url_for, flash, redirect, request
from flask_blog import app, db, bcrypt
from flask_blog.models import Post,User
from flask_blog.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required


posts=[
{
 'author':'Corey Schafer',
 'title':'Blog Post 1',
 'content':'First Post Content',
 'date_posted':'April 20, 2018'
},
{
'author':'Jane Doe',
'title':'Blog Post 2',
'content':'Second Post Content',
'date_posted':'April 21, 2018'
}
]

#localhost is the alias for 127.0.0.1
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',posts=posts)

@app.route("/about")
def about():
    return render_template('about.html',title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,
                  email=form.email.data,
                  password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created. You Can now login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/loginuser", methods=['GET','POST'])
def login():
    #incase the user is trying to login although he has been authentcated, then route him
    #to the home page
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=LoginForm()
    if form.validate_on_submit():
        #check if user exists with the email address:
        user=User.query.filter_by(email=form.email.data).first()
        password_hashed=user.password
        if user and bcrypt.check_password_hash(pw_hash=password_hashed, password=form.password.data):
            login_user(user=user, remember=form.remember.data)
            nextpage=request.args.get('next')
            flash(message=f"Login Successfull for {form.email.data}", category='success')
            return redirect(nextpage) if nextpage else redirect(url_for('home'))
        else:
            flash(message="Login Unsuccessful. Please Check Email and Password", category='danger')
            return(redirect(url_for("home")))
    return render_template('login.html',title='Login',form=form)

#logout and return to home
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html',title=account)
