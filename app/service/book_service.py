from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import os

import schemas
from models import Book, User
from dao import book_dao, shelf_dao
from schemas import BookInDB, ChapterResponse

async def get_book_info(db: Session, book_id: int):
    book = await book_dao.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book

async def create_book(db: Session, book: schemas.BookCreate)-> Book:
    db_book = await book_dao.create_book(db, book)
    return db_book

async def get_book_list(db: Session):
    book_list = await book_dao.get_all_books(db)
    book_list = [BookInDB.model_validate(book,from_attributes=True) for book in book_list]
    return book_list

async def get_chapter(book:BookInDB, chapter_id:int):
    book_path = book.store_path
    content_path = os.path.join(book_path, 'content',f'{chapter_id}.txt')
    words_count:int = 0
    with open(content_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        title = lines[0]
        content = ''.join(lines[1:])
        words_count = len(content)
    response = ChapterResponse(
        chapter_title=title, 
        chapter_content=content.split('\n'), 
        book_id=book.id, 
        chapter_id=chapter_id, 
        words_count=words_count,
        book_title=book.title,
        book_author=book.author,
        total_chapters=book.total_chapters)
    return response

async def get_chapter_list(book:BookInDB):
    book_path = book.store_path
    info_path = os.path.join(book_path, 'info.txt')
    with open(info_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        chapter_list = [{
            'chapter_id': int(item.split(' : ')[0]),
            'chapter_title': item.split(' : ')[1]
        }  for item in lines[5:-1]]
    return chapter_list

async def get_book_cover(book:BookInDB):
    book_path = book.store_path
    cover_path = os.path.join(book_path, 'cover.jpeg')
    with open(cover_path, 'rb') as f:
        cover = f.read()
    return cover

async def collect_book(db:Session,user: User, book: BookInDB):
    user_id = user.id
    book_id = book.id
    shelf = await shelf_dao.get_book_by_userid_and_bookid(db,user_id, book_id)
    if shelf:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book already collected")
    shelf = await shelf_dao.add_book_to_shelf(db, user_id, book_id)
    if not shelf:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Collect failed")
    return shelf
