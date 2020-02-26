from blog import db, login_manager, app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
#    ph_no = db.Column(db.Integer(), unique = True, nullable = False)
    email = db.Column(db.String(50), unique = True, nullable = False)
    img_file = db.Column(db.String(120), nullable = False, default = 'default.svg')
    password = db.Column(db.String(60), nullable = False)
    comments = db.relationship('Comments', backref = 'author', lazy = True)


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return f"User('{self.id}','{self.username}','{self.email}')" 
        #,'{self.ph_no}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    content = db.Column(db.Text, nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    photos = db.relationship('Photo', backref = 'post', lazy = "dynamic")
    comments = db.relationship('Comments', backref = 'post', lazy = True)

    def __repr__(self):
        return f"Post('{self.id}','{self.title}','{self.date_posted}')"

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable = False)

    def __repr__(self):
        return f"Post id('{self.post_id}', Photo id '{self.id}')"

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    comment = db.Column(db.String(), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable = False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __repr__(self):
        return f"Comment id('{self.id}', Post id '{self.post_id}', Author id '{self.author_id}')"
