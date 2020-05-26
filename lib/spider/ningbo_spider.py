#!/usr/bin/env python
# coding=utf-8

import re
import threadpool
from bs4 import BeautifulSoup
from lib.item.ningbo import *
from lib.zone.city import get_city
from lib.zone.decorate import get_decorate_list
from lib.utility.date import *
from lib.utility.path import *
from lib.zone.area import *
from lib.utility.log import *
from urllib.parse import urlparse
from urllib.parse import parse_qs
import lib.utility.version
from datetime import datetime
import urllib3

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
    def collect_ningbo_record_data(self, proxies, fmt="csv"):
        csv_file = self.today_path + "/{0}.csv".format("ningbo")
        open_mode = "w"
        with open(csv_file, open_mode, newline='', encoding='utf-8-sig') as f:
            ningbos = self.get_ningbo_record_info(self.is_all,self.get_date,proxies)
            if self.mutex.acquire(1):
                self.total_num += len(ningbos)
                self.mutex.release()
            if fmt == "csv":
                for ningbo in ningbos:
                    f.write(ningbo.text() + "\n")
            print("Finish crawl ,save data to : " + csv_file)
    @staticmethod
    def get_page_number_by_date(total_page, get_date,proxies = list()):
        first = 1
        last = int(total_page)
        s = requests.session()
        s.verify = False
        urllib3.disable_warnings()
        s.proxies = {'https': "http://127.0.0.1:1080"} 
        while first < last:
            if len(proxies) > 0:
                s.proxies = random.choice(proxies)
            mid = int(first + (last - first) / 2)
            page = 'https://esf.cnnbfdc.com/contract?page={0}'.format(mid)
            print("\r 正在搜索 {0} 出现的第一页，锁定在 {1} ~ {2} 之间 ...".format(
            get_date, first, last), end='')
            base_spider.BaseSpider.random_delay()
            s.headers = create_headers()
            response = s.get(page)
            html = response.content
            soup = BeautifulSoup(html, "lxml")
            data_table = soup.find('table',class_='layui-table')
            house_elements = data_table.findAll('tr')
            #====================第一行=========================
            first_house_element = house_elements[1]
            first_tds = first_house_element.findAll("td")
            #获取第一行数据日期
            first_date_data = first_tds[0].getText()
            
            #====================最后一行=========================
            last_house_element = house_elements[-1]
            last_tds = last_house_element.findAll("td")
            #获取第一行数据日期
            last_date_data = last_tds[0].getText()

            if is_same_day_slash(first_date_data, last_date_data):  # 中间页头尾日期相同
                if is_same_day_slash(first_date_data, get_date):  # 第一行等于要获取的日期
                    last = mid
                elif compare_two_day_slash(first_date_data, get_date):  # 第一大于要获取的日期
                    first = mid + 1
                else:
                    last = mid
            else:  # 第一行大于最后一行
                if is_same_day_slash(last_date_data, get_date):  # 最后一行等于获取日期
                    first = mid  # 返回页数
                    break
                if is_same_day_slash(first_date_data, get_date):  # 最后一行等于获取日期
                    first = mid - 1  # 返回页数
                elif compare_two_day_slash(get_date, last_date_data):  # 最后一行小于获取日期
                    if compare_two_day_slash(first_date_data, get_date):
                        first = 0  # 该日期数据不存在
                        break
                    else:
                        last = mid
                elif compare_two_day_slash(last_date_data, get_date):
                    first = mid + 1
        return first
    
    @staticmethod
    def get_ningbo_record_info(is_all = False,get_date = get_year_month_string_bias(),proxies = list()):
        total_page = 100
        ningbo_list = list()
        ningbo_list.append(Ningbo("合同签订日期","合同编号","所在区","街道（小区）","经纪机构备案名称"))
        page = 'https://esf.cnnbfdc.com/contract?page=1'
        
        s = requests.session()
        s.verify = False
        urllib3.disable_warnings()
        s.proxies = {'https': "http://127.0.0.1:1080"} 

        base_spider.BaseSpider.random_delay()
        s.headers = create_headers()
        response = s.get(page)
        html = response.content
        soup = BeautifulSoup(html, "lxml")
        
        try:
            pagination = soup.find('ul', class_="pagination")
            pagination_last = soup.find('ul', class_="pagination").find('li', class_="PagedList-skipToLast").find('a')
            href = pagination_last.get('href')
            parsed_result = urlparse(href)
            querys = parse_qs(parsed_result.query)
            querys = {k: v[0] for k, v in querys.items()}
            total_page = querys['page']
            print("total = " + total_page)
        except Exception as e:
            print(e)
        if not is_all:
            page_start = NingboSpider.get_page_number_by_date(total_page,get_date,proxies)
            if page_start == 0:
                print("没有该日期数据")
                return list()
            else:
                print("从第{0}页开始爬取".format(page_start))
        else:
            page_start = 1

        try:
            for page_num in range(page_start, int(total_page) + 1):
                page = 'https://esf.cnnbfdc.com/contract?page={0}'.format(page_num)
                print(page)
                base_spider.BaseSpider.random_delay()
                
                if len(proxies) > 0:
                    s.proxies = random.choice(proxies)
                s.headers = create_headers()
                response = s.get(page)
                html = response.content
                soup = BeautifulSoup(html, "lxml")
                data_table = soup.find('table',class_='layui-table')
                house_elements = data_table.findAll('tr')

                #====================第一行=========================
                first_house_element = house_elements[1]
                first_tds = first_house_element.findAll("td")
                #获取第一行数据日期
                first_date_data = first_tds[0].getText()
                
                #====================最后一行=========================
                last_house_element = house_elements[-1]
                last_tds = last_house_element.findAll("td")
                #获取第一行数据日期
                last_date_data = last_tds[0].getText()
                
                #第一行日期不等于获取的日期
                if is_all!=True and first_date_data != get_date:
                    #第一日期小于获取的日期，退出
                    if get_date_by_string(first_date_data) < get_date_by_string(get_date) :   
                        return ningbo_list
                    if first_date_data == last_date_data:
                        continue

                for i , house_element in enumerate(house_elements):
                    if i>0:
                        first_house_element = house_elements[i]
                        first_tds = first_house_element.findAll("td")
                        current_date_data = first_tds[0].getText()
                        #第一行日期不等于获取的日期
                        if is_all!=True and current_date_data != get_date:
                            continue

                        tds = house_element.findAll("td")
                        trs = list()
                        for index, td in enumerate(tds):
                            if index < 4:
                                trs.append(td.getText().replace(' ','').replace("\n", "").replace("\r", "").strip())
                            else:
                                trs.append(td.find('a').getText().replace(' ','').replace("\n", "").replace("\r", "").strip())
                        ningbo = Ningbo(trs[0],trs[1],trs[2],trs[3],trs[4])
                        print(ningbo.text() + '\n')
                        ningbo_list.append(ningbo)
        except KeyboardInterrupt:
            return ningbo_list
        return ningbo_list
    def start(self,is_all = False, get_date = get_year_month_string_bias()):
        proxies = list()
        # proxies = self.get_ip()
        if is_all:
            self.today_path = create_date_city_path("宁波房产交易网_二手房", "all", self.date_string)
        else:
            self.today_path = create_date_path("宁波房产交易网_二手房", get_date.replace('/','_'))
        self.get_date = get_date
        self.is_all = is_all
        t1 = time.time()
        self.collect_ningbo_record_data(proxies)
        # 计时结束，统计结果
        t2 = time.time()
        print("Total cost {0} second to crawl {1} data items.".format(t2 - t1, self.total_num))
