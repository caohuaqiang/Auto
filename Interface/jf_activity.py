# -*- coding: utf-8 -*
import requests
import unittest
from pprint import pprint
import os, sys
sys.path.append(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 父路径-Auto
sys.path.insert(0, parent_dir)
from DB import UseDataBase
from ForUse import read_ini


config = read_ini(ini_path=parent_dir + '/user.ini')
user = eval(config.get(section='user', option='chq'))


class Activity(unittest.TestCase):
    """日常活动"""
    def setUp(self):
        self.yuming = 'https://www-t.jfcaifu.com'
        self.session = requests.session()
# -------------------------------------------回归用的登陆账号----------------------------------------------------

        self.phone = user['username']                       # 日常回归用登录账号
        self.pwd = user['password']

# -------------------------------------------【注册专用】账号----------------------------------------------------
        self.register_phone = '17302188888'                 # 注册专用账号
        self.register_pwd = 'a1234567'

    def tearDown(self):
        with UseDataBase() as cursor:
            cursor.execute("DELETE from rd_user where mobile_phone = %s", args=(self.register_phone,))
            cursor.execute("DELETE from rd_notice where receive_addr = %s and nid = 'notice_reg';",
                           args=(self.register_phone,))

    def login(self, phone, pwd) -> 'response':
        session = self.session
        path_login = '/wap/user/doLogin.html'
        response_login = session.request(method='post', params={'mobilePhone': phone, 'pwd': pwd}, url=self.yuming + path_login)
        if response_login.status_code == 200 and response_login.json()['msg'] == '登录成功！':
            return response_login
        else:
            print(response_login.status_code, response_login.text)
            raise Exception('登录接口请求失败')

    # @unittest.skip('跳过注册活动测试')
    def test_register_without_channelcode(self):
        """注册活动(带渠道码)"""
        session = self.session
        path_register = '/activity/flying.html'
        path_code = '/wap/user/getActivityCode.html'

        channelCode = '40409'
        response_code = session.request(method='post', params={'mobilePhone': self.register_phone}, url=self.yuming + path_code)
        if response_code.status_code == 200:
            print('获取验证码接口:', end=' ')
            pprint(response_code.json())
        else:
            print('验证码接口翻车！！！')

        data_login = {'channelCode': channelCode,
                      'pwd': self.register_pwd,
                      'mobilePhone': self.register_phone,
                      'code': '888888'}
        response_login = session.request(method='get', url=self.yuming + path_register, params=data_login)
        if response_login.status_code == 200:
            self.assertEqual('领取成功！', response_login.json()['msg'])
            print('注册接口返回json：', end=' ')
            pprint(response_login.json())
            with UseDataBase() as cursor:
                # _SQL = "select user_id, user_name, pwd, mobile_phone, channel_type from rd_user where mobile_phone = %s" % self.phone
                # cursor.execute(_SQL)

                _SQL = "select user_id, user_name, pwd, mobile_phone, channel_type from rd_user where mobile_phone = %s"
                cursor.execute(_SQL, args=(self.register_phone))

                contents = cursor.fetchall()
                print('contents: ', contents)
                for data in contents:
                    print('注册用户sql信息：')
                    pprint(data)

                res_login = self.login(phone=self.register_phone, pwd=self.register_pwd)
                pprint(res_login.json())
                self.assertEqual(res_login.status_code, 200)
                self.assertEqual('登录成功！', res_login.json()['msg'])          # 验证一下 注册成功后的账号能否正常登陆

        else:
            raise Exception('注册流程失败')


    # @unittest.skip('跳过登录测试')
    def test_login(self):
        """登录接口"""
        json_login = self.login(phone=self.phone, pwd=self.pwd).json()
        pprint(json_login)


if __name__ == '__main__':
    # suite = unittest.TestSuite()
    # suite.addTest(Activity("test_login"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
    unittest.main()
