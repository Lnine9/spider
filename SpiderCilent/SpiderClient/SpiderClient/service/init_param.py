import json
from random import random

from ..service import m_redis
from ..settings import http
from datetime import datetime
from re import sub

'''
找到对应爬虫初始化参数信息
传入 redis
'''


def param_to_redis(m_spider_id):
    spider_message = http.request(r'spider_init_query', {'spider_id': m_spider_id}).json()
    base_key = http.request(r'spider_model_query', {'spider_id': m_spider_id}).json()['spider']['base_key']

    req_param = {}
    url = spider_message['url']
    body = spider_message['body']
    callback = spider_message['callback']
    method = spider_message['method']

    req_param['url'] = url
    req_param['body'] = body
    req_param['call_back'] = callback
    req_param['method'] = method

    GGZY_END_TIME = datetime.now().strftime('%Y-%m-%d')
    if m_spider_id in ['1001', '1002', '1003', '1004']:
        fix_body = sub(r'(?<=TIMEEND=)\d{4}-\d{2}-\d{2}(?=&)', GGZY_END_TIME, req_param['body'])
        fix_body = sub(r'(?<=TIMEEND_SHOW=)\d{4}-\d{2}-\d{2}(?=&)', GGZY_END_TIME, fix_body)
        req_param['body'] = fix_body

    elif m_spider_id in ['1104', '1105']:
        fix_body = sub(r'<random>', str(random()), req_param['body'])
        req_param['body'] = fix_body

    try:
        back = m_redis.lpush(
            base_key + ":LIST",
            json.dumps(
                req_param
            )
        )
        return {'status': True, 'redis-back': back}
    except Exception as ex:
        return {'status': False, 'error': ex.args}
