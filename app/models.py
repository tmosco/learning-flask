from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin
from app import login
from hashlib import md5



@login.user_loader
def load_user(id):
    return User.query.get(int(id))
#mixin make sure that you can only log in to your page and not
#will not be able to log into another person page using the url
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(64), index=True, unique=True)
    email= db.Column(db.String(120), index=True, unique=True)
    password_hash= db.Column(db.String(128))
    posts=db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
# This tells python how you want to see the object in the terminal
    # def __repr__(self):
    #     return 'User {}'.format(self.email)

    #creating another function to use the password security
    def set_password(self,password):
        # print(password)
        self.password_hash= generate_password_hash(password)
        print(self.password_hash)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    # we want to add avatar to the profile page
    def avatar(self, size):
        print(self.email)
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar.com/{}?d=identicon&s={}'.format(digest,size)


#Another class is created for a new data base
class Post(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    body= db.Column(db.String(140))
    timestamp= db.Column(db.DateTime, index=True, default= datetime.utcnow)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

