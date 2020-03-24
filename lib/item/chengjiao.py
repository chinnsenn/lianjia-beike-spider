#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 二手房信息的数据结构


class ChengJiao(object):
    # 20200322,区,小区,成交日期、成交周期, 挂牌价格,建筑形态,户型,面积(平米),标题,价格(万),装修,朝向,地址
    
    #ChengJiao(chinese_district, community, dealdate, dealcycle_period, positionInfo,listing, house_type, acreage,  price, name, decorate_type, orientation, url)     
    def __init__(self, district, community, dealdate, dealcycle_period, positionInfo, listing,  house_type, acreage, name, price, decorate_type, orientation, url):
        self.district = district
        self.community = community
        self.dealdate = dealdate
        self.dealcycle_period = dealcycle_period
        self.positionInfo = positionInfo
        self.listing = listing
        self.house_type = house_type
        self.acreage = acreage
        self.name = name
        self.price = price
        self.decorate_type = decorate_type
        self.orientation = orientation
        self.url = url

    def text(self):
        return self.community + "," + \
            self.dealdate + "," +\
            self.dealcycle_period + "," + \
            self.listing + "," + \
            self.price + "," + \
            self.positionInfo + "," + \
            self.house_type + "," + \
            self.acreage + "," + \
            self.name + "," + \
            self.decorate_type + "," + \
            self.district + "," + \
            self.url + "," +\
            self.orientation
