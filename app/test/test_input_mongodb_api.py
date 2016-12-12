# -*- coding:utf-8 -*-
import json
import requests

header = {
    "token":"fx123456781"
    # "token":"fx64562983"
}
url = "http://localhost:8080"
# url = "http://114.215.186.236:8888"

def get():
    pass

def post():
    company_data={
    "rule":json.dumps({
        "classify":"company",
    }),
        "data":json.dumps({			 # 数据部分
        		"web_id":"3",         # 网页的id
                "name":"test",           # 公司名称
                "boss":"test",           # 公司老板
                "category":"a",       # 公司类别
                "level":"3",          # 公司融资等级
                "people_number":123,  # 公司人数
                "location":"tttt",       # 公司地址
                "description":"ttttt",    # 公司描述
                "web_url":"http://www.baidu.com",        # 招聘网站页面url
                "company_url":"http://www.baidu.com",    # 公司官方网站url
                "rate":"",           # 公司简历处理率(投递后7天内)
                "from_web":"lagou",       # 数据来源
                "status":"1",         # 数据状态,0表示未完成,1表示已完成,2表示过期
                "aaaa":"bbbb",
                "ccc":"ddd"
        }),
        "relation":json.dumps([])
    }
    company_url = url+"/api/input_mongodb/company"
    req = requests.post(url=company_url, data=company_data, headers=header)
    print(req.content)
    for i in range(100):
        job_data={
        "rule":json.dumps({"classify":"job"}),
            "data":json.dumps({			 # 数据部分
            		"web_id":str(i),          # 网页的id
                    "name":"test",            # 职位名称
                    "salary":1234,          # 薪资
                    "job_year":"1年",       # 工作经验
                    "education":"本科",       # 学历
                    "employee_type":"全职",   # 全职 or 实习
                    "web_url":"www.baidu.com",         # 职位url
                    "from_web":"lagou",	        # 数据来源
                    "status":1,          # 数据状态,0表示未完成,1表示已完成,2表示过期
                    "location":"shanghai"
            }),
            "relation":json.dumps([{
                "table":"company",
                "web_id":"3",
                "from_web":"lagou"
            }])
        }
        company_url = url+"/api/input_mongodb/job"
        req = requests.post(url=company_url, data=job_data, headers=header)
        print(req.content)


def patch():
    return

def delete():
    pass

if __name__ == "__main__":
    post()
