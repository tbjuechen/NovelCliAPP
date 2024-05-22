from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from schemas.book_schema import BookInDB

class ShelfBase(BaseModel):
    user_id: int
    book_id: int

class ShelfCreate(ShelfBase):
    pass

class ShelfReadInfo(ShelfBase):
    latest_read_chapter_index : Optional[int]
    latest_read_chapter_name : Optional[str]
    reading_progress : float

class ShelfInDB(ShelfBase):
    is_read_begin: bool
    is_read_end: bool
    reading_progress: float
    latest_read_chapter_index: Optional[int]
    latest_read_chapter_name: Optional[str]
    latest_read_time: Optional[datetime]
    book : Optional[BookInDB]

    class Config:
        orm_mode = True