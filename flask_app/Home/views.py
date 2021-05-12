import re
from flask import Blueprint,render_template,request,redirect,url_for,flash
from flask_app.models import Blog, User
from flask_app.extensions import db
from werkzeug.security import check_password_hash
from flask_login import login_user,logout_user,current_user,login_required

home = Blueprint('home',__name__,template_folder='templates/Home')

@home.route('/')
def home_view():
    blogs = Blog.query.all()
    context = {'blogs':blogs}
    return render_template('home.html',**context)

@home.route('/blog/<slug>')
def blog_view(slug):
    blog = Blog.query.filter_by(slug=slug).first()
    context = {'blog':blog}
    return render_template('blog.html',**context)

@home.route('/create',methods=['GET','POST'])
def create_blog_view():
    if not current_user.is_authenticated:
        return redirect(url_for('home.login'))
    if request.method == "POST":
        title = request.form['title']
        body = request.form['body']
        blog = Blog(
            title=title,
            body=body,
            author=current_user.id
        )
        db.session.add(blog)
        db.session.commit()
        return redirect(url_for('home.home_view'))
    return render_template('create.html')

@home.route('/register',methods=['GET','POST'])
def register():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        unhashed_password = request.form['password']
        user = User(username = username,
                    email=email,
                    unhashed_password=unhashed_password,
                    admin=False,
                    author=True)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home.login'))
    return render_template('register.html')

@home.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password,password):
            login_user(user)
            if current_user.admin:
                return redirect(url_for('admin.admin_view'))
            return redirect(url_for('home.home_view'))
        else:
            flash('Invalid credentials','danger')
            return redirect(url_for('home.login'))
    return render_template('login.html')

@home.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.login'))