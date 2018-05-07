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

ini_path = parent_dir + '/user.ini'
config = read_ini(ini_path)
config.read(ini_path, encoding='utf-8')
user_login = eval(config.get(section='user', option='chq'))  # 登录账号
user_register = eval(config.get(section='user', option='register'))  # 注册账号


class APP(unittest.TestCase):
    def setUp(self):
        self.ym = 'http://192.168.101.172:8080'
        self.session = requests.session()
        self.signature = app_miyao().copy()

    def test_register(self):
        url_get_verify_code = self.ym + '/app/user/getPortalVerifyCode.html'     # 获取图形验证码接口
        url_register = self.ym + '/app/user/doRegisterWithCode.html'
        data_register = {'imgCode': '1234',
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
        data_get_SMS_code = dict(data_get_SMS_code, **self.signature)
        # pprint(data_get_SMS_code)
        # res_get_SMS_code = self.session.request(method='post', url=self.ym + '/app/user/getRegisterCode.html',
        #                                         params=data_get_SMS_code)                                     # 获取短信验证码接口
        # print(res_get_SMS_code.json())
        res_register = self.session.request(method='post', url=url_register, params=data_register)              # 请求注册接口
        print(res_register.text)

    def tearDown(self):
        sql_user_id = 'select user_id from rd_user where mobile_phone = %s'
        with UseDataBase() as cursor:
            cursor.execute(sql_user_id, args=(user_register['username'],))
            contents = cursor.fetchall()
            user_id = contents[-1]['user_id']

        sql_delete_user = 'DELETE FROM rd_user where mobile_phone = %s'
        # sql_delete_account
        with UseDataBase() as cursor:

            cursor.execute(sql_delete_user, args=(user_register['username'],))



if __name__ == '__main__':
    unittest.main()
