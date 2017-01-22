# -*- coding:utf-8 -*-
import scrapy
from book_spider.items import BookSpiderItem
import re
import json
from bs4 import BeautifulSoup as bs
l = [
['https://list.jd.com/list.html?cat=1713,3258' , u'小说'],
['https://list.jd.com/list.html?cat=1713,3259' , u'文学'],
['https://list.jd.com/list.html?cat=1713,3260' , u'青春文学'],
['https://list.jd.com/list.html?cat=1713,3261' , u'传记'],
# ['https://list.jd.com/list.html?cat=1713,12775' , u'绘画'],
# ['https://list.jd.com/list.html?cat=1713,12776' , u'摄影'],
# ['https://list.jd.com/list.html?cat=1713,13627' , u'书法'],
# ['https://list.jd.com/list.html?cat=1713,13634' , u'音乐'],
# ['https://list.jd.com/list.html?cat=1713,3262' , u'艺术'],
# ['https://list.jd.com/list.html?cat=1713,3263' , u'童书'],
['https://list.jd.com/list.html?cat=1713,3267' , u'励志与成功'],
['https://list.jd.com/list.html?cat=1713,3266' , u'管理'],
['https://list.jd.com/list.html?cat=1713,3264' , u'经济'],
['https://list.jd.com/list.html?cat=1713,3265' , u'金融与投资'],
# ['https://list.jd.com/list.html?cat=1713,13613' , u'孕产/胎教'],
# ['https://list.jd.com/list.html?cat=1713,3270' , u'育儿/家教'],
['https://list.jd.com/list.html?cat=1713,3271' , u'旅游/地图'],
['https://list.jd.com/list.html?cat=1713,9278' , u'烹饪/美食'],
# ['https://list.jd.com/list.html?cat=1713,9291' , u'时尚/美妆'],
# ['https://list.jd.com/list.html?cat=1713,9301' , u'家居'],
# ['https://list.jd.com/list.html?cat=1713,9309' , u'婚恋与两性'],
# ['https://list.jd.com/list.html?cat=1713,9314' , u'娱乐/休闲'],
# ['https://list.jd.com/list.html?cat=1713,3269' , u'健身与保健'],
# ['https://list.jd.com/list.html?cat=1713,3272' , u'动漫'],
['https://list.jd.com/list.html?cat=1713,3273' , u'历史'],
['https://list.jd.com/list.html?cat=1713,3279' , u'心理学'],
['https://list.jd.com/list.html?cat=1713,3276' , u'政治/军事'],
['https://list.jd.com/list.html?cat=1713,3275' , u'国学/古籍'],
['https://list.jd.com/list.html?cat=1713,3274' , u'哲学/宗教'],
# ['https://list.jd.com/list.html?cat=1713,3277' , u'法律'],
['https://list.jd.com/list.html?cat=1713,3280' , u'文化'],
['https://list.jd.com/list.html?cat=1713,3281' , u'社会科学'],
['https://list.jd.com/list.html?cat=1713,9340' , u'科普读物'],
['https://list.jd.com/list.html?cat=1713,3287' , u'计算机与互联网'],
# ['https://list.jd.com/list.html?cat=1713,3284' , u'建筑'],
# ['https://list.jd.com/list.html?cat=1713,3285' , u'医学'],
# ['https://list.jd.com/list.html?cat=1713,3282' , u'工业技术'],
['https://list.jd.com/list.html?cat=1713,9351' , u'电子与通信'],
# ['https://list.jd.com/list.html?cat=1713,9368' , u'农业/林业'],
['https://list.jd.com/list.html?cat=1713,3286' , u'科学与自然'],
# ['https://list.jd.com/list.html?cat=1713,3288' , u'体育/运动'],
# ['https://list.jd.com/list.html?cat=1713,3289' , u'中小学教辅'],
# ['https://list.jd.com/list.html?cat=1713,11047' ,u'大中专教材教辅'],
['https://list.jd.com/list.html?cat=1713,3290' , u'考试'],
['https://list.jd.com/list.html?cat=1713,3291' , u'外语学习'],
['https://list.jd.com/list.html?cat=1713,3294' , u'字典词典/工具书'],
['https://list.jd.com/list.html?cat=1713,4758' , u'杂志/期刊'],
# ['https://list.jd.com/list.html?cat=1713,4855' , u'进口原版'],
# ['https://list.jd.com/list.html?cat=1713,6929' , u'港台图书'],
]

_jsonp_begin = r'showdesc('
_jsonp_end = r')'

import chardet
def from_jsonp(jsonp_str):
    jsonp_str = jsonp_str.decode("GB2312",errors='ignore').strip()
    jsonp_str = jsonp_str.encode("utf-8")
    if not jsonp_str.startswith(_jsonp_begin) or \
            not jsonp_str.endswith(_jsonp_end):
        raise ValueError('Invalid JSONP')
    return json.loads(jsonp_str[len(_jsonp_begin):-len(_jsonp_end)])



class jd_spider(scrapy.Spider):
    name = "jd_1"
    handle_httpstatus_list=[404]  # 对哪些异常返回进行处理
    is_over = False
    dont_redirect = True
    def start_requests(self):
        for i in l[3:4]:
            is_over = False
            for index in range(1,56):
                if is_over:
                    break
                url = i[0]+r"&page="+str(index)
                yield scrapy.Request(url=url, callback=self.list_page, meta={"classify":i[1]},
                                headers={"referer":"https://list.jd.com/list.html?cat=1713,3258",\
                                "pragma":"no-cache","upgrade-insecure-requests":1,'cookie':"TrackID=1YJf-2dIp9ahAOzUIEKv13v4OlMeEyHXNaj0-kexWwwZFHQXpE2ck_ueFTsPJUSzNAs-UHFU3UjW8JpwBoyRvq19yXhAIwbnmqHSqUXUoxlFkvNDQFt4vbtcTsI5jZdIk; pinId=DkQjdZAPprlBmRHLQBnFbrV9-x-f3wj7; unpl=V2_ZzNtbRFWEEdzD05RckxfDGIEElxLU0pHc1pFVX0cVVEzURIPclRCFXMUR1RnGl8UZwIZXEpcQxxFCHZXchBYAWcCGllyBBNNIEwHDCRSBUE3XHxcFVUWF3RaTwEoSVoAYwtBDkZUFBYhW0IAKElVVTUFR21yVEMldQl2VnwYXARgAhtYcmdEJUU4RlZ6GVwHVwIiXHIVF0l3CUNXchkRB2ACElxFVkoQRQl2Vw%3d%3d; areaId=2; __jdv=122270672|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_b0bc76948d284610858c7c20748eec1c|1485065398857; ipLoc-djd=2-2813-51976-0; ipLocation=%u4E0A%u6D77; listck=fabb66020a5b772dd2b204ac53a7ade2; __jda=122270672.360106084.1455325780.1485060877.1485065399.56; __jdb=122270672.21.360106084|56.1485065399; __jdc=122270672; __jdu=360106084"})

    def list_page(self, response):
        classify = response.meta["classify"]
        if response.status == 302:
            self.is_over = True
            yield {}
        div_list = response.xpath("//li[@class='gl-item']/div")

        for div in div_list:
            one = BookSpiderItem()
            one["classify"] = classify
            one["from_web"] = 'jd'

            # 获取url
            url = div.xpath("./div[@class='p-img']/a/@href").extract()[0]
            if not str(url).startswith("https"):
                url = "https:"+url
            one["url"] = url

            # 获取web_id
            s = str(one['url']).rindex(r'/') + 1
            end = str(one['url']).rindex(r'.')
            one["web_id"] = one["url"][s:end]


            # 获取书名
            one["name"] = div.xpath("./div[@class='p-name']/a/em/text()").extract()[0]

            yield scrapy.Request(url=url, callback=self.detail_page, meta={"item":one})

    def detail_page(self, response):
        one = response.meta['item']

        # 获取图片url
        try:
            img_url = response.xpath("//div[@class='jqzoom']/img/@src").extract()[0]
            if not str(img_url).startswith("http"):
                img_url = "http:"+img_url
            one["img_url"] = img_url
        except:
            one["img_url"] = ""

        # 作者
        try:
            p_author = response.xpath("//div[@class='p-author']").xpath('string(.)').extract()[0].strip()
            p_author = "".join([i.strip() for i in p_author.split()])
            one["author"] = p_author
        except:
            one["author"] = ""
        # 出版社
        try:
            one["publisher"] = response.xpath("//ul[@class='p-parameter-list']/li[1]/a/text()").extract()[0]
        except:
            one["publisher"] = ""
        # 出版时间
        tmp = response.xpath("//ul[@class='p-parameter-list']/li").extract()
        publish_time = ""
        try:
            for i in tmp:
                if u"出版时间" in i:
                    publish_time = re.findall(r"\d+-\d+-\d+", i.encode("utf-8"))
                    break
            one["publish_time"] = publish_time[0]
        except:
            one["publish_time"] = ""


        # 介绍  https://dx.3.cn/desc/11153952?cdn=2&callback=showdesc
        desc_url = "https://dx.3.cn/desc/{web_id}?cdn=2&callback=showdesc".format(web_id=one["web_id"])
        yield scrapy.Request(url=desc_url, callback=self.get_desc, meta={"item":one})


    def get_desc(self, response):

        one = response.meta["item"]
        if response.status == 404:
            return one
        body = response.body
        # print type(body)

        data = from_jsonp(body)
        data = data["content"]
        soup = bs(data,'html5lib')
        # print soup.find_all("div",attrs={'id':"detail-tag-id-3"})
        try:
            desc_dom = soup.find('div',attrs={"text":"内容简介"})
            one["desc"] = desc_dom.find("div", class_="book-detail-content").text.strip()
        except:
            one["desc"] = ""
        return one
