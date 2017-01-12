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
