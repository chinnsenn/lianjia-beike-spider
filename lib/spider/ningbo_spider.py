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
import datetime

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

class NingboSpider(base_spider.BaseSpider):
    def collect_ningbo_record_data(self, fmt="csv"):
        csv_file = self.today_path + "/{0}.csv".format("ningbo")
        open_mode = "w"
        with open(csv_file, open_mode, newline='', encoding='utf-8-sig') as f:
            ningbos = self.get_ningbo_record_info(self.is_all,self.get_date)
            if self.mutex.acquire(1):
                self.total_num += len(ningbos)
                self.mutex.release()
            if fmt == "csv":
                for ningbo in ningbos:
                    f.write(ningbo.text() + "\n")
            print("Finish crawl ,save data to : " + csv_file)

    @staticmethod
    def get_ningbo_record_info(is_all = False,get_date = get_year_month_string_bias):
        total_page = 1
        ningbo_list = list()
        ningbo_list.append(Ningbo("合同签订日期","合同编号","所在区","街道（小区）","经纪机构备案名称"))
        page = 'https://esf.cnnbfdc.com/contract'
        print(page)
        headers = create_headers()
        response = requests.get(page, timeout=10000, headers=headers)
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
            print(e)
        is_break = False
        for page_num in range(1, int(total_page) + 1):
            if is_break:
                return ningbo_list
            page = 'https://esf.cnnbfdc.com/contract?page={0}'.format(page_num)
            print(page)
            headers = create_headers()
            base_spider.BaseSpider.random_delay()
            response = requests.get(page, timeout=10000, headers=headers)
            html = response.content
            soup = BeautifulSoup(html, "lxml")
            data_table = soup.find('table',class_='layui-table')
            house_elements = data_table.findAll('tr')
            for i , house_element in enumerate(house_elements):
                if i>0:
                    tds = house_element.findAll("td")
                    trs = list()
                    date_data = tds[0].getText()
                    if len(date_data) == 9:
                        date_data = date_data[0:5] + '0' + date_data[5:9]
                    elif len(date_data) == 8:
                        date_data = date_data[0:5] + '0' + date_data[5:7] + '0' + date_data[7:9]
                    if is_all!=True and date_data != get_date:
                        if date_data < get_date:
                            is_break = True
                            break
                        else:
                            continue
                    for index, td in enumerate(tds):
                        if index < 4:
                            trs.append(td.getText().replace(' ','').replace("\n", "").replace("\r", "").strip())
                        else:
                            trs.append(td.find('a').getText().replace(' ','').replace("\n", "").replace("\r", "").strip())
                    ningbo = Ningbo(*trs)
                    print(ningbo.text() + '\n')
                    ningbo_list.append(ningbo)
        return ningbo_list
    def start(self,is_all = False, get_date = get_year_month_string_bias):
        if is_all:
            self.today_path = create_date_city_path("宁波房产交易网", "all", self.date_string)
        else:
            self.today_path = create_date_path("宁波房产交易网", get_date.replace('/',''))
        self.get_date = get_date
        self.is_all = is_all
        t1 = time.time()
        self.collect_ningbo_record_data()
        # 计时结束，统计结果
        t2 = time.time()
        print("Total cost {0} second to crawl {1} data items.".format(t2 - t1, self.total_num))
