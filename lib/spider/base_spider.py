#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 爬虫基类
# 爬虫名常量，用来设置爬取哪个站点

import threading
from lib.zone.city import lianjia_cities, beike_cities
from lib.utility.date import *
import lib.utility.version
import random
from lxml import etree
import urllib
import urllib3
import random
import requests

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
    
    def get_ip(self,pool_size = 10,num =1):
        proxies = list()
        print('正在获取代理 ip ')
        url = 'http://www.xicidaili.com/nn/' + str(num)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
        }
        res = urllib.request.Request(url,headers=headers)
        response = urllib.request.urlopen(res)
        response = response.read()

        # s = requests.session()
        # s.verify = False
        # urllib3.disable_warnings()
        # response = s.get(url, timeout=10000, verify=False)

        html = etree.HTML(response)  # 转化这个位置 不用解码
        ip_lists = html.xpath('//div//tr')  # 节点
        for tem in ip_lists:
            if len(proxies) == pool_size:
                return proxies
            ip = tem.xpath('./td[2]/text()')
            if not ip:                  # 如果列表是空的跳过本次循环 这个主要是针对最上面的标签问题
                continue
            ip = ip[0]  # xpath 提取数据以后返回的是列表
            host = tem.xpath('./td[3]/text()')[0]
            tcp_type = tem.xpath('./td[6]/text()')[0]  # 获得协议类型

            if tcp_type == 'HTTP':
                # 判断是否是http协议
                ip_host = ip + ':' + host   # 拼接将要使用的地址和端口
                if self.test_http(ip_host):# 测试代理的有效性
                    proxy = {'http':ip_host}
                    proxies.append(proxy)

            elif tcp_type == 'HTTPS':
                ip_host = ip + ':' + host   # 拼接将要使用的地址和端口
                if self.test_https(ip_host):# 测试代理的有效性
                    proxy = {'http':ip_host}
                    proxies.append(proxy)

            else:
                # 可能还会有其他类型的协议
                pass
            print("\r 已获取 {0} 个代理ip ...".format(len(proxies)), end='')
        return proxies

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