#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 页面元素的XPATH

from lib.spider import base_spider

if base_spider.SPIDER_NAME == base_spider.LIANJIA_SPIDER:
    ERSHOUFANG_QU_XPATH = '//*[@id="filter-options"]/dl[1]/dd/div/a'
    ERSHOUFANG_BANKUAI_XPATH = '//*[@id="filter-options"]/dl[1]/dd/div[2]/a'
    XIAOQU_QU_XPATH = '//*[@id="filter-options"]/dl[1]/dd/div/a'
    XIAOQU_BANKUAI_XPATH = '//*[@id="filter-options"]/dl[1]/dd/div[2]/a'
    DISTRICT_AREA_XPATH = '//div[3]/div[1]/dl[2]/dd/div/div[2]/a'
    CITY_DISTRICT_XPATH = '///div[3]/div[1]/dl[2]/dd/div/div/a'
elif base_spider.SPIDER_NAME == base_spider.BEIKE_SPIDER:
    ERSHOUFANG_QU_XPATH = '//*[@id="filter-options"]/dl[1]/dd/div/a'
    ERSHOUFANG_BANKUAI_XPATH = '//*[@id="filter-options"]/dl[1]/dd/div[2]/a'
    XIAOQU_QU_XPATH = '//*[@id="filter-options"]/dl[1]/dd/div/a'
    XIAOQU_BANKUAI_XPATH = '//*[@id="filter-options"]/dl[1]/dd/div[2]/a'
    DISTRICT_AREA_XPATH = '//div[3]/div[1]/dl[2]/dd/div/div[2]/a'
    CITY_DISTRICT_XPATH = '///div[3]/div[1]/dl[2]/dd/div/div/a'
