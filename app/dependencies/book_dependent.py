from fastapi import Depends, Path, HTTPException, status
from sqlalchemy.orm import Session

from dependencies.db_dependent import get_db
from dao import book_dao
from schemas import BookInDB

async def get_book(
        book_id: int = Path(..., title="The ID of the book you want to get"),
        db : Session=Depends(get_db)
        ):
    book = await book_dao.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return BookInDB.model_validate(book, from_attributes=True)