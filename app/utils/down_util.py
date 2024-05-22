import importlib
import sys
import os
import subprocess

from config.download import SPIDER_PATH
from schemas.down_schema import CreateSpider, SpiderInfo, SpiderResponse
from schemas import BookInfo,BookCreate
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
 

spiders = []
spider_id_cnt:int = 0

# 生成爬虫id
def gengerate_spider_id()->int:
    global spider_id_cnt
    spider_id_cnt += 1
    return spider_id_cnt

# 创建爬虫实例
def call_spider(create_down_process: CreateSpider) -> SpiderInfo:
    global spiders
    # 获取当前工作目录
    current_path = os.getcwd()
    # 切换到爬虫目录
    os.chdir(SPIDER_PATH)
    spider_name = create_down_process.spider_name
    src_url = create_down_process.src_url
    spider_id = gengerate_spider_id()
    cmd = ['start','scrapy', 'crawl', spider_name, '-a', f'start_url={src_url}', '-a', f'spider_id={spider_id}']
    subprocess.run(cmd, shell=True, cwd=SPIDER_PATH)
    # 切换回工作目录
    os.chdir(current_path)
    spider_info = SpiderInfo(**create_down_process.dict(), spider_id=spider_id, down_process=0.0,status='created', novel_info=None)
    spiders.append(spider_info)
    return spider_info

# 通过id获取爬虫信息
def get_spider(spider_id: int) -> SpiderInfo:
    global spiders
    for spider in spiders:
        if spider.spider_id == spider_id:
            return spider
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Spider not found')
