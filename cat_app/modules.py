from cat_app import db
from cat_app import login_manger
from flask_login import UserMixin, current_user


@login_manger.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    item = db.relationship('Items', backref='author', lazy=True)

    def __repr__(self):
        return f"user name is {self.username} email is {self.email}"


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    items = db.relationship("Items", backref="category", lazy=True)

    def __repr__(self):
        return f"Category name is {self.name}"


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), unique=True, nullable=False)
    content = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    cat_id = db.Column(db.Integer,
                       db.ForeignKey("category.id"),
                       nullable=False)

    def __repr__(self):
        return f" {self.title} with content {self.content}"
