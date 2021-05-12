from flask import Blueprint,render_template,redirect,url_for
from flask_app.models import User,Blog
from flask_login import current_user,login_required
from flask_app.extensions import db

admin = Blueprint('admin',__name__,template_folder='templates/Admin',url_prefix='/admin')

@admin.route('/')
@login_required
def admin_view():
    if not current_user.admin:
        return redirect(url_for('home.login'))
    no_of_users = User.query.count()
    no_of_blogs = Blog.query.count()
    context = {
        'no_of_users':no_of_users,
        'no_of_blogs':no_of_blogs
    }
    return render_template('admin.html',**context)

@admin.route('/user')
@login_required
def admin_user_view():
    if not current_user.admin:
        return redirect(url_for('home.login'))
    users = User.query.all()
    context = {'users':users}
    return render_template('user.html',**context)

@admin.route('/user/<id>',methods=['GET','DELETE'])
@login_required
def admin_user_delete_view(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin.admin_user_view'))

@admin.route('/blogs')
@login_required
def admin_blogs_view():
    if not current_user.admin:
        return redirect(url_for('home.login'))
    blogs = Blog.query.all()
    context = {'blogs':blogs}
    return render_template('blogs.html',**context)

@admin.route('/blog/<id>',methods=['GET','DELETE'])
@login_required
def admin_blog_delete_view(id):
    blog = Blog.query.get(id)
    db.session.delete(blog)
    db.session.commit()
    return redirect(url_for('admin.admin_blogs_view'))