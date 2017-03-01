# -*- coding:utf-8 -*-
from flask import Blueprint, render_template, request, redirect, session, url_for
from app.views.common.view_decorators import *
from app.models import db, Library_User, Library_Book, Borrow_Lend, Library_Classify, Library_message, Group, User_Group
from app.views.common.utils import *
import json
import random
from hashlib import md5
from sqlalchemy import or_
from collections import OrderedDict
import datetime


library_view = Blueprint("library_view", __name__)


def library_decorator(func):
    @wraps(func)
    def _func(*args, **kwargs):
        uid = session["uid"]
        library_user_id = session.get("library_user_id", None)
        if library_user_id != None:
            return func(*args, **kwargs)
        Library_User_query = Library_User.query.filter_by(user_id=uid).first()
        if not Library_User_query:
            return redirect(url_for("library_view.Library_user"))
        else:
            session["library_user_id"] = Library_User_query.id
            return func(*args, **kwargs)
    return _func


@library_view.route("/Library")
@session_check("/Library")
@library_decorator
def Library_index():
    return redirect(url_for("library_view.Library_books"))


@library_view.route("/Library/user", methods=["POST","GET"])
@session_check("/Library")
def Library_user():     # 我的身份页
    if request.method == "GET":
        library_user_id = session.get("library_user_id", None)
        if not library_user_id:
            uid = session["uid"]
            Library_User_query = Library_User.query.filter_by(user_id=uid).first()
            if not Library_User_query:
                return render_template("library/user_form.html", data={})
            else:
                session["library_user_id"] = Library_User_query.id
                return render_template("library/user_form.html", data=Library_User_query)
        else:
            Library_User_query = Library_User.query.filter_by(id=library_user_id).first()
            if not Library_User_query:
                return render_template("404.html"), 403
            return render_template("library/user_form.html", data=Library_User_query)
    else:
        library_user_id = request.form.get("library_user_id", None)
        name            = request.form.get("name", None)
        phone           = request.form.get("phone", None)
        address         = request.form.get("address", None)
        user_id         = session["uid"]
        sex             = request.form.get("sex",3)

        phone           = Caesar_code(phone, 10)
        address         = Caesar_code(address, 10)

        if not library_user_id:
            one = Library_User(user_id, name, phone, address, sex)
            db.session.add(one)
            db.session.commit()
        else:
            query = Library_User.query.filter_by(id=library_user_id).first()
            if not query or query.user_id != session["uid"]:
                return render_template("404.html"), 403
            query.name    = name
            query.phone   = phone
            query.address = address
            query.user_id = session["uid"]
            query.sex     = sex
            db.session.commit()
        return redirect(url_for("library_view.Library_books"))


@library_view.route("/Library/books", methods=["GET"])
@library_view.route("/Library/books/<int:page>", methods=["GET"])
@session_check("/Library")
@library_decorator
def Library_books(page=1):    # 书目页
    book_name = request.args.get("book_name")
    classify  = request.args.get("classify")
    author    = request.args.get("author")
    publisher = request.args.get("publisher")
    desc      = request.args.get("desc")
    lender    = request.args.get("lender")
    status    = request.args.get('status', None)
    keyword   = request.args.get("keyword", None)
    condition = {}

    # 分组过滤: 根据当前user_id, 得到分组编号, 通过分组编号得到同一组的用户user_id
    subqry = User_Group.query.filter_by(status=1, User_id=session["uid"]).with_entities(User_Group.Group_id.label("group_id")).subquery()
    uid_query = User_Group.query.filter(User_Group.Group_id.in_(subqry), User_Group.User_id != session["uid"], User_Group.status==1).group_by(User_Group.User_id).with_entities(User_Group.User_id.label("user_id")).subquery()
    library_user_id = Library_User.query.filter(Library_User.user_id.in_(uid_query)).with_entities(Library_User.id.label("library_user_id")).subquery()
    book_query = Library_Book.query.outerjoin(Library_User, Library_Book.lender==Library_User.id).filter(Library_Book.status!=-1,Library_Book.lender.in_(library_user_id))
    if not keyword: # 精确匹配: 每一个字段都进行匹配, and操作
        if book_name:
            condition["book_name"] = book_name
            book_query = book_query.filter(Library_Book.name.like("%{name}%".format(name=book_name)))
        if classify:
            condition["classify"] = classify
            classify_list = classify.split(",")
            sql_or = or_()
            for i in classify_list:
                sql_or = or_(sql_or, Library_Book.classify.like("%{classify}%".format(classify=i)))
            book_query = book_query.filter(sql_or)
        if author:
            condition["author"] = author
            book_query = book_query.filter(Library_Book.author.like("%{author}%".format(author=author)))
        if publisher:
            condition["publisher"] = publisher
            book_query = book_query.filter(Library_Book.publisher.like("%{publisher}%".format(publisher=publisher)))
        if desc:
            condition["desc"] = desc
            book_query = book_query.filter(Library_Book.desc.like("%{key}%".format(key=desc)))
    else: # 模糊匹配: 每一个字段都进行模糊匹配, or操作
        condition["keyword"] = keyword
        book_query = book_query.filter(or_(Library_Book.name.like("%{keyword}%".format(keyword=keyword)),
                                            Library_Book.classify.like("%{keyword}%".format(keyword=keyword)),
                                            Library_Book.author.like("%{keyword}%".format(keyword=keyword)),
                                            Library_Book.publisher.like("%{keyword}%".format(keyword=keyword)),
                                            Library_Book.desc.like("%{keyword}%".format(keyword=keyword))
                                            ))
    if status: # 书目借阅状态, 精确匹配
        condition["status"] = status
        book_query = book_query.filter(Library_Book.status == status)
    if lender: # 书目出借者id, 精确匹配
        condition["lender"] = lender
        book_query = book_query.filter(Library_Book.lender == lender)

    book_query = book_query.with_entities(Library_Book.id.label("id"),\
                                          Library_Book.name.label('name'),\
                                          Library_Book.classify.label('classify'),
                                          Library_Book.author.label('author'),\
                                          Library_Book.publisher.label('publisher'),\
                                          Library_Book.desc.label('desc'),\
                                          Library_Book.status.label('status'),\
                                          Library_User.name.label('lender_name')).\
                                          order_by(Library_Book.id.desc()).\
                                          paginate(page, per_page=50, error_out=False)
    book_id_list = [i.id for i in book_query.items]
    borrow_query = Borrow_Lend.query.filter_by(borrower=session["library_user_id"]).\
                                     filter(Borrow_Lend.book_id.in_(book_id_list),\
                                            Borrow_Lend.action.in_([3,1])).all()
    borrow_dict = {i.book_id:i.action for i in borrow_query}
    pre_href = "/Library/books/{page}?".format(page=book_query.prev_num)
    next_href = "/Library/books/{page}?".format(page=book_query.next_num)
    for key,value in condition.items():
        pre_href = pre_href + "{key}={value}".format(key=key,value=value)
        next_href = next_href + "{key}={value}".format(key=key,value=value)

    book_id_list = ",".join([str(i) for i in book_id_list])
    keyword_list = []
    for key, value in condition.items():
        if key == "classify":
            keyword_list.extend(condition[key].split(","))
        else:
            keyword_list.append(value)
    return render_template("library/books.html", data=book_query, classify_list=get_book_classify(), \
                            borrow_dict=borrow_dict, pre_href=pre_href, next_href=next_href, book_id_list=book_id_list,\
                            keyword_list = " ".join(keyword_list))

@library_view.route("/Library/reserve_book", methods=["POST"])
@session_check("/Library")
@library_decorator
def reserve_book(): # 预定书目接口
    book_id = request.form.get("book_id",None)
    library_user_id = session["library_user_id"]

    Borrow_Lend_query = Borrow_Lend.query.filter_by(book_id=book_id, borrower=library_user_id).\
                                          filter(Borrow_Lend.action.in_([1,3])).first()
    if Borrow_Lend_query:
        if Borrow_Lend_query.action == 3:
            return succeed_resp(status=0, book_id=book_id, info="你已预定了该书, 不要重复预定!")
        elif Borrow_Lend_query.action == 1:
            return succeed_resp(status=0, book_id=book_id, info="你已经借了该书!")
    else:


        book_query = Library_Book.query.filter_by(id=book_id).first()
        if book_query and book_query.status==0:
            book_query.status = 1
            db.session.commit()
        if book_query and book_query.status==-1:
            return succeed_resp(status=-1, info="书目刚刚被下架了")
        if not book_query:
            return succeed_resp(status=-1,info="书目不存在")

        one = Borrow_Lend(book_id, library_user_id, book_query.lender)
        db.session.add(one)
        db.session.commit()

        return succeed_resp(status=1, book_id=book_id, info="预定成功!")

@library_view.route("/Library/check_book", methods=["POST"])
@session_check("/Library")
@library_decorator
def check_book(): # 轮询检测书目状态接口
    book_id_list = request.form.get("book_id_list","")
    book_id_list = book_id_list.split(',')
    book_query = Library_Book.query.filter(Library_Book.id.in_(book_id_list)).all()
    data = {i.id:{"status":i.status, "action":0, "name":i.name} for i in book_query}   # status字段: -1,下架 0,空闲 1,有人预定 2,出借中
    Borrow_Lend_query = Borrow_Lend.query.filter_by(borrower=session["library_user_id"]).\
                                     filter(Borrow_Lend.book_id.in_(book_id_list)).\
                                     filter(Borrow_Lend.action.in_([1,3])).all()
    for i in Borrow_Lend_query:  # action字段: 1,已借到 3,已预订, 0,其他
        data[i.book_id]["action"] = i.action

    return succeed_resp(data=data)


@library_view.route("/Library/add_edit_book", methods=["GET", "POST"])
@session_check("/Library")
@library_decorator
def Library_add_book():   # 新增和编辑图书页面
    if request.method == "GET":
        book_id = request.args.get("book_id", None)
        if not book_id:
            classify = get_book_classify()
            return render_template("library/add_book.html", data={}, classify=classify)
        else:
            lender_id  = session["library_user_id"]
            book_query = Library_Book.query.filter_by(id=book_id, lender=lender_id).first()
            classify = get_book_classify(set(book_query.classify.split(",")))
            if not book_query:
                return render_template("404.html"), 403
            else:
                return render_template("library/add_book.html", data=book_query, classify=classify)
    else:
        book_id      = request.form.get("book_id", None)
        name         = request.form.get("name", None)
        classify     = request.form.get("classify", None)
        author       = request.form.get("author", None)
        ISBN         = request.form.get("ISBN", None)
        publisher    = request.form.get("publisher",None)
        publish_time = request.form.get("publish_time",None)
        desc         = request.form.get("desc",None)
        lender_id    = session["library_user_id"]
        if not book_id:
            one = Library_Book(name, lender_id, classify, author, desc, publisher, publish_time, ISBN=ISBN)
            db.session.add(one)
            db.session.commit()
            return redirect(url_for("library_view.my_books"))

        else:
            book_query = Library_Book.query.filter_by(id=book_id, lender=lender_id).first()
            if not book_query:
                return render_template("404.html"), 403
            else:
                book_query.name         = name
                book_query.classify     = classify
                book_query.author       = author
                book_query.desc         = desc
                book_query.publisher    = publisher
                book_query.publish_time = publish_time
                book_query.ISBN         = ISBN
                db.session.commit()
                return redirect(url_for("library_view.my_books"))

@library_view.route("/Library/mybooks", methods=["GET"])
@library_view.route("/Library/mybooks/<int:page>", methods=["GET"])
@session_check("/Library")
@library_decorator
def my_books(page=1):
    book_name = request.args.get("book_name")
    classify  = request.args.get("classify")
    author    = request.args.get("author")
    publisher = request.args.get("publisher")
    desc      = request.args.get("desc")
    borrower  = request.args.get("borrower")
    status    = request.args.get('status', None)
    keyword   = request.args.get("keyword", None)
    condition = {}

    book_query = Library_Book.query.outerjoin(Library_User, Library_Book.borrower==Library_User.id).filter(Library_Book.lender==session["library_user_id"])
    if not keyword: # 精确匹配: 每一个字段都进行匹配, and操作
        if book_name:
            condition["book_name"] = book_name
            book_query = book_query.filter(Library_Book.name.like("%{name}%".format(name=book_name)))
        if classify:
            condition["classify"] = classify
            classify_list = classify.split(",")
            sql_or = or_()
            for i in classify_list:
                sql_or = or_(sql_or, Library_Book.classify.like("%{classify}%".format(classify=classify)))
            book_query = book_query.filter(sql_or)
        if author:
            condition["author"] = author
            book_query = book_query.filter(Library_Book.author.like("%{author}%".format(author=author)))
        if publisher:
            condition["publisher"] = publisher
            book_query = book_query.filter(Library_Book.publisher.like("%{publisher}%".format(publisher=publisher)))
        if desc:
            condition["desc"] = desc
            book_query = book_query.filter(Library_Book.desc.like("%{key}%".format(key=desc)))
    else: # 模糊匹配: 每一个字段都进行模糊匹配, or操作
        condition["keyword"] = keyword
        book_query = book_query.filter(or_(Library_Book.name.like("%{keyword}%".format(keyword=keyword)),
                                            Library_Book.classify.like("%{keyword}%".format(keyword=keyword)),
                                            Library_Book.author.like("%{keyword}%".format(keyword=keyword)),
                                            Library_Book.publisher.like("%{keyword}%".format(keyword=keyword)),
                                            Library_Book.desc.like("%{keyword}%".format(keyword=keyword))
                                            ))
    if status: # 书目借阅状态, 精确匹配
        condition["status"] = status
        book_query = book_query.filter(Library_Book.status == status)
    if borrower: # 书目出借者id, 精确匹配
        condition["borrower"] = borrower
        book_query = book_query.filter(Library_Book.borrower == borrower)

    book_query = book_query.with_entities(Library_Book.id.label("id"),\
                                          Library_Book.name.label('name'),\
                                          Library_Book.classify.label('classify'),
                                          Library_Book.author.label('author'),\
                                          Library_Book.publisher.label('publisher'),\
                                          Library_Book.desc.label('desc'),\
                                          Library_Book.status.label('status'),\
                                          Library_User.name.label('borrower_name')).\
                                          paginate(page, per_page=50, error_out=False)

    pre_href = "/Library/books/{page}?".format(page=book_query.prev_num)
    next_href = "/Library/books/{page}?".format(page=book_query.next_num)
    for key,value in condition.items():
        pre_href = pre_href + "{key}={value}".format(key=key,value=value)
        next_href = next_href + "{key}={value}".format(key=key,value=value)

    return render_template("library/mybooks.html", data=book_query, pre_href=pre_href, next_href=next_href)

@library_view.route("/Library/change_book_status", methods=["POST"])
@session_check("/Library")
@library_decorator
def change_book_status():
    book_id = request.form.get("book_id", None)
    book_query = Library_Book.query.filter_by(id=book_id, lender=session["library_user_id"]).first()
    if not book_query:
        return succeed_resp(status=0, info=u'书目不存在!')
    else:
        status = book_query.status
        if status != -1:
            book_query.status = -1
            db.session.commit()
            return succeed_resp(status=1, book_status=-1, info=u'书目下架成功!')
        else:
            book_query.status = 0
            db.session.commit()
            return succeed_resp(status=1, book_status=0, info=u'书目上架成功!')

@library_view.route("/Library/me_to_friend", methods=["GET"])
@library_view.route("/Library/me_to_friend/<int:page>", methods=["GET"])
@session_check("/Library")
@library_decorator
def me_to_friend(page=1):
    keyword = request.args.get("keyword")
    action = request.args.get("action")
    condition = {}
    query = Borrow_Lend.query.join(Library_User, Borrow_Lend.borrower==Library_User.id).\
                              join(Library_Book, Borrow_Lend.book_id==Library_Book.id).\
                              filter(Borrow_Lend.lender==session["library_user_id"])
    if keyword:
        condition["keyword"] = keyword
        query = query.filter(or_(Library_Book.name.like("%{keyword}%".format(keyword=keyword)),
                                 Library_User.name.like("%{keyword}%".format(keyword=keyword))))
    if action:
        condition["action"] = action
        query = query.filter(Borrow_Lend.action==action)

    query = query.with_entities(Borrow_Lend.id.label("id"),
                                Library_Book.name.label("book_name"),
                                Library_User.name.label("borrower_name"),
                                Borrow_Lend.create_time.label("create_time"),
                                Borrow_Lend.borrow_time.label("borrow_time"),
                                Borrow_Lend.return_time.label("return_time"),
                                Borrow_Lend.action.label("action"),
                                Library_User.phone.label("phone"),
                                Library_User.address.label("address")
                                ).order_by(Borrow_Lend.id.desc()).paginate(page, per_page=50, error_out=False)

    pre_href = "/Library/me_to_friend/{page}?".format(page=query.prev_num)
    next_href = "/Library/me_to_friend/{page}?".format(page=query.next_num)
    for key,value in condition.items():
        pre_href = pre_href + "{key}={value}".format(key=key,value=value)
        next_href = next_href + "{key}={value}".format(key=key,value=value)

    return render_template("library/me_to_friend.html",data=query, pre_href=pre_href, \
                            next_href=next_href, keyword=keyword)

@library_view.route("/Library/change_borrow_lend_status", methods=["POST"])
@session_check("/Library")
@library_decorator
def change_borrow_lend_status():
    borrow_lend_id = request.form.get("borrow_lend_id")
    action = int(request.form.get("action"))
    query = Borrow_Lend.query.filter_by(id=borrow_lend_id, lender=session["library_user_id"]).first()
    if not query:
        return succeed_resp(status=0, info=u'条目不存在!')
    else:
        if query.action in (2,4) or \
           (query.action == 1 and action != 2) or \
           (query.action == 3 and action in (2,3)):
            return succeed_resp(status=0, info=u'拒绝此操作')
        query.action = action
        book_id = query.book_id
        borrower_id = query.borrower
        update_time = datetime.datetime.now()
        if action == 1:
            query.borrow_time = update_time
        elif action == 2:
            query.return_time = update_time

        db.session.commit()
        if action == 1:
            Library_Book.query.filter_by(id=book_id).update({"status":2, "borrower":borrower_id})
        elif action == 2:
            count = Borrow_Lend.query.filter_by(lender=session["library_user_id"], action=3).count()
            if count > 0:
                Library_Book.query.filter_by(id=book_id).update({"status":1, "borrower":None})
            else:
                Library_Book.query.filter_by(id=book_id).update({"status":0, "borrower":None})
        db.session.commit()
        return succeed_resp(status=1, info=u'操作成功', action=action, \
                        update_time=update_time.strftime("%Y-%m-%d %H:%M:%S"))

@library_view.route("/Library/friend_to_me", methods=["GET"])
@library_view.route("/Library/friend_to_me/<int:page>", methods=["GET"])
@session_check("/Library")
@library_decorator
def friend_to_me(page=1):
    keyword = request.args.get("keyword")
    action = request.args.get("action")
    condition = {}

    query = Borrow_Lend.query.join(Library_User, Borrow_Lend.lender==Library_User.id).\
                              join(Library_Book, Borrow_Lend.book_id==Library_Book.id).\
                              filter(Borrow_Lend.borrower==session["library_user_id"])
    if keyword:
        condition["keyword"] = keyword
        query = query.filter(or_(Library_Book.name.like("%{keyword}%".format(keyword=keyword)),
                                 Library_User.name.like("%{keyword}%".format(keyword=keyword))))
    if action:
        condition["action"] = action
        query = query.filter(Borrow_Lend.action==action)

    query = query.with_entities(Borrow_Lend.id.label("id"),
                                Library_Book.name.label("book_name"),
                                Library_User.name.label("lender_name"),
                                Borrow_Lend.create_time.label("create_time"),
                                Borrow_Lend.borrow_time.label("borrow_time"),
                                Borrow_Lend.return_time.label("return_time"),
                                Borrow_Lend.action.label("action"),
                                Library_User.phone.label("phone"),
                                Library_User.address.label("address"),
                                ).order_by(Borrow_Lend.id.desc()).paginate(page, per_page=50, error_out=False)

    pre_href = "/Library/friend_to_me/{page}?".format(page=query.prev_num)
    next_href = "/Library/friend_to_me/{page}?".format(page=query.next_num)
    for key,value in condition.items():
        pre_href = pre_href + "{key}={value}".format(key=key,value=value)
        next_href = next_href + "{key}={value}".format(key=key,value=value)

    return render_template("library/friend_to_me.html",data=query, pre_href=pre_href, \
                            next_href=next_href, keyword=keyword)


def get_book_classify(filter_string=()):  # 获取图书分类表
    query = Library_Classify.query.all()
    data = OrderedDict({})
    for i in query:
        first_level  = i.first_level
        second_level = i.second_level
        if second_level in filter_string:
            status = 1
        else:
            status = 0
        if i.first_level in data.keys():
            data[first_level][second_level] = status
        else:
            data[first_level] = {second_level:status}
    return data
