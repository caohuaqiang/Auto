import requests
from pprint import pprint
from DB import UseDataBase


def chq(data):
    session = requests.session()
    url = 'http://139.196.107.14:9000/cms/images/queryEnableImages'
    res = session.request(method='post', url=url, params=data)
    return res.json()
    # pprint(res.json())


def search_article(data):
    session = requests.session()
    url = 'http://139.196.107.14:9000/cms/article/query/enableArticles'
    res = session.request(method='get', url=url, params=data)
    return res






if __name__ == '__main__':
    # data = {'imageTypes': 'find_icon_mb',
    #         'source': ''}
    # print('传参： ',data)
    #
    # print(chq(data))
    # print('=================================上面是完整json=================================================')
    # dt = chq(data)['data']
    # if dt:
    #     try:
    #         contents = dt[data['imageTypes']]
    #         for content in contents:
    #             pprint(content)
    #             print('------------------------------------------------------------------------------------------------')
    #     except Exception:
    #         raise Exception('数组越界')
    tp = 'site_notice'
    data = {'menuCode': tp,
            'pageIndex': '4',
            'pageSize': '5',
            }
    res = search_article(data)

    pprint(res.json())

    # articles = res.json()['data'][tp]['articleDtoList']
    # n = 0
    # for article in articles:
    #     pprint(article)
    #     print('-----------------------------------------------------------------------------------------------------------------------------')
    #     n += 1
    # print(n)


























