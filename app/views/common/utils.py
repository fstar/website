# -*- coding:utf-8 -*-
import numpy as np
import cv2
import zbar
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

def cal(image):
    '''
        说明: 从照片中获取条形码的位置,返回条形码区域的图片
        1. 首先是获取照片的灰度图像
        2. 对灰度图像进行Sobel运算, 获得x方向和y方向的边缘检测的图像灰度值
        3. x方向的梯度-y方向的梯度
        4. 进行平局模糊化
        5. 过滤,将灰度值小于245的变为0,大于245的变为1
        6. 进行一次腐蚀,把一些小点去掉
        7. 进行一次闭运算, 企图把条形码的区域变成一大块
        8. 进行4次膨胀, 把条形码区域里的空隙填满
        9. 找出图像中最大的区块
        10. 获取该块区域的坐标, 从原灰度图中抠出来, 返回抠出来的图像
    '''

    # image = cv2.imread(image)
    # image = cv2.resize(image, (800,800))
    gray  = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gradX = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    gradY = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)

    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)

    # cv2.imshow("test",gradX)
    # cv2.waitKey(0)

    blurred = cv2.blur(gradient, (3,3))
    # blurred = gradient
    # cv2.imshow("test",blurred)
    # cv2.waitKey(0)
    (_, thresh) = cv2.threshold(blurred, 245, 255, cv2.THRESH_BINARY)
    #
    # cv2.imshow("test",thresh)
    # cv2.waitKey(0)

    thresh = cv2.erode(thresh, None, iterations=1)
    # cv2.imshow("test",thresh)
    # cv2.waitKey(0)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20,7))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)



    closed = cv2.erode(closed, None, iterations=4)
    # cv2.imshow("test",closed)
    # cv2.waitKey(0)


    closed = cv2.dilate(closed, None, iterations=4)
    # cv2.imshow("test",closed)
    # cv2.waitKey(0)

    (_, cnts, hi) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.imshow("test",closed)
    # cv2.waitKey(0)

    c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
    # cv2.imshow("test",c)
    # cv2.waitKey(0)
    rect = cv2.minAreaRect(c)
    box = np.int0(cv2.boxPoints(rect))

    top = min(box[:,1])
    left = min(box[:,0])
    right = max(box[:,0])
    bottom = max(box[:,1])


    cv2.drawContours(image, [box], -1, (0, 255, 0), 3)
    target_img = gray[top:bottom+1,left:right+1]

    # cv2.imshow("test",target_img)
    # cv2.waitKey(0)
    return target_img


def rec_bar(grayImg):
    '''
        利用zbar工具, 把之前抠出来的条形码区域图片放入zbar中进行条形码识别, 并且返回条形码的值
        如果zbar无法识别条形码,则返回为空
    '''

    scanner = zbar.Scanner()
    image = np.array(grayImg)
    results = scanner.scan(image)
    for result in results:
        print(result.type, result.data, result.quality)
        return result.data if result and result.data else ''
