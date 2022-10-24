# -*- coding: UTF-8 -*-
import re

from BaseSpider.base_component.SubResolver import SubResolver
from BaseSpider.base_component.announcement_page_resolver.SC_Annoucement.tool.tool import  *
CONST_PARAM = {
    # 公告标题参数
    'TITLE': '//*[@id="tab-503"]/div/div[2]/div/div/h2/text()',
    'attachments': '//a[@class="attachUrl"]/@href'
}


class SC_SJ_Annouce_Resolver_GetBid_base(SubResolver):
    """公告页请求解析器"""
    timePattern2 = re.compile(
        "(((\d{4})-(0[13578]|1[02])-(0[1-9]|[12]\d|3[01]))|((\d{4})-(0[469]|11)-(0[1-9]|[12]\d|30))|((\d{4})-(02)-(0[1-9]|1\d|2[0-8]))|((\d{2}(0[48]|[2468][048]|[13579][26]))-(02)-(29))|(((0[48]|[2468][048]|[13579][26])00)-(02)-(29)))")

    def __init__(self):
        self.content = {"title": None, "proj_name": None, "proj_code": None, "call_unit": None,
               "ancm_time": None,  "proj_rel_p": None, "proj_rel_m": None,
               "region": None, "purchase_m": None, "actual_price": None, "provide_unit": None,
               "other_ex": None, "review_place": "",'source_web_name': "四川省政府采购网",
               "web_site":"http://www.ccgp-sichuan.gov.cn/view/srplatform/portal/index.html", "agent_unit_name": None
        , "agent_unit_address": None,"call_unit_address":""}

    def resolver_page(self) -> dict:

        allTd = self.response_text.xpath('//*[@id="myPrintArea"]/table//tr/td')
        resultTd = []
        for td in allTd:
            result = td.xpath('string(.)').get()
            if result != "免责申明：以下信息由采购人或代理机构发布，信息的真实性、合法性、有效性由采购人或代理机构负责。":
                resultTd.append(result)

        messageDict = {}
        for index, td in enumerate(resultTd):
            allTd[index] = ''.join(td.split())
            if td == '' or td is None:
                td = "无"

        keys = allTd[0: len(allTd): 2]
        values = allTd[1: len(allTd): 2]
        for i in range(len(keys) - 1):
            messageDict.update({keys[i]: values[i]})
        try:
            content = self.getCallBidGovernment(messageDict)
            code_dict = getCodeHtml(self.response_text)
            at_dict = getAttachment(self.response_text)
            prov_dict = getProvideUnit(messageDict,"中标供应商信息")
            undefined_exp =getUndefinedExp(messageDict,"评标委员会成员名单")
            experts = getExpert()
            call_unit = getCallBidUnit(messageDict)
            agent_unit = getAgentUnit(messageDict,2)
            new_page_attr =  {'WB_G': content, 'code_dict': code_dict, 'at_dict': at_dict,
                'prov_dict': prov_dict, 'undefined_exp': undefined_exp, 'experts': experts,
                'call_unit': call_unit, 'agent_unit': agent_unit}
            self.page_attr.update(new_page_attr)
            return self.page_attr
        except:
            return self.page_attr

    def getCallBidGovernment(self, messageDict):

        self.content["sourse_url"] = self.response_url
        self.content["title"] = self.response_text.xpath('/html/body/div[2]/div[2]/h1/text()').get()
        self.content["proj_name"] = messageDict.get("采购项目名称", None)
        self.content["proj_code"] = messageDict.get("采购项目编号", None)
        self.content["call_unit"] = messageDict.get("采购人", None)
        self.content["ancm_time"] = trans_time(messageDict.get("公告发布时间", ""))
        self.content["region"] = messageDict.get("行政区划", None)
        if self.content['region'] is None  or self.content["region"] == "":
            self.content["region"] = messageDict.get("行政区域", "四川省")

        agent_address, agent_p, agent_phone = get_call_bid_agent_unit_message(messageDict)
        self.content["agent_unit_p"] = agent_p
        self.content["agent_unit_m"] = agent_phone
        self.content["agent_unit_address"] = agent_address
        self.content["agent_unit_name"] = messageDict.get("采购代理机构名称", None)
        if self.content["agent_unit_name"] is None:
            self.content["agent_unit_name"] = messageDict.get("代理机构", None)
        p, m = split_P_M(messageDict.get("采购项目联系人姓名和电话", ""))
        if p == "":
            p = messageDict.get("采购项目联系人姓名和电话", "")
        if m == "":
            m = messageDict.get("采购项目联系人姓名和电话", "")


        self.content["proj_rel_p"] = p
        self.content["proj_rel_m"] = m
        self.content["other_ex"] = messageDict.get("其他补充事宜", None)
        self.content["purchase_m"] = messageDict.get("采购方式", None)
        self.content["actual_price"] = messageDict.get("采购结果总金额", None)
        self.content["provide_unit"] = messageDict.get("各包中标/成交供应商名称、地址及报价", None)
        self.content["review_time"] = ""
        self.content["call_unit_address"] = messageDict.get("采购人地址")
        if messageDict.get("开标时间", None) is not None:
            self.content["bid_time"] = trans_time(messageDict.get("定标日期", ""))
        else:
            if messageDict.get("定标日期", None) is not None:
                if messageDict.get("定标日期", None) is not None:
                    self.content["bid_time"] = trans_time(messageDict.get("定标日期", ""))
        self.content['pxy_fee_standard'] = messageDict.get("代理机构收费标准", None)
        self.content['pxy_fee'] = messageDict.get("代理机构收费金额（元）", None)
        return self.contentrun



    '''
    获取未定义专家
    '''

    def getUndefinedExp(self, messageDict):
        undefined_exp = []
        experts = messageDict.get("评标委员会成员名单", "")
        experts = experts.split("、")
        for expert in experts:
            item = {}
            item['name'] = expert
            undefined_exp.append(item)

        return undefined_exp

