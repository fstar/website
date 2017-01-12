from flask import Blueprint, request, render_template, session, redirect, url_for
from app.models import db, User, Role
from app.views.common.utils import *
import datetime

login_view = Blueprint("login_view", __name__)

@login_view.route("/", methods=["GET", "POST"])
@login_view.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if session.get("uid",""):
            return redirect(url_for("index_view.index"))
        return render_template("login/login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        user_query = User.query.filter_by(name=username, password=password, status=1).first()
        if not user_query:
            return succeed_resp(result=0)
        else:
            uid                        = user_query.uid
            name                       = user_query.name
            token                      = user_query.token
            user_query.last_login_time = datetime.datetime.now()
            user_query.last_IP         = request.remote_addr
            db.session.commit()

            role_query                 = Role.query.filter_by(id=user_query.role_id, status=1).first()
            session["uid"]             = uid
            return succeed_resp(result = 1)

@login_view.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return render_template("login/login.html")
