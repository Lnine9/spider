from BaseSpider.base_component.PageResolver import PageResolver
from BaseSpider.base_component.entity.PageAttribute import PageAttribute
from BaseSpider.tool.DealDate import get_one_time_from_str
import json
import re

class YN_Intention(PageResolver):

    def __init__(self):
        self.url_prefix = 'http://www.ccgp-yunnan.gov.cn/governmentpolicy.do?method=viewPurchaseInfo&sys_purchaseintention_id='

    def resolver_page(self) -> PageAttribute:
        string = json.loads(self.response.text)
        data = string['rows']
        page_size = int(string['rowCount'])
        largest_page = int(string['total']) // page_size
        aim_crawl_page = int(string['current'])


        url_list = list(self.url_prefix + item['sys_purchaseintention_id'] for item in data)
        url_list = list(set(url_list))
        cur_latest_url = url_list[0]
        newest_time = get_one_time_from_str(data[0]['send_date'])
        oldest_time = get_one_time_from_str(data[-1]['send_date'])
        # 该位置必须实现
        # page_attribute 参数必须全部有值
        page_attribute = PageAttribute(largest_page, cur_latest_url, page_size, aim_crawl_page, url_list, newest_time,
                                       oldest_time)
        print(aim_crawl_page, newest_time, oldest_time, largest_page)
        return page_attribute

