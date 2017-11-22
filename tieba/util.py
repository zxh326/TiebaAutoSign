import random
import hashlib
import requests
from bs4 import BeautifulSoup as bf

baidu_spider_ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) \
                   AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 \
                   Mobile/13B143 Safari/601.1 (compatible; \
                   Baiduspider-render/2.0; \
                   +http://www.baidu.com/search/spider.html)'


def get_tieba_list(bduss):
    tiebas = []
    s = requests.Session()
    data = s.get('https://tieba.baidu.com/?page=like',
                 headers={'User-Agent': baidu_spider_ua},
                 cookies={'BDUSS': bduss})
    soup = bf(data.text, 'lxml')
    ties = soup.find_all('li', class_=['forumTile forumTile_withLevel'])
    # print (soup)

    for t in ties:
        tmplist = []
        tmp = t.select('a')[0].attrs
        fid = tmp['data-fid']
        titile = tmp['data-start-app-param']
        tmplist.append(fid)
        tmplist.append(titile)
        tiebas.append(tmplist)

    # print (tiebas)
    return tiebas


def _get_tbs(bduss):
    s = requests.get('http://tieba.baidu.com/dc/common/tbs',
                     headers={'User-Agent': 'fuck phone',
                              'Referer': 'http://tieba.baidu.com/',
                              'X-Forwarded-For': '115.28.1.{}'
                              .format(random.randint(1, 255))},
                     cookies={'BDUSS': bduss})
    return s.json()['tbs']


def do_sign(bduss, fid, tiename):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Fucking iPhone/1.0 BadApple/99.1',
    }
    cookies = {
        'BDUSS': bduss,
    }
    datas = {
        'BDUSS': bduss,
        '_client_id': '03-00-DA-59-05-00-72-96-06-00-01-00-\
                       04-00-4C-43-01-00-34-F4-02-00-BC-25-\
                       09-00-4E-36',
        '_client_type': '4',
        '_client_version': '1.2.1.17',
        '_phone_imei': '540b43b59d21b7a4824e1fd31b08e9a6',
        'fid': fid,
        'kw': tiename,
        'net_type': '3',
        'tbs': _get_tbs(bduss)
    }

    hashstr = ''
    keys = 'tiebaclient!!!'
    datakeys = datas.keys()
    # datakeys.sort()
    for i in datakeys:
        hashstr += str(i) + '=' + str(datas[i])

    # error_code 0 正常           => 成功
    # error_code 160002 重复      => 成功
    # error_code * 失败           => 失败

    sign = hashlib.md5(hashstr.encode('utf-8') +
                       keys.encode('utf-8')).hexdigest().upper()

    datas['sign'] = sign

    res = requests.post('http://c.tieba.baidu.com/c/c/forum/sign',
                        headers=headers, cookies=cookies, data=datas)

    return (res.json())
