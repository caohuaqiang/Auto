# -*- coding: utf-8 -*
import requests
import unittest
import os, sys
sys.path.append(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 父路径-Auto
sys.path.insert(0, parent_dir)
from pprint import pprint
from DB import UseDataBase
import base64
import time
import hashlib
from ForUse import read_ini


ini_path = parent_dir + '/user.ini'
config = read_ini(ini_path)
config.read(ini_path, encoding='utf-8')
user = eval(config.get(section='user', option='chq'))


class App(unittest.TestCase):
    """app移动端"""
    def setUp(self):
        """ios签名加密"""
        appkey = 'V/SQ/yTyYjDmNLXB2unELw=='  # 固定值，得到了appkey
        a = 'LzgvD74cyEspGADEKOxAhA=='
        ts = int(time.time())
        A = a + str(ts)
        A_md5 = hashlib.md5(A.encode('utf-8'))
        B = A_md5.hexdigest()  # 按16位输出
        C = B + appkey
        C_md5 = hashlib.md5(C.encode('utf-8'))
        D = C_md5.hexdigest()  # 按16位输出
        signa = D.upper()  # 转成大写，得到了signa
#---------------------------------------------------------------------------------------
        # self.phone = '15821903152'
        # self.password = 'a1234567'
        self.phone = user['username']
        self.password = user['password']
        signature = {'appkey': appkey,
                     'signa': signa,
                     'ts': ts}
        self.signature = signature.copy()
        self.session = requests.session()
        self.login()
        self.user_id = self.login().json()['res_data']['user_id']
        self.token = self.login().json()['res_data']['oauth_token']
        self.signature['sign'] = self.login().json()['res_data']['oauth_token']

    def login(self):
        """登录"""
        data_login = self.signature
        data_login['id'] = self.phone
        data_login['pwd'] = base64.b64encode(self.password.encode(encoding='utf-8'))
        response = self.session.request(method='post', url='https://www-t.jfcaifu.com/app/user/doLogin.html', params=data_login)
        try:
            if response.status_code == 200 and response.json()['res_msg'] == '登录成功':
                return response
        except Exception as err:
            print(err)
            raise Exception('登录接口翻车')

    def test_recommended_product(self):
        """有推荐标时检查推荐标列表是否为空"""
        url_index = 'https://www-t.jfcaifu.com/app/v500/index.html'
        data_index = self.signature.copy()
        data_index['user_id'] = self.user_id
        res_recommend = self.session.request(method='get', url=url_index, params= data_index,)
        if res_recommend.status_code == 200:
            rec_pro = res_recommend.json()['res_data']['fixBorrowList']
            pprint(rec_pro)
        else:
            raise Exception('首页接口翻车')

        with UseDataBase() as cursor:
            _sql = "SELECT * from rd_borrow where `status` = 1 and is_recommend = 1;"
            cursor.execute(_sql)
            contents = cursor.fetchall()
        if contents:
            self.assertNotEqual([], rec_pro)


if __name__ == '__main__':
    unittest.main()



