# -*- coding:utf-8 -*-
import json
from macpath import split
str = """上海虹桥国际机场 SHA 上海;上海浦东国际机场 PVG 上海;北京首都国际机场 PEK 北京;南苑机场 AAA 北京
        """
d_airports = {}
l_name = str.split(";")
for name in l_name:
    airports = name.split(" ")
    d_airports[airports[0]] = airports[1]
    
fout = open("/root/AirTicketSpider/common/airport_code.py","w")
fout.write("#coding:utf-8\nairports = ")
json.dump(d_airports, fout,ensure_ascii=False) 
fout.close()