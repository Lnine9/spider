import json
import re
import math

from BaseSpider.base_component.PageResolver import PageResolver
from BaseSpider.base_component.entity.PageAttribute import PageAttribute

'''
必须定义的参数
'''
CONST_PARAM = {
    # 网址前缀
    'BASE_URL': 'http://www.ccgp-sichuan.gov.cn',
    # 当前最大网页
    'LARGEST_PAGE': '//div[@class="page-cell"]/div[1]/text()',
    # 当前网页最新URl
    'CUR_LATEST_URL': '//div[@class="info"]/ul/li[1]/a/@href',
    # URL列表XPATH路径
    'LINK_HREFS': '//div[@class="info"]/ul/li/a/@href',
    # 当前页面页码
    'AIM_CRAWL_PAGE': '//div[@class="page-cell"]/div[1]/text()',
}


class SC_Annouce_List_Resolver_CallBid(PageResolver):
    #  该init方法必须在子类（该类）实现
    """URL列表，起始页解析器"""

    def __init__(self):
        self.x_base_url = CONST_PARAM.get('BASE_URL')
        self.x_largest_page = CONST_PARAM.get('LARGEST_PAGE')
        self.x_cur_latest_url = CONST_PARAM.get('CUR_LATEST_URL')
        self.x_link_hrefs = CONST_PARAM.get('LINK_HREFS')
        self.x_aim_crawl_page = CONST_PARAM.get('AIM_CRAWL_PAGE')

    # 将页面解析，返回当前页面信息
    def resolver_page(self) -> PageAttribute:
            """
            通过设置的位置提取当前页的信息并返回
            :return: 当前页面的信息   最大页，最新页网址，页面大小，当前页 ，公告URL列表，
            """
            try:
                page = self.response.xpath(self.x_largest_page).get()
                largest_page = int(page.split("/")[1].replace("页",""))
                aim_crawl_page =(page.split("/")[0]).split("：")[1]

            except:
                return PageAttribute(0, "", 0, int(0), [])
            cur_latest_url = self.response.xpath(self.x_cur_latest_url).get()
            if "http" in cur_latest_url or "202.61.88.152:8006" in cur_latest_url :
                cur_latest_url = cur_latest_url
            else:
                cur_latest_url = 'http://www.ccgp-sichuan.gov.cn' + self.response.xpath(self.x_cur_latest_url).get()
            link_hrefs = self.response.xpath(self.x_link_hrefs)
            url_list = []

            page_size = 0
            for each in link_hrefs:
                page_size += 1
                act_url = each.get()
                if "http" in act_url or "202.61.88.152:8006" in act_url:
                    act_url = act_url
                else:
                    act_url = 'http://www.ccgp-sichuan.gov.cn' + each.get()
                url_list.append(act_url)

            # 该位置必须实现
            # page_attribute 参数必须全部有值
            page_attribute = PageAttribute(largest_page, cur_latest_url, page_size, int(aim_crawl_page), url_list)
            return page_attribute

            # 正则匹配数字数组，并筛选出最后一个元素

    @staticmethod
    def get_largest_page(str_temp) -> str:
        return re.findall(r"\d+\.?\d*", str_temp)[-1]


