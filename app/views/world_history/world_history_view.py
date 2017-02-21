from flask import Blueprint, render_template
from flask import request, redirect, session, url_for
from app.views.common.view_decorators import *
from app.models import db, User, History_action, Action_relationship
from app.views.common.utils import *
import json

world_history_view = Blueprint("world_history_view", __name__)

@world_history_view.route("/History")
@session_check("/History")
def history_index():  # 历史首页
    return render_template("history/index.html")

@world_history_view.route("/History/insert_data", methods=['POST'])
@session_check("/History")
def history_insert_data(): # 插入或者修改一条历史数据
    id      = request.form.get('id', None)
    year    = request.form.get('year', None)
    area    = request.form.get('area', None)
    country = request.form.get('country', None)
    county  = request.form.get('county', None)
    action  = request.form.get('action', None)
    person  = request.form.get('person', None)
    user_id = session['user_id']
    if not year or not area or not action:
        return failed_resp(message='数据不完整')
    if id:
        one         = History_action.query.filter_by(id=id).first()
        one.year    = year
        one.area    = area
        one.country = country
        one.county  = county
        one.action  = action
        one.person  = person
        db.session.commit()
    else:
        one = History_action(year, area, country, county, action, person, user_id)
        db.session.add(one)
        db.session.commit()
    return succeed_resp(status=1)

@world_history_view.route("/History/get_data")
@session_check("/History")
def history_get_data():
    History_action_query = History_action.query.join(User, History_action.user_id==User.uid).\
                            order_by(History_action.year_num).all()

    title = []
    data = [{
        "id":i.id,
        "year":i.year,
        "area":i.area,
        "country":i.country,
        "county":i.county,
        "action":i.action,
        "person":i.person,
        "year_num":i.year_num,
        "create_user":i.name

    } for i in History_action_query]
    return succeed_resp(data=data)
