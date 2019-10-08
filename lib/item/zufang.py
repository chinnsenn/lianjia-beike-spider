#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 二手房信息的数据结构


class ZuFang(object):
    def __init__(self, district, xiaoqu, layout, size, price,url):
        self.district = district
        self.xiaoqu = xiaoqu
        self.layout = layout
        self.size = size
        self.price = price
        self.url = url

    def text(self):
        return self.district + "," + \
                self.xiaoqu + "," + \
                self.layout + "," + \
                self.size + "," + \
                self.price + "," + \
                self.url
