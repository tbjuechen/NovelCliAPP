from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from dependencies.db_dependent import get_db
from dependencies.auth_dependent import get_current_user
from dependencies.book_dependent import get_book
from dao import shelf_dao

async def get_shelf(
        db:Session = Depends(get_db),
        user = Depends(get_current_user),
        book = Depends(get_book)        
        ):
    user_id = user.id
    book_id = book.id
    shelf = await shelf_dao.get_book_by_userid_and_bookid(db, user_id, book_id)
    if not shelf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not in shelf")
    return shelf