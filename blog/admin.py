from blog import db, admin
from blog.models import *
from blog.forms import PostForm
from blog.routes import save_picture
from flask import request, flash, redirect
from flask_admin import expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class UserView(ModelView):
    column_searchable_list = ['id','username', 'email']
    column_editable_list = ['username', 'email']
    column_list = ('id', 'username', 'email','img_file')

    def is_accessible(self):
        if current_user.is_authenticated:
            return True if current_user.username == 'Sahaj' else False
        else :
            return False

class PostView(ModelView):
    column_searchable_list = ['id','title']
    create_template = "admin/create_post.html"

    @expose('/new/', methods=('GET', 'POST'))
    def create_post(self):
        form = PostForm()
        if form.validate_on_submit():
            new_post = Post(title = form.title.data, content = form.content.data)
            db.session.add(new_post)
            for file in request.files.getlist("file"):
                pic = Photo(name = save_picture(file, "post_pics"), post = new_post)
                db.session.add(pic)
            db.session.commit()
            flash('Post Has Been Added', 'success')
            return redirect('/admin/post')

        return self.render('admin/create_post.html', form=form)

    def is_accessible(self):
        if current_user.is_authenticated:
            return True if current_user.username == 'Sahaj' else False
        else :
            return False

class PhotoView(ModelView):
    column_searchable_list = ['id']
    can_create = False
    can_edit = False
    column_list = ('id', 'name', 'post_id')

    def is_accessible(self):
        if current_user.is_authenticated:
            return True if current_user.username == 'Sahaj' else False
        else :
            return False

class CommentView(ModelView):
    column_searchable_list = ['id', 'comment']
    can_create = False
    can_edit = False
    column_list = ('id', 'comment', 'date_posted', 'post_id', 'author_id')

    def is_accessible(self):
        if current_user.is_authenticated:
            return True if current_user.username == 'Sahaj' else False
        else :
            return False

admin.add_view(UserView(User, db.session))
admin.add_view(PostView(Post, db.session))
admin.add_view(PhotoView(Photo, db.session))
admin.add_view(CommentView(Comments, db.session))
