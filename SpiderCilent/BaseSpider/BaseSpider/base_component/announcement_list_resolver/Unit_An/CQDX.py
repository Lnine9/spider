from scrapy import Request

from BaseSpider.base_component.PageResolver import PageResolver
from BaseSpider.base_component.entity.PageAttribute import PageAttribute
from BaseSpider.tool.DealDate import get_one_time_from_str
import json
import re

class CQDX(PageResolver):

    def __init__(self):
        self.url_prefix = 'https://www.yuncaitong.cn/api/publish/'

    def resolver_page(self) -> PageAttribute:
        req = self.response.request
        string = json.loads(self.response.body)
        data = string['resultset']
        largest_page = 30

        start = int(re.search(r'start=(\d+)&', str(req.body)).group(1))
        aim_crawl_page = start // len(data) + 1

        data = [item for item in data if item['syncId']]
        cur_latest_url = self.url_prefix + data[0]['syncId']

        url_list = list(self.url_prefix + item['syncId'] for item in data)
        newest_time = get_one_time_from_str(data[0]['syncTime'])
        oldest_time = get_one_time_from_str(data[-1]['syncTime'])
        page_size = len(data)
        # 该位置必须实现
        # page_attribute 参数必须全部有值
        page_attribute = PageAttribute(largest_page, cur_latest_url, page_size, aim_crawl_page, url_list, newest_time,
                                       oldest_time)
        print(aim_crawl_page, newest_time, oldest_time, largest_page)
        return page_attribute

