from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models import Source
from schemas import SrcInDB
from dao.source_dao import get_src_list

async def list_source(db: Session):
    src_lsit = await get_src_list(db)
    if not src_lsit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No source found")
    src_lsit = [SrcInDB.model_validate(src,from_attributes=True) for src in src_lsit]
    return src_lsit