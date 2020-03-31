#!/usr/bin/env python
# coding=utf-8

import re
import threadpool
from bs4 import BeautifulSoup
from lib.item.ningbohouse import *
from lib.zone.city import get_city
from lib.zone.decorate import get_decorate_list
from lib.spider import *
from lib.utility.date import *
from lib.utility.path import *
from lib.zone.area import *
from lib.utility.log import *
from urllib.parse import urlparse
from urllib.parse import parse_qs
from tool.definetools import *
import lib.utility.version
import datetime
import urllib3
import os
import requests
import logging

# w：以写方式打开， 
# a：以追加模式打开 (从 EOF 开始, 必要时创建新文件) 
# r+：以读写模式打开 
# w+：以读写模式打开 (参见 w ) 
# a+：以读写模式打开 (参见 a ) 
# rb：以二进制读模式打开 
# wb：以二进制写模式打开 (参见 w ) 
# ab：以二进制追加模式打开 (参见 a ) 
# rb+：以二进制读写模式打开 (参见 r+ ) 
# wb+：以二进制读写模式打开 (参见 w+ ) 
# ab+：以二进制读写模式打开 (参见 a+ )


class NingboHouseListSpider(base_spider.BaseSpider):
    def collect_ningbo_record_data(self, total_page, threadNo=-1, fmt="csv"):
        csv_file = self.today_path + "/{0}_house_list.csv".format("ningbo")
        open_mode = "a"
        with open(csv_file, open_mode, newline='', encoding='utf-8-sig') as f:
            ningbos = self.get_ningbo_record_info(self.get_date,self.is_all,self.pool_size,total_page, threadNo)
            if not os.path.exists(csv_file) or os.path.getsize(csv_file) <= 0:
                ningbos.insert(0, NingboHouse(
                    "时间", "价格", "单价", "面积", "小区", "区域", "核验编码", "房产公司", "住宅", "楼层", "抵押","独家与否","经纪人"))
            if self.mutex.acquire(1):
                self.total_num += len(ningbos)
                self.mutex.release()
            if fmt == "csv":
                for ningbo in ningbos:
                    f.write(ningbo.text() + "\n")
            if self.is_all:
                print("\n线程 {0} 已完成爬取,写入文件:".format(threadNo) + csv_file)
            else:
                print("已完成爬取,写入文件: " + csv_file)

    def getPageSize(self):
        page = 'https://esf.cnnbfdc.com/home/houselist'
        headers = create_headers()
        urllib3.disable_warnings()
        response = requests.get(page, timeout=10000,
                                headers=headers, verify=False)
        html = response.content
        soup = BeautifulSoup(html, "lxml")

        try:
            pagination_last = soup.find('ul', class_="pagination").find(
                'li', class_="PagedList-skipToLast").find('a')
            href = pagination_last.get('href')
            parsed_result = urlparse(href)
            querys = parse_qs(parsed_result.query)
            querys = {k: v[0] for k, v in querys.items()}
            total_page = querys['page']
            print("total = " + total_page)
        except Exception as e:
            return 100
        return total_page

    @staticmethod
    def get_ningbo_record_info(get_date=get_year_month_string_separator(), is_all=False, pool_size = 1, total_page=100, threadNo=-1):
        if is_all: #爬取全部数据
            if(threadNo < pool_size - 1):
                page_size_tread = int(int(total_page) / int(pool_size))
                page_start = int(threadNo) * page_size_tread + 1
                page_end = page_start + page_size_tread
            else:
                page_start = int(int(total_page) / int(pool_size)) * threadNo + 1
                page_end = int(total_page) + 1
        else:#爬取某日数据
            page_start = 1
            page_end = int(total_page) + 1
        ningbo_list = list()

        s = requests.session()
        s.verify = False
        urllib3.disable_warnings()

        try:
            for page_num in range(page_start, page_end):
                page = 'https://esf.cnnbfdc.com/home/houselist?page={0}'.format(
                    page_num)

                if(is_all):
                    print("\r 线程:{0} 进度:{1}/{2}".format(threadNo,page_num - page_start + 1,page_end - page_start),end='')
                else:
                    print(page)
                base_spider.BaseSpider.random_delay()
                s.headers = create_headers()
                urllib3.disable_warnings()
                response = s.get(page)
                html = response.content
                soup = BeautifulSoup(html, "lxml")

                house_elements = soup.find_all(
                    "li", class_="listbody__main__row")
                #====================第一行=========================
                first_house_element = house_elements[0]
                #获取第一行数据日期
                first_date_data = first_house_element.find("div",class_="group-right").find("span",class_="group-right__date").get_text()
                #====================最后一行=========================
                last_house_element = house_elements[-1] 
                #获取第一行数据日期
                last_date_data = last_house_element.find("div",class_="group-right").find("span",class_="group-right__date").get_text()
                
                #第一行日期不等于获取的日期
                if not is_all and first_date_data != get_date:
                    #第一日期小于获取的日期，退出
                    if first_date_data < get_date:   
                        return ningbo_list
                    if first_date_data == last_date_data:
                        continue
                
                for house_element in house_elements:
                    try:
                        #date, price, price_per, average, community, district, guid, agency_name, residence_type, floor, mortage_state
                        date = house_element.find("div",class_="group-right").find("span",class_="group-right__date").get_text()
                        #第一行日期不等于获取的日期
                        if not is_all  and date != get_date:
                            continue
                        price = house_element.find("div",class_="group-right").find("span",class_="group-right__price").find("b").get_text().strip()
                        averages = house_element.findAll("span",class_="group-right__average__price")
                        if averages is not None:
                            price_per = averages[0].find("em").get_text()
                            area = averages[1].find("em").get_text()
                        else:
                            price_per = "无"
                            area = "无"
                        community = house_element.find("div",class_="project-title").find("a")
                        if community is not None:
                            community = community.get_text()
                        else:
                            community = "无"
                        district = house_element.find("small",class_="color--grey")
                        if district is not None:
                            district = district.get_text().replace("/","无").strip()
                        else:
                            district ="无"
                        guid = house_element.find("div",class_="project-details__address")
                        if guid is not None:
                            guid = "".join(filter(saveNum,guid.find("a").get_text()))
                        else:
                            guid = "无"
                        agency_name = house_element.find("div",class_="project-details__company").find("a")
                        if agency_name is not None:
                            agency_name = agency_name.get_text().strip()
                        else:
                            agency_name = "无"
                        residence_type = house_element.find("span",class_="project-decorations__sign ys")
                        if residence_type is not None:
                            residence_type = residence_type.get_text().strip()
                        else:
                            residence_type = "无"
                        floor = house_element.find("span",class_="project-decorations__sign bpf")
                        if floor is not None:
                            floor = floor.get_text().strip()
                        else:
                            floor ="无"
                        mortage_state = house_element.find("span",class_="mortgage-state project-decorations__sign bpf")
                        if mortage_state is not None:
                            mortage_state = mortage_state.get_text().strip()
                        else:
                            mortage_state = "无"
                        exclusive_or_not = house_element.find("span",class_="project-details__company__du")
                        if exclusive_or_not is not None:
                            exclusive_or_not = exclusive_or_not.get_text().strip()
                        else:
                            exclusive_or_not = "无"
                        agent = house_element.find("span",class_="project-details__company__right")
                        if agent is not None:
                            agent = agent.get_text().strip()
                        else:
                            agent = "无"

                        ningbo_house = NingboHouse(date, price, price_per, area, community, district, guid, agency_name, residence_type, floor, mortage_state,exclusive_or_not,agent)
                        ningbo_list.append(ningbo_house)
                    except BaseException as e:
                        print(e)
                        continue
        except BaseException as e:
            print(e)
            return ningbo_list
        return ningbo_list

    def start(self,get_date = "",is_all=False):
        if is_all:
            self.today_path = create_date_city_path(
                "宁波房产交易网_房源", "all", self.date_string)
            self.get_date = get_date
            self.is_all = is_all
            self.pool_size = 10
            total_page = self.getPageSize()
            # total_page = 100

            nones = [None for i in range(self.pool_size)]
            total_page_list = [total_page for i in range(self.pool_size)]
            args = zip(
                zip(total_page_list, [i for i in range(self.pool_size)]), nones)

            pool = threadpool.ThreadPool(self.pool_size)
            my_requests = threadpool.makeRequests(
                self.collect_ningbo_record_data, args)
            [pool.putRequest(req) for req in my_requests]
            pool.wait()
            pool.dismissWorkers(self.pool_size, do_join=True)  # 完成后退出
            print("crawl %d data" %(self.total_num) )
        else:
            if get_date is None or len(get_date) < 8:
                get_date = get_year_month_string_separator()
            self.today_path = create_date_path(
                "宁波房产交易网_房源", get_date.replace('-', '_'))
            self.get_date = get_date
            self.is_all = is_all
            self.pool_size = 1
            t1 = time.time()
            total_page = self.getPageSize()
            self.collect_ningbo_record_data(total_page)

            # 计时结束，统计结果
            t2 = time.time()
            print("Total cost {0} second to crawl {1} data items.".format(
                t2 - t1, self.total_num))
