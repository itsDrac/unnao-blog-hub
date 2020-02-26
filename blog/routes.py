import os
import secrets
from PIL import Image
from flask import render_template, redirect, url_for, flash, request
from blog import app, db, bcrypt, mail
from blog.models import *
from blog.forms import *
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("index.html", posts=posts)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f"Logged In","success")
            return redirect(next_page) if next_page else redirect(url_for("index"))
        else:
            flash("Login Unsuccessful, Check Username or Password","danger")
    return render_template("login.html",form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}! You may login now","success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route('/About')
def about():
    return render_template("about.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

def save_picture(form_picture, folder):
    random_hex = secrets.token_hex(16)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', folder, picture_fn)
    
    output_size = (700, 700)
    img = Image.open(form_picture)
    img.thumbnail(output_size)

    img.save(picture_path)
    return picture_fn

@app.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data,"profile_pics")
            current_user.img_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account Updated', 'info')
        return redirect(url_for('account'))
    image_file = url_for('static', filename='images/profile_pics/' + current_user.img_file)
    print (image_file)
    return render_template("account.html", image_file=image_file, form=form)

@app.route('/comment/<int:post_id>', methods =['GET','POST'])
def comment(post_id):
    form = CommentForm()
    post = Post.query.get(int(post_id))
    print (current_user)
    if form.validate_on_submit():
        comment = Comments(comment = form.comment.data, post = post, author = current_user)
        db.session.add(comment)
        db.session.commit()
        return redirect('/comment/'+str(post_id))
    return render_template('comment.html', form=form, post=post)

def send_reset_email(user):
    token = user.get_reset_token()
    print(f"token is {token}")
    msg = Message('Password Rest Request', sender='gpt.sahaj28@gmail.com', recipients=[user.email])
    msg.body='''To Reset your password, visit the following link:
<resetlink>

If you did not make this request then simply ignore this email and no changes will be made
'''
    mail.send(msg)

@app.route('/reset_password', methods = ['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RequestResetForm()
    if form.validate_on_submit():
        print (form.validate_on_submit())
        user=User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        print ("line 119")
        flash('An email has been sent with instruction to reset your password','info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', form=form)

@app.route('/reset_password/<token>', methods = ['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token','warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f"Your Password has been updated! You may login now","success")
        return redirect(url_for("login"))
    return render_template('reset_token.html', form=form)