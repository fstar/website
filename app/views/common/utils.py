# -*- coding:utf-8 -*-
from flask import jsonify, make_response

from app.models import db

def succeed_resp(status_code=200, **kwargs):
    return make_response(jsonify(response_code=1, message="success", **kwargs), status_code)

def failed_resp(message, status_code):
    return make_response(jsonify(message=message, response_code=0), status_code)

def get_or_insert(table, **filter_clause):
    row = table.query.filter_by(**filter_clause).first()
    if row:
        return row
    new_row = table(**filter_clause)
    db.session.add(new_row)
    db.session.commit()
    return new_row

def Caesar_code(s, t=10):
    l = ""
    for i in s:
        tmp = ord(i) + t
        l = l + chr(ord(i) + t)
    return l

def Caesar_decode(s, t=10):
    l = ""
    for i in s:
        tmp = ord(i) - t
        l = l + chr(ord(i) - t)
    return l
