# -*- coding:utf-8 -*-
'''
Created on 2016年3月7日

@author: Administrator
'''

# sys.path.append("/root/AirTicketSpider/database/")
# sys.path.append("/root/AirTicketSpider/common/")

import json
import re
import threading
import time
import requests

from common.air_company_code import companies
from common.city_code import hot_city
from database.dbClass import DBUtils

# start_city = raw_input("请输入出发城市：")
# reach_city = raw_input("请输入到达城市：")
NUM_THREAD = 2
DB_NAME = "test"
TABLE_NAME = "flight_details_info_test"
USER = "root"
PASSWD = ""
HOST = "localhost"


def get_root_url(start_city, reach_city):
    return "http://flights.ctrip.com/booking/%s-%s-day-1.html" % (start_city, reach_city)


def get_real_url(s_start_city, s_reach_city, s_start_date):
    return "http://flights.ctrip.com/domesticsearch/search/SearchFirstRouteFlights?DCity1=%s&ACity1=%s&DDate1=%s" % (
        s_start_city, s_reach_city, s_start_date)


def get_header(s_root_url):
    d_headr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36',
        'Referer': s_root_url,
        'Host': 'flights.ctrip.com'
    }
    return d_headr


def get_title_info(s_pingtai, s_start_city, s_reach_city, s_start_date):
    return "平台：%s\n出发城市：%s\t到达城市：%s:出发时间：%s\n" % (s_pingtai, s_start_city, s_reach_city, s_start_date)


def get_create_table_sql():
    return """
        CREATE TABLE %s (
        platform varchar(5) NOT NULL,
        departcity varchar(255) NOT NULL,
        arrivecity varchar(255) NOT NULL,
        departdate varchar(255) NOT NULL,
        flightID varchar(255) NOT NULL,
        airCompanyID varchar(255) NOT NULL,
        departtime varchar(255) NOT NULL,
        arrivetime varchar(255) NOT NULL,
        seatlevel varchar(2555),
        discount char(20) DEFAULT NULL,
        price int NOT NULL,
        departport varchar(255) NOT NULL,
        departT varchar(255),
        arriveport varchar(255) NOT NULL,
        arriveT varchar(255),
        ontimeRate float DEFAULT NULL,
        tax int DEFAULT NULL,
        oilfee int DEFAULT NULL,
        Meals varchar(255) DEFAULT NULL)
         """ % (TABLE_NAME)


def get_flight_info(thread_no, l_part_city, s_start_date):
    for city1 in l_part_city:
        s_start_city = city1
        for city2 in l_city_name:
            s_reach_city = city2
            if s_start_city == s_reach_city:
                continue
            else:
                print "thread-%d:%s----------------->%s" % (thread_no, s_start_city, s_reach_city)
                s_root_url = get_root_url(hot_city[s_start_city], hot_city[s_reach_city])
                s_real_url = get_real_url(hot_city[s_start_city], hot_city[s_reach_city], s_start_date)
                #                 print "thread-%d:test0<---%s" % (thread_no,time.time())
                req = requests.get(s_real_url, headers=get_header(s_root_url))
                #                 print "thread-%d:test1<---%s" % (thread_no,time.time())
                if req.status_code != 200:
                    print "页面丢失！"
                    continue
                d_origin_data = json.loads(req.content.decode('gbk').encode('utf-8'))
                #                 print s_real_url
                l_flight_info = d_origin_data['fis']
                #                 print l_flight_info
                if len(l_flight_info) == 0:
                    print "Thread-%d:%s--->%s没有直飞！！！" % (thread_no, s_start_city, s_reach_city)
                    continue
                for info in l_flight_info:
                    # 航站楼
                    s_start_airport = ""
                    s_reach_airport = ""
                    s_start_port = ""
                    s_reach_port = ""

                    s_start_code = "%s%d" % (info['dpc'], info['dbid'])
                    s_reach_code = "%s%d" % (info['apc'], info['abid'])
                    s_start_name = d_origin_data['apb'][s_start_code]
                    s_reach_name = d_origin_data['apb'][s_reach_code]
                    tmp1 = re.search("T[\d]", s_start_name)
                    tmp2 = re.search("T[\d]", s_reach_name)

                    if (tmp1):
                        s_start_airport = s_start_name[:-2]
                        s_start_port = s_start_name[-2:]
                    else:
                        s_start_airport = s_start_name

                    if (tmp2):
                        s_reach_airport = s_reach_name[:-2]
                        s_reach_port = s_reach_name[-2:]
                    else:
                        s_reach_airport = s_reach_name
                    # 时间
                    s_start_time = info['dt'][11:-3]
                    s_reach_time = info['at'][11:-3]
                    # 历史准点率
                    f_punctuality_rate = info['pr']
                    # 附加费
                    i_tax = info['tax']
                    i_oil_fee = info['of']
                    # 餐食类型
                    s_meal_type = ''
                    s_meal_type = info['mt']
                    # 航班号
                    s_flight_code = info['fn']
                    # 航空公司名称
                    tmp = d_origin_data['als'][info['alc']].encode("utf8")
                    try:
                        s_air_name = companies[tmp]
                    except:
                        print tmp + " 未找到简码"
                    for price in info['scs'][:min(1, len(info['scs']))]:
                        # 折扣
                        s_rate = price['rate'] * 10
                        # 价格
                        i_price = price['salep']
                        # 舱位
                        s_seat_level = price['c']
                        #                         print "thread-%d:price,%s" % (thread_no,i_price)
                        try:
                            sql = """
                                insert into %s values('%s','%s','%s','%s','%s','%s','%s',
                                '%s','%s','%s','%i','%s','%s','%s','%s','%.2f','%i','%i','%s')
                                """ % (TABLE_NAME, s_platform, hot_city[s_start_city],
                                       hot_city[s_reach_city], s_start_date,
                                       s_flight_code, s_air_name,
                                       s_start_time, s_reach_time,
                                       s_seat_level, s_rate, i_price,
                                       s_start_airport, s_start_port,
                                       s_reach_airport, s_reach_port,
                                       f_punctuality_rate, i_tax, i_oil_fee,
                                       s_meal_type
                                       )
                            db_flight1.insert_data(sql)
                        # print time.time() - tmpt
                        except Exception, e:
                            print e


def create_thread(func, args):
    return threading.Thread(target=func, args=args)


if __name__ == "__main__":
    i_begin_time = time.time()
    s_platform = "X"
    s_start_city = "上海"
    s_reach_city = "北京"
    s_start_date = "2017-06-02"
    # 删除旧表
    db_flight = DBUtils(HOST, USER, PASSWD, DB_NAME)
    db_flight.delete_table(TABLE_NAME)
    db_flight.close_db
    # 创建新表
    db_flight1 = DBUtils(HOST, USER, PASSWD, DB_NAME)
    db_flight1.create_table(get_create_table_sql())
    l_city_name = hot_city.keys()

    threads = []
    num_per_thread = len(l_city_name) / NUM_THREAD
    start = 0
    for i in range(NUM_THREAD):
        thread_no = i + 1
        stop = start + num_per_thread
        thread = create_thread(get_flight_info, (thread_no, l_city_name[start:stop], s_start_date))
        threads.append(thread)
        start = stop

    for t in threads:
        t.setDaemon(True)
        t.start()

    for t in threads:
        t.join()

    db_flight1.close_db

    i_end_time = time.time()
    i_run_time = i_end_time - i_begin_time
    print "运行时间:%.2f秒" % i_run_time
