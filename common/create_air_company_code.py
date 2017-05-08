# -*- coding:utf-8 -*-
import json
from macpath import split
str = """Z1 北部湾航空股份有限公司 北部湾航空:Z2 扬子江航空股份有限公司 扬子江航空:Z3 九元航空股份有限公司 九元航空:Z4 瑞丽航空股份有限公司 瑞丽航空:Z5 福州航空股份有限公司 福州航空:Z6 东海航空股份有限公司 东海航空:Z7 青岛航空股份有限公司 青岛航空:Z8 重庆航空股份有限公司 重庆航空:Z9 长龙航空股份有限公司 长龙航空:TV 西藏航空股份有限公司 西藏航空:Z0 春秋航空股份有限公司 春秋航空:BK 奥凯航空有限公司 奥凯航空:CA 中国国际航空公司 中国国航:EU 成都航空有限公司 成都航空:FM 上海航空公司 上海航空:HO 上海吉祥航空公司 吉祥航空:HU 海南航空股份有限公司 海南航空:KN 中国联合航空公司 中国联航:KY 昆明航空有限公司 昆明航空:NS 河北航空有限公司 河北航空:PN 西部航空有限责任公司 西部航空:YI 云南英安航空有限公司 云南英航:ZH 深圳航空公司 深圳航空:8L 祥鹏航空公司 祥鹏航空:CN 新华航空控股有限公司 新华航空:CZ 中国南方航空公司 南方航空:G5 华夏航空有限公司 华夏航空:GS 天津航空有限责任公司 天津航空:JD 北京首都航空有限公司 首都航空:JR 幸福航空有限责任公司 幸福航空:MF 厦门航空有限公司 厦门航空:MU 中国东方航空公司 东方航空:SC 山东航空公司 山东航空:VD 河南航空有限公司 河南航空:3U 四川航空公司 四川航空:8C 东星航空公司 东星航空"""
d_companies = {}
l_name = str.split(":")
for name in l_name:
#     print name
#     name = name.strip('\n')
    companies = name.split(" ")
#     print type(companies)
#     for i in companies:
#         print i+"=="
    d_companies[companies[2]] = companies[0]
    
fout = open("../air_company_code.py","w")
fout.write("#coding:utf-8\ncompanies = ")
json.dump(d_companies, fout,ensure_ascii=False) 
fout.close()