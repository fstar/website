from flask import Blueprint, request, render_template, session, redirect, url_for
from app.models import db, User, Role
from app.views.common.utils import *

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
        query = User.query.join(Role).\
                filter(User.name==username, User.password==password, User.status==1, Role.status==1).\
                with_entities(User.uid.label("uid"),User.name.label("name"),\
                              User.role_id.label("role_id"),User.token.label("token"),\
                              Role.name.label("role")).first()
        if not query:
            return succeed_resp(result=0)
        else:
            session["uid"] = query.uid
            session["name"] = query.name
            session["role_id"] = query.role_id
            session["role"] = query.role
            session["token"] = query.token
            return succeed_resp(result=1)

@login_view.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return render_template("login/login.html")
