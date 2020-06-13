from flask import Blueprint,render_template,request
from flask_blog.models import Post

main=Blueprint(name='main', import_name='__name_')


#localhost is the alias for 127.0.0.1
@main.route("/",methods=['GET'])
@main.route("/home",methods=['GET'])
def home():
    # Display all the posts. To display only the
    # users posts, we must replace it with current_user.posts
    #wall_post=Post.query.all()
    #We want to paginate
    page=request.args.get('page',1,type=int)
    '''
    wall_post will contain the list of posts
    for the particular page as passed.
    '''
    wall_post=Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5,page=page)
    return render_template('home.html',posts=wall_post,title='Home')

@main.route("/about")
def about():
    return render_template('about.html',title='About')
