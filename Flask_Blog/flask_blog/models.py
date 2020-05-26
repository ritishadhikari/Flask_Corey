from flask_blog import db,login_manager
from datetime import datetime

#UserMixin class looks into the user.is_authenticated ralated functionalities.
from flask_login import UserMixin


class User(db.Model,UserMixin):
    # The table name will be user
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    image_file=db.Column(db.String(20),nullable=False, default='default.jpeg')
    password=db.Column(db.String(60),nullable=False)
    posts=db.relationship('Post',backref='author',lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

#user loader is used for reloading the user from the userid stored in the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(ident=int(user_id))

class Post(db.Model):
    # The table name will be post
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    date_posted=db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    content=db.Column(db.Text, nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"
