#!/usr/bin/env python
# coding=utf-8
# author: Zeng YueTian
# 此代码仅供学习与交流，请勿用于商业用途。
# 获得指定城市的二手房数据
import sys
from lib.utility.version import PYTHON_3
from lib.spider.ershou_spider import *

if __name__ == "__main__":
    choice = "你想要爬取 1:贝壳网，2:链家 的数据，请输入对应数字:\n"
    if not PYTHON_3:  # 如果小于Python3
        city = raw_input(choice)
    else:
        city = input(choice)
    if len(city) == 1:
        if city == "1":
            print("你选择了贝壳网")
            spider = ErShouSpider(base_spider.BEIKE_SPIDER)
            spider.start()
        elif city == "2":
            print("你选择了链家网")
            spider = ErShouSpider(base_spider.LIANJIA_SPIDER)
            spider.start()
        else:
            print("请输入有效数字")
    else:
            print("请输入有效数字")