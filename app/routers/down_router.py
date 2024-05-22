from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.orm import Session
from typing import List

from schemas import SpiderResponse, SpiderInfo, BookCreate, CreateSpider
from dependencies.spider_dependent import spider
from dependencies.db_dependent import get_db
from service.down_service import update_book_info, refresh_down_process,create_spider
from service import down_service

down_router = APIRouter(prefix="/down")

@down_router.post("/info", response_model= SpiderInfo, tags=["down"])
async def update_spider_info(
    book_info:BookCreate, 
    spider:SpiderInfo = Depends(spider), 
    db:Session = Depends(get_db)
    ):
    spider =await update_book_info(book_info, spider, db)
    return spider

@down_router.post("/schedule", response_model= SpiderInfo, tags=["down"])
async def refresh_spider_schedule(
    spider:SpiderInfo = Depends(spider), 
    schedule:SpiderResponse = Body(...)
    ):
    spider = refresh_down_process(spider, schedule)
    return spider

@down_router.post("/create", response_model= SpiderInfo, tags=["down"])
def create_spider(
    spider_create:CreateSpider = Body(...)
    ):
    spider = down_service.create_spider(spider_create)
    return spider

@down_router.get("/schedule", response_model= float, tags=["down"])
async def get_spider_schedule(
    spider:SpiderInfo = Depends(spider)
    ):
    return spider.down_process

@down_router.get('/tasks', response_model=List[SpiderInfo], tags=["down"])
def get_spiders():
    return down_service.get_spiders()