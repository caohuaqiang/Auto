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
user_login = eval(config.get(section='user', option='chq'))             # 登录账号
user_register = eval(config.get(section='user', option='register'))     # 注册账号


class Center_Product(unittest.TestCase):
    """center_product服务接口（小刚）"""
    def setUp(self):
        self.session = requests.session()
        self.ip = 'http://139.196.107.14:9000'
        self.ym = 'https://www-t.jfcaifu.com'
        self.signature = app_miyao()

    # @unittest.skip('跳过')
    def test_app_homepage(self):
        """APP首页标列表"""
        data_after_login = app_login(phone=user_login['username'], pwd=user_login['password'])         # 登录后的字典
        # print(data_after_login)

        url = self.ip + '/product/indexBorrowList'
        data_homepage = {'userId': 0, }
        res_homepage = self.session.request(method='post', url=url, params=data_homepage)
        print()
        # pprint(res_homepage.json())
        borr_type = res_homepage.json()['data']
        for borr in borr_type['new']:
            print(borr['name'])

    @unittest.skip('跳过')
    def test_app_investplaza(self):
        """APP理财广场列表"""
        data_after_login = app_login(phone=user_login['username'], pwd=user_login['password'])  # 登录后的字典
        url = self.ip + '/product/productList'
        data_investplaza = {'userId': 0, 'orderBy': 'apr', 'timeLimit': 30}
        res_investplaza = self.session.request(method='post', url=url, params=data_investplaza)
        # pprint(res_investplaza.json())
        borrs = res_investplaza.json()['data']
        print()
        for borr in borrs:
            # pprint(borr)
            print(borr['name'])


if __name__ == '__main__':
    unittest.main()


