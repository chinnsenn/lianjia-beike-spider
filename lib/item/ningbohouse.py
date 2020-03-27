#!/usr/bin/env python
# coding=utf-

# 时间/价格/单价/面积/小区/区域/核验编码/房产公司/住宅/楼层/抵押/


class NingboHouse(object):
    def __init__(self, date, price, price_per, average, community, district, guid, agency_name, residence_type, floor, mortage_state):
        self.date = date
        self.price = price
        self.price_per = price_per
        self.average = average
        self.community = community
        self.district = district
        self.guid = guid
        self.agency_name = agency_name
        self.residence_type = residence_type
        self.floor = floor
        self.mortage_state = mortage_state

    def text(self):
        return self.date + "," + \
            self.price + "," + \
            self.price_per + "," + \
            self.average + "," + \
            self.community + "," + \
            self.district + "," + \
            self.guid + "," + \
            self.agency_name + "," + \
            self.residence_type + "," + \
            self.floor + "," + \
            self.mortage_state
