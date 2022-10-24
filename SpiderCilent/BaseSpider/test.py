import json

import redis

# 
# rd = redis.Redis('127.0.0.1', port=6379, db=0, password='root')
# 
# req_param = {}
#
# url = 'http://www.ccgp-guizhou.gov.cn/article-search.html',
# body = 'siteId=1&articlePageNo=' + str(1) + '&category.id=1153797950913584&articlePageSize=15',
# callback = 'parse',
# method = 'POST',
# 
# req_param['url'] = url
# req_param['body'] = body
# req_param['call_back'] = callback
# req_param['method'] = method
# 
# rd.lpush(
#         'BASE_SPIDER',
#         json.dumps(
#             req_param
#         )
#     )

from tools.RequestTool import HttpSession

var = HttpSession().request(r'spider_list_query', {'spider_id': '1004'}).json()['spider']