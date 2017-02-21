# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name         = scrapy.Field()   # 书名
    classify     = scrapy.Field()   # 分类
    author       = scrapy.Field()   # 作者
    publisher    = scrapy.Field()   # 出版社
    publish_time = scrapy.Field()   # 出版时间
    desc         = scrapy.Field()   # 描述
    from_web     = scrapy.Field()   # 来源网站
    web_id       = scrapy.Field()   # 来源id
    url          = scrapy.Field()   # 详情页url
    img_url      = scrapy.Field()   # 图片url

class BookSpiderItem_list(scrapy.Item):
    data         = scrapy.Field()
