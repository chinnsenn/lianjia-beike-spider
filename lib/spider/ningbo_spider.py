#!/usr/bin/env python
# coding=utf-8

import re
import threadpool
from bs4 import BeautifulSoup
from lib.item.ningbo import *
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


class NingboSpider(base_spider.BaseSpider):
    def collect_ningbo_record_data(self, fmt="csv"):
        csv_file = self.today_path + "/{0}.csv".format("ningbo")
        with open(csv_file, "w", newline='', encoding='utf-8-sig') as f:
            ningbos = self.get_ningbo_record_info()
            if self.mutex.acquire(1):
                self.total_num += len(ningbos)
                self.mutex.release()
            if fmt == "csv":
                for ningbo in ningbos:
                    f.write(self.date_string + "," + ningbo.text() + "\n")
            print("Finish crawl ,save data to : " + csv_file)

    @staticmethod
    def get_ningbo_record_info():
        total_page = 1
        ningbo_list = list()
        ningbo_list.append(Ningbo("合同签订日期","合同编号","所在区","街道（小区）","经纪机构备案名称"))
        page = 'https://esf.cnnbfdc.com/contract'
        print(page)
        headers = create_headers()
        response = requests.get(page, timeout=20, headers=headers)
        html = response.content
        soup = BeautifulSoup(html, "lxml")

        try:
            pagination_last = soup.find('ul', class_="pagination").find(
                'li', class_="PagedList-skipToLast").find('a')
            href = pagination_last.get('href')
            parsed_result = urlparse(href)
            querys = parse_qs(parsed_result.query)
            querys = {k: v[0] for k, v in querys.items()}
            total_page = int(querys['page'])
            print("total = " + querys['page'])
        except Exception as e:
            print(e)

        for page_num in range(1, total_page + 1):
            page = 'https://esf.cnnbfdc.com/contract?page={0}'.format(page_num)
            print(page)
            headers = create_headers()
            base_spider.BaseSpider.random_delay()
            response = requests.get(page, timeout=20, headers=headers)
            html = response.content
            soup = BeautifulSoup(html, "lxml")
            data_table = soup.find('table',class_='layui-table')
            house_elements = data_table.findAll('tr')
            for i , house_element in enumerate(house_elements):
                if i>0:
                    tds = house_element.findAll("td")
                    trs = list()
                    for index, td in enumerate(tds):
                        if index < 4:
                            trs.append(td.getText().replace(' ','').replace("\n", "").replace("\r", "").strip())
                        else:
                            trs.append(td.find('a').getText().replace(' ','').replace("\n", "").replace("\r", "").strip())
                    ningbo = Ningbo(*trs)
                    print(ningbo.text() + '\n')
                    ningbo_list.append(ningbo)
        return ningbo_list
    def start(self):
        self.today_path = create_date_path("ningbo_housing_estates", "ningbo", self.date_string)

        t1 = time.time()
        self.collect_ningbo_record_data()
        # 计时结束，统计结果
        t2 = time.time()
        print("Total cost {0} second to crawl {1} data items.".format(t2 - t1, self.total_num))
