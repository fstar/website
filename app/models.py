import time
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import VARCHAR, INTEGER, TEXT, DATETIME
from hashlib import md5
import datetime
db = SQLAlchemy()

class User(db.Model):
    MALE = 0
    FEMALE = 1
    OTHER = 2


    __tablename__   = "User"
    uid             = db.Column('uid', INTEGER(), primary_key=True, nullable=False, autoincrement=True)  # 用户ID
    name            = db.Column("name", VARCHAR(255), nullable=False)                                    # 用户名
    password        = db.Column("password", VARCHAR(255), nullable=False)                                # 用户密码
    token           = db.Column("token", VARCHAR(255), nullable=False)                                   # 用户token
    status          = db.Column("status", INTEGER(), default=1)                                          # 用户状态, 1.正常 0.停用
    role_id         = db.Column("role_id", INTEGER(), db.ForeignKey("Role.id"), default=2)               # 角色ID,外键,关联到Role表的id字段
    create_time     = db.Column("create_time", DATETIME(), default=datetime.datetime.now)                # 创建时间
    last_login_time = db.Column("last_login_time", DATETIME())                                           # 最后登录时间
    last_IP         = db.Column("last_IP", VARCHAR(length=16))                                           # 最后登录IP
    sex             = db.Column("sex", INTEGER(), default=2)
    def __init__(self, name, password, role_id, sex):
        self.name        = name
        self.token       = md5(self.name.encode("utf-8")).hexdigest()
        self.password    = password
        self.role_id     = role_id
        self.sex         = sex

class Role(db.Model):
    __tablename__ = "Role"
    id            = db.Column('id', INTEGER(), primary_key=True, nullable=False, autoincrement=True)     # 角色id
    name          = db.Column("name", VARCHAR(255), nullable=False)                                      # 角色名
    create_time   = db.Column("create_time", DATETIME(), default=datetime.datetime.now)                  # 创建时间
    status        = db.Column("status", INTEGER(), default=1)                                            # 角色状态, 1.正常 0.停用

    def __init__(self, name):
        self.name = name


class Module(db.Model):
    __tablename__ = "Module"
    id = db.Column("id", INTEGER(), primary_key=True, nullable=False, autoincrement=True)                # 模块id
    name = db.Column("name", VARCHAR(255), nullable=False)                                               # 模块名
    url = db.Column("url",VARCHAR(255))                                                                  # 模块url
    status = db.Column("status", INTEGER(), default=1)                                                   # 模块状态, 1.正常 0.停用
    icon = db.Column("icon", VARCHAR(255), default="home.svg")                                           # 模块图标
    create_time   = db.Column("create_time", DATETIME(), default=datetime.datetime.now)                  # 创建时间

    def __init__(self, name, url, icon):
        self.name = name
        self.url = url
        self.icon = icon

class Role_Module(db.Model):
    __tablename__ = "Role_Module"
    id = db.Column("id", INTEGER(), primary_key=True, nullable=False, autoincrement=True)                # 角色与模块关联id
    role_id = db.Column("role_id", INTEGER(), db.ForeignKey("Role.id"), nullable=False)                  # 角色id, 外键, 关联Role表id
    module_id = db.Column("module_id", INTEGER(), db.ForeignKey("Module.id"), nullable=False)            # 模块id, 外键, 关联Module表id
    control = db.Column("control", VARCHAR(length=255), nullable=False)                                  # 权限, add, delete, edit, select, 增删改查
    status = db.Column("status", INTEGER(), default=1)                                                   # 关联状态, 1.正常 0.停用

    def __init__(self, role_id, module_id, control="add,delete,edit,select", status=1):
        self.role_id = role_id
        self.module_id = module_id
        self.control = control
        self.status = status

class Group(db.Model):
    __tablename__ = "Group"

    RUN = 1
    STOP = 0
    ERROR = -1

    id     = db.Column("id", INTEGER(), primary_key=True, nullable=False, autoincrement=True)            # 分组id
    name   = db.Column("name", VARCHAR(255),nullable=False, default='')                                  # 分组名
    status = db.Column('status', INTEGER(), nullable=False, default=1)                             # 分组状态

    def __init__(self, name):
        self.name = name

class User_Group(db.Model):
    __tablename__ = 'User_Group'

    RUN = 1
    STOP = 0
    ERROR = -1

    id       = db.Column("id", INTEGER(), primary_key=True, nullable=False, autoincrement=True)          # 分组id
    User_id  = db.Column("User_id", INTEGER(), db.ForeignKey("User.uid"), nullable=False)                # 用户id
    Group_id = db.Column("Group_id", INTEGER(), db.ForeignKey("Group.id"), nullable=False)               # 分组id
    status   = db.Column('status', INTEGER(), nullable=False, default=1)                           # 分组状态

    def __init__(self, User_id, Group_id, status=1):
        self.User_id  = User_id
        self.Group_id = Group_id
        self.status   = status





class Library_User(db.Model):
    __tablename__ = 'Library_User'
    id            = db.Column("id", INTEGER(), primary_key=True, nullable=False, autoincrement=True)     # id
    user_id       = db.Column("user_id", INTEGER(), db.ForeignKey("User.uid"), nullable=False)           # 用户表id
    name          = db.Column("name", VARCHAR(255), nullable=False)                                      # 用户昵称
    phone         = db.Column("phone", VARCHAR(20))                                                      # 用户联系电话
    address       = db.Column("address", VARCHAR(500))                                                   # 用户地址
    create_time   = db.Column("create_time", DATETIME(), default=datetime.datetime.now)                  # 创建时间
    update_time   = db.Column("update_time", DATETIME(), onupdate=datetime.datetime.now)                 # 修改时间
    sex           = db.Column("sex", INTEGER(), default=3)                                               # 性别 1.男 2.女 3.其他

    def __init__(self, user_id, name, phone, address, sex):
        self.user_id = user_id
        self.name    = name
        self.phone   = phone
        self.address = address
        self.sex     = sex

class Library_Book(db.Model):
    __tablename__ = 'Library_Book'
    id            = db.Column("id", INTEGER(), primary_key=True, nullable=False, autoincrement=True)     # id
    name          = db.Column("name", VARCHAR(255), nullable=False)                                      # 书名
    classify      = db.Column("classify", VARCHAR(255), nullable=False, default=u'其他')      # 分类(以豆瓣的读书分类作参考, 前端写死), 多标签用逗号隔开
    author        = db.Column('author', VARCHAR(255), nullable=False, default=u"未知")                    # 作者
    ISBN          = db.Column('ISBN', VARCHAR(255), nullable=False, default=u"")                         # ISBN
    publisher     = db.Column('publisher', VARCHAR(255), nullable=False, default=u'其他')                 # 出版社
    publish_time  = db.Column("publish_time", VARCHAR(255), default=u"未知")                             # 出版时间
    desc          = db.Column("desc", TEXT(), default='')                                               # 描述, 简介, 看点等等
    lender        = db.Column('lender', INTEGER(), db.ForeignKey("Library_User.id"), nullable=False)     # 出借人(书的所有者)id
    borrower      = db.Column('borrower', INTEGER(), db.ForeignKey("Library_User.id"))                   # 借书人id
    status        = db.Column("status", INTEGER(), nullable=False, default=0)                            # 状态: -1,下架 0,未借出 1,预订中 2,已借出
    create_time   = db.Column("create_time", DATETIME(), default=datetime.datetime.now)                  # 创建时间
    update_time   = db.Column("update_time", DATETIME(), onupdate=datetime.datetime.now)                 # 修改时间
    img_url       = db.Column("img_url", VARCHAR(255))
    def __init__(self, name, lender, classify, author, desc, publisher, img_url=None, ISBN=None):
        self.name   = name
        self.lender = lender
        if classify:
            self.classify = classify
        if author:
            self.author = author
        if desc:
            self.desc = desc
        if publisher:
            self.publisher = publisher
        if img_url:
            self.img_url = img_url
        if ISBN:
            self.ISBN = ISBN

class Borrow_Lend(db.Model):
    __tablename__ = 'Borrow_Lend'
    id            = db.Column("id", INTEGER(), primary_key=True, nullable=False, autoincrement=True)     # id
    book_id       = db.Column("book_id", INTEGER(), db.ForeignKey('Library_Book.id'), nullable=False)    # 书的id
    lender        = db.Column("lender", INTEGER(), db.ForeignKey('Library_User.id'), nullable=False)     # 出借人的id
    borrower      = db.Column("borrower", INTEGER(), db.ForeignKey('Library_User.id'), nullable=False)   # 借书人的id
    action        = db.Column("action", INTEGER(), nullable=False)                                       # 动作:1,borrow(借),2,return(还),3,reservation(预定), 4,refuse(拒绝)
    create_time   = db.Column("create_time", DATETIME(), default=datetime.datetime.now)                  # 创建时间
    borrow_time   = db.Column("borrow_time", DATETIME())                                                 # 出借时间
    return_time   = db.Column("return_time", DATETIME())                                                 # 归还时间
    update_time   = db.Column("update_time", DATETIME(), default=datetime.datetime.now, onupdate=datetime.datetime.now)                 # 更新时间

    def __init__(self, book_id, borrower, lender):
        self.book_id  = book_id
        self.borrower = borrower
        self.lender   = lender
        self.action   = 3


class Library_Classify(db.Model):
    '''
        说明:
            这张表用来记录各个书目分类的表, 目前根据豆瓣分类, 会先写死, 之后会新增, 新增并不是用户写一个新的, 就新增一条, 而是后期统计之后
          发现有些新增分类的书籍占到一定数量时, 那么再填入这张表.
    '''
    __tablename__ = 'Library_Classify'
    id            = db.Column("id", INTEGER(), primary_key=True, nullable=False, autoincrement=True)     # id
    first_level   = db.Column("first_level", VARCHAR(255), nullable=False)                               # 第一层分类
    second_level  = db.Column("second_level", VARCHAR(255), nullable=False)                              # 第二层分类

class Library_message(db.Model):
    '''
        保存所有的聊天信息
        1. 方便留言
        2. 方便看历史记录
    '''
    __tablename__ = 'Library_message'
    id            = db.Column("id", INTEGER(), primary_key=True, nullable=False, autoincrement=True)     # id
    sender        = db.Column("sender", INTEGER(), db.ForeignKey('Library_User.id'), nullable=False)     # 发送方id
    receiver      = db.Column("receiver", INTEGER(), db.ForeignKey('Library_User.id'), nullable=False)   # 接受方id
    message       = db.Column("message", TEXT(), nullable=False, default="")                             # 消息
    status        = db.Column("status", INTEGER(), default=0)                                            # 是否已被查看

    def __init__(self, sender, receiver, message, status=0):
        self.sender   = sender
        self.receiver = receiver
        self.message  = message
        self.status   = status

class Book_Spider(db.Model):
    '''
        图书爬虫
    '''
    __tablename__ = "Book_Spider"
    id            = db.Column("id", INTEGER(), primary_key=True, nullable=False, autoincrement=True)     # id
    name          = db.Column('name', VARCHAR(255),nullable=False)                                       # 书名
    classify      = db.Column("classify", VARCHAR(255), nullable=False, default=u'其他')                  # 分类
    author        = db.Column('author', VARCHAR(255), nullable=False, default=u"未知")                    # 作者
    publisher     = db.Column('publisher', VARCHAR(255), nullable=False, default=u'其他')                 # 出版社
    publish_time  = db.Column("publish_time", VARCHAR(255))                                              # 出版时间
    desc          = db.Column("desc", TEXT(), default='空')                                              # 描述, 简介, 看点等等
    from_web      = db.Column('from_web', VARCHAR(255), nullable=False)                                  # 来源
    web_id        = db.Column('web_id', VARCHAR(255), nullable=False)                                    # 来源站内的图书id
    url           = db.Column('url', VARCHAR(255), nullable=False)                                       # 图书详情页url
    img_url       = db.Column('img_url', TEXT())                                                         # 图书图片组url
    uid           = db.Column("user_id", INTEGER(), db.ForeignKey("User.uid"), nullable=False)           # 用户表id

    def __init__(self, name, from_web, web_id, url, uid, classify=None, author=None, publisher=None,\
                 publish_time=None, desc=None, img_url=None):
        self.name     = name
        self.from_web = from_web
        self.web_id   = web_id
        self.url      = url
        self.uid      = uid
        if classify:
            self.classify = classify
        if author:
            self.author = author
        if publisher:
            self.publisher = publisher
        if publish_time:
            self.publish_time = publish_time
        if desc:
            self.desc = desc
        if img_url:
            self.img_url = img_url

class History_action(db.Model):
    '''
        历史事件表
    '''
    __tablename__ = 'history_action'

    id       = db.Column("id", INTEGER(), primary_key=True, nullable=False, autoincrement=True)     # id
    year     = db.Column('year',VARCHAR(255),nullable=False,default='')                    # 事件发生时间
    area     = db.Column('area',VARCHAR(255),nullable=False,default='')                    # 地点
    country  = db.Column('country',VARCHAR(255),default='')                     # 国家
    county   = db.Column('county',VARCHAR(255),default='')                      # 洲
    action   = db.Column('action',TEXT(),default='')                            # 事件内容
    person   = db.Column('person',VARCHAR(255),default='')                      # 事件人物
    year_num = db.Column('year_num',INTEGER(),default=0)                        # 事件年份统一化
    user_id  = db.Column('user_id',INTEGER(),db.ForeignKey("User.uid"))         # 写入事件的用户

    def __init__(self, year, area, country, county, action, person, user_id):
        self.year     = year
        self.area     = area
        self.country  = country
        self.county   = county
        self.action   = action
        self.person   = person
        self.user_id  = user_id
        self.year_num = history_action.year_to_year_num(year)

    @classmethod
    def year_to_year_num(cls, year):
        sign      = 1
        year_num  = "%04d"
        month_num = "%02d"
        day_num   = "%02d"

        if year.startswith("公元前"):
            sign = -1
        elif year.startswith("公元后"):
            sign = 1


        date = year.split(":")[-1]
        year_index = date.find("年")
        year_num = year_num%(int(date[:year_index]))

        month_index = date.find("月")
        if month_index != -1:
            month_num = month_num % (int(date[year_index+1:month_index]))
        else:
            month_num = month_num % (0)

        day_index = date.find("日")
        if day_index != -1:
            day_num = day_num%(int(date[month_index+1:day_index]))
        else:
            day_num = day_num%(0)

        return sign * int(year_num+month_num+day_num)

class Action_relationship(db.Model):
    __tablename__ = 'action_relationship'

    id            = db.Column("id", INTEGER(), primary_key=True, nullable=False, autoincrement=True) # id
    first_action  = db.Column("first_action", INTEGER(), db.ForeignKey("history_action.id"), nullable=False)  # 事件1
    second_action = db.Column("second_action", INTEGER(), db.ForeignKey("history_action.id"), nullable=False) # 事件2
    reason        = db.Column("reason", TEXT(),nullable=False, default="")
    user_id       = db.Column('user_id',INTEGER(),db.ForeignKey("User.uid"))    # 写入事件的用户

    def __init__(self, first_action, second_action, reason, user_id):
        self.first_action = first_action
        self.second_action = second_action
        self.reason
        self.user_id

class UN_Country(db.Model):
    __tablename__ = "UN_Country"
    id            = db.Column("id", INTEGER(), primary_key=True, nullable=False, autoincrement=True)     # id
    continent     = db.Column('continent', VARCHAR(255),nullable=False, default='')
    capital       = db.Column('capital', VARCHAR(255),nullable=False, default='')
    languages     = db.Column('languages', VARCHAR(255),nullable=False, default='')
    geonameId     = db.Column('geonameId', INTEGER(),nullable=False)
    south         = db.Column('south', INTEGER(),nullable=False)
    isoAlpha3     = db.Column('isoAlpha3', VARCHAR(255),nullable=False, default='')
    north         = db.Column('north', INTEGER(),nullable=False)
    fipsCode      = db.Column('fipsCode', VARCHAR(255),nullable=False, default='')
    population    = db.Column('population', VARCHAR(255),nullable=False, default='')
    east          = db.Column('east', INTEGER(),nullable=False)
    isoNumeric    = db.Column('isoNumeric', VARCHAR(255),nullable=False, default='')
    areaInSqKm    = db.Column('areaInSqKm', VARCHAR(255),nullable=False, default='')
    countryCode   = db.Column('countryCode', VARCHAR(255),nullable=False, default='')
    west          = db.Column('west', INTEGER(),nullable=False)
    countryName   = db.Column('countryName', VARCHAR(255),nullable=False, default='')
    continentName = db.Column('continentName', VARCHAR(255),nullable=False, default='')
    currencyCode  = db.Column('currencyCode', VARCHAR(255),nullable=False, default='')

    def __init__(self,data):
        self.continent = data["continent"]
        self.capital = data["capital"]
        self.languages = data["languages"]
        self.geonameId = data["geonameId"]
        self.south = data["south"]
        self.isoAlpha3 = data["isoAlpha3"]
        self.north = data["north"]
        self.fipsCode = data["fipsCode"]
        self.population = data["population"]
        self.east = data["east"]
        self.isoNumeric = data["isoNumeric"]
        self.areaInSqKm = data["areaInSqKm"]
        self.countryCode = data["countryCode"]
        self.west = data["west"]
        self.countryName = data["countryName"]
        self.continentName = data["continentName"]
        self.currencyCode = data["currencyCode"]
