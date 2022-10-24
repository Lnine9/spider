import re

import BaseSpider.base_component.announcement_sub_resolver.GGZY_Announcement.util as util
from BaseSpider.base_component.SubResolver import SubResolver
from BaseSpider.tool import DealDate
from BaseSpider.tool.DealDate import get_one_time_from_str
from BaseSpider.tool.param_tool import process_dict
import BaseSpider.base_component.announcement_page_resolver.ZGZF_Annoucement.getValue as getValue
from BaseSpider.tool.judge_tool.content_count import content_count
import traceback


class GGZY_WinBid_sub_component1(SubResolver):
    count_list = ['proj_name', 'call_unit', 'ancm_time', 'actual_price', 'proj_rel_p',
                  'proj_rel_m', 'agent_unit_name', 'agent_unit_address', 'agent_unit_p',
                  'agent_unit_m', 'sourse_url', 'bid_time', 'provide_unit', 'review_time',
                  'review_place', 'title', 'web_site', 'source_web_name']

    def resolver_page(self) -> dict:
        response = self.response_text.response.body.decode('utf-8')
        html_list = util.parseHtml_list(response)

        item = util.parse2dict(html_list)

        dict_title = util.parse2dict_title(html_list)

        content = process_dict('WB_G', item)

        content['source_web_name'] = '公共资源交易平台'
        content['title'] = self.response_text.xpath('//h4[@class="h4_o"]/text()').extract_first()
        content['proj_name'] = re.sub('(?:中标|结果|公示|公告).*$', '', content['title'])
        content['ancm_time'] = get_one_time_from_str(
            self.response_text.xpath('//p[@class="p_o"]//span[1]/text()').extract_first())
        content['proj_item'] = '政府采购'
        content['sourse_url'] = self.response_url
        content['web_site'] = 'http://deal.ggzy.gov.cn/'
        content['purchase_m'] = '公开招标'

        content['proj_code'] = util.search_code(html_list)
        if (content['proj_code'] == ''):
            content['proj_code'] = self.get_info(html_list, '项目', '编号')
        content['provide_unit'] = self.get_info(html_list, '供应商', '名称')
        content['provide_address'] = self.get_info(html_list, '供应商', '地址')
        content['actual_price'] = self.get_info(html_list, '中标', '金额')
        ex = self.response_text.xpath('//label[@id="platformName"]/text()').extract_first()
        content['region'] = util.get_region_from_str(content['title'], ex)

        content.update(util.process_callbid_file(dict_title))
        content.update(util.process_callbid_tender(dict_title))
        content.update(util.process_callbid_open(dict_title))
        content.update(util.process_callbid_other_ex(dict_title))
        content.update(util.process_callbid_money(dict_title))
        content.update(util.process_callbid_contact(dict_title))

        content['ancm_time'] = DealDate.get_one_time_from_str(content['ancm_time'])
        content['call_unit'] = getValue.unit_name_standardization(content['call_unit'])
        content['agent_unit_name'] = getValue.unit_name_standardization(content['agent_unit_name'])
        content['bid_time'] = DealDate.get_one_time_from_str(content['bid_time'])

        content['resolution_rate'] = '%.2f' % content_count(content, self.count_list)

        try:
            prov_dict = self.getProvideUnit(content)
            at_dict = self.get_attach(self.response_text)
            experts = self.getExpert()
            call_unit = self.getCallBidUnit(content)
            agent_unit = self.getAgentUnit(content)
        except Exception:
            traceback.print_exc()
            return {'WB_G': content, 'code_dict': {}, 'at_dict': [], 'prov_dict': [], 'undefined_exp': [],
                    'experts': [], 'call_unit': {}, 'agent_unit': []}
        else:
            return {'WB_G': content, 'code_dict': {}, 'at_dict': at_dict, 'prov_dict': prov_dict,
                    'undefined_exp': [],
                    'experts': [], 'call_unit': call_unit, 'agent_unit': []}

    def get_attach(self, response_text):
        file_name_list = response_text.xpath("//a[not(text()='原文链接地址')]/text()").extract()
        file_url_list = response_text.xpath("//a[not(text()='原文链接地址')]/@href").extract()

        at_dict = []
        for i in range(len(file_url_list)):
            item = {'url': file_url_list[i],
                    'file_name': file_name_list[i],
                    'file_type': file_name_list[i][file_name_list[i].rfind('.') + 1:],
                    'file_size': -1,
                    'local_path': '暂无'}
            at_dict.append(item)
        return at_dict

    def getProvideUnit(self, content):
        agent_unit = []
        provide_unit = []
        provide_address = []

        if content['provide_unit']:
            provide_unit = content['provide_unit'].split('，')
        if content['provide_address']:
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

    '''
    获取专家
    '''

    def getExpert(self):
        return []

    '''
    获取采购机构
    '''

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

    '''
    获取代理机构
    '''

    def getAgentUnit(self, content):
        agent_unit = []
        item = {}
        item['code'] = content['agent_unit_name']
        item['name'] = content['agent_unit_name']
        item['address'] = content['agent_unit_address']
        if item['name'] and item['address']:
            agent_unit.append(item)
        return agent_unit

    def get_info(self, lis, str1, str2):
        try:
            for index in range(len(lis)):
                lis[index] = lis[index].strip()
                if re.search(str1, lis[index]) and re.search(str2, lis[index]):
                    if re.search(':|\s', lis[index]) and re.search(str2 + '[^\u4e00-\u9fa5\w\d]*([\u4e00-\u9fa5\w\d]*)',
                                                                   lis[index]).group(1):
                        return re.findall(str2 + '[：:\s]*\s+([^\n]*)', lis[index])[0]

                    if index + 1 < len(lis):
                        return lis[index + 1]
        except Exception:
            return ''
        return ''
