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
from BaseSpider.tool.param_tool import process_dict_call_GGZY
from BaseSpider.tool.DealDate import get_one_time_from_str, stamp2time
from BaseSpider.tool.judge_tool.content_count import content_count



class CQDX(HtmlPageResolver):
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
        resp = json.loads(self.response_text)
        self.resp = resp
        try:
            title = resp['subject']
            if not title:
                return {}
            if re.search('意向|询价|流标|更正|变更|废标', title):
                return {}
            elif re.search(r'招标|采购公告', title):
                content = standardization(self.getCBContent())
            else:
                return {}
            new_page_attr = {'CB_G': content, 'code_dict': {}, 'at_dict': [], 'call_unit': self.getCallBidUnit(content)}
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

    def getCBContent(self):
        resp = self.resp
        proj_resp = requests.get('https://www.yuncaitong.cn/api/enquiry/' + resp.get('projectId'))
        proj = json.loads(proj_resp.text)

        content = self.content

        content['proj_code'] = resp['projectCode']
        content['title'] = resp['subject']
        content['proj_name'] = resp['projectName']
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
        content['budget'] = str(proj.get('budget'))
        content['bid_time'] = stamp2time(resp.get('timeBegin'))
        content['bid_end_time'] = stamp2time(resp.get('timeEnd'))
        content['other_ex'] = '到货地址：'+proj.get('receiveAddress') +\
                              '到货时间要求：' + proj.get('receiveTimeHope') +\
                              '付款方式：' + proj.get('payWay')




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
