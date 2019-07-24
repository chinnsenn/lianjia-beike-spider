#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 爬取二手房数据的爬虫派生类

import re
import threadpool
from bs4 import BeautifulSoup
from lib.item.ershou import *
from lib.zone.decorate import get_decorate_list
from lib.spider import *
from lib.utility.date import *
from lib.utility.path import *
from lib.zone.area import *
from lib.utility.log import *
import lib.utility.version
from urllib.parse import urlparse
from urllib.parse import parse_qs


def not_empty(s):
    return s and s.strip()
def removeTag(s):
    return s.getText()

class ErShouAjkSpider(base_spider.BaseSpider):
    def collect_area_ershou_data(self, fmt="csv"):
        """
        对于每个板块,获得这个板块下所有二手房的信息
        并且将这些信息写入文件保存
        :param city_name: 城市
        :param area_name: 板块
        :param fmt: 保存文件格式
        :return: None
        """
        # district_name = area_dict.get(area_name, "")
        csv_file = self.today_path + "/{0}.csv".format("ajk")
        with open(csv_file, "w", newline='', encoding='utf-8-sig') as f:
            # 开始获得需要的板块数据
            ershous = list()
            try:
                ershous = self.get_area_ershou_info()
            except RuntimeError as e:
                print(e)
            if len(ershous) > 1:
                # 锁定，多线程读写
                if self.mutex.acquire(1):
                    self.total_num += len(ershous)
                    # 释放
                    self.mutex.release()
                if fmt == "csv":
                    for ershou in ershous:
                        # print(date_string + "," + xiaoqu.text())
                        f.write(self.date_string + "," + ershou.text() + "\n")
                print("Finish crawl ,save data to : " + csv_file)

    @staticmethod
    def get_area_ershou_info():
        """
        通过爬取页面获得城市指定版块的二手房信息
        :param city_name: 城市
        :param area_name: 版块
        :return: 二手房数据列表
        """
        total_page = 1
        decorate_list = dict()
        ershou_ajk_list = list()
        ershou_ajk_list.append(ErShou("区","小区","户型","面积","装修","标题","价格","描述","地址"))

        page = 'https://nb.anjuke.com/sale/'
        print(page)  # 打印版块页面地址
        headers = create_headers()
        response = requests.get(page, timeout=10, headers=headers)

        if 'captcha' in response.url:
            raise RuntimeError("无法获取网页内容，网站可能添加验证码验证，请打开网页 https://nb.anjuke.com/sale/  ，手动通过验证后重试")

        html = response.content
        soup = BeautifulSoup(html, "lxml")

#   <li class=''> <a href='https://nb.anjuke.com/sale/d111/?d=' rel='nofollow'>毛坯</a> </li><li class='selected'>
#    <a href='https://nb.anjuke.com/sale/d112_123/?d=' rel='nofollow'>普通装修</a> </li><li class=''>
#     <a href='https://nb.anjuke.com/sale/d114/?d=' rel='nofollow'>豪华装修</a> </li><li class=''>
#     <a href='https://nb.anjuke.com/sale/d113/?d=' rel='nofollow'>精装修</a> </li>

        try:
            search_bottom = soup.find('div', class_='search_bottom clearfix')
            conddecoration_id = search_bottom.find(
                'li', id="conddecoration_id")
            ul_conddecoration = conddecoration_id.find('ul')
            li_conddecorations = ul_conddecoration.findAll('li')
            for j, li in enumerate(li_conddecorations):
                if j == 0:
                    continue
                key = li.find('a').get('href')
                parse_result = urlparse(key)
                key = list(filter(not_empty, parse_result.path.split('/')))[1]
                value = li.getText().strip()
                decorate_list[key] = value
        except Exception as e:
            print(e)

        for decorate_code, decorate_type in decorate_list.items():
            if decorate_code == 'sale':
                continue
            for num in range(1, 1000):
                try:
                    page = 'https://nb.anjuke.com/sale/{0}-p{1}/'.format(
                        decorate_code, num)
                    print(page)  # 打印版块页面地址
                    headers = create_headers()
                    response = requests.get(page, timeout=10, headers=headers)
                    if response.url != page:
                        if 'captcha' in response.url:
                            raise RuntimeError("无法获取网页内容，网站可能添加验证码验证，请打开网页 https://nb.anjuke.com/sale/  ，手动通过验证后重试")
                            return ershou_ajk_list
                        else:
                            break
                    html = response.content
                    soup = BeautifulSoup(html, "lxml")

                    house_elements = soup.find(
                        'ul', class_='houselist-mod').findAll('li', class_='list-item')
                    for house_element in house_elements:
                        # "区","小区","户型","面积","装修","标题","价格","描述","地址"
                        # district, community, house_type, acreage, decorate_type, name, price, desc, url
                        house_details  = house_element.find('div', class_='house-details')
                        address = house_details.find('span',class_='comm-address').get('title').split()
                        #区
                        district = ''
                        if address[1] is not None:
                            districts = address[1].split('-')
                            district = districts[0]
                        #小区
                        community = ''
                        if address[0] is not None:
                            community = address[0]

                        details_items = house_details.findAll('div',class_='details-item')
                        details_item = details_items[0]
                        details_item = details_item.findAll('span')
                        details_item = list(map(removeTag,details_item))

                        #户型
                        house_type = details_item[0].strip()
                        #面积
                        acreage = details_item[1].strip()
                        #总价
                        price = house_element.find('span', class_='price-det')
                        price = price.find('strong').getText().strip()
                        
                        name = house_details.find('a')
                        #地址
                        url = name.get('href')
                        #标题
                        name = name.getText().replace(',',"，").strip()

                        #描述
                        desc = str.join("|",details_item).replace(',',"，")
                        ershou = ErShou(district,community,house_type,acreage,decorate_type,name,price,desc,url)
                        ershou_ajk_list.append(ershou)
                except Exception as e:
                    print(e)
                    return ershou_ajk_list
        return ershou_ajk_list
                    


    def start(self):
        self.today_path = create_date_path(
            "ajk_nb", "ningbo", self.date_string)
        t1 = time.time()  # 开始计时
        self.collect_area_ershou_data()
        t2 = time.time()
        print("Total cost {0} second to crawl {1} data items.".format(
            t2 - t1, self.total_num))


if __name__ == '__main__':
    pass
