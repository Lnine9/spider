import json
import logging

import scrapy
from scrapy import Request
from scrapy.http import Response
from BaseSpider.tool.DealDate import get_one_time_from_str
import re

from BaseSpider.tool.RequestTool import HttpSession

CATEGORY = {
    1: '粮油',
    2: '蔬菜',
    3: '水果',
    4: '肉蛋',
    5: '水产',
    6: '农资',
}


class FarmMarketSpider(scrapy.Spider):
    name = "FARM_MARKET_SPIDER"
    base_url = "http://sc.cqnync.cn/marketSta/"
    http = HttpSession()

    def start_requests(self):
        for key in CATEGORY.keys():
            yield Request(url=self.base_url + '?vexp=' + str(key) + '&classId=' + str(key), dont_filter=True)


    def parse(self, response: Response, **kwargs):
        content = {'F_M': [], 'an_type': 'F_M', 'version_no': 1}

        category_id =int(re.search(r'classId=(?P<cate>\d)', response.url).group('cate'))
        category = CATEGORY.get(category_id)

        trs = response.xpath("(//div[@id='scroller']//table)[1]//tr")

        varieties = []

        for tr in trs:
            item = {}
            item['variety'] = tr.xpath("./td[@class='variety']/text()").extract_first()
            if not item['variety']:
                continue
            elif item['variety'] in varieties:
                break
            else:
                varieties.append(item['variety'])
            item['time'] = get_one_time_from_str(tr.xpath("./td[@class='gatherTime']/text()").extract_first())
            item['method'] = tr.xpath("./td[@class='saleType']/text()").extract_first()
            item['price'] = float(tr.xpath("./td[@class='price']/span/text()").extract_first())
            item['unit'] = tr.xpath("./td[@class='unit']/text()").extract_first()
            item['yesterdaynum'] = tr.xpath("./td[@class='volume']/text()").extract_first()
            if item['yesterdaynum'] == '-':
                item['yesterdaynum'] = '0'
            item['market'] = tr.xpath("./td[@class='market']/text()").extract_first()
            item['category'] = category

            logging.info(item)

            content['F_M'].append(item)

        if len(content['F_M']) > 0:
            self.write_ann_to_db(content)

    def write_ann_to_db(self, item):
        try:
            x = json.dumps(item)
            an_id = self.http.request(r'add_an_to_db', {'item': x}).json()
            an_id = an_id['an_id']
            return {'an_id': an_id, 'error': None}
        except AttributeError as abe:
            logging.error('Database connection error：' + str(abe.args))
            return {'an_id': None, 'exception_type': 'spider exception', 'reason': abe}
        except Exception as e:
            logging.warning('Data into inventory is error：' + str(e.args))
            return {'an_id': None, 'exception_type': 'resolver exception', 'reason': e}







