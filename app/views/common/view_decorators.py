# -*- coding:utf-8 -*-
from flask import request, session, redirect
from functools import wraps
from app.views.common.utils import failed_resp
from app.models import db, User


def cls_decorate(my_decorator, exempt=None):
    if exempt is None:
        exempt = []
    else:
        exempt = exempt if isinstance(exempt, list) else [exempt]
    def add_decorator(cls, addr, func, deco):
        if func.__name__ in exempt:
            print ("%s exempt deco:%s" % (func.__name__, deco.__name__))
            return
        setattr(cls, addr, deco(func))
    def decorator(cls):
        for attr in cls.__dict__:  # just for it's own method without inherited method:
            func = getattr(cls, attr)
            if callable(func):
                if isinstance(my_decorator, list):
                    for deco in my_decorator:
                        add_decorator(cls, attr, func, deco)
                else:
                    add_decorator(cls, attr, func, my_decorator)
        return cls
    return decorator

def permission_check(func):
    @wraps(func)
    def _decorate(*args, **kwargs):
        token = request.headers.get("token","")
        if not token:   # 如果头部信息里没有token,返回401
            return failed_resp("token missing", 401)
        user_query = spider_user.query.filter_by(token=token, status=1).first()
        if not user_query: # 如果token在数据库里不存在,返回401
            return failed_resp(u"token 错误", 401)
        # 如果token存在,则返回uid
        uid = user_query.uid
        kwargs.update(uid=uid)
        return func(*args, **kwargs)
    return _decorate


def session_check(redirect_for='/'):
    """只验证session"""

    def decorated(f):
        @wraps(f)
        def decorated_fn(*args, **kwargs):
            if not session or "uid" not in session or "name" not in session:
                return redirect(redirect_for)
            return f(*args, **kwargs)
        return decorated_fn
    return decorated
