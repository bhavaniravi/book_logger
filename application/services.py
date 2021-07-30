from application.models import Book, Author, User, Publisher
from application.app import db

class BookService:
    @classmethod
    def create(cls, book_name, authors, publisher):
        book = Book(book_name=book_name, authors=authors, publisher=publisher.id)
        db.session.add(book)
        db.session.commit()
        return book

    @classmethod
    def get_by_id(cls, book_id):
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
        return author
    
    @classmethod
    def get_by_name(cls, name):
        return Author.query.filter_by(name=name).first()


class PublisherService:
    @classmethod
    def get_by_name(cls, name):
        return Publisher.query.filter_by(publisher_name=name).first()
    
    @classmethod
    def create(cls, publisher_name):
        publisher = Publisher(publisher_name=publisher_name)
        db.session.add(publisher)
        db.session.commit()
        return publisher