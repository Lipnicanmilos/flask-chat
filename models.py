from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    posts = db.relationship("Post", backref="user")
    comments = db.relationship("Comment", backref="user")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    code = db.Column(db.Text)
    created = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    comments = db.relationship("Comment", backref="post")

    def __repr__(self):
        return f"Post(id={self.id}, user_id={self.user_id})"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    text = db.Column(db.String(200))
    created = db.Column(db.DateTime)
