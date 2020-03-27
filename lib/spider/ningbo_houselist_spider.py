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
import lib.utility.version
import datetime
import urllib3
import os

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
    def collect_ningbo_record_data(self, fmt="csv"):
        csv_file = self.today_path + "/{0}_house_list.csv".format("ningbo")
        open_mode = "w"
        with open(csv_file, open_mode, newline='', encoding='utf-8-sig') as f:
            ningbos = self.get_ningbo_record_info(self.is_all,self.get_date)
            if not os.path.exists(csv_file) or os.path.getsize(csv_file) <= 0:
                ningbos.insert(0,NingboHouse("时间","价格","单价","面积","小区","区域","核验编码","房产公司","住宅","楼层","抵押"))
            if self.mutex.acquire(1):
                self.total_num += len(ningbos)
                self.mutex.release()
            if fmt == "csv":
                for ningbo in ningbos:
                    f.write(ningbo.text() + "\n")
            print("Finish crawl ,save data to : " + csv_file)

    @staticmethod
    def get_ningbo_record_info(is_all = False,get_date = get_year_month_string_bias):
        total_page = 2
        ningbo_list = list()
        #时间/价格/单价/面积/小区/区域/核验编码/房产公司/住宅/楼层/抵押/
        page = 'https://esf.cnnbfdc.com/home/houselist'
        print(page)
        headers = create_headers()
        urllib3.disable_warnings()
        response = requests.get(page, timeout=10000, headers=headers,verify=False)
        html = response.content
        soup = BeautifulSoup(html, "lxml")

        try:
            pagination_last = soup.find('ul', class_="pagination").find('li', class_="PagedList-skipToLast").find('a')
            href = pagination_last.get('href')
            parsed_result = urlparse(href)
            querys = parse_qs(parsed_result.query)
            querys = {k: v[0] for k, v in querys.items()}
            total_page = querys['page']
            print("total = " + total_page)
        except Exception as e:
            total_page = 100
        try:
            for page_num in range(1, int(total_page) + 1):
                page = 'https://esf.cnnbfdc.com/home/houselist?page={0}'.format(page_num)
                print(page)
                headers = create_headers()
                base_spider.BaseSpider.random_delay()
                response = requests.get(page, timeout=10000, headers=headers,verify=False)
                html = response.content
                soup = BeautifulSoup(html, "lxml")
                
                house_elements = soup.find_all("li",class_="listbody__main__row")

                for house_element in house_elements:
                    #date, price, price_per, average, community, district, guid, agency_name, residence_type, floor, mortage_state
                    date = house_element.find("div",class_="group-right").find("span",class_="group-right__date").text
                    price = house_element.find("div",class_="group-right").find("span",class_="group-right__price").find("b").text.strip()
                    averages = house_element.findAll("span",class_="group-right__average__price")
                    price_per = averages[0].find("em").text
                    area = averages[1].find("em").text
                    community = house_element.find("div",class_="project-title").find("a").text
                    district = house_element.find("small",class_="color--grey").text.replace("/","").strip()
                    guid = house_element.find("div",class_="project-details__address").find("a").text
                    agency_name = house_element.find("div",class_="project-details__company").find("a").text.strip()
                    residence_type = house_element.find("span",class_="project-decorations__sign ys").text.strip()
                    floor = house_element.find("span",class_="project-decorations__sign bpf").text.strip()
                    mortage_state = house_element.find("span",class_="mortgage-state project-decorations__sign bpf").text.strip()

                    ningbo_house = NingboHouse(date, price, price_per, area, community, district, guid, agency_name, residence_type, floor, mortage_state)
                    ningbo_list.append(ningbo_house)
        except KeyboardInterrupt:
            return ningbo_list
        return ningbo_list
    def start(self,is_all = False, get_date = get_year_month_string_bias):
        if is_all:
            self.today_path = create_date_city_path("宁波房产交易网", "all", self.date_string)
        else:
            self.today_path = create_date_path("宁波房产交易网", get_date.replace('/','_'))
        self.get_date = get_date
        self.is_all = is_all
        t1 = time.time()
        self.collect_ningbo_record_data()

        # 计时结束，统计结果
        t2 = time.time()
        print("Total cost {0} second to crawl {1} data items.".format(t2 - t1, self.total_num))
