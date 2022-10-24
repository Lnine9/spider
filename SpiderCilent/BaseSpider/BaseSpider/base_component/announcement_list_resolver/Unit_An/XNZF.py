from BaseSpider.base_component.PageResolver import PageResolver
from BaseSpider.base_component.entity.PageAttribute import PageAttribute
from BaseSpider.tool.DealDate import get_one_time_from_str
import json
import re

class XNZF(PageResolver):

    def __init__(self):
        self.url_prefix = 'https://jhc.swupl.edu.cn/tzgg/'

    def resolver_page(self) -> PageAttribute:
        resp = self.response

        largest_page = resp.xpath("(//a[contains(text(),'最后页')])[1]/@href").extract_first()
        largest_page = re.search(r'index(\d+).htm', largest_page).group(1)
        largest_page = int(largest_page) + 1
        aim_crawl_page = resp.xpath("//div[@class='page']//font[@color='red']/text()").extract_first()

        url_list = resp.xpath("//div[@class='articleList articleList2']//a/@href").extract()
        titles = resp.xpath("//div[@class='articleList articleList2']//a/text()").extract()
        cur_latest_url = url_list[0]

        for i, v in enumerate(titles):
            if not i == 0 and (not re.search(r'招标|采购公告', v) or re.search('意向|询价|流标|更正|变更|废标', v)):
                url_list[i] = None

        url_list = list(self.url_prefix + u for u in url_list if u)
        time_list = resp.xpath("//div[@class='articleList articleList2']//li/span/text()").extract()
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



