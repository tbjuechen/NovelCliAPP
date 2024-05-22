from fastapi import Depends, Query

from utils.down_util import get_spider
from schemas import SpiderInfo  

def spider(spider_id:int = Query(...,description='爬虫id')) -> SpiderInfo:
    return get_spider(spider_id)