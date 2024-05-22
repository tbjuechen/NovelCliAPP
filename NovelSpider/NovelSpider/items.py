# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NovelInfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title : str = scrapy.Field()
    author : str = scrapy.Field()
    cover : str = scrapy.Field()
    intro : str = scrapy.Field()
    catalog : list = scrapy.Field()
    total_chapters : int = scrapy.Field()
    down_path: str = scrapy.Field()

class NovelContentItem(scrapy.Item):
    index : int = scrapy.Field()
    title : str = scrapy.Field()
    content : str = scrapy.Field()
    down_path : str = scrapy.Field()
    down_precent :float = scrapy.Field()