# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import logging
import re
import base64
import requests

from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .items import NovelInfoItem, NovelContentItem
from .web_conf import fastapi_url

class NovelspiderPipeline:
    def __init__(self):
        self.broswer = webdriver.Chrome(options=image_options)
        # 日志等级:WARNING
        LOGGER.setLevel(logging.WARNING) 


    def process_item(self, item, spider):
        # 小说信息
        if isinstance(item, NovelInfoItem):
            item_dict = ItemAdapter(item).asdict()
            path = item_dict['down_path']
            if not os.path.exists(path):
                os.makedirs(path)
            self.down_cover(item)
            self.save_info(item)
            # 将小说信息发布到后端
            spider_id  = spider.spider_id
            param = {'spider_id': spider_id}
            book_info = {
                'title': item_dict['title'],
                'author': item_dict['author'],
                'source_spider': spider.name,
                'total_chapters': item_dict['total_chapters'],
                'introduction': item_dict['intro'],
                'store_path': item_dict['down_path']
            }
            requests.post(fastapi_url + '/down/info', params=param, json=book_info)

        # 小说内容
        elif isinstance(item, NovelContentItem):
            item_dict = ItemAdapter(item).asdict()
            self.save_content(item)
             # 将下载进度发布到后端
            spider_id = spider.spider_id
            param = {'spider_id': spider_id}
            data = {
                'spider_id': spider_id,
                'down_process': item_dict['down_precent'],
                'status': 'running' if item_dict['down_precent'] < 100 else 'finished'
            }
            requests.post(fastapi_url + '/down/schedule',params=param,json=data)

    def save_content(self, item):
        item_dict = ItemAdapter(item).asdict()
        path = item_dict['down_path']
        if not os.path.exists(path):
            os.makedirs(path)
        chapter_file_name = str(item_dict['index']) + '.txt'
        with open(os.path.join(path, chapter_file_name),'w', encoding='utf-8') as f:
            f.write(f"{item_dict['title']}\n")
            f.write(f"{item_dict['content']}\n")

    def save_info(self, item):
        item_dict = ItemAdapter(item).asdict()
        path = item_dict['down_path']
        with open(os.path.join(path, 'info.txt'), 'w', encoding='utf-8') as f:
            f.write(f"书名: {item_dict['title']}\n")
            f.write(f"作者: {item_dict['author']}\n")
            f.write(f"简介: {item_dict['intro']}\n")
            f.write(f"总章节数: {item_dict['total_chapters']}\n")
            f.write("目录:\n")
            for index,chapter in enumerate(item_dict['catalog']):
                f.write(f"{str(index)} : {chapter['title']}\n")    

    def down_cover(self, item):
        cover_url = item['cover']
        self.broswer.get(cover_url)
        WebDriverWait(self.broswer, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'img'))
        )
        dataUrl = self.broswer.execute_script('''
                            const cover = document.querySelector("img");
                            if(!cover) throw Error("cannot find cover image node");
                            const width = cover.naturalWidth;
                            const height = cover.naturalHeight;
                            console.log(`find cover image ${{width}} x ${{height}}`);

                            const canvas = document.createElement('canvas');
                            canvas.width = width;
                            canvas.height = height;
                            const context = canvas.getContext('2d');
                            context.drawImage(cover, 0, 0);

                            return canvas.toDataURL("image/jpeg");
                                ''')
        result = re.search("data:image/(?P<ext>.*?);base64,(?P<data>.*)", dataUrl, re.DOTALL)
        if result:
            ext = result.group('ext')
            data = result.group('data')
            img = base64.urlsafe_b64decode(data)
            filename = f'cover.{ext}'
            cover_path = os.path.join(item['down_path'], filename)
            with open(cover_path, 'wb') as f:
                f.write(img)



image_options = Options()
image_options.add_experimental_option('excludeSwitches', ['enable-logging'])
image_options.add_argument('window-size=1920x3000')  # 指定浏览器分辨率
image_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
image_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
image_options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
image_options.add_argument('--ignore-certificate-errors')  # 屏蔽ssl错误
image_options.add_argument('log-level=3')  # 通知等级 fail 
