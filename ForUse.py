# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from pprint import pprint
import requests
import smtplib
import configparser
import hashlib
import base64
import time



class Report_Mail:
    def __init__(self, report_dict):
        self.report_dict = report_dict

    def search_latest_file(self):
        """查找出最新的html文件"""
        lists = os.listdir(self.report_dict)
        lists.sort(key=lambda fn: os.path.getmtime(self.report_dict + fn))
        file_name = lists[-1]
        file_new = os.path.join(self.report_dict, file_name)  # join将报告路径及排序后的最新报告名称合并
        print('file_new: ', file_new)
        print('file_name: ', file_name)
        file_for_deliver = {'file_new': file_new,
                            'file_name': file_name}
        return file_for_deliver

    def send_mail(self, receiver):
        """发邮件（附件+正文）"""
        file = self.search_latest_file()
        file_new = file['file_new']
        file_name = file['file_name']
        f = open(file_new, 'rb')
        mail_body = f.read()
        f.close()

        # 邮件正文为测试报告
        msg = MIMEText(mail_body, 'html', 'utf-8')
        msg['Subject'] = Header("自动化测试报告", 'utf-8')

        # 添加附件
        send_file = open(file_new, 'rb').read()
        att = MIMEText(send_file, 'base-64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att['Content-Disposition'] = 'attachment; filename = %s' % file_name  # 附件的文件名-在new_report方法中返回可取得

        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = Header("曹华强", 'utf-8')  # 邮件主题
        msgRoot.attach(att)
        msgRoot.attach(msg)

        smtp = smtplib.SMTP_SSL()
        smtpsever = "smtp.qq.com"  # 服务器地址
        port = 465
        # 发件人邮箱的账号和密码
        send_user = '342473195@qq.com'
        password = 'nklgzyvjnnxzbggb'
        # 收件人邮箱
        smtp.connect(host=smtpsever, port=port)
        smtp.login(send_user, password)
        smtp.sendmail(send_user, receiver, msgRoot.as_string())
        smtp.quit()
        print("send email success!")


# class Houtai:
#     def __init__(self):
#         self.session = requests.session()
#         self.login_data = {'userName': 'admin', 'password': '123456', 'valicode': 'jfcf',}
#         self.ym = 'https://erp-t.jfcaifu.com'
#
#     def login(self):
#         url_login = self.ym + '/modules/login.html'
#         res_login = self.session.request(method='post', url=url_login, params=self.login_data)
#         return res_login
#
#     def search_money(self):
#         self.login()
#         url_search_money = self.ym + '/modules/account/account/accountList.html'
#         data_search_money = {'searchName': '15821903152',
#                              'page': 1,
#                              'rows': 20,
#                              'sort': 'id',
#                              'order': 'desc',}
#         res_search_money = self.session.request(method='post', url=url_search_money, params=data_search_money)
#         pprint(res_search_money.json())
#
#     def search_huifu_money(self):
#         self.login()
#         url_huifu_money = self.ym + '/modules/account/account/tppQueryUserBalance.html'
#         res_huifu_money = self.session.request(method='post', url=url_huifu_money, params={'id': 1687})
#         # print(res_huifu_money.text)
#         return res_huifu_money.text


def read_ini(ini_path: str) -> 'config':
    """读取ini配置文件，传入参数为文件路径（字符串格式），返回config对象，可对该对象使用config.get(section,name)方法取得相应的参数"""
    config = configparser.ConfigParser()
    config.read(ini_path, encoding='utf-8')
    return config


def app_miyao():
    """app传参密钥"""
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
    signature = {'appkey': appkey,
                 'signa': signa,
                 'ts': ts}
    return signature


def app_login(phone, pwd) -> 'dict':
    """app登录(返回字典)"""
    signature = app_miyao()
    data_login = signature.copy()
    data_login['id'] = phone
    data_login['pwd'] = base64.b64encode(pwd.encode(encoding='utf-8'))
    data_login['code'] = '888888'
    # print(data_login)
    url = 'https://www-t.jfcaifu.com/app/user/doLogin.html'
    session = requests.session()
    res_login = session.request(method='post', url=url, params=data_login)

    try:
        if res_login.status_code == 200 and res_login.json()['res_msg'] == '登录成功':
            login_res_json = res_login.json()
            data_after_login = signature.copy()

            data_after_login['user_id'] = login_res_json['res_data']['user_id']
            data_after_login['sign'] = login_res_json['res_data']['oauth_token']
            return data_after_login
    except Exception as err:
        print(err)
        raise Exception('登录接口翻车')


if __name__ == '__main__':
    A = app_login(phone='15821903152', pwd='a1234567')
    pprint(A)







