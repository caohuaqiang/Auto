# -*- coding: utf-8 -*
import sys, os
sys.path.append(os.path.abspath(__file__))
import pymysql
from pymysql.err import OperationalError
import configparser as cparser
from pprint import pprint

# ==================== 读取db_config.ini文件设置========================
base_dir = str(os.path.dirname(os.path.abspath(__file__)))              # 根目录-Auto
base_dir = base_dir.replace('\\', '/')
filepath = base_dir + '/db_config.ini'

cf = cparser.ConfigParser()
cf.read(filepath)
db_config = eval(cf.get(section='mysqlconf', option='mysql'))


# =====================封装Mysql基本操作================================
class UseDataBase:
    def __init__(self) -> None:
        self.configuration = db_config

    def __enter__(self):
        try:
            self.conn = pymysql.connect(**self.configuration)
            self.cursor = self.conn.cursor()
            return self.cursor

        except OperationalError as err:
            print('Mysql Error %d: %s' % (err.args[0], err.args[1]))

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def clear(self, table_name):
        real_sql = 'DELETE FROM ' + table_name + ';'
        print(real_sql)
        with self.conn.cursor() as cursor:
            cursor.execute('SET FOREIGN_KEY_CHECKS=0;')
            cursor.execute(real_sql)
        self.conn.commit()

    def insert(self, table_name, table_data):
        for key in table_data:
            table_data[key] = "'" + str(table_data[key]) + "'"       # 这个for循环是为了把字典里的value都套上引号，如果没有引号，那么insert的sql语句会报错（insert的values值要引号）
        key = ','.join(table_data.keys())
        value = ','.join(table_data.values())
        sql = 'INSERT INTO ' + table_name + " ("+key+") VALUES ("+value+")"
        print(sql)
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
        self.conn.commit()


if __name__ == '__main__':
    with UseDataBase() as cursor:
        _SQL = "select user_id, user_name, pwd, mobile_phone, channel_type from rd_user where mobile_phone = '15821903152'"
        cursor.execute(_SQL)
        contents = cursor.fetchall()
        for data in contents:
            pprint(data)