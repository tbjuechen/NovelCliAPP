from pydantic import BaseModel
from typing import Optional

from schemas.book_schema import BookInfo

class CreateSpider(BaseModel):
    spider_name: str
    src_url: str

class SpiderInfo(CreateSpider):
    spider_id: int
    down_process: float
    status: str
    novel_info: Optional[BookInfo]

class SpiderResponse(BaseModel):
    spider_id: int
    down_process: float
    status: str
    