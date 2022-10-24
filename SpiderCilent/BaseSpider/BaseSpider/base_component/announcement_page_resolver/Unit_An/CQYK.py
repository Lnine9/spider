import re
import traceback

from scrapy import Selector

from BaseSpider.base_component.HtmlPageResolver import HtmlPageResolver
from BaseSpider.base_component.SubResolver import SubResolver
from BaseSpider.base_component.announcement_page_resolver import util

from BaseSpider.base_component.announcement_page_resolver.ZGZF_Annoucement import getValue
from BaseSpider.base_component.announcement_page_resolver.ZGZF_Annoucement.getValue import standardization, \
    unit_name_standardization
from BaseSpider.tool import DealDate
from BaseSpider.tool.param_tool import process_dict_call_GGZY
from BaseSpider.tool.DealDate import get_one_time_from_str
from BaseSpider.tool.judge_tool.content_count import content_count



class CQYK(HtmlPageResolver):
    content = {"proj_name": None, "proj_code": None, "proj_item": None, "call_unit": None,
               "region": None, "ancm_time": None, "budget": None, "proj_rel_p": None,
               "proj_rel_m": None, "agent_unit_p": None, "agent_unit_m": None, "tender_place": None,
               "bid_sale_m": None, "bid_sale_op_time": None, "bid_sale_en_time": None,
               "bid_sale_place": None, "bid_price": None, "bid_place": None, "other_ex": None,
               "purchase_m": None, "sourse_url": None, "bid_time": None, "title": None,
               "agent_unit_name": None, "agent_unit_address": None, "purchasing_unit_name": None,
               "call_unit_address": None,

               'web_site': '', 'source_web_name': ''
               }
    count_list = ['proj_name', 'call_unit', 'ancm_time', 'budget', 'proj_rel_p', 'proj_rel_m', 'agent_unit_name',
                  'agent_unit_address', 'agent_unit_p', 'agent_unit_m', 'tender_place', 'bid_sale_m',
                  'bid_sale_op_time', 'bid_sale_en_time', 'bid_sale_place', 'bid_price', 'sourse_url', 'bid_time',
                  'title', 'web_site', 'source_web_name']

    def resolver_page(self) -> dict:
        resp = Selector(text=self.response_text)
        self.resp = resp
        try:
            main = resp.xpath("//div[@class='v_news_content']/p[1]/text()").extract_first()
            if re.search('详见附件', main):
                return {}

            title = resp.xpath("//div[@class='contsed']//h3/text()").extract_first()
            content = None
            if not title:
                return {}
            if re.search('意向|询价|流标|更正|变更|废标', title):
                return {}
            elif re.search(r'招标|采购公告', title):
                content = standardization(self.getCBContent())
            elif re.search(r'中标|成交|结果', title):
                content = standardization(self.getWBContent())
            else:
                return {}
            code_dict = self.getCodeHtml()
            at_dict = self.get_attach(self.resp)
            call_unit = self.getCallBidUnit(content)
            new_page_attr = {'CB_G': content, 'code_dict': code_dict, 'at_dict': at_dict, 'call_unit': call_unit}
            print(content)
            return new_page_attr

        except Exception:
            traceback.print_exc()
            return {}

    def getCallBidUnit(self, content):
        call_unit = {}
        if 'call_unit' in content and not content['call_unit'] == '':
            call_unit['name'] = content['call_unit']
            call_unit['code'] = content['call_unit']
        else:
            return {}
        if 'call_unit_address' in content and not content['call_unit_address'] == '':
            call_unit['address'] = content['call_unit_address']
        else:
            return {}

        return call_unit

    def getCodeHtml(self):
        code_dict = {}

        code_dict['url'] = self.response_url
        code_dict['file_type'] = self.response_url[self.response_url.rfind('.') + 1:]
        code_dict['file_size'] = '-1'
        code_dict['local_path'] = '暂无'
        code_dict['code'] = self.resp.xpath("//div[@class='contsed']").get(0)

        return code_dict

    def getCBContent(self):
        resp = self.resp.xpath("//div[@class='contsed']")

        text = resp.get(0)
        html_list = util.parseHtml_list(text)
        item = util.parse2dict(html_list)
        dict_title = util.parse2dict_title_with_dig(html_list)

        content = process_dict_call_GGZY(item)
        content.update(util.process_callbid_file(dict_title))
        content.update(util.process_callbid_tender(dict_title))
        content.update(util.process_callbid_open(dict_title))
        content.update(util.process_callbid_other_ex(dict_title))
        content.update(util.process_callbid_money(dict_title))
        content.update(util.process_contact_simple(dict_title))

        content['proj_code'] = util.search_code(html_list)

        content['proj_rel_p'] = util.find_in_list(html_list, '联系人.+?([\u4e00-\u9fa5](?:老师))')
        content['proj_rel_m'] = util.find_in_list(html_list, '联系人.+?([\d\-]+)')

        # 复杂数据获取
        content['title'] = self.resp.xpath("//div[@class='contsed']//h3/text()").extract_first()
        content['proj_name'] = re.sub(r'招标公告|采购公告|公告', '', content['title'])
        content['proj_item'] = ''
        content['ancm_time'] = get_one_time_from_str(resp.xpath(".//div[@class='addtime']/span[1]/text()").extract_first())
        content['sourse_url'] = self.response_url
        content['web_site'] = 'https://www.hospital-cqmu.com/'
        content['purchase_m'] = content['purchase_m'] if content['purchase_m'] else '公开招标'
        content['source_web_name'] = '重庆医科大学附属第一医院'
        content['region'] = '重庆市.渝中区.重庆医科大学附属第一医院'
        content['call_unit'] = '重庆市重庆医科大学附属第一医院'
        content['call_unit_address'] = '重庆市渝中区重庆医科大学附属第一医院'
        content['agent_unit_name'] = '重庆市重庆医科大学附属第一医院'
        content['agent_unit_address'] = '重庆市渝中区重庆医科大学附属第一医院'

        # 数据格式修改
        content['call_unit'] = unit_name_standardization(content['call_unit'])
        content['agent_unit_name'] = unit_name_standardization(content['agent_unit_name'])
        content['bid_sale_op_time'] = DealDate.get_one_time_from_str(content['bid_sale_op_time'])
        content['bid_sale_en_time'] = DealDate.get_one_time_from_str(content['bid_sale_en_time'])
        content['bid_time'] = DealDate.get_one_time_from_str(content['bid_time'])
        content['bid_end_time'] = DealDate.get_one_time_from_str(content['bid_end_time'])
        content['bid_price'] = getValue.change_money(content['bid_price'])
        content['budget'] = getValue.change_money(content['budget'])

        content['resolution_rate'] = '%.2f' % content_count(content, self.count_list)

        return content

    def getWBContent(self):
        return {}

    '''
    获取附件信息
    '''

    def get_attach(self, response_text):
        return []
