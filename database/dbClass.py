# -*- coding: utf-8 -*-  
'''
Created on 2016年3月15日

@author: dict
'''
import MySQLdb


# import cPickle
# import pickle

class DBUtils:
    def __init__(self, host, user, passwd, dbname):
        self.conn = MySQLdb.connect(host=host,
                                    user=user,
                                    passwd=passwd,
                                    db=dbname,
                                    charset="utf8")
        self.cursor = self.conn.cursor()

    def create_table(self, sql):
        self.cursor.execute(sql)

    def delete_table(self, table_name):
        try:
            self.cursor.execute("DROP TABLE IF EXISTS %s" % table_name)
        except:
            print "table:%s doesn't exists!!!" % table_name

    def insert_data(self, sql):
        '''测试'''
        self.cursor.execute(sql)

    def delete_data(self, sql):
        self.cursor.execute(sql)

    def change_data(self, sql):
        self.cursor.execute(sql)

    def search_data(self, sql):
        return self.cursor.execute(sql)

    def add_column(self, sql):
        self.cursor.execute(sql)

    def reduce_column(self, sql):
        self.cursor.execute(sql)

    def print_all_data(self, table_name):
        num = self.search_data("select * from %s" % table_name)
        infos = self.cursor.fetchmany(num)
        for info in infos:
            print info

    @property
    def close_db(self):
        self.cursor.close()
        self.conn.commit()
        self.conn.close()


if __name__ == "__main__":
    db_flight = DBUtils("localhost", "root", "", "test")
    db_flight.delete_table("flight_details1_info")
    db_flight.close_db

    my_db = DBUtils("localhost", "root", "", "test")
    sql = '''
      CREATE TABLE IF NOT EXISTS flight_details_info (
          flightID varchar(255) NOT NULL,
          airCompanyID int(255) NOT NULL,
          ontime datetime NOT NULL,
          offtime datetime NOT NULL,
          discount float DEFAULT NULL,
          price decimal(10,0) NOT NULL,
          onAddress varchar(255) NOT NULL,
          offAddress varchar(255) NOT NULL,
          ontimeRate decimal(10,0) DEFAULT NULL,
          extraCharge double DEFAULT NULL,
          Meals char(255) DEFAULT NULL
      )
  '''

    my_db.create_table(sql)
    b1 = "KN5986663"
    sql1 = """insert into flight_details_info values(
    '%s','1','2016-04-01 8:50','2016-04-01 11:50',
    '4.5','445','shanghai','beijing','98','50','s') """ % (b1)
    my_db.insert_data(sql1)

    #     print num
    #     my_db.print_data(num)
    my_db.close_db
    print "Over!"

