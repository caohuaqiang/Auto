import urllib
import urllib.request
import requests
import re


# def get_image(url):
#     request = urllib.request.Request(url)
#     response = urllib.request.urlopen(request)
#     get_image = response.read()
#     with open(file='001.jpg', mode='wb', ) as fp:
#         fp.write(get_image)
#         print('图片下载完成')
#     return


# def get_image(url):
#     session = requests.session()
#     response = session.request(method='get', url=url)
#     get_image = response.content
#     with open(file='002.jpg', mode='wb', ) as fp:
#         fp.write(get_image)
#         print('图片下载完成')
#
#
# if __name__ == '__main__':
#     url = 'http://p2.123.sogoucdn.com/imgu/2016/10/20161019124600_428.jpg'
#     get_image(url)


def download_page(url):
    response = requests.request(method='get', url=url)
    data = response.content
    return data


def get_image(html):
    regx = r'https://[\S]*\.jpg'
    pattern = re.compile(pattern=regx)
    image_urls = re.findall(pattern=pattern, string=repr(html))
    num = 1
    for image_url in image_urls:
        image = download_page(image_url)
        with open(file='%s.jpg' % num, mode='wb', ) as fp:
            fp.write(image)
            num += 1
            print('正在下载第%s张图片' % num)
    return


if __name__ == '__main__':
    url = 'https://tieba.baidu.com/f?kw=鹰眼'
    html = download_page(url)
    get_image(html)





























