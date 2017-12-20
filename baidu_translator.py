#/usr/bin/env python
#coding=utf8
from __future__ import print_function

import http.client
import hashlib
import random
import json
from urllib import parse

appid = ''
secretKey = ''

 
def baidu_translator(q):
    httpClient = None
    myurl = '/api/trans/vip/translate'
    fromLang = 'en'
    toLang = 'zh'
    salt = random.randint(32768, 65536)

    sign = appid+q+str(salt)+secretKey
    m1 = hashlib.md5()
    m1.update(sign.encode(encoding='gb2312'))
    sign = m1.hexdigest()
    myurl = myurl+'?appid='+appid+'&q='+parse.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        response = httpClient.getresponse() # response是HTTPResponse对象
        res_str = response.read()
        # print(res_str)
        res_obj = json.loads(res_str)
    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()
    return "|".join([i["dst"] for i in res_obj["trans_result"]])

if __name__ == '__main__':
    query_list = [
        # "apple",
        # "pen",
        # "I need to find an expensive restauant that's in the south section of the city.",
        # "expensive",
        "No I don't care about the type of cuisine.",
        "dontcare"
    ]
    for cur_q in query_list:
        print("------------------")
        cur_r = baidu_translator(q=cur_q)
        print(cur_r)

