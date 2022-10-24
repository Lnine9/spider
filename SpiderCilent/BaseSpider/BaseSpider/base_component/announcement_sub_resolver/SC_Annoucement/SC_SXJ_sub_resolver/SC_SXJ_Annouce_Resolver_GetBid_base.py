# -*- coding: UTF-8 -*-
import re

from BaseSpider.base_component.SubResolver import SubResolver
from BaseSpider.base_component.announcement_page_resolver.SC_Annoucement.tool.tool import *

'''中标'''
CONST_PARAM = {
    # 公告标题参数
    'TITLE': '//*[@id="tab-503"]/div/div[2]/div/div/h2/text()',
    'attachments': '//a[@class="attachUrl"]/@href'
}


class SC_SXJ_Annouce_Resolver_GetBid_base(SubResolver):
    """公告页请求解析器"""
    timePattern2 = re.compile(
        "(((\d{4})-(0[13578]|1[02])-(0[1-9]|[12]\d|3[01]))|((\d{4})-(0[469]|11)-(0[1-9]|[12]\d|30))|((\d{4})-(02)-(0[1-9]|1\d|2[0-8]))|((\d{2}(0[48]|[2468][048]|[13579][26]))-(02)-(29))|(((0[48]|[2468][048]|[13579][26])00)-(02)-(29)))")

    def __init__(self):
        self.content = {"title": None, "proj_name": None, "proj_code": None, "call_unit": None,
               "ancm_time": None, "agent_unit_p_m": None, "proj_rel_p": None, "proj_rel_m": None,
               "region": None, "purchase_m": None, "actual_price": None, "provide_unit": None,
               "other_ex": None, "review_place": "无", 'source_web_name': "四川省政府采购网",
               "web_site": "http://www.ccgp-sichuan.gov.cn/view/srplatform/portal/index.html",
               "agent_unit_address": "", "agent_unit_name": "", "call_unit_address": ""}

    def resolver_page(self) -> dict:

        allTd = self.response_text.xpath('//*[@id="myPrintArea"]/table//tr/td')
        resultTd = []
        for td in allTd:
            result = td.xpath('string(.)').get()
            if result != "免责申明：以下信息由采购人或代理机构发布，信息的真实性、合法性、有效性由采购人或代理机构负责。":
                resultTd.append(result)

        messageDict = {}
        for index, td in enumerate(resultTd):
            allTd[index] = ''.join(td.split()).encode(encoding="utf-8")
            if td == '' or td is None:
                td = "无"

        keys = resultTd[0: len(allTd): 2]
        values = resultTd[1: len(allTd): 2]
        for i in range(len(keys) - 1):
            key = ''.join(keys[i].split())
            if "时间" not in keys[i] and "日期" not in keys[i]:
                value = ''.join(values[i].split())
            else:
                value = values[i]
            messageDict.update({key: value})

        try:
            content = self.getCallBidGovernment(messageDict)
            code_dict = getCodeHtml(self.response_text)
            at_dict = getAttachment(self.response_text)
            prov_dict = getProvideUnit(messageDict, "中标供应商信息")
            undefined_exp = getUndefinedExp(messageDict, "评标委员会成员名单")
            experts = getExpert()
            call_unit = getCallBidUnit(messageDict)
            agent_unit = getAgentUnit(messageDict, 1)
            new_page_attr = {'WB_G': content, 'code_dict': {}, 'at_dict': [],
                             'prov_dict': [], 'undefined_exp': [], 'experts': [],
                             'call_unit': call_unit, 'agent_unit': agent_unit}
            self.page_attr.update(new_page_attr)
            return new_page_attr
        except:
            return self.page_attr

    def getCallBidGovernment(self, messageDict):

        self.content["sourse_url"] = self.response_url
        self.content["title"] = self.response_text.xpath('/html/body/div[2]/div[2]/h1/text()').get()
        self.content["proj_name"] = messageDict.get("采购项目名称", None)
        self.content["proj_code"] = messageDict.get("采购项目编号", None)
        self.content["call_unit"] = messageDict.get("采购人", None)
        self.content["agent_unit_address"] = messageDict.get("代理机构地址", None)
        self.content["ancm_time"] = trans_time(
            self.response_text.xpath('/html/body/div[2]/div[2]/p/text()').get().split("：")[1])
        self.content["region"] = messageDict.get("行政区划", None)
        if self.content['region'] is None or self.content["region"] == "":
            self.content["region"] = messageDict.get("行政区域", "四川市县级")
        self.content["aget_unit_address"] = messageDict.get("代理机构地址", None)
        self.content["agent_unit_name"] = messageDict.get("代理机构", None)
        self.content["call_unit_address"] = messageDict.get("采购人地址", None)
        if self.content["agent_unit_name"] is None:
            self.content["agent_unit_name"] = messageDict.get("采购代理机构名称", None)
        # 形式一
        self.content["agent_unit_p"] = messageDict.get("代理机构联系人", None)
        self.content["agent_unit_m"] = messageDict.get("代理机构联系电话", None)

        # 形式二，无法解析时返回原始的数据
        agent_message = []
        if self.content["agent_unit_p"] is None:
            if messageDict.get("代理机构联系方式", None) is not None:
                key = ""
                if "、" in messageDict.get("代理机构联系方式"):
                    key = "、"
                if "，" in messageDict.get("代理机构联系方式"):
                    key = "，"
                    agent_message = messageDict.get("代理机构联系方式").split(key)
                if len(agent_message) == 2:
                    self.content["agent_unit_p"] = agent_message[0]
                    self.content["agent_unit_m"] = agent_message[1]
                else:
                    self.content["agent_unit_p"] = messageDict.get("代理机构联系方式")
                    self.content["agent_unit_m"] = messageDict.get("代理机构联系方式")

        self.content["proj_rel_p"] = messageDict.get("项目联系人", None)
        self.content["proj_rel_m"] = messageDict.get("项目联系电话", None)
        self.content["other_ex"] = messageDict.get("其他补充事宜", "无")
        self.content["purchase_m"] = messageDict.get("采购方式", None)
        self.content["actual_price"] = messageDict.get("总中标金额（元）", None)
        self.content["provide_unit"] = messageDict.get("中标供应商信息", None)
        self.content["review_time"] = "无"
        if messageDict.get("开标时间", None) is not None:
            self.content["bid_time"] = trans_time(messageDict.get("开标时间", ""))
        else:
            if messageDict.get("定标日期", None) is not None:
                self.content["bid_time"] = trans_time(messageDict.get("定标日期", ""))
        self.content['pxy_fee_standard'] = messageDict.get("代理机构收费标准", None)
        if messageDict.get("代理机构收费金额", None) is not None:
            self.content['pxy_fee'] = messageDict.get("代理机构收费金额", "无")
        else:
            self.content['pxy_fee'] = messageDict.get("代理机构收费金额（元）", "无")

        return self.content
