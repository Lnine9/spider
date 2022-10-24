import re

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
    'CUR_LATEST_URL': '/html/body//*[@class="vT-srch-result-list-bid"]/li[1]/a/@href',
    # URL列表XPATH路径
    'LINK_HREFS': '/html/body//*[@class="vT-srch-result-list-bid"]/li/a/@href',
    # 当前页面页码
    'AIM_CRAWL_PAGE': '',
}


class ZGZFDishonestListResolver(PageResolver):
    #  该init方法必须在子类（该类）实现
    def __init__(self):
        self.x_base_url = CONST_PARAM.get('BASE_URL')
        self.x_largest_page = CONST_PARAM.get('LARGEST_PAGE')
        self.x_cur_latest_url = CONST_PARAM.get('CUR_LATEST_URL')
        self.x_link_hrefs = CONST_PARAM.get('LINK_HREFS')
        self.x_aim_crawl_page = CONST_PARAM.get('AIM_CRAWL_PAGE')

    # 将页面解析，返回当前页面信息
    def resolver_page(self) -> PageAttribute:
        trs = self.response.xpath('//table[@id="tableInfo"]//tr[@class="trShow"]')
        url_list = []
        for tr in trs:
            name = tr.xpath('.//td[2]//text()').get()
            url_id = re.findall('\'.+\'', tr.xpath('.//td[2]/a[@onclick]/@onclick').get())[0].replace("'", '')
            ann_time = tr.xpath('.//td[9]//text()').get()
            url_list.append('http://www.ccgp.gov.cn/cr/list/detail?id=' + url_id)
        largest_page = self.response.xpath('//*[@id="totalPag"]//text()').get()
        aim_crawl_page = self.response.xpath('//*[@id="gp"]/@value').get()
        cur_latest_url = url_list[0]

        page_attribute = PageAttribute(int(largest_page), cur_latest_url, len(url_list), aim_crawl_page, url_list)
        return page_attribute
