from sqlalchemy.orm import Session, joinedload
from datetime import datetime

from models import Bookshelf, User
from schemas import ShelfReadInfo, ChapterResponse

async def get_user_shelf(db: Session, user_id: int):
    shelfs = db.query(Bookshelf).filter(Bookshelf.user_id == user_id).options(joinedload(Bookshelf.book)).all()
    return shelfs

async def add_book_to_shelf(db: Session, user_id:int, book_id:int) -> Bookshelf:
    shelf = Bookshelf(user_id=user_id, book_id=book_id)
    db.add(shelf)
    db.commit()
    db.refresh(shelf)
    return shelf

async def get_book_by_userid_and_bookid(db: Session, user_id:int, book_id:int) -> Bookshelf:
    return db.query(Bookshelf).filter(Bookshelf.user_id == user_id, Bookshelf.book_id == book_id).first()

async def update_latest_read_time(db: Session, shelf: Bookshelf):
    shelf.latest_read_time = datetime.now()
    db.commit()
    db.refresh(shelf)
    return shelf

async def update_latest_read_chapter(db: Session, shelf: Bookshelf, chapter: ChapterResponse):
    shelf.latest_read_chapter_name = chapter.chapter_title
    shelf.latest_read_chapter_index = chapter.chapter_id
    db.commit()
    db.refresh(shelf)
    return shelf

async def update_reading_process(db: Session, shelf: Bookshelf, reading_process: float):
    shelf.reading_progress = reading_process
    shelf.is_read_begin = False if reading_process == 0 else True
    shelf.is_read_end = False if reading_process < 100 else True
    db.commit()
    db.refresh(shelf)
    return shelf