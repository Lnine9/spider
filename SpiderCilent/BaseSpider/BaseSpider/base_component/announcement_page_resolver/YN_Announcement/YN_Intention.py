import json
import traceback
from datetime import datetime

from scrapy import Selector
import cpca
import re
import requests
import time as t
from BaseSpider.tool.DealDate import get_one_time_from_str
from BaseSpider.base_component.HtmlPageResolver import HtmlPageResolver


class YN_Intention(HtmlPageResolver):

    def resolver_page(self) -> dict:
        content = {
            'province': None, 'city': None, 'region': None, 'level': None, 'call_unit': None, 'purchase_unit': None,
            'title': None, 'acnm_time': None, 'total_budget': None, 'source_website': None, 'source_url': None
        }
        details = []
        page_attr = {}
        try:
            id = re.search(r'sys_purchaseintention_id=(.+)$', self.response_url).group(1)
            url = 'http://www.yngp.com/governmentpolicy.do?method=viewPurchaseInfoA&R='+str(t.time())
            headers = {
                "accept": "*/*",
                "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                "cache-control": "no-cache",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "pragma": "no-cache",
                "useajaxprep": "true",
                "x-requested-with": "XMLHttpRequest",
                "cookie": "__jsluid_h=894825045bc96a0da689b83642f0566c; "
                          "CoreSessionId=ea3ac91f2a15cd4847ed3c4d09b1582e953c1b785bc917bc; "
                          "_g_sign=dd04ac280bb9008ae1c76b96ffa54046; elvasid=799246ff8823967b3b5bfa435e85bc98; "
                          "xincaigou=49737.2918.1072.0000; "
                          "JSESSIONID=yubMPzH33QyTuC4t66D-Hm15LCbiFi-DTlfF-EFVq_qyhOrKwQPf!809653513",
                "Referer": "http://www.yngp.com/governmentpolicy.do?method=viewPurchaseInfo&sys_purchaseintention_id={}".format(id),
                "Referrer-Policy": "strict-origin-when-cross-origin",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44 "
            }
            data = requests.post(url, {'sys_purchaseintention_id': id}, headers=headers)
            data = json.loads(data.text)
            resp = Selector(text=data['opcontent'])
            content['title'] = resp.xpath("//div[@class='divcss5']/h2/b/text()").get().strip()
            content['source_website'] = '云南省政府采购系统'
            content['source_url'] = self.response_url
            content['province'] = '云南省'
            content['city'] = cpca.transform([content['title']]).loc[0, "市"]
            content['region'] = cpca.transform([content['title']]).loc[0, "区"]
            if content['region']:
                content['level'] = 3
            elif content['city']:
                content['level'] = 2
            else:
                content['level'] = 1
            content['call_unit'] = resp.xpath("(//div[@class='divcss5']//table[2]//font)[1]/text()").get().strip()
            content['purchase_unit'] = resp.xpath("(//div[@class='divcss5']//table[2]//font)[1]/text()").get().strip()
            content['acnm_time'] = get_one_time_from_str(resp.xpath("//table[2]//tr[3]//td//text()").get())

            ds = resp.xpath("//div[@class='divcss5']//table[1]//tr")
            total_budget = 0
            index = 1
            for item in ds:
                if index == 1:
                    index += 1
                    continue
                detail = {'proj_name': item.xpath("./td[2]/font/text()").get().strip(),
                          'survey': item.xpath("./td[3]/font/text()").get().strip()}
                money = item.xpath("./td[4]/font/text()").get().strip()
                total_budget += float(money)
                detail['budget'] = money
                time = item.xpath("./td[5]/font/text()").get().strip()
                if '日' not in time:
                    time += '01日'
                detail['purchase_time'] = get_one_time_from_str(time)
                detail['other'] = item.xpath("./td[6]/font/text()").get().strip()
                details.append(detail)

            content['total_budget'] = '{:.2f}'.format(total_budget)

            page_attr = {'I_G': content, 'details': details}
        except Exception as e:
            traceback.print_exc()

        return page_attr
