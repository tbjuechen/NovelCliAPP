from urllib.parse import urljoin
import os

import scrapy
from scrapy.http import HtmlResponse
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from ..items import NovelInfoItem, NovelContentItem


class BaseSpider(scrapy.Spider):
    def __init__(self, *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)
        self.down_path = kwargs.get('down_path', 'F:\\Scripts\\novelCliAPP\\NovelSpider\\novels')
        self.start_urls = [kwargs.get('start_url', 'https://www.biququ.la/html/59199/')]
        self.spider_id = kwargs.get('spider_id', 0)
        self.down_path:str = os.path.join(self.down_path, self.name)
        self.down_cnt:int = 0

    def start_requests(self):
        for url in self.start_urls:
            meta_data = {'wait_element_id': 'list'}
            yield SeleniumRequest(
                url=url, 
                callback=self.parse, 
                meta=meta_data,
                wait_time=10,
                wait_until=EC.presence_of_element_located((By.ID, 'list'))    
            )

    def parse(self, response: HtmlResponse):
        self.down_path = os.path.join(self.down_path, self.get_title(response))
        # 保存小说信息
        item = NovelInfoItem()
        item['title'] = self.get_title(response)
        item['author'] = self.get_author(response)
        item['cover'] = self.generate_full_url(self.get_cover(response))
        item['intro'] = self.get_intro(response)
        item['catalog'] = self.get_catalog(response)
        item['total_chapters'] = len(item['catalog'])
        item['down_path'] = self.down_path
        self.logger.info(f'parse: {item["title"]} from {response.url}\n\
                           writer: {item["author"]}\n\
                           intro: {item["intro"]}\n\
                           totle chapters: {len(item["catalog"])}\n')
        yield item
        self.chapter_cnt = len(item['catalog'])
        for index,chapter in enumerate(item['catalog']):
            chapter_url = self.generate_full_url(chapter['link'])
            meta_data = {
                'wait_element_id': 'content',
                'chapter_index' : index,
                'chapter_title' : chapter['title'],
                'chapter_cnt' : self.chapter_cnt,
                }
            title = chapter['title']
            self.logger.info(f'parse_chapter: {index} : {title} from {response.url}\n')
            yield SeleniumRequest(
                url=chapter_url, 
                callback=self.parse_chapter, 
                meta=meta_data,
                wait_time=10,
                wait_until=EC.presence_of_element_located((By.ID, 'content'))
            )
        

    def parse_chapter(self, response: HtmlResponse):
        charpter_index = response.request.meta['chapter_index']
        charpter_title = response.request.meta['chapter_title']
        content = self.get_content(response)
        self.down_cnt += 1
        item = NovelContentItem()
        item['index'] = charpter_index
        item['content'] = content
        item['title'] = charpter_title
        item['down_path'] = os.path.join(self.down_path, 'content')
        item['down_precent'] = self.down_cnt/self.chapter_cnt * 100
        yield item