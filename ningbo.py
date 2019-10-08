#!/usr/bin/env python
# coding=utf-8
# author: Zeng YueTian
# 此代码仅供学习与交流，请勿用于商业用途。
# 获得指定城市的所有新房楼盘数据

import sys
from lib.utility.version import PYTHON_3
from lib.spider.ningbo_spider import *

if __name__ == "__main__":
    prompt_start = "请输入对应数字:\n 1. 爬取某日信息\n2.爬取全部信息\n(默认 1):\n"
    if not PYTHON_3:  # 如果小于Python3
        page = raw_input(prompt_start)
    else:
        page = input(prompt_start)
    if page is None or len(page) == 0 or int(page) == 1:
        prompt_date = "请输入日期，如 2019/10/8:\n"
        if not PYTHON_3:  # 如果小于Python3
            date_str = raw_input(prompt_date)
        else:
            date_str = input(prompt_date)
        date = None
        if date_str is None:
            print("请输入有效日期")
        else:
            spider = NingboSpider(base_spider.NINGBO_SPIDER)
            if date_str is None:
                spider.start(False)
            else:
                spider.start(False,date_str)
    else:
        spider = NingboSpider(base_spider.NINGBO_SPIDER)
        spider.start(True)