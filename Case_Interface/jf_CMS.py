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
        self.ip = 'http://139.196.107.14:9000'

    # @unittest.skip('跳过sms图片查询列表')
    def test_picture_query(self):
        """图片查询"""
        url = self.ip + '/cms/images/queryEnableImages'
        data = {'source': 'baidu', }
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
            # pprint(res.json())
            dt = res.json()['data']     # 图片数据字典

            if dt:      #检查是否是空字典
                try:
                    with UseDataBase() as cursor:
                        sql = "SELECT * from tn_cms_images where hide_time > NOW() and show_time < NOW() and image_type = %s;"
                        cursor.execute(sql, args=(k, ))
                        contents = cursor.fetchall()
                        if contents:
                            self.assertNotEqual([], dt[k], msg='数据库有数据，但是给的列表为空！')

                except Exception as err:
                    raise Exception(err)
            print('===============================================以上是【' + v + '】的内容=========================================================')

        print()
        print()
        print('************************************不传source（渠道号）******************************************')
        for k, v in imageTypes.items():
            data_kong = {}
            data_kong['imageTypes'] = k
            print('传参： ', data_kong)
            res_kong = self.session.request(method='post', url=url, params=data_kong)
            self.assertEqual(200, res_kong.status_code, msg='响应状态码非200！')
            # pprint(res_kong.json())
            dt_kong = res_kong.json()['data']  # 图片数据字典
            if dt_kong:
                try:
                    with UseDataBase() as cursor:
                        sql = "SELECT * from tn_cms_images where hide_time > NOW() and show_time < NOW() and image_type = %s and source is NULL ;"
                        cursor.execute(sql, args=(k, ))
                        contents = cursor.fetchall()
                        if contents:
                            self.assertNotEqual([], dt_kong[k], msg='数据库有数据，但是给的列表为空！')

                except Exception as err:
                    raise Exception(err)
            print('===============================================以上是【' + v + '】的内容=========================================================')

    def test_article_query(self):
        """文章查询"""
        url = self.ip + '/cms/article/query/enableArticles'
        menuCode = {'site_notice': '网站公告',                  # 图片类型
                    'media_report': '媒体报道',
                    }
        data_search_article = {'menuCode': '',
                               'pageIndex': '3',
                               'pageSize': '5',
                               }

        for k, v in menuCode.items():
            print(v + ': ')
            data_search_article['menuCode'] = k
            res = self.session.request(method='get', url=url, params=data_search_article)
            self.assertEqual(200, res.status_code)
            articles = res.json()['data'][k]['articleDtoList']
            num = 0
            for article in articles:
                # pprint(article)
                # print('-----------------------------------------------------------------------------------------------------------------------------')
                num += 1                                                                # 统计出 接口返回的列表内有几条数据
            sql = "SELECT COUNT(*) AS NUM from tn_cms_article where menu_code = %s;"
            with UseDataBase() as cursor:
                cursor.execute(sql, args=(k, ))
                contents = cursor.fetchall()
            sql_num = contents[-1]['NUM']                                   # sql_num:数据库中的条数；num:接口返回的条数
            print('sql_num数据库中的总条数：', sql_num)

            pagesize = int(data_search_article['pageSize'])                 # 每页想要的条数
            pageindex = int(data_search_article['pageIndex'])               # 接口传参-【想要】显示的是第几页
            sql_index = int(sql_num/pagesize)                               # 算出能全显示条数的页数
            print('sql_index能全显示条数的页数:', sql_index)
            print('pagesize想要显示几条数据：', pagesize)
            yushu = int(sql_num % pagesize)
            print('余数:', yushu)

            if yushu != 0 and (pageindex - sql_index) == 1:      # 逻辑：以数据库查出14条数据为例，请求参数为每页5条数据，那么第一第二页都能按照要求显示5条，但最后一页就只能显示最后剩下的4条
                self.assertEqual(yushu, num)
            elif (pageindex - sql_index) > 1:                   # 超过最后一页的页数时，空列表
                self.assertEqual(0, num)
            else:
                self.assertEqual(pagesize, num)


if __name__ == '__main__':
    unittest.main()

