import json
import requests

header = {
    "token":"Fx645629834"
}

def get():
    pass

def post():
    company_data ={
                "web_id":"1234",         # 网页的id
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
            }
    company_url = "http://114.215.186.236:8888/api/input_data/company_info"
    req = requests.post(url=company_url, data=company_data, headers=header)
    print(req.content)

    job_data ={
                "web_id":"a123",          # 网页的id
                "company_id":"1",      # 公司表的唯一id
                "name":"码农",            # 职位名称
                "salary":"123456",          # 薪资
                "job_year":"1年",	        # 工作经验
                "education":"本科",       # 学历
                "employee_type":"全职",   # 全职 or 实习
                "web_url":"http://www.baidu.com",         # 职位url
                "from_web":"lagou",	        # 数据来源
                "status":"1",          # 数据状态,0表示未完成,1表示已完成,2表示过期
                "aaaa":"bbbb",
                "ccc":"ddd"
            }
    job_url = "http://114.215.186.236:8888/api/input_data/job_info"
    req = requests.post(url=job_url, data=job_data, headers=header)
    print (req.content)

def patch():
    company_data = {
        "web_id":"1234",         # 网页的id
        "from_web":"lagou",       # 数据来源
        "status":1,         # 数据状态,0表示未完成,1表示已完成,2表示过期
        "db_id":"1",          # 数据库中某条记录的唯一id
        "data_json":json.dumps({"category":"b",       # 公司类别
                                "level":"4",          # 公司融资等级
                                "people_number":1123,  # 公司人数})
                                "aaaa":"fffff",
                                "ddd":"eeee",
                                "status":1,
                                "12312":1231231
                               })
        }
    job_url = "http://114.215.186.236:8888/api/input_data/company_info"
    req = requests.patch(url=job_url, data=company_data, headers=header)
    print (req.content)

    job_data = {
        "web_id":"a123",         # 网页的id
        "from_web":"lagou",       # 数据来源
        "status":1,         # 数据状态,0表示未完成,1表示已完成,2表示过期
        "db_id":"1",          # 数据库中某条记录的唯一id
        "data_json":json.dumps({"salary":"999999",          # 薪资
                                "job_year":"2年",	        # 工作经验
                                "web_url":"http://www.google.com",         # 职位url
                                "status":"1",          # 数据状态,0表示未完成,1表示已完成,2表示过期
                                "aaaa":"eee",
                                "ccc":"fff",
                                "xxx":"yyy"
                               })
        }
    job_url = "http://114.215.186.236:8888/api/input_data/job_info"
    req = requests.patch(url=job_url, data=job_data, headers=header)
    print (req.content)

def delete():
    pass

if __name__ == "__main__":
    patch()
