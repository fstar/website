# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import json
import scrapy
import requests

class BookSpiderPipeline(object):
    def __init__(self):
        self.host = "http://127.0.0.1:8080/Library/book_spider_api"
        self.header = {"token":'fx'}
        self.data = []

    def process_item(self, item, spider):
        if not item:
            return None

        one = dict(item)
        self.data.append(one)
        print "data num:",len(self.data)
        if len(self.data) > 60:
            post_data = {"data":json.dumps(self.data)}
            req = requests.post(url=self.host, data=post_data, headers=self.header)
            print req.content
            self.data = []
            return req.content
        else:
            return None
