import time
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import VARCHAR, INTEGER, TEXT, DATETIME
from hashlib import md5
import datetime
db = SQLAlchemy()

class User(db.Model):
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

    def __init__(self, name, password, role_id):
        self.name        = name
        self.token       = md5(self.name.encode("utf-8")).hexdigest()
        self.password    = password
        self.role_id     = role_id


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
