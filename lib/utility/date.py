#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 日期和时间的字符串辅助函数

import time
from datetime import datetime, timedelta
import datetime as date_time
def get_time_string():
    """
    获得形如20161010120000这样的年月日时分秒字符串
    :return:
    """
    current = time.localtime()
    return time.strftime("%Y%m%d%H%M%S", current)


def get_date_string():
    """
    获得形如20161010这样的年月日字符串
    :return:
    """
    current = time.localtime()
    return time.strftime("%Y%m%d", current)


def get_year_month_string():
    """
    获得形如201610这样的年月字符串
    :return:
    """
    current = datetime.localtime()
    return datetime.strftime("%Y%m", current)

def get_year_month_string_bias():
    today_o=date_time.date.today()
    oneday=date_time.timedelta(days=1) 
    yesterday=today_o-oneday
    return yesterday.strftime("%Y/%m/%d")

def get_year_month_string_separator():
    today_o=date_time.date.today()
    oneday=date_time.timedelta(days=1) 
    yesterday=today_o-oneday
    return yesterday.strftime("%Y-%m-%d")

def get_date_by_string(stringdate):
    return datetime.strptime(stringdate,"%Y/%m/%d")

def compare_two_day(date_one,date_two):
    dayone = datetime.strptime(date_one,"%Y-%m-%d")
    daytwo = datetime.strptime(date_two,"%Y-%m-%d")
    return dayone - daytwo > timedelta(days=0)

def is_same_day(date_one,date_two):
    dayone = datetime.strptime(date_one,"%Y-%m-%d")
    daytwo = datetime.strptime(date_two,"%Y-%m-%d")
    return dayone - daytwo == timedelta(days=0)

def compare_two_day_slash(date_one,date_two):
    dayone = datetime.strptime(date_one,"%Y/%m/%d")
    daytwo = datetime.strptime(date_two,"%Y/%m/%d")
    return dayone - daytwo > timedelta(days=0)

def is_same_day_slash(date_one,date_two):
    dayone = datetime.strptime(date_one,"%Y/%m/%d")
    daytwo = datetime.strptime(date_two,"%Y/%m/%d")
    return dayone - daytwo == timedelta(days=0)

if __name__ == "__main__":
    print(get_date_string())
