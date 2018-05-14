# -*- coding: utf-8 -*
import requests
import unittest
from pprint import pprint
import os, sys
sys.path.append(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 父路径-Auto
sys.path.insert(0, parent_dir)
from DB import UseDataBase


class XA(unittest.TestCase):
    def setUp(self):
        self.session = requests.session()
        self.ip = 'http://139.196.107.14:9000'

    # @unittest.skip('跳过图片查询接口')
    def test_CMS_picture(self):
        url = self.ip + '/cms/images/queryEnableImages'
        image_type = 'find_center_banner'
        data = {'source': '', 'imageTypes': image_type, }
        res = self.session.request(method='post', url=url, params=data)
        # print(res.json())
        print()
        if res.json()['data']:
            n = 0
            for A in res.json()['data'][image_type]:
                pprint(A)
                # print(A['keyWord'])
                n += 1
            print(n)

    @unittest.skip('跳过文章查询接口')
    def test_CMS_article(self):
        url = self.ip + '/cms/article/query/enableArticles'
        menuCode = 'media_report'
        data_search_article = {'menuCode': menuCode,
                               'pageIndex': '1',
                               'pageSize': '5',
                               }
        print()
        res = self.session.request(method='get', url=url, params=data_search_article)
        # pprint(res.json())


        articles = res.json()['data'][menuCode]['articleDtoList']
        n = 0
        for article in articles:
            pprint(article['title'])
            n += 1
            print('---------------------------------------------------------------')
        print(n)



if __name__ == '__main__':
    unittest.main()
























