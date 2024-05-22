from urllib.parse import urljoin
import os

from scrapy.http import HtmlResponse

from .baseSpider import BaseSpider

class BiququSpider(BaseSpider):
    name = "biququSpider"
    allowed_domains = ["www.biququ.la"]
    start_urls = ["https://www.biququ.la/html/59199/"]

    def __init__(self, *args, **kwargs):
        super(BiququSpider, self).__init__(*args, **kwargs)
        
    def get_title(self, response: HtmlResponse):
        title = response.xpath('//div[@id="info"]/h1/text()').get()
        return title
    
    def get_author(self, response: HtmlResponse):
        author = response.xpath('//div[@id="info"]/p[1]/text()').get()[5:]
        return author
    
    def get_cover(self, response: HtmlResponse):
        cover = response.xpath('//div[@id="fmimg"]/img/@src').get()
        return cover

    def get_intro(self, response: HtmlResponse):
        intro = response.xpath('//div[@id="intro"]/text()').get()
        return intro
        
    def get_catalog(self, response: HtmlResponse):
        dd_items = response.xpath('//div[@id="list"]/dl/dd')
        catalog = []
        for dd in dd_items:
            chapter = dict()
            chapter['title'] = dd.xpath('a/text()').get()
            chapter['link'] = dd.xpath('a/@href').get()
            catalog.append(chapter)
        return catalog
    
    def get_content(self, response: HtmlResponse):
        texts = response.xpath('//div[@id="content"]/p/text()').getall()
        content = '\n'.join(['    ' + element for element in texts])
        return content
    
    def generate_full_url(self, url):
        return urljoin(f'https://{self.allowed_domains[0]}', url)
