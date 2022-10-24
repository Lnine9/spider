import re
import json

from BaseSpider.base_component.PageResolver import PageResolver
from BaseSpider.base_component.entity.PageAttribute import PageAttribute

'''
必须定义的参数
'''
CONST_PARAM = {
    # 网址前缀
    'BASE_URL': '',
    # 当前最大网页
    'LARGEST_PAGE': '',
    # 当前网页最新URl
    'CUR_LATEST_URL': '',
    # URL列表XPATH路径
    'LINK_HREFS': '',
    # 当前页面页码
    'AIM_CRAWL_PAGE': '',
}


class GZPR_Annouce_List_Resolver_CallBid(PageResolver):
    #  该init方法必须在子类（该类）实现
    def __init__(self):
        self.x_base_url = CONST_PARAM.get('BASE_URL')
        self.x_largest_page = CONST_PARAM.get('LARGEST_PAGE')
        self.x_cur_latest_url = CONST_PARAM.get('CUR_LATEST_URL')
        self.x_link_hrefs = CONST_PARAM.get('LINK_HREFS')
        self.x_aim_crawl_page = CONST_PARAM.get('AIM_CRAWL_PAGE')

    # 将页面解析，返回当前页面信息
    def resolver_page(self) -> PageAttribute:
        response = self.response
        json_data = json.loads(response.text)
        page=json_data['page']
        content = page['content']

        largest_page = page['totalPages']
        page_size = page['pageSize']
        aim_crawl_page = page['pageNumber']
        url_list = [index['docpuburl'] for index in content]

        cur_latest_url = url_list[0]
        # 该位置必须实现
        # page_attribute 参数必须全部有值
        page_attribute = PageAttribute(largest_page, cur_latest_url, page_size, aim_crawl_page, url_list)
        return page_attribute
