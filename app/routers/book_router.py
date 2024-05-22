from fastapi import APIRouter, Depends, Query, Path, Response
from sqlalchemy.orm import Session
from typing import List

from models import User
from schemas import BookInfo, BookInDB, ChapterResponse, CatalogItem, ShelfInDB
from service import book_service,shelf_service
from dependencies.db_dependent import get_db
from dependencies.book_dependent import get_book
from dependencies.auth_dependent import get_current_user
from dependencies.shelf_dependent import get_shelf


book_routers = APIRouter(prefix="/book")

@book_routers.get("/{book_id}/info", response_model=BookInfo, tags=["book"])
async def book_info(book: BookInDB = Depends(get_book)):
    return book

@book_routers.get("/list", response_model=List[BookInDB], tags=["book"])
async def book_list(db: Session = Depends(get_db)):
    return await book_service.get_book_list(db)

@book_routers.get("/{book_id}/chapter/{chapter_id}", response_model=ChapterResponse, tags=["book"])
async def chapter(
        book: BookInDB = Depends(get_book), 
        chapter_id: int = Path(..., title="The ID of the chapter you want to get"),
        db: Session = Depends(get_db),
        shelf: ShelfInDB = Depends(get_shelf)
        ):
    chapter = await book_service.get_chapter(book, chapter_id)
    await shelf_service.update_read_time(db, shelf, chapter)
    return chapter

@book_routers.get("/{book_id}/chapter", response_model=List[CatalogItem], tags=["book"])
async def chapter_list(book: BookInDB = Depends(get_book)):
    return await book_service.get_chapter_list(book)

@book_routers.get("/{book_id}/cover", tags=["book"])
async def book_cover(book: BookInDB = Depends(get_book)):
    cover = await book_service.get_book_cover(book)
    return Response(content=cover, media_type="image/jpeg")

@book_routers.post("/collect/{book_id}",response_model=ShelfInDB, tags=["book"])
async def collect_book(
        user: User = Depends(get_current_user),
        book: BookInDB = Depends(get_book),
        db: Session = Depends(get_db)
        ):
    shelf = await book_service.collect_book(db, user, book)
    return shelf

@book_routers.get("/{book_id}/inshelf", response_model=ShelfInDB, tags=["book"])
async def get_book_schedule(
        db: Session = Depends(get_db),
        shelf: ShelfInDB = Depends(get_shelf)
        ):
    return shelf
