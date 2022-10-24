import json
import re
import traceback

import requests
from scrapy import Selector

from BaseSpider.base_component.HtmlPageResolver import HtmlPageResolver
from BaseSpider.base_component.SubResolver import SubResolver
from BaseSpider.base_component.announcement_page_resolver import util

from BaseSpider.base_component.announcement_page_resolver.ZGZF_Annoucement import getValue
from BaseSpider.base_component.announcement_page_resolver.ZGZF_Annoucement.getValue import standardization, \
    unit_name_standardization
from BaseSpider.tool import DealDate
from BaseSpider.tool.param_tool import process_dict_call_GGZY, process_dict
from BaseSpider.tool.DealDate import get_one_time_from_str, stamp2time
from BaseSpider.tool.judge_tool.content_count import content_count



class CQDX_W(HtmlPageResolver):
    count_list = ['proj_name', 'call_unit', 'ancm_time', 'actual_price', 'proj_rel_p',
                  'proj_rel_m', 'agent_unit_name', 'agent_unit_address', 'agent_unit_p',
                  'agent_unit_m', 'sourse_url', 'bid_time', 'provide_unit', 'review_time',
                  'review_place', 'title', 'web_site', 'source_web_name']

    def resolver_page(self) -> dict:
        resp = json.loads(self.response_text)
        self.resp = resp
        try:
            title = resp.get('subject')
            if not title:
                return {}
            if re.search('意向|询价|流标|更正|变更|废标', title):
                return {}
            elif re.search(r'中标|成交|结果', title):
                content = standardization(self.getWBContent())
            else:
                return {}
            prov_dict = self.getProvideUnit(content)
            call_unit = {}
            new_page_attr = {'WB_G': content, 'code_dict': {}, 'at_dict': [], 'prov_dict': prov_dict,
                    'undefined_exp': [],
                    'experts': [], 'call_unit': call_unit, 'agent_unit': []}
            print(content)
            return new_page_attr

        except Exception:
            traceback.print_exc()
            return {}

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
        resp = self.resp

        proj_resp = requests.get('https://www.yuncaitong.cn/api/enquiry/' + resp.get('projectId'))
        proj = json.loads(proj_resp.text)

        content = process_dict('WB_G', {})

        content['proj_code'] = resp.get('projectCode')
        content['title'] = resp.get('subject')
        content['proj_name'] = resp.get('projectName')
        content['ancm_time'] = stamp2time(resp.get('createTime'))
        content['sourse_url'] = 'http://ztbzx.cqu.edu.cn/provider/#/publish/' + resp['id']
        content['web_site'] = 'http://ztbzx.cqu.edu.cn/'
        content['purchase_m'] = resp['projectTypeName']
        content['source_web_name'] = '重庆大学'
        content['region'] = '重庆市.沙坪坝区.重庆大学'
        content['call_unit'] = '重庆市重庆大学'
        content['call_unit_address'] = '重庆市沙坪坝区重庆大学'
        content['agent_unit_name'] = '重庆市重庆大学'
        content['agent_unit_address'] = '重庆市沙坪坝区重庆大学'

        content['provide_unit'] = proj.get('winBid').get('providerName')
        content['provide_address'] = ''
        content['actual_price'] = str(proj.get('winBid').get('price'))
        content['bid_time'] = stamp2time(resp.get('timeBegin'))
        content['bid_end_time'] = stamp2time(resp.get('timeEnd'))
        content['other_ex'] = '到货地址：' + proj.get('receiveAddress') + \
                              '到货时间要求：' + proj.get('receiveTimeHope') + \
                              '付款方式：' + proj.get('payWay')

        content['ancm_time'] = DealDate.get_one_time_from_str(content['ancm_time'])
        content['call_unit'] = getValue.unit_name_standardization(content['call_unit'])
        content['agent_unit_name'] = getValue.unit_name_standardization(content['agent_unit_name'])
        content['bid_time'] = DealDate.get_one_time_from_str(content['bid_time'])

        content['resolution_rate'] = '%.2f' % content_count(content, self.count_list)

        return content
