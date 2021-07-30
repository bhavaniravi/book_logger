from application.models import Book, Author, User
from application.app import db

class BookService:
    @classmethod
    def create(cls, book_name, authors, publisher):
        book = Book(book_name=book_name, authors=authors, publisher=publisher)
        db.session.add(book)
        db.session.commit()
        return book

    @classmethod
    def get_book_by_id(cls, book_id):
        book = Book.query.get(book_id)
        return book

    def delete_book():
        pass

    def update_book():
        pass


class AuthorService:
    @classmethod
    def create(cls, author_name):
        author = Author(name=author_name)
        db.session.add(author)
        db.session.commit()
    
    @classmethod
    def get_author_by_name(cls, name):
        return Author.query.filter_by(name=name).first()