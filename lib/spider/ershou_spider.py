#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 爬取二手房数据的爬虫派生类

from os import pipe
import re
import platform
import time
import os
from time import sleep
import threadpool
from bs4 import BeautifulSoup
from lib.item.ershou import *
from lib.zone.city import get_city
from lib.zone.decorate import get_decorate_list
from lib.spider import *
from lib.utility.date import *
from lib.utility.path import *
from lib.zone.area import *
from lib.utility.log import *
from tool.definetools import *
import platform
import urllib3

class ErShouSpider(base_spider.BaseSpider):

    distric_message_dict = dict()
    is_mac = True

    def printCurrentProcess(self,threadName,message):
        if self.mutex.acquire(1):
            self.distric_message_dict[threadName] = message
            total_message = "============================================================================================================================================\n"
            total_message += "\n".join(str(self.distric_message_dict[key]) for key in self.distric_message_dict)
            total_message += "\n============================================================================================================================================\n"
            if self.is_mac:
                os.system('clear')
            else:
                os.system('cls')
            print('\r'+"{0}".format(total_message), end='', flush=True)
            self.mutex.release()

    def collect_area_ershou_data(self, city_name, district_name, fmt="csv"):
        """
        对于每个板块,获得这个板块下所有二手房的信息
        并且将这些信息写入文件保存
        :param city_name: 城市
        :param area_name: 板块
        :param fmt: 保存文件格式
        :return: None
        """
        # 开始获得需要的板块数据
        self.is_mac = re.search('mac', platform.platform(), re.IGNORECASE) is not None
        ershous = self.get_area_ershou_info(city_name,district_name)
        chinese_district = str(get_chinese_district(district_name)).replace("区","")
        ershou_len = len(ershous)
        if ershou_len > 0:
            csv_file = self.today_path + "/ershou_" + district_name +"_"+ time.strftime("%H_%M_%S", time.localtime()) +".csv"
            if not os.path.exists(csv_file) or os.path.getsize(csv_file) <= 0:
                ershous.insert(0,ErShou("区","小区","户型","面积(平米)","装修","标题","价格(万)","单价(万/平)","描述","链接"))
            with open(csv_file, "a",newline='',encoding='utf-8-sig') as f:
                    # 锁定，多线程读写
                    if self.mutex.acquire(1):
                        self.total_num += ershou_len
                        # 释放
                        self.mutex.release()
                    if fmt == "csv":
                        for ershou in ershous:
                            f.write(self.date_string + "," + ershou.text() + "\n")
            
            self.printCurrentProcess(district_name,"{0}共获取{1}条数据，已存储在{2}:".format(chinese_district,ershou_len, csv_file))
        else: 
            self.printCurrentProcess(district_name,"{0}没有二手房数据".format(chinese_district))
    def get_area_ershou_info(self, city_name, district_name):
        """
        通过爬取页面获得城市指定版块的二手房信息
        :param city_name: 城市
        :param area_name: 版块
        :return: 二手房数据列表
        """
        total_page = 1
        # district_name = area_dict.get(area_name, "")
        # 中文区县
        chinese_district = str(get_chinese_district(district_name)).replace("区","")
        decorate_list = get_decorate_list()
        # 中文版块
        # chinese_area = chinese_area_dict.get(district_name, "")

        ershou_list = list()
        # ershou_list.append(ErShou("区","小区","户型","面积(平米)","装修","标题","价格(万)","描述","地址"))

        headers = create_headers()
        for decorate_code,decorate_type in decorate_list.items():
            page = 'http://{0}.{1}.com/ershoufang/{2}/pg1{3}'.format(city_name, base_spider.SPIDER_NAME, district_name,decorate_code)
            mock_headers = create_headers()
            urllib3.disable_warnings()
            response = requests.get(page, timeout=10000, headers=mock_headers)
            html = response.content
            soup = BeautifulSoup(html, "lxml")

            # 获得总的页数，通过查找总页码的元素信息
            try:
                page_box = soup.find_all('div', class_='page-box')[0]
                matches = re.search('.*"totalPage":(\d+),.*', str(page_box))
                total_page = int(matches.group(1))
            except Exception as e:
                pass
            #第一页开始,一直遍历到最后一页
            for num in range(1, total_page + 1):
                page = 'http://{0}.{1}.com/ershoufang/{2}/pg{3}{4}sf1sf6'.format(city_name, base_spider.SPIDER_NAME, district_name, num,decorate_code)
                try_time = 3
                while(try_time > 0):
                    try:
                        currentMessage = "正在获取{0}区第{1}页，总共{2}页, 当前链接为: {3}".format(chinese_district, num, total_page, page)
                        self.printCurrentProcess(district_name,currentMessage)
                        ershou_sub_list = self.get_data_from_page(page, chinese_district, decorate_type)
                        ershou_list.extend(ershou_sub_list)
                        break
                    except Exception as e:
                        try_time = try_time - 1
                        for i in range(20):
                            currentMessage = "{0}区第{1}页获取失败，{2}秒后重试, 当前链接为: {3}".format(chinese_district,num,i,page)
                            self.printCurrentProcess(district_name,currentMessage)
                            sleep(1)
        return ershou_list

    def get_data_from_page(self, page, chinese_district, decorate_type):
        # print(page)  # 打印每一页的地址
        mock_headers = create_headers()
        base_spider.BaseSpider.random_delay()
        response = requests.get(page, timeout=10000, headers=mock_headers)
        html = response.content
        soup = BeautifulSoup(html, "lxml")

        ershou_sub_list = list()
        # 获得有小区信息的panelhz
        house_elements = soup.find_all('li', class_="clear")
        for house_elem in house_elements:
            price = house_elem.find('div', class_="totalPrice")
            unit_price = house_elem.find('div', class_="unitPrice")
            name = house_elem.find('div', class_='title')
            desc = house_elem.find('div', class_="houseInfo")
            position = house_elem.find('div',class_="positionInfo")
            #链家与贝壳跳转链接获取不一样
            if(base_spider.SPIDER_NAME == base_spider.BEIKE_SPIDER):
                url = house_elem.find('a', class_="img VIEWDATA CLICKDATA maidian-detail")
            else:
                url = house_elem.find('div', class_="title").find('a')
            # 继续清理数据
            price = "".join(filter(saveNum,price.text))
            unit_price = unit_price['data-price']
            name = name.text.replace("\n", "").replace(",", "，")
            desc = desc.text.replace("\n", "").replace(' ', '').strip()
            #判断分割符
            if(desc.find("|")):
                descs = desc.split("|")
            else:
                descs = desc.split("/")
            url = url.get('href').strip()
            position = position.text.replace("\n", "").replace(",", "，")
            community = '' 
            if position is not None and '层' not in position:
                community = position
            else:
                community = descs[0]
            for x in descs:
                if "室" in x:
                    house_type = x
                if "米" in x:
                    acreage = "".join(filter(saveNum,x))
            # print(pic)
            # 作为对象保存
            ershou = ErShou(chinese_district,community,house_type,acreage,decorate_type, name, price,unit_price, desc, url)
            ershou_sub_list.append(ershou)
        return ershou_sub_list

    def start(self):
        city = get_city()
        self.today_path = create_date_city_path("{0}/ershou".format(base_spider.SPIDER_NAME), city, self.date_string)

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
        pool_size = base_spider.thread_pool_size
        pool = threadpool.ThreadPool(pool_size)
        my_requests = threadpool.makeRequests(self.collect_area_ershou_data, args)
        [pool.putRequest(req) for req in my_requests]
        pool.wait()
        pool.dismissWorkers(pool_size, do_join=True)  # 完成后退出

        # 计时结束，统计结果
        t2 = time.time()
        print("总共获取 {0} 个区.".format(len(districts)))
        print("总耗时 {0} 秒获取 {1} 条数据.".format(t2 - t1, self.total_num))
    
if __name__ == '__main__':
    pass
