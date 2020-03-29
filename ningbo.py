#!/usr/bin/env python
# coding=utf-8
# author: Zeng YueTian
# 此代码仅供学习与交流，请勿用于商业用途。
# 获得指定城市的所有新房楼盘数据

import sys
from lib.utility.version import PYTHON_3
from lib.spider.ningbo_spider import *
from lib.spider.ningbo_houselist_spider import *

if __name__ == "__main__":
    prompt_start = "请输入对应数字:\n1.爬取宁波房产网信息公示\n2.爬取宁波房产网二手房源\n"
    num = input(prompt_start)

    if num == "1":
        ningbo = "请输入对应数字:\n1.爬取某日信息\n2.爬取全部信息\n(默认 1):\n"
        page = input(ningbo)
        if page is None or len(page) == 0 or int(page) == 1:
            prompt_date = "请输入日期，如 2019/10/8:\n"
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
    elif num == "2":
        crawl_all = "请输入对应数字:\n1.爬取某日信息\n2.爬取全部信息\n(默认 1):\n"
        num = input(crawl_all)
        if num is None or len(num) == 0 or int(num) == 1:
            prompt_date = "请输入日期，如 2019-10-08:\n"
            date_str = input(prompt_date)
            date = None
            if date_str is None:
                print("请输入有效日期")
            else:
                spider = NingboHouseListSpider(base_spider.NINGBO_SPIDER)
                if date_str is None:
                    spider.start(None,is_all=False)
                else:
                    spider.start(date_str,is_all=False)
        else:
            spider = NingboHouseListSpider(base_spider.NINGBO_SPIDER)
            spider.start(True)
    else:
        print("请输入有效数字")