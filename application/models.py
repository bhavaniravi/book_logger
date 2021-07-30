from application.app import app, db
import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120))


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)


class Publisher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    publisher_name = db.Column(db.String(80), nullable=False)
    publisher_address = db.Column(db.String(200))


author_book = db.Table('author_book_table',
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True)
)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(180), nullable=False)
    publisher = db.Column(db.Integer, db.ForeignKey('publisher.id'), nullable=False)
    authors = db.relationship("Author", secondary=author_book, lazy='subquery', backref=db.backref('author', lazy=True))




class BookReviews(db.Model):
    review_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    review_text = db.Column(db.String(1000), nullable=False)
    star_rating = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    


def save_objects(objects):
    for obj in objects:
        db.session.add(obj)

db.init_app(app)
db.create_all()