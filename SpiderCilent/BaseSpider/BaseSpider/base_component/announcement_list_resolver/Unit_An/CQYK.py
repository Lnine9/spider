from BaseSpider.base_component.PageResolver import PageResolver
from BaseSpider.base_component.entity.PageAttribute import PageAttribute
from BaseSpider.tool.DealDate import get_one_time_from_str
import json
import re

class CQYK(PageResolver):

    def __init__(self):
        self.url_prefix = 'https://www.hospital-cqmu.com/'

    def resolver_page(self) -> PageAttribute:
        resp = self.response

        largest_page = resp.xpath("(//a[@href='zbgg1/1.htm'])[1]/text()").extract_first()
        aim_crawl_page = resp.xpath("//span[@class='p_no_d']/text()").extract_first()

        url_list = resp.xpath("//div[@class='lists']//ul/li/a/@href").extract()
        url_list = list(self.url_prefix + u.replace('../', '') for u in url_list)
        cur_latest_url = url_list[0]
        time_list = resp.xpath("//div[@class='areds']/span[1]/text()").extract()
        newest_time = get_one_time_from_str(time_list[0])
        oldest_time = get_one_time_from_str(time_list[-1])
        page_size = len(url_list)
        # 该位置必须实现
        # page_attribute 参数必须全部有值
        page_attribute = PageAttribute(int(largest_page), cur_latest_url, int(page_size), int(aim_crawl_page), url_list,
                                       newest_time,
                                       oldest_time)
        print(aim_crawl_page, newest_time, oldest_time, largest_page)
        return page_attribute

