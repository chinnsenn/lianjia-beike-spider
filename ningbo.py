#!/usr/bin/env python
# coding=utf-8
# author: Zeng YueTian
# 此代码仅供学习与交流，请勿用于商业用途。
# 获得指定城市的所有新房楼盘数据

import sys
from lib.utility.version import PYTHON_3
from lib.spider.ningbo_spider import *

if __name__ == "__main__":
    page_start = "请输入起始页码,直接回车从第一页开始爬取\n(注:如果从第一页开始爬取会覆盖同一天目录下同名文件的数据，注意备份):\n"
    if not PYTHON_3:  # 如果小于Python3
        page = raw_input(page_start)
    else:
        page = input(page_start)
    if page is None or len(page) == 0:
        print("从第1页开始爬去数据")
        spider = NingboSpider(base_spider.NINGBO_SPIDER)
        spider.start()
    elif int(page) < 1:
        print("请输入有效数字")
    else:
        print("从第" + page + "页开始爬取数据")
        spider = NingboSpider(base_spider.NINGBO_SPIDER)
        spider.start(page)