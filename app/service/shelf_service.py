from sqlalchemy.orm import Session

from models import Bookshelf
from dao import shelf_dao,book_dao
from schemas import ChapterResponse


async def update_read_time(db: Session, shelf: Bookshelf, chapter: ChapterResponse):
    await shelf_dao.update_latest_read_time(db, shelf)
    await shelf_dao.update_latest_read_chapter(db, shelf, chapter)
    book = await book_dao.get_book_by_id(db, shelf.book_id)
    reading_process = (chapter.chapter_id + 1) / book.total_chapters * 100
    print(reading_process)
    shelf = await shelf_dao.update_reading_process(db, shelf, reading_process)
    return shelf