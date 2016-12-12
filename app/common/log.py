# coding=utf-8
import os
import logging
import platform
from app.config import log_file, error_log_file


LOG_FORMATTER = logging.Formatter('%(asctime)s [%(pathname)s:%(lineno)04d %(funcName)s %(thread)d %(levelname)s]:%(message)s')


def wrapstring(string, level=logging.INFO):
    """
    打印到屏幕时上色
    """
    COLOR = {
        logging.INFO: '\033[92m',   # 绿
        logging.ERROR: '\033[91m',  # 红
        logging.WARN: '\033[93m',   # 黄
        logging.DEBUG: '\033[43m',
        "end": "\33[0m"}
    return COLOR[level] + string + COLOR["end"]

def create_file_handler(log_name, level=logging.DEBUG, formatter=LOG_FORMATTER):
    file_handler = logging.FileHandler(log_name)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    return file_handler

def create_stream_handler(level=logging.DEBUG, formatter=LOG_FORMATTER):
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)
    return stream_handler

def create_time_rotate_handler(log_name):
    """
    多进程时进程间相互竞争，会导致log丢失
    """
    from logging.handlers import TimedRotatingFileHandler
    time_rotate_handler = TimedRotatingFileHandler(filename=log_name, when="midnight", backupCount=30)
    time_rotate_handler.setLevel(logging.INFO)
    time_rotate_handler.setFormatter(LOG_FORMATTER)
    return time_rotate_handler


def create_logger_handler(logger_name, is_stream_handler=False, add_error_log=True, log_level=logging.INFO):
    is_windows = "windows" in platform.system().lower()
    path, file_name = os.path.split(log_file)
    handler_lst = []
    if not is_windows:
        if path and not os.path.exists(path):
            os.makedirs(path)
        info_file_handler = create_file_handler(log_file, level=log_level)
        handler_lst.append(info_file_handler)
        if add_error_log:
            error_file_handler = create_file_handler(error_log_file, level=logging.ERROR)
            handler_lst.append(error_file_handler)
    else:
        is_stream_handler = True
    if is_stream_handler:
        stream_handler = create_stream_handler(level=log_level)
        handler_lst.append(stream_handler)
    return handler_lst
