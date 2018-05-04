# -*- coding: utf-8 -*
import requests
import unittest
import os, sys
sys.path.append(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 父路径-Auto
sys.path.insert(0, parent_dir)
from pprint import pprint
from DB import UseDataBase
import time
from ForUse import read_ini, app_miyao, app_login


ini_path = parent_dir + '/user.ini'
config = read_ini(ini_path)
config.read(ini_path, encoding='utf-8')
user_login = eval(config.get(section='user', option='chq'))
user_register = eval(config.get(section='user', option='register'))


class Center_Product(unittest.TestCase):
    """center_product服务接口（小刚）"""
    def setUp(self):
        self.session = requests.session()
        self.ym = 'http://139.196.107.14:9000'
        self.signature = app_miyao()

    def test_app_homepage(self):
        """APP首页"""
        data_after_login = app_login(phone=user_login['username'], pwd=user_login['password'])         # 登录后的字典
        print(data_after_login)

        url = self.ym + '/product/indexBorrowList'
        data_homepage = {'userId': 0, }
        res_homepage = self.session.request(method='post', url=url, params=data_homepage)
        pprint(res_homepage.json())


if __name__ == '__main__':
    unittest.main()


