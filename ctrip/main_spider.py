# -*- coding:utf-8 -*-
'''
Created on 2016年3月7日

@author: Administrator
'''
import json
import time

import requests
from database.dbClass import DBUtils

from city_code import city

i_begin_time = time.time()
# start_city = raw_input("请输入出发城市：")
# reach_city = raw_input("请输入到达城市：")
pingtai = "携程"
s_start_city = "上海"
s_reach_city = "西安"
s_start_date = "2017-06-01"
s_root_url = "http://flights.ctrip.com/booking/%s-%s-day-1.html" % (city[s_start_city], city[s_reach_city])
d_headr = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
    'Referer': s_root_url
    }
s_real_url = "http://flights.ctrip.com/domesticsearch/search/SearchFirstRouteFlights?DCity1=%s&ACity1=%s&DDate1=%s" % (
city[s_start_city], city[s_reach_city], s_start_date)
req = requests.get(s_real_url, headers=d_headr)
d_origin_data = json.loads(req.content.decode('gbk').encode('utf-8'))

l_flight_info = d_origin_data['fis']
file_info = open("flight_details_info1.txt", "w")
file_info.write("平台：%s\n出发城市：%s\t到达城市：%s:出发时间：%s\n" % (pingtai, s_start_city, s_reach_city, s_start_date))
# 打开数据库
# db_flight = DBUtils("localhost", "root", "", "test")
# db_flight.delete_table("flight_details1_info")
# db_flight.close_db
# exit(0)
db_flight1 = DBUtils("localhost", "root", "", "test")

for info in l_flight_info:
    # 航站楼
    s_start_code = "%s%d" % (info['dpc'], info['dbid'])
    s_reach_code = "%s%d" % (info['apc'], info['abid'])
    s_start_port = d_origin_data['apb'][s_start_code]
    s_reach_port = d_origin_data['apb'][s_reach_code]
    # 时间
    s_start_time = info['dt']
    s_reach_time = info['at']
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
    s_air_name = d_origin_data['als'][info['alc']]
    for price in info['scs']:
        # 折扣
        s_rate = price['rt']
        # 价格
        i_price = price['salep']
    try:
        sql = """
            insert ignore into flight_details1_info values(
            '%s','%s','%s','%s','%s','%i','%s','%s','%f','%i','%s') 
            """ % (s_flight_code, s_air_name,
                   s_start_time, s_reach_port,
                   s_rate, i_price,
                   s_start_port, s_reach_port,
                   f_punctuality_rate, i_tax + i_oil_fee,
                   s_meal_type
                   )
        db_flight1.insert_data(sql)
    finally:
        file_info.write("航班号：%s\t折扣：%s\t价格：%i\t出发航站楼：%s\t出发时间：%s\t到达航站楼：%s\t到达时间：%s\t准点率：%f\t附加费：%i\t餐食：%s\n"
                        % (s_flight_code + s_air_name, s_rate, i_price,
                           s_start_port, s_start_time, s_reach_port,
                           s_reach_time, f_punctuality_rate,
                           i_tax + i_oil_fee, s_meal_type))
db_flight1.print_all_data("flight_details1_info")
db_flight1.close_db
file_info.close()

i_end_time = time.time()
i_run_time = i_end_time - i_begin_time
print "运行时间:%.2f秒" % i_run_time
