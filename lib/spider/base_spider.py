#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 爬虫基类
# 爬虫名常量，用来设置爬取哪个站点

import threading
from lib.zone.city import lianjia_cities, beike_cities
from lib.utility.date import *
import random
from lxml import etree
import urllib
import urllib3
import requests
from lib.request.proxy import *
import os

thread_pool_size = 10

# 防止爬虫被禁，随机延迟设定
# 如果不想delay，就设定False，
# 具体时间可以修改random_delay()，由于多线程，建议数值大于10
RANDOM_DELAY =True
LIANJIA_SPIDER = "lianjia"
BEIKE_SPIDER = "ke"
NINGBO_SPIDER = "esf.cnnbfdc"
ANJUKE_SPIDER = "nb.anjuke"
SPIDER_NAME = BEIKE_SPIDER

class BaseSpider(object):

    distric_message_dict = dict()
    is_mac = True

    TRY_TIMES = 10
    TRY_DELAY = 30

    def printParallelProcess(self,threadName,message):
        if self.mutex.acquire(1):
            self.distric_message_dict[threadName] = message
            total_message = "============================================================================================================================================\n"
            total_message += "\n\n".join(str(self.distric_message_dict[key]) for key in self.distric_message_dict)
            total_message += "\n============================================================================================================================================\n"
            if self.is_mac:
                os.system('clear')
            else:
                os.system('cls')
            print('\r'+"{0}".format(total_message), end='', flush=True)
            self.mutex.release()

    @staticmethod
    def random_delay():
        if RANDOM_DELAY:
            time.sleep(random.randint(0, 16))
    def __init__(self, name):
        global SPIDER_NAME
        SPIDER_NAME = name
        self.name = name
        if self.name == LIANJIA_SPIDER:
            self.cities = lianjia_cities
        elif self.name == BEIKE_SPIDER:
            self.cities = beike_cities
        else:
            self.cities = None
        # 准备日期信息，爬到的数据存放到日期相关文件夹下
        self.date_string = get_date_string()
        print('Today date is: %s' % self.date_string)

        self.total_num = 0  # 总的小区个数，用于统计
        print("Target site is {0}.com".format(name))
        self.mutex = threading.Lock()  # 创建锁

    def create_prompt_text(self):
        """
        根据已有城市中英文对照表拼接选择提示信息
        :return: 拼接好的字串
        """
        city_info = list()
        count = 0
        for en_name, ch_name in self.cities.items():
            count += 1
            city_info.append(en_name)
            city_info.append(": ")
            city_info.append(ch_name)
            if count % 4 == 0:
                city_info.append("\n")
            else:
                city_info.append(", ")
        return 'Which city do you want to crawl?\n' + ''.join(city_info)

    def get_chinese_city(self, en):
        """
        拼音拼音名转中文城市名
        :param en: 拼音
        :return: 中文
        """
        return self.cities.get(en, None)
    
    def get_random_proxy_ip(self):
        return get_random_proxy_ip()

    def test_http(self,ip_host):
        # 测试http代理是否有效
    # 调用ProxyHandler  代理IP的形式是字典
    # px = urllib.request.ProxyHandler({'http':ip_host})
    # 用build_opener()来构建一个opener对象
    # opener = urllib.request.build_opener(px)
    # 然后调用构建好的opener对象里面的open方法来发生请求。
    # 实际上urlopen也是类似这样使用内部定义好的opener.open()，这里就相当于我们自己重写。

        s = requests.session()
        s.verify = False
        s.proxies = {'http':ip_host}
        urllib3.disable_warnings()

        try:
            page = 'https://www.baidu.com'
            response = s.get(page, timeout=10000, verify=False)

            if response:
                return True
        except:
                return False

    def test_https(self,ip_host):
        s = requests.session()
        s.verify = False
        s.proxies = {'https':ip_host}
        urllib3.disable_warnings()

        try:
            page = 'https://www.baidu.com'
            response = s.get(page, timeout=10000, verify=False)

            if response:
                return True
        except:
                return False