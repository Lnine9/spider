import re


from ..PageResolver import PageResolver
from ..entity.PageAttribute import PageAttribute

'''
必须定义的参数
'''
CONST_PARAM = {
    # 网址前缀
    'BASE_URL': 'http://www.ccgp-guizhou.gov.cn',
    # 当前最大网页
    'LARGEST_PAGE': '/html/body/div[3]/div[2]/div[2]/div[3]/ul/li[13]/a',
    # 当前网页最新URl
    'CUR_LATEST_URL': '/html/body/div[3]/div[2]/div[2]/div[2]/div[2]/ul/li[1]/a/@href',
    # URL列表XPATH路径
    'LINK_HREFS': '//div[@class="xnrx"]/ul/li/a/@href',
    # 当前页面页码
    'AIM_CRAWL_PAGE': '/html/body/div[3]/div[2]/div[2]/div[3]/ul/li[13]/a/input[1]/@value',
}


class TestFPResolver(PageResolver):
    #  该init方法必须在子类（该类）实现
    def __init__(self):
        self.x_base_url = CONST_PARAM.get('BASE_URL')
        self.x_largest_page = CONST_PARAM.get('LARGEST_PAGE')
        self.x_cur_latest_url = CONST_PARAM.get('CUR_LATEST_URL')
        self.x_link_hrefs = CONST_PARAM.get('LINK_HREFS')
        self.x_aim_crawl_page = CONST_PARAM.get('AIM_CRAWL_PAGE')

    # 将页面解析，返回当前页面信息
    def resolver_page(self) -> PageAttribute:
        largest_page = self.response.xpath(self.x_largest_page).get()
        largest_page = int(self.get_largest_page(largest_page))
        cur_latest_url = CONST_PARAM.get('BASE_URL') + self.response.xpath(self.x_cur_latest_url).get()
        aim_crawl_page = int(self.response.xpath(self.x_aim_crawl_page).get())

        link_hrefs = self.response.xpath(self.x_link_hrefs)
        url_list = []

        page_size = 0
        for each in link_hrefs:
            page_size += 1
            act_url = CONST_PARAM.get('BASE_URL') + each.get()
            url_list.append(act_url)

        # 该位置必须实现
        # page_attribute 参数必须全部有值
        page_attribute = PageAttribute(largest_page, cur_latest_url, page_size, aim_crawl_page, url_list)
        return page_attribute

    # 正则匹配数字数组，并筛选出最后一个元素
    @staticmethod
    def get_largest_page(str_temp) -> str:
        return re.findall(r"\d+\.?\d*", str_temp)[-1]


