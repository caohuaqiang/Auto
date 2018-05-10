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
import base64
from ForUse import read_ini, app_miyao, app_login
from decimal import *

ini_path = parent_dir + '/user.ini'
config = read_ini(ini_path)
config.read(ini_path, encoding='utf-8')
user_login = eval(config.get(section='user', option='chq'))  # 登录账号
user_register = eval(config.get(section='user', option='register'))  # 注册账号


class APP(unittest.TestCase):
    """日常app接口"""
    def setUp(self):
        self.ym = 'https://www-t.jfcaifu.com'
        self.bendi_lrj = 'http://192.168.101.33:8080'   # 刘仁杰本地
        self.session = requests.session()
        self.signature = app_miyao().copy()

    @unittest.skip('跳过app注册')
    def test_register(self):
        """app注册"""
        url_get_verify_code = self.ym + '/app/user/getPortalVerifyCode.html'     # 获取图形验证码接口
        url_register = self.ym + '/app/user/doRegisterWithCode.html'
        data_register = {'imgCode': 'jfcf',
                         'phone': user_register['username'],
                         'pwd': base64.b64encode(user_register['password'].encode(encoding='utf-8')),
                         'code': '888888',
                         'idfa': '',
                         'inviteCode': '',
                         }
        data_register = dict(data_register, **self.signature)
        print()
        pprint(data_register)
        data_get_SMS_code = {'phone': user_register['username']}
        data_get_SMS_code = dict(data_get_SMS_code, **self.signature)   # 拼接app秘钥
        # pprint(data_get_SMS_code)
        res_get_SMS_code = self.session.request(method='post', url=self.ym + '/app/user/getRegisterCode.html',
                                                params=data_get_SMS_code)                                       # 获取短信验证码接口
        print(res_get_SMS_code.json())
        res_register = self.session.request(method='post', url=url_register, params=data_register)              # 请求注册接口
        print(res_register.text)

    # @unittest.skip('跳过短信快捷登录')
    def test_app_login_SMS(self):
        """短信快捷登录"""
        phone = user_login['username']
        url_get_SMS = self.ym + '/app/user/getLoginAuthCode.html'
        data_get_SMS = {'phone': phone}
        res_get_SMS = self.session.request(method='post', url=url_get_SMS, params=dict(self.signature, **data_get_SMS))
        print()
        # print(dict(self.signature, **data_get_SMS))
        # pprint(res_get_SMS.json())
        self.assertEqual('9999', res_get_SMS.json()['res_code'])
        with UseDataBase() as cursor:
            sql_verify_code = "SELECT receive_user, receive_addr, `code` from rd_notice where receive_addr = %s and nid = 'login_auth_code' ORDER BY id DESC limit 1;"
            cursor.execute(sql_verify_code, args=(phone, ))
            contents = cursor.fetchall()
            # pprint(contents)
            if contents:
                verify_code = contents[-1]['code']
            else:
                raise Exception('数据库内没有验证码记录')
            url_login_authcode = self.ym + '/app/user/loginByAuthCode.html'
            data_login_authcode = {'phone': phone, 'authCode': verify_code, }
            data_login_authcode = dict(data_login_authcode, **self.signature)
            res_login_authcode = self.session.request(method='post', url=url_login_authcode, params=data_login_authcode)
            pprint(res_login_authcode.json())
            self.assertEqual('登录成功', res_login_authcode.json()['res_msg'])

    # @unittest.skip('跳过我的页面')
    def test_myaccount(self):
        """我的页面（我的账户）"""
        url = self.ym + '/app/v600/account/basic.html'
        phone = user_login['username']
        pwd = user_login['password']
        data_after_login = app_login(phone=phone, pwd=pwd)  # 登录后的字典
        # pprint(data_after_login)
        res = self.session.request(method='post', url=url, params=data_after_login)
        print()
        res_data_account = res.json()['res_data']

        pprint(res_data_account)
        print('------------------------------------------------------------------------')

        wants_key = ['useMoney', 'noUseMoney', 'collection', 'total', 'totalInterest']
        account_lrj = {}
        for key in wants_key:
            account_lrj[key] = res_data_account[key]
        pprint(account_lrj)
        print('============================')

    # @unittest.skip('跳过查询抽奖')
    def test_app_queryprizetime(self):
        """app查询抽奖"""
        url = self.ym + '/app/v500/query_times.html'
        phone = user_login['username']
        pwd = user_login['password']
        data_after_login = app_login(phone=phone, pwd=pwd)
        pprint(data_after_login)
        res = self.session.request(method='post', url=url, params=data_after_login)
        pprint(res.json())



    def tearDown(self):
        sql_user_id = 'select user_id from rd_user where mobile_phone = %s'
        with UseDataBase() as cursor:
            cursor.execute(sql_user_id, args=(user_register['username'],))
            contents = cursor.fetchall()
            if contents:
                user_id = contents[-1]['user_id']
                sql_delete_user = 'DELETE FROM rd_user where user_id = %s'
                sql_delete_account = 'DELETE FROM rd_account where user_id = %s'
                cursor.execute(sql_delete_user, args=(user_id,))
                cursor.execute(sql_delete_account, args=(user_id,))


if __name__ == '__main__':
    unittest.main()
