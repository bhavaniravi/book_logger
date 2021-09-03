from application.app import app
from flask import request
# Import your models here
from application.models import Book, save_objects, db, User, BookReviews
from application.services import BookService, AuthorService, PublisherService
import traceback

from flask_jwt import jwt_required, JWT, current_identity

def identity(payload):
    user_id = payload['identity']
    return User.query.filter_by(id=user_id).first()

def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        return user

jwt = JWT(app, authenticate, identity)

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    try:
        # Get or create user
        try:
            user = User(username=data['username'], password=data['password'])
            db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()
            user = User.query.filter_by(username=data['username']).first()
        
        access_token = jwt.jwt_encode_callback(user)
        return {"token": access_token.decode('utf-8')}
    except Exception as e:
        print(e)
        traceback.print_exc()
        return "Could not register user"



@app.route("/book", methods=["GET"])
@jwt_required()
def get_books():
    books = Book.query.all()
    results = []
    for book in books:
        results.append({
            "id": book.id,
            "book_name": book.book_name
        })
    return {"results": results}


@app.route("/book", methods=["POST"])
def add_books():
    params = request.json
    try:
        if params["book_name"] == "":
            raise Exception
        author = AuthorService.get_by_name(params["author_name"])
        if not author:
            author = AuthorService.create(author_name=params["author_name"])


        publisher = PublisherService.get_by_name(params["publisher"])
        print (publisher)
        if not publisher:
            publisher = PublisherService.create(params["publisher"])

        book = BookService.create(book_name=params["book_name"], authors=[author], publisher=publisher)
        return {"results": {"id": book.id, "book_name": book.book_name}}, 201
    except Exception as e:
        exception_string = traceback.format_exc()
        print (exception_string)
        return {"status": "error", "error_message": "Data in wrong format", "error_traceback": exception_string}, 400
    

@app.route("/book/<id>", methods=["GET"])
def get_book(id):
    book = Book.query.filter_by(id=id).first()
    return {
        "id": book.id,
        "name": book.book_name,
        "authors":  [author.name for author in book.authors]
    }

@app.route("/book/<id>/review", methods=["POST"])
def add_book_review(id):
    params = request.json
    try:
        book = BookService.get_book_by_id(id)
        if not book:
            return {"status": "error", "error_message": "Invalid book id"}, 400
        user = User.query.filter_by(username=params["username"]).first()
        if not user:
            return {"status": "error", "error_message": "Invalid user"}, 400
        
        
        book_review = BookReviews(book_id=book.id, created_by=user.id, review_text=params["review_text"])
        db.session.add(book_review)
        db.session.commit()

        return {"results": {"id": book_review.review_id, "review_text": book_review.review_text}}, 201
    except Exception as e:
        print (e)
        return {"status": "error", "error_message": "Data in wrong format", "error_traceback": traceback.format_exc()}, 400


@app.route("/book/<id>/review", methods=["GET"])
def get_all_reviews(id):
    book_reviews = BookReviews.query.filter_by(book_id=id).all()
    return {"results": [{"review_id": review.review_id, "review_text": review.review_text} for review in book_reviews]}


@app.route("/book/<id>", methods=["DELETE"])
def delete_book(id):
    book = Book.query.filter_by(id=id).first()
    if not book:
        return {"status": "error", "error_message": "Invalid book id"}, 400
    db.session.delete(book)
    db.session.commit()
    return {"status": "success", "message": "Book deleted"}