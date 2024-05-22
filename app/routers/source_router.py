from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from schemas import SrcInDB
from service import source_service
from dependencies.db_dependent import get_db

source_router = APIRouter(prefix="/source")

@source_router.get("/list",response_model=List[SrcInDB],tags=["source"])
async def list_source(db: Session = Depends(get_db)):
    src_list = await source_service.list_source(db)
    return src_list
    