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
from BaseSpider.tool.param_tool import process_dict_call_GGZY, process_dict
from BaseSpider.tool.DealDate import get_one_time_from_str
from BaseSpider.tool.judge_tool.content_count import content_count



class XQYY_W(HtmlPageResolver):
    count_list = ['proj_name', 'call_unit', 'ancm_time', 'actual_price', 'proj_rel_p',
                  'proj_rel_m', 'agent_unit_name', 'agent_unit_address', 'agent_unit_p',
                  'agent_unit_m', 'sourse_url', 'bid_time', 'provide_unit', 'review_time',
                  'review_place', 'title', 'web_site', 'source_web_name']

    def resolver_page(self) -> dict:
        resp = Selector(text=self.response_text)
        self.resp = resp
        try:
            title = resp.xpath("//table//table[1]//td[1][contains(text(),'公告')]").extract_first()
            if not title:
                return {}
            if re.search('意向|询价|流标|更正|变更|废标', title):
                return {}
            elif re.search(r'中标|成交|结果', title):
                content = standardization(self.getWBContent())
            else:
                return {}
            prov_dict = self.getProvideUnit(content)
            call_unit = self.getCallBidUnit(content)
            new_page_attr = {'WB_G': content, 'code_dict': {}, 'at_dict': [], 'prov_dict': prov_dict,
                    'undefined_exp': [],
                    'experts': [], 'call_unit': call_unit, 'agent_unit': []}
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


    def getProvideUnit(self, content):
        agent_unit = []
        provide_unit = []
        provide_address = []

        if 'provide_unit' in content and content['provide_unit']:
            provide_unit = content['provide_unit'].split('，')
        if 'provide_address' in content and content['provide_address']:
            provide_address = content['provide_address'].split('，')

        # 对列表去重，并保持原顺序
        removal_provide_unit = list(set(provide_unit))
        removal_provide_unit.sort(key=provide_unit.index)
        removal_provide_address = list(set(provide_address))
        removal_provide_address.sort(key=provide_address.index)

        if len(removal_provide_unit) == len(removal_provide_address):
            for i in range(len(removal_provide_unit)):
                # 供应商名称、地址不包含或不等于某些特定字符
                regex = re.compile(r'(^无$|^null$|^/$|^-$|^——$|^--$|.*详见.*|.*见附件.*|)')
                if removal_provide_unit[i] is not None and removal_provide_unit[i] is not None and \
                        regex.match(removal_provide_unit[i]) == '' and regex.match(removal_provide_address[i]) == '':
                    item = {'code': removal_provide_unit[i],
                            'name': removal_provide_unit[i],
                            'address': removal_provide_address[i]}
                    agent_unit.append(item)
        return agent_unit

    def getWBContent(self):
        resp = self.resp.xpath("//table//table[1]//td[1][contains(text(),'公告')]/../../../../td")
        html_list = util.parseHtml_list(resp.get(0))

        item = util.parse2dict(html_list)

        dict_title = util.parse2dict_title_with_dig(html_list)

        content = process_dict('WB_G', item)

        content.update(util.process_callbid_other_ex(dict_title))
        content.update(util.process_contact_simple(dict_title))
        content.update(util.process_winbid_common_GCJS(html_list))

        content['title'] = self.resp.xpath("//table//table[1]//td[1][contains(text(),'公告')]/text()").extract_first()
        content['proj_name'] = re.sub(r'采购结果|中标公告|成交公告|成交|结果|公告', '', content['title'])
        content['proj_item'] = ''
        content['ancm_time'] = get_one_time_from_str(
            resp.xpath(".//td[starts-with(text(),'发布时间')]/text()").extract_first())
        content['sourse_url'] = self.response_url
        content['web_site'] = 'http://www.xqhospital.com.cn/'

        content['purchase_m'] = content['purchase_m'] if content['purchase_m'] else '公开招标'
        content['source_web_name'] = '新桥医院'
        content['region'] = '重庆市.沙坪坝区'
        content['call_unit'] = '重庆市新桥医院'
        content['call_unit_address'] = '重庆市沙坪坝区新桥医院'
        content['agent_unit_name'] = '重庆市新桥医院'
        content['agent_unit_address'] = '重庆市沙坪坝区新桥医院'

        content['proj_code'] = util.search_code(html_list)
        content['provide_unit'] = util.find_in_list(html_list, '供应商：(.+(?:公司))')
        content['provide_address'] = ''
        content['actual_price'] = util.find_in_list(html_list, '报价：(.+(?:元))')
        content['purchase_m'] = util.find_in_list(html_list, '采购方式：(.{0,6})')


        content['ancm_time'] = DealDate.get_one_time_from_str(content['ancm_time'])
        content['call_unit'] = getValue.unit_name_standardization(content['call_unit'])
        content['agent_unit_name'] = getValue.unit_name_standardization(content['agent_unit_name'])
        content['bid_time'] = DealDate.get_one_time_from_str(content['bid_time'])

        content['resolution_rate'] = '%.2f' % content_count(content, self.count_list)

        return content
