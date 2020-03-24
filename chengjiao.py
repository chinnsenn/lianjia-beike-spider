#!/usr/bin/env python
# coding=utf-8
# author: Zeng YueTian
# 此代码仅供学习与交流，请勿用于商业用途。
# 获得指定城市的二手房数据
import sys
from lib.utility.version import PYTHON_3
from lib.spider.chengjiao_spider import *
from lib.spider.chengjiao_lastday_spider import *


if __name__ == "__main__":
    choice = "你想要爬取\n1:贝壳网\n2:链家\n3:贝壳最新一天数据\n4:链家最新一天数据\n请输入对应数字:"
    if not PYTHON_3:  # 如果小于Python3
        city = raw_input(choice)
    else:
        city = input(choice)
    if len(city) == 1:
        if city == "1":
            print("你选择了贝壳网")
            spider = ChengjiaoSpider(base_spider.BEIKE_SPIDER)
            spider.start()
        elif city == "2":
            print("你选择了链家网")
            spider = ChengjiaoSpider(base_spider.LIANJIA_SPIDER)
            spider.start()
        elif city == "3":
            print("你选择了贝壳最新一天数据")
            spider = ChengjiaoLastDaySpider(base_spider.BEIKE_SPIDER)
            spider.start()
        elif city == "4":
            print("你选择了链家最新一天数据")
            spider = ChengjiaoLastDaySpider(base_spider.LIANJIA_SPIDER)
            spider.start()
        else:
            print("请输入有效数字")
    else:
            print("请输入有效数字")