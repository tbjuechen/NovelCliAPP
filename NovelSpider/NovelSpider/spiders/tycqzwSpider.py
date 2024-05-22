from urllib.parse import urljoin
import os

from scrapy.http import HtmlResponse

from .baseSpider import BaseSpider

class TycxswSpider(BaseSpider):
    name = "tycxswSpider"
    allowed_domains = ["www.tycqzw.net"]
    start_urls = ["http://www.tycqzw.net/0_325/"]

    def __init__(self, *args, **kwargs):
        super(TycxswSpider, self).__init__(*args, **kwargs)
        
    def get_title(self, response: HtmlResponse):
        title = response.xpath('//div[@id="info"]/h1/text()').get()
        return title
    
    def get_author(self, response: HtmlResponse):
        author = response.xpath('//div[@id="info"]/p[1]/text()').get()[7:]
        return author
    
    def get_cover(self, response: HtmlResponse):
        cover = response.xpath('//div[@id="fmimg"]/img/@src').get()
        return cover

    def get_intro(self, response: HtmlResponse):
        intro = response.xpath('//div[@id="intro"]/p/text()').get()
        return intro
        
    def get_catalog(self, response: HtmlResponse):
        dd_items = response.xpath('//div[@id="list"]/dl/dt/following-sibling::dd')
        catalog = []
        for dd in dd_items:
            chapter = dict()
            chapter['title'] = dd.xpath('a/text()').get()
            chapter['link'] = dd.xpath('a/@href').get()
            catalog.append(chapter)
        return catalog
    
    def get_content(self, response: HtmlResponse):
        texts = response.xpath('//div[@id="content"]/text()').getall()
        content = []
        for item in texts:
            if item != '\n\r':
                content.append('    ' + item[5:-1])
        content = content[:-3]
        return '\n'.join(content)
    
    def generate_full_url(self, url):
        return urljoin(f'http://{self.allowed_domains[0]}', url)