from flask import Blueprint
from flask import (render_template, url_for, flash,
                redirect, request,abort)
from flask_blog import db
from flask_blog.models import Post
from flask_blog.posts.forms import (PostForm)
from flask_login import (current_user,login_required)


posts=Blueprint(name='posts', import_name='__name_')

@posts.route("/post/new", methods=['GET','POST'])
@login_required
def new_post():
    form=PostForm()
    if form.validate_on_submit():
        post=Post(title=form.title.data,
                  content=form.content.data,
                  user_id=current_user.id)
                  #author=current_user, #can also use this.
        db.session.add(post)
        db.session.commit()
        flash(message='Post Creation Successful', category='success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html',title='New Post',form=form,
                            legend='New Post')

@posts.route("/post/<int:post_id>")
def post(post_id):
    post=Post.query.get_or_404(ident=post_id)
    return render_template('post.html',title=post.title,post=post)

@posts.route("/post/<int:post_id>/update", methods=['GET','POST'])
@login_required
def update_post(post_id):
    post=Post.query.get_or_404(ident=post_id)
    if current_user!=post.author:
        abort(403)
    else:
        form=PostForm()
        if form.validate_on_submit():
            post.title=form.title.data
            post.content=form.content.data
            db.session.commit()
            flash("Your Post have been updated", category='success')
            return redirect(url_for('posts.post',post_id=post.id))
        elif request.method=='GET':
            form.title.data=post.title
            form.content.data=post.content
            return render_template('create_post.html',title='Update Post',
            form=form,legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post=Post.query.get_or_404(ident=post_id)
    if current_user!=post.author:
        abort(403)
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Your Post have been Deleted", category='success')
        return redirect(url_for('main.home'))
