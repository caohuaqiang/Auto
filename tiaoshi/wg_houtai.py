import requests
import json
from pprint import pprint


def chq():
    session = requests.session()
    url = 'https://ceshiopen.jfcaifu.com/gateway/per/login/adminLogin'
    data = {'loginName': 'it009',
            'password': '9db06bcff9248837f86d1a6bcf41c9e7',
            }
    res = session.request(method='post', url=url, params=data)
    # res = requests.post(url=url, data=data)
    print(res.status_code)
    # print(res.text)
    pprint(res.json())


if __name__ == '__main__':
    chq()
