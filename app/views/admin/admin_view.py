# -*- coding:utf-8 -*-
from flask import Blueprint, render_template, request
from flask_restful import Resource, Api
from app.views.common.view_decorators import *
from app.models import db, Module, Role_Module, User, Role
from app.views.common.utils import *
import json
import random
from hashlib import md5

admin_view = Blueprint("admin_view", __name__)
admin_view_api = Api(admin_view)


class admin_api_user(Resource):
    method_decorators = [session_check("/admin")]

    '''
        GET:  用于获取数据
        url:  /admin/api/user or /admin/api/user/<int:uid>
        request:
            {
                page: 默认为1  一页100个
                name: 选填, 搜索时用
                role_id: 选填, 搜索时用
                status: 选填, 搜索时用

            }
        response:
            {
                data:[{
                    id:         # 用户id
                    name:       # 用户名
                    password:   # 密码
                    token:      # token
                    role_name:  # 角色名
                    role_id:    # 角色id
                    status:     # 用户状态
                }],
                current_page:   # 当前页码
                total_page:     # 总页数
                has_next:       # 是否有下一页
                has_prev:       # 是否有上一页
                code:200
            }
    '''
    def get(self, uid=-1):
        one_page = 100
        page = request.args.get("page",1)
        name = request.args.get("name","")
        role_id = request.args.get("role_id","")
        status = request.args.get("status","")

        query = User.query.join(Role)

        if uid != -1:
            page = 1
            one_page = 1
            query = query.filter(User.uid==uid)

        else:
            if name:
                query = query.filter(User.name.like(u'%{name}%'.format(name=name)))
            if role_id:
                query = query.filter(User.role_id==role_id)
            if status:
                query = query.filter(User.status==status)

        query = query.with_entities(User.uid.label("uid"),\
                              User.name.label("name"),\
                              User.password.label("password"),\
                              User.token.label("token"),\
                              User.role_id.label("role_id"),\
                              Role.name.label("role_name"),\
                              User.status.label("status")).paginate(page=int(page), per_page=one_page, error_out=False)
        data = [{
                    "id":i.uid,
                    "name":i.name,
                    "password":i.password,
                    "token":i.token,
                    "role_name":i.role_name,
                    "role_id":i.role_id,
                    "status":i.status
                }for i in query.items]
        current_page = page
        total_page = query.pages
        has_next = query.has_next
        has_prev = query.has_prev
        return succeed_resp(code=200, data=data, current_page=current_page, total_page=total_page,\
                                has_prev=has_prev, has_next=has_next)

    '''
        POST:   创建新数据
        url:  /admin/api/user
        request:
            {
                name:           # 新增的用户名
                password:       # 密码
                role_id:        # 角色id
            }
        response:
            {
                code: 201 添加成功 or 422 验证失败(可能是用户名重复)
                info: 状态原因
                name: 出错的字段
            }
    '''
    def post(self):
        username = request.form.get("username")
        password = request.form.get("password")
        role_id = request.form.get("role_id")

        query = User.query.filter_by(name=username).first()
        if query:
            return succeed_resp(code=422, name="username", info=u'用户名已存在')
        else:
            one = User(name=username, password=password, role_id=role_id)
            db.session.add(one)
            db.session.flush()
            uid = one.uid
            db.session.commit()
            return succeed_resp(code=201, info=u'新增成功')

    '''
        PATCH:   修改数据
        url:  /admin/api/user/<int:uid>
        request:
            {
                password:       # 修改密码
                role_id:        # 修改角色id
            }
        response:
            {
                code: 201 添加成功 or 422 验证失败(可能是uid不存在)
                info: 状态原因
                name: 出错的字段
            }
    '''
    def patch(self, uid):
        # uid = request.form.get("uid")
        password = request.form.get("password","")
        role_id = request.form.get("role_id","")

        query = User.query.filter_by(uid=uid).first()
        if not query:
            return succeed_resp(code=422, name="username", info=u'用户不存在')
        else:
            if password:
                query.password = password
            if role_id:
                query.role_id = role_id
            db.session.commit()
            return succeed_resp(code=201, info=u'修改成功')

    '''
        DELETE:  删除数据 / 恢复数据
        url:  /admin/api/user/<int:uid>
        response:
            {
                code: 204 删除成功 or 422 用户不存在
                info: 状态原因
                user_status: 用户当前状态
            }
    '''
    def delete(self, uid):
        user_query = User.query.filter_by(uid=int(uid)).first()
        if user_query:
            status = 1 - int(user_query.status)
            user_query.status = status
            db.session.commit()
            return succeed_resp(status=1, user_status=status, info=u"success")
        else:
            return failed_resp(info=u"用户不存在", code=422)

class admin_api_role(Resource):
    method_decorators = [session_check("/admin")]

    '''
        GET:  用于获取数据
        url:  /admin/api/role
        request:
            {
                page: 默认为1  一页100个
            }
        response:
            {
                data:[{
                    id:         # 角色id
                    name:       # 角色名
                    status:     # 用户状态
                }],
                current_page:   # 当前页码
                total_page:     # 总页数
                has_next:       # 是否有下一页
                has_prev:       # 是否有上一页
                code:200
            }
    '''
    def get(self):
        one_page = 100
        page = request.form.get("page",1)
        query = Role.query.paginate(page=int(page), per_page=one_page, error_out=False)
        data = [{
                    "id":i.id,
                    "name":i.name,
                    "status":i.status
                }for i in query.items]
        current_page = page
        total_page = query.pages
        has_next = query.has_next
        has_prev = query.has_prev
        return succeed_resp(code=200, data=data, current_page=current_page, total_page=total_page,\
                                has_prev=has_prev, has_next=has_next)


class admin_api_module(Resource):
    method_decorators = [session_check("/admin")]

    '''
        GET:  用于获取数据
        url:  /admin/api/module
        request:
            {
                page: 默认为1  一页100个
            }
        response:
            {
                data:[{
                    id:         # 角色id
                    name:       # 角色名
                    url:        # 模块链接
                    icon:       # 模块图标
                    status:     # 用户状态
                }],
                current_page:   # 当前页码
                total_page:     # 总页数
                has_next:       # 是否有下一页
                has_prev:       # 是否有上一页
                code:200
            }
    '''
    def get(self):
        one_page = 100
        page = request.form.get("page",1)
        query = Module.query.paginate(page=int(page), per_page=one_page, error_out=False)
        data = [{
                    "id":i.id,
                    "name":i.name,
                    "url":i.url,
                    "icon_url":i.icon_url,
                    "status":i.status
                }for i in query.items]
        current_page = page
        total_page = query.pages
        has_next = query.has_next
        has_prev = query.has_prev

        return succeed_resp(code=200, data=data, current_page=current_page, total_page=total_page,\
                                has_prev=has_prev, has_next=has_next)
admin_view_api.add_resource(admin_api_user, "/admin/api/user", "/admin/api/user/<int:uid>")
admin_view_api.add_resource(admin_api_role, "/admin/api/role")
admin_view_api.add_resource(admin_api_module, "/admin/api/module")

@admin_view.route("/admin")
@session_check("/admin")
def admin_index():
    left = [{
        "url":"/admin",
        "child":[{
            "url":"/admin/User",
            "name":u"用户管理",
        },{
            "url":u"/admin/Role",
            "name":"角色管理",
        },{
            "url":"/admin/Module",
            "name":u"模块管理",
        }],
        "name":u"用户权限管理",
    }]
    return render_template("admin/index.html",left=left,title=u"用户权限管理")


@admin_view.route("/admin/User")
@session_check("/admin")
def admin_user():
    left = [{
        "url":"/admin",
        "child":[{
            "url":"/admin/User",
            "name":u"用户管理",
        },{
            "url":u"/admin/Role",
            "name":"角色管理",
        },{
            "url":"/admin/Module",
            "name":u"模块管理",
        }],
        "name":u"用户权限管理",
    }]
    return render_template("admin/User.html",left=left,title=u"用户权限管理")

@admin_view.route("/admin/Role")
@session_check("/admin")
def admin_role():
    left = [{
        "url":"/admin",
        "child":[{
            "url":"/admin/User",
            "name":u"用户管理",
        },{
            "url":u"/admin/Role",
            "name":"角色管理",
        },{
            "url":"/admin/Module",
            "name":u"模块管理",
        }],
        "name":u"用户权限管理",
    }]
    return render_template("admin/Role.html",left=left,title=u"用户权限管理")


@admin_view.route("/admin/api/get_role", methods=["POST"])
@session_check("/admin")
def admin_get_role():
    one_page = 100
    page = request.form.get("page",1)
    role_id = request.form.get("role_id")

    query = Role.query.paginate(page=int(page), per_page=one_page, error_out=False)
    data = [{
                "id":i.id,
                "name":i.name,
                "status":i.status
            }for i in query.items]
    current_page = page
    total_page = query.pages
    has_next = query.has_next
    has_prev = query.has_prev
    return succeed_resp(data=data, current_page=current_page, total_page=total_page,\
                            has_prev=has_prev, has_next=has_next)


@admin_view.route("/admin/api/get_module", methods=["POST"])
@session_check("/admin")
def admin_get_module():
    one_page = 100
    page = request.form.get("page",1)
    query = Module.query.paginate(page=int(page), per_page=one_page, error_out=False)
    data = [{
                "id":i.id,
                "name":i.name,
                "url":i.url,
                "icon_url":i.icon_url,
                "status":i.status
            }for i in query.items]
    current_page = page
    total_page = query.pages
    has_next = query.has_next
    has_prev = query.has_prev

    return succeed_resp(data=data, current_page=current_page, total_page=total_page,\
                            has_prev=has_prev, has_next=has_next)

@admin_view.route("/admin/api/get_role_module", methods=["GET"])
@session_check("/admin")
def admin_get_role_module():
    query = Role_Module.query.join(Role).join(Module).\
            with_entities(Role.id.label("Role_id"), Role.name.label("Role_name"),\
                          Module.id.label("Module_id"), Module.name.label("Module_name")).all()


    nodes = {}
    color_list = ["#CA0B66", "#1685C2", "#00C740", "#A219C0", "#C88230",
                  "#9CC742", "#00C8BA", "#871CC0", "#B7C642", "#00008B"]
    id_string = "{table}_{id}"
    edges = []
    index = 0
    for i in query:
        role_id = id_string.format(table="Role", id=i.Role_id)
        if role_id not in nodes:
            nodes[role_id] = {
                "id":role_id,
                "name":i.Role_name,
                "symbolSize":44,
                "itemStyle":{
                    "normal":{
                        "color": color_list[0]
                    }
                }
            }
            index += 1
        module_id = id_string.format(table="module", id=i.Module_id)
        if module_id not in nodes:
            nodes[module_id] = {
                "id":module_id,
                "name":i.Module_name,
                "symbolSize":20,
                "itemStyle":{
                    "normal":{
                        "color": color_list[1]
                    }
                }
            }
            index += 1
        edges.append({
            "source":role_id,
            "target":module_id,
            "value":random.randint(100,300)
        })
    nodes = list(nodes.values())
    # print (nodes)

    # dic = {
    #     "nodes":nodes,
    #     "edges":edges
    # }
    return succeed_resp(nodes=nodes, edges=edges)


@admin_view.route("/admin/api/change_user_status", methods=["POST"])
@session_check("/admin")
def admin_delete_user():
    uid = request.form.get("uid")
    user_query = User.query.filter_by(uid=int(uid)).first()
    if user_query:
        status = 1 - int(user_query.status)
        user_query.status = status
        db.session.commit()
        return succeed_resp(status=1, user_status=status)
    else:
        return failed_resp(message="id not exists", code=500)


@admin_view.route("/admin/api/add_edit_user", methods=["POST"])
@session_check("/admin")
def admin_add_edit_user():
    uid = request.form.get("uid")
    username = request.form.get("username")
    password = request.form.get("password")
    role_id = request.form.get("role_id")

    if int(uid) == -1:
        query = User.query.filter_by(name=username).first()
        if query:
            return succeed_resp(status='n', name="username", info=u'用户名已存在')
        else:
            one = User(name=username, password=password, role_id=role_id)
            db.session.add(one)
            db.session.flush()
            uid = one.uid
            db.session.commit()
            return succeed_resp(status='y',info=u'新增成功', uid=uid)
    else:
        query = User.query.filter_by(uid=uid, name=username).first()
        if not query:
            return succeed_resp(status='n', info=u'用户id不存在')
        else:
            query.password = password
            query.role_id = role_id
            db.session.commit()
            return succeed_resp(status='y',info=u'修改成功', uid=uid)


    return succeed_resp()
