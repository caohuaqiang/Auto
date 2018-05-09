# -*- coding: utf-8 -*
import requests
import unittest
from pprint import pprint
import os, sys
sys.path.append(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 父路径-Auto
sys.path.insert(0, parent_dir)
from DB import UseDataBase


class HT(unittest.TestCase):
    def setUp(self):
        self.session = requests.session()
        self.ip = 'http://139.196.107.14:9000'

    def test_update(self):
        url = self.ip + '/cms/article/status/update'
        data = {'id': 185, 'isShow': 1}
        res = self.session.request(method='post', url=url, params=data)
        pprint(res.json())

if __name__ == '__main__':
    unittest.main()