#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 用于获取代理

import random
from lib.spider import base_spider

http_proxy = [
'http://167.71.27.73:8080',
'http://191.234.166.244:80',
'http://216.21.18.193:80',
'http://51.91.157.66:80',
'http://60.216.20.210:8001'
]

https_proxy = [
'http://178.63.17.151:3128',
'http://195.154.67.61:3128',
'http://103.110.184.109:8181',
'http://114.121.248.251:8080',
'http://202.150.144.210:8080',
'http://173.166.149.188:8080',
'http://78.108.108.9:8080',
'http://118.163.13.200:8080',
'http://149.34.1.95:8080'
]

def get_random_proxy_ip():
    return {"http":random.choice(http_proxy), "https":random.choice(https_proxy)}

if __name__ == '__main__':
    pass
