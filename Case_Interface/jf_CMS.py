# -*- coding: utf-8 -*
import requests
import unittest
from pprint import pprint
import os, sys
sys.path.append(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 父路径-Auto
sys.path.insert(0, parent_dir)
from DB import UseDataBase


class CMS(unittest.TestCase):
    """CMS新项目接口（肖傲）"""
    def setUp(self):
        self.session = requests.session()
        self.ym = 'http://139.196.107.14:9000'

    def test_picture_query(self):
        """图片查询"""
        url = self.ym + '/cms/images/queryEnableImages'
        data = {'source': '40404', }
        imageTypes = {'index_loop_banner_mb': '移动首页轮播图',
                      'index_float_icon_mb': '移动首页悬浮ICON图',
                      'index_up_banner_mb': '首页固定图（上）',
                      'index_down_banner_mb': '首页固定图（下）',
                      'index_bank_manage_banner': '首页银行存管图',
                      'prd_loop_banner_mb': '产品轮播图',
                      'find_loop_banner_mb': '发现页轮播图',
                      'find_center_banner': '发现页央企图',
                      'find_icon_mb': '发现页icon图',
                      'app_start_banner': 'app启动图', }                   # 各个参数值代表的含义
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~传source(渠道号)~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        for k, v in imageTypes.items():
            data['imageTypes'] = k
            print('传参： ', data)
            res = self.session.request(method='post', url=url, params=data)
            self.assertEqual(200, res.status_code, msg='响应状态码非200！')
            pprint(res.json())
            print('===============================================以上是【' + v + '】的内容=========================================================')
        print()
        print()
        print('*************************不传source（渠道号）**********************')
        for k, v in imageTypes.items():
            data_kong = {}
            data_kong['imageTypes'] = k
            print('传参： ', data_kong)
            res_kong = self.session.request(method='post', url=url, params=data_kong)
            self.assertEqual(200, res_kong.status_code, msg='响应状态码非200！')
            pprint(res_kong.json())
            print('===============================================以上是【' + v + '】的内容=========================================================')


if __name__ == '__main__':
    unittest.main()

