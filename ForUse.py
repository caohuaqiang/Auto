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
