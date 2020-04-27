#!/usr/bin/env python
# coding=utf-

# 时间/价格/单价/面积/小区/区域/核验编码/房产公司/住宅/楼层/抵押/


class NingboHouse(object):
    def __init__(self, date, price, price_per, average, community, district, guid, agency_name, residence_type, floor, mortage_state,exclusive_or_not,agent):
        self.date = date.replace(',','/')
        self.price = price.replace(',','/')
        self.price_per = price_per.replace(',','/')
        self.average = average.replace(',','/')
        self.community = community.replace(',','/')
        self.district = district.replace(',','/')
        self.guid = guid.replace(',','/')
        self.agency_name = agency_name.replace(',','/')
        self.residence_type = residence_type.replace(',','/')
        self.floor = floor.replace(',','/')
        self.mortage_state = mortage_state.replace(',','/')
        self.exclusive_or_not = exclusive_or_not.replace(',','/')
        self.agent = agent.replace(',','/')

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
            self.mortage_state + "," + \
            self.exclusive_or_not+ "," + \
            self.agent 
