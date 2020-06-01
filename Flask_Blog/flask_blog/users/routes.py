from flask import Blueprint

from flask import (render_template, url_for, flash,
                redirect, request)
from flask_blog import  db, bcrypt
from flask_blog.models import Post,User
from flask_blog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                            RequestResetForm, ResetPasswordForm)
from flask_login import (login_user, current_user,
                        logout_user, login_required)
from flask_blog.users.utils import save_picture, send_reset_email

users=Blueprint(name='users', import_name='__name_')

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,
                  email=form.email.data,
                  password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created. You Can now login', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route("/loginuser", methods=['GET','POST'])
def login():
    #incase the user is trying to login although he has been authentcated, then route him
    #to the home page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form=LoginForm()
    if form.validate_on_submit():
        #check if user exists with the email address:
        user=User.query.filter_by(email=form.email.data).first()
        password_hashed=user.password
        if user and bcrypt.check_password_hash(pw_hash=password_hashed, password=form.password.data):
            login_user(user=user, remember=form.remember.data)
            nextpage=request.args.get('next')
            flash(message=f"Login Successfull for {form.email.data}", category='success')
            return redirect(nextpage) if nextpage else redirect(url_for('main.home'))
        else:
            flash(message="Login Unsuccessful. Please Check Email and Password", category='danger')
            return(redirect(url_for("main.home")))
    return render_template('login.html',title='Login',form=form)

#logout and return to home
@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account",methods=['GET','POST'])
@login_required
def account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file=save_picture(form_picture=form.picture.data)
            current_user.image_file=picture_file
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash(message="Details have been Updated", category="success")
        redirect(url_for('users.account'))
    elif request.method=='GET':
        form.username.data=current_user.username
        form.email.data=current_user.email
    image_file=url_for(endpoint='static',filename='profile_pics/' + current_user.image_file)
    print(image_file)
    return render_template('account.html',title=account,
                            image_file=image_file,form=form)


@users.route("/user/<string:username>",methods=['GET'])
def user_posts(username):
    page=request.args.get('page',1,type=int)
    user=User.query.filter_by(username=username).first_or_404()
    wall_post=Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(per_page=2,page=page)
    return render_template('user_posts.html',posts=wall_post,user=user)


@users.route("/reset_password",methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    else:
        form=RequestResetForm()
        if form.validate_on_submit():
            user=User.query.filter_by(email=form.email.data).first()
            send_reset_email(user)
            flash(message=f"Password reset instruction sent to {form.email.data}", category='info')
            redirect(url_for('users.login'))
        return render_template('reset_request.html',title='Verify Username', form=form)

@users.route("/reset_password/<token>",methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    else:
        user=User.verify_reset_token(token=token)

    if user is None:
        flash(message='Invalid or expired Token Supplied', category='warning')
        return redirect(url_for('users.reset_request'))
    else:
        form=ResetPasswordForm()
        if form.validate_on_submit():
            hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.password=hashed_password
            db.session.commit()
            flash(f'Password has been updated. You can now able to Login', 'success')
            return redirect(url_for('users.login'))
        return render_template('reset_token.html',title='Reset Password',form=form)
