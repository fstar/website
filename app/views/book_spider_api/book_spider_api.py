# -*- coding:utf-8 -*-
from flask import Blueprint, render_template, request
from flask_restful import Resource, Api
from app.views.common.view_decorators import *
from app.models import db, Module, Book_Spider
from app.views.common.utils import *
import json


book_spider_api_view = Blueprint("book_spider_api_view",__name__)
book_spider_api_api = Api(book_spider_api_view)

class book_spider_api(Resource):
    method_decorators = [permission_check]
    '''
        通过关键字得到数据
    '''
    def get(self, uid):
        keyword    = request.args.get("keyword")
        page       = int(request.args.get("page", 1))
        one_page   = int(request.args.get("one_page", 5))
        book_query = Book_Spider.query.filter(Book_Spider.name.like("{keyword}%".format(keyword=keyword))).\
                                              group_by(Book_Spider.name).order_by(Book_Spider.desc.desc()).\
                                              paginate(page, per_page=one_page, error_out=False)

        data = [{
                "id":i.id,
                "name":i.name,
                "classify":i.classify,
                "author":i.author,
                "publisher":i.publisher,
                "publish_time":i.publish_time,
                "desc":i.desc,
                "img_url":i.img_url
                } for i in book_query.items]
        has_prev = 1 if book_query.has_prev else 0
        has_next = 1 if book_query.has_next else 0
        url = "/Library/book_spider_api?keyword={keyword}&one_page={one_page}".\
                format(keyword=keyword, one_page=one_page)
        prev_url = (url+r"&page={page}".format(page=page-1)) if has_prev == 1 else ""
        next_url = (url+r"&page={page}".format(page=page+1)) if has_next == 1 else ""

        return succeed_resp(data=data,status=1,has_prev=has_prev, \
                            has_next=has_next, prev_url=prev_url, next_url=next_url)

    '''
        插入数据api:
        POST:
        {
            "data":[{
                name:
                classify:
                author:
                publisher:
                publish_time:
                desc:
                from_web:
                web_id:
                url:
                img_url:
            }]
        }
    '''
    def post(self, uid):
        data = request.form.get("data","[]")
        data = json.loads(data)
        if not data:
            return succeed_resp(status=1)
        web_id_list = [item["web_id"] for item in data]
        from_web    = data[0]["from_web"]
        book_query  = Book_Spider.query.filter_by(from_web=from_web).\
                                        filter(Book_Spider.web_id.in_(web_id_list)).\
                                        with_entities(Book_Spider.web_id).all()
        result = set(web_id_list) - set([item.web_id for item in book_query])
        for item in data:
            name         = item["name"]
            classify     = item["classify"]
            author       = item.get("author",None)
            publisher    = item.get("publisher",None)
            publish_time = item.get("publish_time",None)
            desc         = item.get("desc",None)
            from_web     = item["from_web"]
            web_id       = item["web_id"]
            url          = item["url"]
            img_url      = item.get("img_url",None)
            if web_id not in result:
                continue
            one = Book_Spider(  name = name,
                                classify = classify,
                                author = author,
                                publisher = publisher,
                                publish_time = publish_time,
                                desc = desc,
                                from_web = from_web,
                                web_id = web_id,
                                url = url,
                                img_url = img_url,
                                uid=uid)
            db.session.add(one)
        db.session.commit()
        return succeed_resp(status=1)

book_spider_api_api.add_resource(book_spider_api, "/Library/book_spider_api")
