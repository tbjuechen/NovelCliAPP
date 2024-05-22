from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from pydantic import parse_obj_as

from schemas import BookCreate, SpiderInfo, CreateSpider, BookInfo, SpiderResponse, BookInDB
from utils.down_util import call_spider, spiders
from service.book_service import create_book
from models import Book


# 创建下载进程
def create_spider(spider_create: CreateSpider)-> SpiderInfo:
    spider = call_spider(spider_create)
    return spider

# 开始下载
async def update_book_info(
        book_info: BookCreate, 
        spider: SpiderInfo, 
        db: Session)-> SpiderInfo:
    # 更新爬虫信息
    if spider.status == 'created':
        spider.status = 'running'
        # 创建书籍
        db_book = await create_book(db, book_info)
        spider.novel_info = BookInfo.model_validate(db_book,from_attributes=True)
        return spider
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Spider is {spider.status}')
    
# 更新进度信息
def refresh_down_process(spider: SpiderInfo, schedule: SpiderResponse)->SpiderInfo:
    spider.down_process = schedule.down_process
    spider.status = schedule.status
    return spider

def get_spiders()->list[SpiderInfo]:
    return spiders
    