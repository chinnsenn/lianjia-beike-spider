#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 爬取二手房数据的爬虫派生类

import re
import os
import threadpool
from bs4 import BeautifulSoup
from lib.item.chengjiao import *
from lib.zone.city import get_city
from lib.zone.decorate import get_decorate_list
from lib.spider import *
from lib.utility.date import *
from lib.utility.path import *
from lib.zone.area import *
from lib.utility.log import *
import lib.utility.version
from tool.definetools import *
import urllib3


class ChengjiaoLastDaySpider(base_spider.BaseSpider):
    def collect_area_chengjiao_data(self, city_name, district_name, fmt="csv"):
        """
        对于每个板块,获得这个板块下所有二手房的信息
        并且将这些信息写入文件保存
        :param city_name: 城市
        :param area_name: 板块
        :param fmt: 保存文件格式
        :return: None
        """                                                              
        # district_name = area_dict.get(area_name, "")

        lastDayDate = self.get_last_day_date(city_name, district_name)

        # 开始获得需要的板块数据
        chengjiaos = self.get_area_chengjiao_info(city_name, district_name,lastDayDate)
        if len(chengjiaos) > 1:
            csv_file = self.today_path + "/chengjiao_lastday.csv"
            if not os.path.exists(csv_file) or os.path.getsize(csv_file) <= 0:
                chengjiaos.insert(0,ChengJiao("区", "小区", "成交日期", "成交周期（天）", "挂牌价格(万)","楼层板楼", "户型", "面积(平米)", "标题", "价格(万)", "装修", "朝向", "地址"))
            with open(csv_file, "a", newline='', encoding='utf-8-sig') as f:
                # 锁定，多线程读写
                if self.mutex.acquire(1):
                    self.total_num += len(chengjiaos)
                    # 释放
                    self.mutex.release()
                if fmt == "csv":
                    for chengjiao in chengjiaos:
                        f.write(chengjiao.text() + "\n")
                print("Finish crawl ,save data to : " + csv_file)
                
    def get_last_day_date(self,city_name, district_name):
        page = 'http://{0}.{1}.com/chengjiao/pg1'.format(city_name, base_spider.SPIDER_NAME)
        headers = create_headers()
        urllib3.disable_warnings()
        response = requests.get(page, timeout=10000, headers=headers)
        html = response.content
        soup = BeautifulSoup(html, "lxml")

        # 获得总的页数，通过查找总页码的元素信息
        try:
            # 获得有小区信息的panelhz
            left_content = soup.find('div', class_="leftContent").find(
                'ul', class_="listContent")
            house_elements = left_content.findAll('div', class_="info")
            dealdate = house_elements[0].find('div', class_="dealDate")
            dealdate = dealdate.text.replace(
                    "\n", "").replace(",", "，").strip()
        except Exception as e:
            print("\tWarning: 只有一页".format(district_name))
            print(e)
        return dealdate

    @staticmethod
    def get_area_chengjiao_info(city_name, district_name,lastDayDate):
        """
        通过爬取页面获得城市指定版块的二手房信息
        :param city_name: 城市
        :param area_name: 版块
        :return: 二手房数据列表
        """
        total_page = 1
        # district_name = area_dict.get(area_name, "")
        # 中文区县
        chinese_district = get_chinese_district(district_name)
        decorate_list = get_decorate_list()
        # 中文版块
        # chinese_area = chinese_area_dict.get(district_name, "")

        chengjiao_list = list()
        # chengjiao_list.append(ChengJiao("区", "小区", "成交日期", "成交周期（天）", "挂牌价格(万)",
        #                                 "楼层板楼", "户型", "面积(平米)", "标题", "价格(万)", "装修", "朝向", "地址"))

        page = 'http://{0}.{1}.com/chengjiao/{2}/pg1'.format(city_name, base_spider.SPIDER_NAME, district_name)
        headers = create_headers()
        urllib3.disable_warnings()
        response = requests.get(page, timeout=10000, headers=headers)
        html = response.content
        soup = BeautifulSoup(html, "lxml")

        # 获得总的页数，通过查找总页码的元素信息
        try:
            page_box = soup.find_all('div', class_='page-box')[0]
            matches = re.search('.*"totalPage":(\d+),.*', str(page_box))
            total_page = int(matches.group(1))
        except Exception as e:
            print("\tWarning: 只有一页".format(district_name))
            print(e)

            # 第一页开始,一直遍历到最后一页
        for num in range(1, total_page + 1):
            page = 'http://{0}.{1}.com/chengjiao/{2}/pg{3}'.format(
                city_name, base_spider.SPIDER_NAME, district_name, num)
            print(page)  # 打印每一页的地址
            base_spider.BaseSpider.random_delay()
            response = requests.get(page, timeout=10000, headers=headers)
            html = response.content
            soup = BeautifulSoup(html, "lxml")

            # 获得有小区信息的panelhz
            left_content = soup.find('div', class_="leftContent").find(
                'ul', class_="listContent")
            house_elements = left_content.findAll('div', class_="info")
            for house_elem in house_elements:
                dealdate = house_elem.find('div', class_="dealDate")
                dealdate = dealdate.text.replace("\n", "").replace(",", "，").strip()
                if(dealdate != lastDayDate):
                    return chengjiao_list
                price = house_elem.find('div', class_="totalPrice")
                name = house_elem.find('div', class_='title')
                desc = house_elem.find('div', class_="houseInfo")
                positionInfo = house_elem.find('div', class_="positionInfo")
                dealCycleTxt = house_elem.find('span', class_="dealCycleTxt")

                # 链家与贝壳跳转链接获取不一样
                if(base_spider.SPIDER_NAME == base_spider.BEIKE_SPIDER):
                    url = house_elem.find(
                        'a', class_="CLICKDATA maidian-detail")
                else:
                    url = house_elem.find('div', class_="title").find('a')
                # 继续清理数据
                price = "".join(filter(saveNum, price.text))
                name = name.text.replace("\n", "").replace(",", "，")
                desc = desc.text.replace("\n", "").replace(' ', '').strip()
                positionInfo = positionInfo.text.replace(
                    "\n", "").replace(' ', '').strip()

                # 朝向，装修
                decorate_type = ''
                orientation = ''
                if(desc.find("|")):
                    descs = desc.split("|")
                    decorate_type = descs[1]
                    orientation = descs[0]

                url = url.get('href').strip()
                community = ''

                dealInfo = dealCycleTxt.findAll('span')
                listing = "".join(filter(saveNum, dealInfo[0].text.replace(
                    "\n", "").replace(' ', '').strip()))
                dealcycle_period = "".join(
                    filter(saveNum, dealInfo[1].text.replace("\n", "").replace(' ', '').strip()))

                # 面积，户型
                houseinfo = name.split(" ")
                community = houseinfo[0]
                for x in houseinfo:
                    if "室" in x:
                        house_type = x
                    if "米" in x:
                        acreage = "".join(filter(saveNum, x))
                # print(pic)
                # 作为对象保存
                #ChengJiao("区","小区","成交日期","成交周期", "挂牌价格","楼层板楼","户型","面积(平米)","标题","价格(万)","装修","地址","朝向")
                chengjiao = ChengJiao(chinese_district, community, dealdate, dealcycle_period,
                                      listing, positionInfo, house_type, acreage,name,  price, decorate_type, orientation, url)
                chengjiao_list.append(chengjiao)
        return chengjiao_list

    def start(self):
        city = get_city()
        self.today_path = create_date_city_path(
            "{0}/chengjiao".format(base_spider.SPIDER_NAME), city, self.date_string)

        t1 = time.time()  # 开始计时

        # 获得城市有多少区列表, district: 区县
        districts = get_districts(city)
        print('City: {0}'.format(city))
        print('Districts: {0}'.format(districts))

        # 获得每个区的板块, area: 板块
        # areas = list()
        # for district in districts:
        #     areas_of_district = get_areas(city, district)
        #     print('{0}: Area list:  {1}'.format(district, areas_of_district))
        #     # 用list的extend方法,L1.extend(L2)，该方法将参数L2的全部元素添加到L1的尾部
        #     areas.extend(areas_of_district)
        #     # 使用一个字典来存储区县和板块的对应关系, 例如{'beicai': 'pudongxinqu', }
        #     for area in areas_of_district:
        #         area_dict[area] = district
        # print("Area:", areas)
        # print("District and areas:", area_dict)

        # 准备线程池用到的参数
        nones = [None for i in range(len(districts))]
        city_list = [city for i in range(len(districts))]
        args = zip(zip(city_list, districts), nones)
        # areas = areas[0: 1]   # For debugging

        # 针对每个板块写一个文件,启动一个线程来操作
        pool_size = 1
        pool = threadpool.ThreadPool(pool_size)
        my_requests = threadpool.makeRequests(
            self.collect_area_chengjiao_data, args)
        [pool.putRequest(req) for req in my_requests]
        pool.wait()
        pool.dismissWorkers(pool_size, do_join=True)  # 完成后退出

        # 计时结束，统计结果
        t2 = time.time()
        print("Total crawl {0} districts.".format(len(districts)))
        print("Total cost {0} second to crawl {1} data items.".format(
            t2 - t1, self.total_num))


if __name__ == '__main__':
    pass
