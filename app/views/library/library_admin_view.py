from flask import Blueprint, render_template, request, redirect, session, url_for
from app.views.common.view_decorators import *
from app.models import db, User, Library_User, Library_Book, Borrow_Lend, Library_Classify, Library_message
from app.views.common.utils import *
import json
from sqlalchemy import func
from sqlalchemy.orm import aliased

library_admin_view = Blueprint("library_admin_view", __name__)


def library_admin_decorator(func):
    @wraps(func)
    def _func(*args, **kwargs):
        role_id = session["role_id"]
        if role_id == 1:
            return func(*args, **kwargs)
        else:
            return render_template("404.html"), 403
    return _func


@library_admin_view.route("/Library/admin")
@session_check("/Library")
@library_admin_decorator
def Library_admin_index():
    return render_template("/library/admin_index.html")


@library_admin_view.route("/Library/admin/pie_data")
@session_check("/Library")
@library_admin_decorator
def Library_admin_user():
    # 用户统计数据
    user_query = Library_User.query.group_by(Library_User.sex).\
            with_entities(Library_User.sex.label('sex'), func.count(Library_User.sex).label('num')).\
            all()
    user_data = [
                {"value":0, "name":'男'},
                {"value":0, "name":'女'},
                {"value":0, "name":'其他'},
            ]
    for i in user_query:
        user_data[i.sex-1]['value'] += i.num

    # 书目统计信息
    books_publish_query = Library_Book.query.group_by(Library_Book.publish_time, Library_Book.publisher).\
            with_entities(Library_Book.publish_time.label('publish_time'),Library_Book.publisher.label('publisher'),\
            func.count(Library_Book.publish_time).label('num')).\
            all()
    book_publisher_time_data = []
    book_publisher = []
    temp_data = {}
    temp_data2 = {}
    for i in books_publish_query:
        if i.publish_time in temp_data:
            temp_data[i.publish_time] += i.num
        else:
            temp_data[i.publish_time] = i.num
        if i.publisher in temp_data2:
            temp_data2[i.publisher] += i.num
        else:
            temp_data2[i.publisher] = i.num

    book_publisher_time_data = [{"value":value, "name":key} for key, value in temp_data.items()]
    book_publisher = [{"value":value, "name":key} for key, value in temp_data2.items()]

    # 借阅统计信息
    history_query = Borrow_Lend.query.group_by(Borrow_Lend.action).\
            with_entities(Borrow_Lend.action.label('action'), func.count(Borrow_Lend.action).label('num')).\
            all()
    history_data = []
    temp_data = {}
    for i in history_query:
        if i.action in temp_data:
            temp_data[i.action] += i.num
        else:
            temp_data[i.action] = i.num
    dic = {
        1:"借",
        2:"还",
        3:"预定",
        4:"拒绝"
    }
    history_data = [{"value":value, "name":dic[key]} for key, value in temp_data.items()]
    return succeed_resp(user_data=user_data, book_publisher_time_data = book_publisher_time_data, \
            book_publisher=book_publisher, history_data=history_data)

@library_admin_view.route("/Library/admin/user_data")
@session_check("/Library")
@library_admin_decorator
def Library_admin_user_data():
    # page = request.args.get('page',1)
    sex = request.args.get('sex',None)
    user_query = Library_User.query.join(User, Library_User.user_id==User.uid).\
                with_entities(Library_User.name.label('lib_name'),\
                              Library_User.phone.label('phone'),\
                              Library_User.address.label('address'),\
                              Library_User.sex.label('sex'),\
                              User.name.label('user_name'))
    if sex:
        user_query = user_query.order_by(func.field(Library_User.sex,sex).desc())
    user_query = user_query.all()
    data = [{
        "lib_name":i.lib_name,
        "phone":Caesar_decode(i.phone),
        "address":Caesar_decode(i.address),
        "sex":i.sex,
        "user_name":i.user_name
    }for i in user_query]
    return succeed_resp(data=data)


@library_admin_view.route("/Library/admin/book_data")
@library_admin_view.route("/Library/admin/book_data/<int:page>")
@session_check("/Library")
@library_admin_decorator
def Library_admin_book_data(page=1):
    User_table = aliased(Library_User, name='user2')
    book_query = Library_Book.query.\
        outerjoin(Library_User, Library_Book.borrower==Library_User.id).\
        join(User_table, Library_Book.lender == User_table.id).\
        with_entities(Library_Book.id.label("id"),\
                                              Library_Book.name.label('name'),\
                                              Library_Book.classify.label('classify'),
                                              Library_Book.author.label('author'),\
                                              Library_Book.publisher.label('publisher'),\
                                              Library_Book.publish_time.label('publish_time'),\
                                              Library_Book.desc.label('desc'),\
                                              Library_Book.status.label('status'),\
                                              User_table.name.label('lender_name'),\
                                              Library_User.name.label('borrower_name')).\
                                              paginate(page, per_page=50, error_out=False)
    pre_href = "/Library/admin/book_data/{page}".format(page=book_query.prev_num) if book_query.has_prev else ""
    next_href = "/Library/admin/book_data/{page}".format(page=book_query.next_num) if book_query.has_next else ""
    data = [{
        "name":i.name,
        "classify":i.classify,
        "author":i.author,
        "publisher":i.publisher,
        "publish_time":i.publish_time if i.publish_time else "",
        "desc":i.desc,
        "status":i.status,
        "borrower_name":i.borrower_name if i.borrower_name else "",
        "lender_name":i.lender_name
    }for i in book_query.items]
    return succeed_resp(data=data, pre_href=pre_href, next_href=next_href)

@library_admin_view.route("/Library/admin/history")
@library_admin_view.route("/Library/admin/history/<int:page>")
@session_check("/Library")
@library_admin_decorator
def Library_admin_history(page=1):
    User_table = aliased(Library_User, name='user2')
    query = Borrow_Lend.query.join(Library_User, Borrow_Lend.borrower==Library_User.id).\
                              join(Library_Book, Borrow_Lend.book_id==Library_Book.id).\
                              join(User_table, Borrow_Lend.lender==User_table.id).\
                              with_entities(
                                          Library_Book.name.label("book_name"),
                                          Library_User.name.label("borrower_name"),
                                          Borrow_Lend.create_time.label("create_time"),
                                          Borrow_Lend.borrow_time.label("borrow_time"),
                                          Borrow_Lend.return_time.label("return_time"),
                                          Borrow_Lend.action.label("action"),
                                          User_table.name.label('lender_name'),
                                          ).order_by(Borrow_Lend.id.desc()).paginate(page, per_page=50, error_out=False)
    pre_href = "/Library/admin/history/{page}".format(page=query.prev_num) if query.has_prev else ""
    next_href = "/Library/admin/history/{page}".format(page=query.next_num) if query.has_next else ""

    data = [{
        "book_name":i.book_name,
        "borrower_name":i.borrower_name,
        "create_time":i.create_time.strftime("%Y-%m-%d %H:%M:%S") if i.create_time else "",
        "borrow_time":i.borrow_time.strftime("%Y-%m-%d %H:%M:%S") if i.borrow_time else "",
        "return_time":i.return_time.strftime("%Y-%m-%d %H:%M:%S") if i.return_time else "",
        "action":i.action,
        'lender_name':i.lender_name,
    }for i in query.items]
    return succeed_resp(data=data, pre_href=pre_href, next_href=next_href)
