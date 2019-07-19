#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 二手房信息的数据结构


class ErShou(object):
    def __init__(self, district,community,house_type,acreage,decorate_type, name, price, desc,url):
        self.district = district
        self.community = community
        self.house_type = house_type
        self.acreage = acreage
        self.decorate_type = decorate_type
        self.price = price
        self.name = name
        self.desc = desc
        self.url = url

    def text(self):
        return self.district + "," + \
                self.community + "," + \
                self.house_type + "," + \
                self.acreage + "," + \
                self.name + "," + \
                self.price + "," + \
                self.decorate_type + "," + \
                self.url + "," +\
                self.desc
