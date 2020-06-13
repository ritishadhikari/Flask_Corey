from flask_blog import db,login_manager
from datetime import datetime
#UserMixin class looks into the user.is_authenticated related functionalities.
from flask_login import UserMixin
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class User(db.Model,UserMixin):
    # The table name will be user
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    image_file=db.Column(db.String(20),nullable=False, default='default.jpeg')
    password=db.Column(db.String(60),nullable=False)
    '''
    Lazy loading refers to objects are returned from a query
    without the related objects loaded at first. When the given
    collection or reference is first accessed on a particular object,an
    additional SELECT statement is emitted such that the requested collection is loaded.
    '''
    posts=db.relationship('Post',backref='author',lazy=True)

    def get_reset_token(self,expires_sec=1800):
        '''
        This method will take the id of the user from the email id
        so provided from the user and would create an encryption of the id
        by dumping it through the serializer object which will be returned
        to the mail of the user.
        '''
        s=Serializer(secret_key=current_app.config['SECRET_KEY'], expires_in=expires_sec)
        #returns an encrypted id of the User
        return s.dumps(obj={'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        '''
        This Method receives the token so generated in the get_reset_token
        method and would decrypt the user id of the user and would return
        the User Details of the User who wants to change his/her password.
        '''
        s=Serializer(secret_key=current_app.config['SECRET_KEY'])
        try:
            user_id=s.loads(s=token)['user_id']
        except:
            return None
        return User.query.get(ident=int(user_id))


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
