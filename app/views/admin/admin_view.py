# -*- coding:utf-8 -*-
from flask import Blueprint, render_template, request
from flask_restful import Resource, Api
from app.views.common.view_decorators import *
from app.models import db, Module, Role_Module, User, Role
from app.views.common.utils import *
import json
import random
from hashlib import md5
from sqlalchemy import or_

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
        return succeed_resp(data=data, current_page=current_page, total_page=total_page,\
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
        password = request.form.get("password", "").strip()
        role_id = request.form.get("role_id")

        query = User.query.filter_by(name=username).first()
        if not password:
            return succeed_resp(code=422, name="password", info=u"密码不能为空")
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
        url:  /admin/api/role or /admin/api/role/<int:role_id>
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
    def get(self, role_id=None):
        query = Role.query.all()
        data = [{
                "id":i.id,
                "name":i.name,
                "status":i.status
                }for i in query]
        return succeed_resp(code=200, data=data)

    '''
        POST:   创建新角色
        url:  /admin/api/role
        request:
            {
                name:           # 新增的角色名
                module_list     # 新增角色的模块权限

            }
        response:
            {
                code: 201 添加成功 or 422 验证失败(可能是用户名重复)
                info: 状态原因
                name: 出错的字段
                role_id: 成功添加后, 会返回新生成的role_id
            }
    '''
    def post(self):
        name = request.form.get("name")
        module_list = request.form.get("module_list",None)

        query = Role.query.filter_by(name=name).first()
        if query:
            return succeed_resp(code=422, name="name", info=u'角色已存在')
        else:
            one = Role(name=name)
            db.session.add(one)
            db.session.flush()
            role_id = one.id
            db.session.commit()
            if module_list:
                module_list = json.loads(module_list)
                for key, value in module_list.items():
                    one = Role_Module(role_id, key, "add,delete,edit,select", value)
                    db.session.add(one)
                db.session.commit()
            return succeed_resp(role_id=role_id, code=201, info=u'新增成功')

    '''
        DELETE:  删除数据 / 恢复数据
        url:  /admin/api/role/<int:role_id>
        response:
            {
                code: 204 删除成功 or 422 用户不存在
                info: 状态原因
                user_status: 用户当前状态
            }
    '''
    def delete(self, role_id):
        query = Role.query.filter_by(id=int(role_id)).first()
        if query:
            status = 1 - int(query.status)
            query.status = status
            db.session.commit()
            return succeed_resp(status=1, role_status=status, info=u"success")
        else:
            return failed_resp(info=u"角色不存在", code=422)

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
        query = Module.query.all()
        data = [{
                    "id":i.id,
                    "name":i.name,
                    "url":i.url,
                    "icon_url":i.icon,
                    "status":i.status
                }for i in query]

        return succeed_resp(code=200, data=data)
    '''
        POST:   创建新模块
        url:  /admin/api/module
        request:
            {
                name:           # 新增的模块名
                url:            # 新增的模块url
                icon_url:       # 模块图片url 200*200 默认home.svg
            }
        response:
            {
                code: 201 添加成功 or 422 验证失败(可能是用户名重复)
                info: 状态原因
                name: 出错的字段
            }
    '''
    def post(self):
        name = request.form.get("name")
        url = request.form.get("url")
        icon_url = request.form.get("icon_url")

        query = Module.query.filter(or_(Module.name==name, Module.url==url)).first()
        if query:
            if query.name == name:
                return succeed_resp(code=422, name="name", info=u'模块名已存在')
            if query.url == url:
                return succeed_resp(code=422, name="url", info=u'模块url已存在')
        else:
            one = Module(name=name, url=url, icon=icon_url)
            db.session.add(one)
            db.session.flush()
            module_id = one.id
            db.session.commit()
            return succeed_resp(module_id=module_id, code=201, info=u'新增成功')

    '''
        PATCH:   修改数据
        url:  /admin/api/module/<int:module_id>
        request:
            {
                url:            # 模块的url
                icon_url:       # 图标的url
            }
        response:
            {
                code: 201 添加成功 or 422 验证失败(可能是uid不存在)
                info: 状态原因
                name: 出错的字段
            }
    '''
    def patch(self, module_id):
        # uid = request.form.get("uid")
        url = request.form.get("url","")
        icon_url = request.form.get("icon_url","")

        query = Module.query.filter_by(id=module_id).first()
        if not query:
            return succeed_resp(code=422, name="module_id", info=u'模块不存在')
        else:
            url_query = Module.query.filter(Module.id!=module_id, Module.url==url).first()
            if url_query:
                return succeed_resp(code=422, name='url', info=u'url已存在, 请看module_id={module_id}'.format(module_id=url_query.id))
            if url:
                query.url = url
            if icon_url:
                query.icon = icon_url
            db.session.commit()
            return succeed_resp(code=201, info=u'修改成功')

    '''
        DELETE:  删除数据 / 恢复数据
        url:  /admin/api/module/<int:module_id>
        response:
            {
                code: 204 删除成功 or 422 用户不存在
                info: 状态原因
                module_status: 用户当前状态
            }
    '''
    def delete(self, module_id):
        query = Module.query.filter_by(id=int(module_id)).first()
        if query:
            status = 1 - int(query.status)
            query.status = status
            db.session.commit()
            return succeed_resp(status=1, module_status=status, info=u"success")
        else:
            return failed_resp(info=u"模块不存在", code=422)

class admin_api_role_module(Resource):
    method_decorators = [session_check("/admin")]

    '''
        GET:  用于获取数据
        url:  /admin/api/role_module
        request:
            {
                role_id:        # 角色id
            }
        response:
            {
                data:[{
                    module_id:  # 模块id
                }],
                code:200
            }
    '''
    def get(self):
        role_id = request.args.get("role_id",-1)
        query = Role_Module.query.filter_by(role_id=role_id, status=1).all()
        data = [i.module_id for i in query]
        return succeed_resp(code=200, data=data)
    '''
        POST:   创建或修改新的角色模块关系
        url:  /admin/api/role_module
        request:
            {
                role_id:        # 角色id
                module:         # 模块id
                        {
                            module_id1 : status,
                            module_id2 : status,
                            module_id3 : status,
                        }
            }
        response:
            {
                code: 201 添加成功 or 422 验证失败(可能是用户名重复)
                info: 状态原因
                name: 出错的字段
            }
    '''
    def post(self):
        role_id = request.form.get("role_id")
        module_list = json.loads(request.form.get("module_list"))

        role_query = Role.query.filter_by(id=role_id).first()
        if not role_query:
            return failed_resp(message=u"role_id 不存在")

        module_query = Module.query.filter(Module.id.in_(module_list.keys())).count()
        if len(module_list.keys()) != module_query:
            return failed_resp(message=u"module 的数据有异常")

        for module_id, status in module_list.items():
            query = Role_Module.query.filter_by(role_id=role_id, module_id=module_id).first()
            if query:
                query.status = status
            else:
                one = Role_Module(role_id=role_id, module_id=module_id, status=status)
                db.session.add(one)
            db.session.commit()
        return succeed_resp(code=201, info=u'修改成功')

admin_view_api.add_resource(admin_api_user, "/admin/api/user", "/admin/api/user/<int:uid>")
admin_view_api.add_resource(admin_api_role, "/admin/api/role", "/admin/api/role/<int:role_id>")
admin_view_api.add_resource(admin_api_module, "/admin/api/module", "/admin/api/module/<int:module_id>")
admin_view_api.add_resource(admin_api_role_module, "/admin/api/role_module")

@admin_view.route("/admin")
@session_check("/admin")
def admin_index():
    left = [{
        "url":"/admin",
        "child":[{
            "url":"/admin/User",
            "name":u"用户管理",
        },{
            "url":u"/admin/Role_Module",
            "name":"角色模块管理",
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
            "url":u"/admin/Role_Module",
            "name":"角色模块管理",
        }],
        "name":u"用户权限管理",
    }]
    return render_template("admin/User.html",left=left,title=u"用户权限管理")

@admin_view.route("/admin/Role_Module")
@session_check("/admin")
def admin_role():
    left = [{
        "url":"/admin",
        "child":[{
            "url":"/admin/User",
            "name":u"用户管理",
        },{
            "url":u"/admin/Role_Module",
            "name":"角色模块管理",
        }],
        "name":u"用户权限管理",
    }]
    return render_template("admin/Role.html",left=left,title=u"用户权限管理")


@admin_view.route("/admin/api/get_role_module", methods=["GET"])
@session_check("/admin")
def admin_get_role_module():
    query = Role.query.outerjoin(Role_Module).outerjoin(Module).\
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
        if i.Role_id and role_id not in nodes:
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
        if i.Module_id and module_id not in nodes:
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
    return succeed_resp(nodes=nodes, edges=edges)
