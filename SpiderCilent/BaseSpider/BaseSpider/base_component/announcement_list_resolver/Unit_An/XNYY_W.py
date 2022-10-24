from BaseSpider.base_component.PageResolver import PageResolver
from BaseSpider.base_component.entity.PageAttribute import PageAttribute
from BaseSpider.tool.DealDate import get_one_time_from_str
import json
import re

class XNYY_W(PageResolver):

    def __init__(self):
        self.url_prefix = 'http://www.xnyy.cn/'

    def resolver_page(self) -> PageAttribute:
        resp = self.response

        largest_page = resp.xpath("//span[@class='p_no'][last()]/a/text()").extract_first()
        aim_crawl_page = resp.xpath("//span[@class='p_no_d']/text()").extract_first()

        url_list = resp.xpath("//a[@class='fr']/@href").extract()
        titles = resp.xpath("//p[@class='no-wrap']/text()").extract()
        cur_latest_url = url_list[0]

        for i, v in enumerate(titles):
            if not i == 0 and (not re.search(r'中标|成交|结果', v) or re.search('意向|询价|流标|更正|变更|废标', v)):
                url_list[i] = None

        url_list = list(self.url_prefix + u.replace('../', '') for u in url_list if u)
        days = resp.xpath("//div[@class='list-time fl']/p/text()").extract()
        yms = resp.xpath("//div[@class='list-time fl']/span/text()").extract()
        newest_time = get_one_time_from_str(yms[0] + '-' + days[0])
        oldest_time = get_one_time_from_str(yms[-1] + '-' + days[-1])
        page_size = len(url_list)
        # 该位置必须实现
        # page_attribute 参数必须全部有值
        page_attribute = PageAttribute(int(largest_page), cur_latest_url, int(page_size), int(aim_crawl_page), url_list,
                                       newest_time,
                                       oldest_time)
        print(aim_crawl_page, newest_time, oldest_time, largest_page)
        return page_attribute

