# -*- coding: utf-8 -*
import time, sys, os
parent_dir = os.path.dirname(os.path.abspath(__file__))     # 根目录-Auto
sys.path.append(parent_dir)
sys.path.append(os.path.abspath(__file__))
sys.path.append('./')
from HTMLTestRunner import HTMLTestRunner
import unittest
from ForUse import Report_Mail, read_ini

# 指定测试用例为当前目录下的Case_Interface目录
test_dir = parent_dir + '/Case_Interface'
discover = unittest.defaultTestLoader.discover(test_dir, pattern='jf*.py')


if __name__ == '__main__':
    now = time.strftime('%Y-%m-%d %H_%M_%S')
    filename = './Report_Interface/' + now + '_result.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(stream=fp,
                            title='曹华强自动化测试报告(接口)',
                            description='接口自动化测试报告')
    # runner = unittest.TextTestRunner()
    runner.run(discover)
    fp.close()

    report_dict = parent_dir + '/Report_Interface/'
    Email = eval(read_ini(parent_dir + '/user.ini').get(section='Email', option='email'))
    rm = Report_Mail(report_dict)
    rm.send_mail(receiver=[Email['chq'], ])


