import re

from BaseSpider.base_component.PageResolver import PageResolver
from BaseSpider.base_component.entity.PageAttribute import PageAttribute
from BaseSpider.tool.DealDate import get_one_time_from_str
import json
import re

'''
必须定义的参数
'''
CONST_PARAM = {
    # 网址前缀
    'BASE_URL': '',
    # 当前最大网页
    'LARGEST_PAGE': '//div[@id="paging"]/a[last()-1]/text()',
    # 当前网页最新URl
    'CUR_LATEST_URL': '//div[@class="publicont"][1]//a/@href',
    # URL列表XPATH路径
    'LINK_HREFS': '//div[@class="publicont"]//a/@href',
    # 当前页面页码
    'AIM_CRAWL_PAGE': '//div[@id="paging"]/a[@class="a_hover"]/text()',

}


class GGZY_Announce_List_Resolver(PageResolver):
    #  该init方法必须在子类（该类）实现
    def __init__(self):
        self.x_base_url = CONST_PARAM.get('BASE_URL')
        self.x_largest_page = CONST_PARAM.get('LARGEST_PAGE')
        self.x_cur_latest_url = CONST_PARAM.get('CUR_LATEST_URL')
        self.x_link_hrefs = CONST_PARAM.get('LINK_HREFS')
        self.x_aim_crawl_page = CONST_PARAM.get('AIM_CRAWL_PAGE')

    # 将页面解析，返回当前页面信息
    def resolver_page(self) -> PageAttribute:
        string = json.loads(self.response.body)
        largest_page = int(string['ttlpage'])
        aim_crawl_page = int(string['currentpage'])
        data = string['data']
        cur_latest_url = data[0]['url']

        url_list = list((re.sub(r'/a/', r'/b/', item['url'], 1) for item in data))
        newest_time = get_one_time_from_str(data[0]['timeShow'])
        oldest_time = get_one_time_from_str(data[-1]['timeShow'])
        page_size = len(data)

        # 该位置必须实现
        # page_attribute 参数必须全部有值
        page_attribute = PageAttribute(largest_page, cur_latest_url, page_size, aim_crawl_page, url_list, newest_time,
                                       oldest_time)
        return page_attribute
