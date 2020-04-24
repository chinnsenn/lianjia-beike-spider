#!/usr/bin/env python
# coding=utf-

# 时间/价格/单价/面积/小区/区域/核验编码/房产公司/住宅/楼层/抵押/


class NingboHouse(object):
    def __init__(self, date, price, price_per, average, community, district, guid, agency_name, residence_type, floor, mortage_state,exclusive_or_not,agent):
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
        self.exclusive_or_not = exclusive_or_not
        self.agent = agent

    def text(self):
        return self.date + "\t" + \
            self.price + "\t" + \
            self.price_per + "\t" + \
            self.average + "\t" + \
            self.community + "\t" + \
            self.district + "\t" + \
            self.guid + "\t" + \
            self.agency_name + "\t" + \
            self.residence_type + "\t" + \
            self.floor + "\t" + \
            self.mortage_state + "\t" + \
            self.exclusive_or_not+ "\t" + \
            self.agent 
