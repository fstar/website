import time
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import VARCHAR, INTEGER, TEXT
from hashlib import md5
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "User"
    uid = db.Column('uid', INTEGER(), primary_key=True, nullable=False, autoincrement=True)
    name = db.Column("name", VARCHAR(255), nullable=False)
    token = db.Column("token", VARCHAR(255), nullable=False)
    create_time = db.Column("create_time", INTEGER())
    status = db.Column("status", INTEGER(), default=1)
    password = db.Column("password", VARCHAR(255), nullable=False)
    role_id = db.Column("role_id", INTEGER(), db.ForeignKey("Role.id"), default=2)

    def __init__(self, name, password, role_id):
        self.name = name
        self.token = md5(self.name.encode("utf-8")).hexdigest()
        self.create_time = int(time.time())
        self.password = password
        self.role_id = role_id


class Role(db.Model):
    __tablename__ = "Role"
    id = db.Column('id', INTEGER(), primary_key=True, nullable=False, autoincrement=True)
    name = db.Column("name", VARCHAR(255), nullable=False)
    create_time = db.Column("create_time", INTEGER())
    status = db.Column("status", INTEGER(), default=1)

    def __init__(self, name):
        self.name = name
        self.create_time = int(time.time())


class Module(db.Model):
    __tablename__ = "Module"
    id = db.Column("id", INTEGER(), primary_key=True, nullable=False, autoincrement=True)
    name = db.Column("name", VARCHAR(255), nullable=False)
    url = db.Column("url",VARCHAR(255))
    create_time = db.Column("create_time", INTEGER())
    status = db.Column("status", INTEGER(), default=1)
    icon_url = db.Column("icon_url", VARCHAR(255), default="home.svg")

    def __init__(self, name, url, icon_url):
        self.name = name
        self.url = url
        self.create_time = int(time.time())
        self.icon_url = icon_url

class Role_Module(db.Model):
    __tablename__ = "Role_Module"
    id = db.Column("id", INTEGER(), primary_key=True, nullable=False, autoincrement=True)
    role_id = db.Column("role_id", INTEGER(), db.ForeignKey("Role.id"))
    module_id = db.Column("module_id", INTEGER(), db.ForeignKey("Module.id"))
    status = db.Column("status", INTEGER(), default=1)

    def __init__(self, role_id, module_id):
        self.role_id = role_id
        self.module_id = module_id
