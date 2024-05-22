from sqlalchemy.orm import Session
from models import Source

async def get_src_list(db: Session)->list[Source]:
    srcs = db.query(Source).all()
    return srcs