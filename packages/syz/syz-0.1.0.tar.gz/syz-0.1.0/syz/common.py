#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import sys
import os
import psutil
import logging
import datetime


# 设置 log 的格式
logging.basicConfig(format='[%(levelname)s] - [%(asctime)s.%(msecs)03d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)


def current_python_file_path(double_underscore_file=sys.argv[0]):
    """
    获取脚本的路径
    :param double_underscore_file: __file__
    """
    return os.path.abspath(os.path.dirname(double_underscore_file))


def date_to_str(input_datetime: datetime.datetime = datetime.datetime.now()):
    """获取日期字符串 yyyy-MM-dd"""
    return input_datetime.strftime('%Y-%m-%d')


def date_to_short_str(input_datetime: datetime.datetime = datetime.datetime.now()):
    """获取当前的日期字符串 yyyyMMdd"""
    return input_datetime.strftime('%Y%m%d')


def datetime_to_str(input_datetime: datetime.datetime = datetime.datetime.now()):
    """获取当前的日期时间字符串"""
    return input_datetime.strftime('%Y-%m-%d %H:%M:%S')


def file_extension(file_name):
    """获取文件的【小写后缀名】 如：a.JPG 结果是 jpg"""
    return os.path.splitext(file_name)[1].replace('.', '').lower()


def file_prefix(file_name):
    """获取文件的名字 不包含后缀名 如：a.JPG 结果是 a"""
    return os.path.splitext(file_name_without_path(file_name))[0]


def file_name_without_path(file_name):
    """获取文件名 去除路径信息"""
    return os.path.split(file_name)[1]


def physical_cpu_count():
    """获取物理CPU的个数"""
    return psutil.cpu_count(logical=False)
