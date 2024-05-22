from sqlalchemy.orm import Session
from typing import Union

from models import Book
from schemas import BookInfo, BookCreate

async def get_book_by_id(db: Session, book_id: int) -> Union[Book, None]:
    book = db.query(Book).filter(Book.id == book_id).first()
    return book

async def create_book(db: Session, book: BookCreate) -> Union[Book, None]:
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

async def get_all_books(db: Session) -> Union[Book, None]:
    return db.query(Book).all()