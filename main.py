from flask import Flask, render_template, request, abort, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail  # to send email through flask
from datetime import datetime
import json
import os
from werkzeug.utils import secure_filename
import math

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = True

app = Flask(__name__, template_folder='./templates', static_folder='./static')
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = params['upload_location']
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail_username'],
    MAIL_PASSWORD=params['gmail_password'],
)

mail = Mail(app)

if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']

else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)


class Contacts(db.Model):
    '''
    content of contacts table are sno, name, phone_num, msg, date, email
    '''

    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    email = db.Column(db.String(50), nullable=False)


class Posts(db.Model):
    '''
    content of contacts table are sno, title, slug, content, date
    '''

    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    subtitle = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(21), nullable=False)
    content = db.Column(db.String(1200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    img_file = db.Column(db.String(255), nullable=True)


@app.route("/")
def home():
    posts = Posts.query.filter_by().all()
    last = math.ceil(len(posts)/int(params['no_of_posts'])) #This will give us (total no of pages / how many posts we have on one page)
    page = (request.args.get('page'))  #getting page no from url
    if not str(page).isnumeric():
        page = 1
    page = int(page)
    posts = posts[(page-1)*int(params['no_of_posts']):(page-1)*int(params['no_of_posts']) + int(params['no_of_posts'])] #post slicing
    #pagination logic: list slicing You can also write it like j=(page-1)*int(params['no_of_posts']) and posts=posts[j:j+2]
    #When user on first page
    if page == 1:
        prev = "#"
        next = "/?page=" + str(page+1)

    # When user on last post
    elif page == last:
        prev = "/?page=" + str(page-1)
        next = "#"

    # When user on middle post
    else:
        prev = "/?page=" + str(page-1)
        next = "/?page=" + str(page+1)

    return render_template('index.html', params=params, posts=posts, prev=prev, next=next)


@app.route("/post/<string:post_slug>", methods=['get'])
def post_route(post_slug):
    print("this is my slug: " + post_slug)
    # post = Posts.query.filter_by(slug=post_slug).first()
    post = Posts.query.filter_by(slug=post_slug).first()
    # print(post)

    if post:
        return render_template('post.html', params=params, post=post)
    else:
        return abort(404)


@app.route("/about")
def about():
    return render_template('about.html', params=params)


# @app.route("/uploader", methods=['GET', 'POST'])
# def uploader():
#     if 'user' in session and session['user'] == params['admin_user']:
#         if request.method == 'POST':
#             f = request.files['file1']
#             f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
#             # print(secure_filename(f.filename), f.filename)
#             return "Uploaded successfully"


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        massage = request.form.get('massage')

        entry = Contacts(name=name, phone_num=phone, msg=massage, email=email,
                         date=datetime.now())  # LHS is a column of our database and RHS is input taken from user
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New massage from blog',
                          sender=params['gmail_username'],
                          recipients=[params['admin_gmail_username']],
                          body=massage + "\n" + phone + "\n" + email)

        mail.send_message('support.' + params['blog_name'], sender=params['gmail_username'],
                          recipients=[email], body="Thanks for contacting us")

    return render_template('contact.html', params=params)


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if 'user' in session and session['user'] == params['admin_user']:
        posts = Posts.query.all()
        return render_template('dashboard.html', params=params, posts=posts)

    if request.method == 'POST':
        username = request.form.get('uname')
        password = request.form.get("pass")
        # print(username)
        # print(password)
        if username == params['admin_user'] and password == params['admin_password']:
            session['user'] = username
            posts = Posts.query.all()
            return render_template('dashboard.html', params=params, posts=posts)

    return render_template('login.html', params=params)


@app.route("/edit/<string:sno>", methods=['GET', 'POST'])
def edit(sno):
    if 'user' in session and session['user'] == params['admin_user']:
        if request.method == 'POST':
            box_title = request.form.get('title')
            subtitle = request.form.get('subtitle')
            slug = request.form.get('slug')
            content = request.form.get('content')
            # img_file = request.form.get('img_file')
            date = datetime.now()
            f = request.files['file1']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            img_file = secure_filename(f.filename)
            print(img_file)

            if sno == '0':
                p1 = Posts(title=box_title, subtitle=subtitle, slug=slug, content=content, img_file=img_file,
                           date=date)
                db.session.add(p1)
                db.session.commit()
                return redirect('/dashboard')

            else:
                post = Posts.query.filter_by(sno=sno).first()
                post.title = box_title
                post.subtitle = subtitle
                post.slug = slug
                post.content = content
                post.img_file = img_file
                post.date = date
                db.session.commit()
                return redirect('/dashboard')

        post = Posts.query.filter_by(sno=sno).first()
        return render_template("edit.html", params=params, post=post)


@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/dashboard')


@app.route("/delete/<string:sno>")
def delete(sno):
    if 'user' in session and session['user'] == params['admin_user']:
        post = Posts.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
    return redirect('/dashboard')


if __name__ == '__main__':
    app.run(debug=True)
