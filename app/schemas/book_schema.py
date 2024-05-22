from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: str
    source_spider: str
    total_chapters: int
    introduction: str
    store_path: str

class BookBase(BaseModel):
    id: int

class BookInfo(BookBase):
    title: str
    author: str
    source_spider: str
    total_chapters: int
    introduction: str
    tags: str
    store_path: str

class BookInDB(BookInfo):
    created_at: datetime
    last_updated: datetime
    is_complete: bool
    latest_chapter: Optional[str]

    class Config:
        orm_mode = True

class ChapterResponse(BaseModel):
    book_id: int
    book_title: str
    book_author: str
    chapter_id: int
    chapter_title: str
    chapter_content: list[str]
    words_count: int
    total_chapters: int

class CatalogItem(BaseModel):
    chapter_id: int
    chapter_title: str

