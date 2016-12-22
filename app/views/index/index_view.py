# -*- coding:utf-8 -*-
from flask import Blueprint, render_template
from app.views.common.view_decorators import *
from app.models import db, Module, Role_Module
from app.views.common.utils import *

index_view = Blueprint("index_view", __name__)


@index_view.route("/index")
@session_check()
def index():
    return render_template("index/index.html")


@index_view.route("/index/get_module")
@session_check()
def index_get_module():
    role_id = session["role_id"]
    query = Module.query.join(Role_Module).\
            filter(Role_Module.role_id==role_id, Role_Module.status==1, Module.status==1).\
            with_entities(Module.name.label("name"), Module.url.label("url"), Module.icon_url.label("icon_url")).all()
    dic =[{"name":u"退出", "url":"/logout", "icon_url":"logout9.svg"}]+ [{"name":i.name, "url":i.url, "icon_url":i.icon_url} for i in query]
    return succeed_resp(data=dic)
