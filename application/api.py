from application.app import app
from flask import request
# Import your models here
from application.models import Book, save_objects, db, User, BookReviews
from application.services import BookService, AuthorService
import traceback

@app.route("/book", methods=["GET"])
def get_books():
    books = Book.query.all()
    results = []
    for book in books:
        results.append({
            "id": book.id,
            "book_name": book.name
        })
    return {"results": results}


@app.route("/book", methods=["POST"])
def add_books():
    params = request.json
    try:
        if params["book_name"] == "":
            raise Exception
        author = AuthorService.get_author_by_name(params["author_name"])
        if not author:
            author = AuthorService.create(author_name=params["author_name"])
        book = BookService.create(book_name=params["book_name"], authors=[author], publisher=params["publisher"],)
        return {"results": {"id": book.id, "book_name": book.book_name}}, 201
    except Exception as e:
        print (e)
        return {"status": "error", "error_message": "Data in wrong format", "error_traceback": traceback.format_exc()}, 400
    

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

