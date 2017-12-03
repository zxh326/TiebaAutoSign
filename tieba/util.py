# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     util.py  
   Description :  签到 | 获取 | 核心
   date：          2017/11/19
-------------------------------------------------
   Change Activity:
                   2017/12/03: 
-------------------------------------------------
    TODO：
        速度优化
-------------------------------------------------       
"""
import re
import time
import random
import hashlib
import requests
from bs4 import BeautifulSoup as bf
baidu_spider_ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) \
                   AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 \
                   Mobile/13B143 Safari/601.1 (compatible; \
                   Baiduspider-render/2.0; \
                   +http://www.baidu.com/search/spider.html)'

normal_ua = 'Mozilla/5.0 (SymbianOS/9.3; Series60/3.2 NokiaE72-1/021.021; \
             Profile/MIDP-2.1 Configuration/CLDC-1.1 ) \
             AppleWebKit/525 (KHTML, like Gecko) \
             Version/3.0 BrowserNG/7.1.16352'


def get_user_bname(bduss):
    tiebas = []
    result = {}
    s = requests.Session()
    data = s.get('https://tieba.baidu.com/?page=like',
                 headers={'User-Agent': baidu_spider_ua},
                 cookies={'BDUSS': bduss})

    soup = bf(data.text, 'lxml')
    try:
        bname = re.findall('.*uname: "(.*?)"',
                           str(soup.select('body > script')))[0]
    except:
        bname = 'null'

    result['bname'] = bname

    if result['bname'] == 'null' or result['bname'] == '':
        result['status'] = 1
    else:
        result['status'] = 0

    return result


def get_user_tieba(bduss, bname):
    s = requests.Session()
    result = []
    page_count = 1
    has_more = '1'

    while True:
        datas = {
            '_client_id': 'wappc_' + str(int(time.time())) + '_' + '258',
            '_client_type': 2,
            '_client_version': '6.5.8',
            '_phone_imei': '357143042411618',
            'from': 'baidu_appstore',
            'is_guest': 1,
            'model': 'H60-L01',
            'page_no': page_count,
            'page_size': 200,
            'timestamp': str(int(time.time())) + '903',
            'uid': getuserid(bname),
        }

        datas['sign'] = gen_hash(datas)

        detail = s.post('http://c.tieba.baidu.com/c/f/forum/like',
                        headers={'User-Agent': normal_ua,
                                 'Content-Type': 'application/x-www-form-urlencoded'},
                        cookies={'bduss': bduss},
                        data=datas)

        for tieba in detail.json()['forum_list']['non-gconforum']:
            fid = tieba['id']
            name = tieba['name']
            result.append([fid, name])

        page_count = page_count + 1
        has_more = detail.json()['has_more']
        
        if has_more == '0':
            break
    
    return result


def getuserid(bname):
    res = requests.get(
        'http://tieba.baidu.com/home/get/panel?ie=utf-8&un={}'.format(bname))
    return res.json()['data']['id']


def get_tbs(bduss):
    s = requests.get('http://tieba.baidu.com/dc/common/tbs',
                     headers={'User-Agent': 'fuck phone',
                              'Referer': 'http://tieba.baidu.com/',
                              'X-Forwarded-For': '115.28.1.{}'
                              .format(random.randint(1, 255))},
                     cookies={'BDUSS': bduss})
    return s.json()['tbs']


def gen_hash(datas):
    hashstr = ''
    keys = 'tiebaclient!!!'
    datakeys = datas.keys()

    for i in datakeys:
        hashstr += str(i) + '=' + str(datas[i])

    sign = hashlib.md5(hashstr.encode('utf-8') +
                       keys.encode('utf-8')).hexdigest().upper()
    return sign


def do_sign(tbs, bduss, fid, tiename):
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
        'tbs': tbs
    }

    # error_code 0            => Success
    # error_code 16023        => Success
    # error_code *            => Faild

    datas['sign'] = gen_hash(datas)
 
    res = requests.post('http://c.tieba.baidu.com/c/c/forum/sign',
                        headers=headers, cookies=cookies, data=datas)

    return (res.json())
