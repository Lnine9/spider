# -*- coding: UTF-8 -*-
import re

'''
市级招标
'''

from BaseSpider.base_component.SubResolver import SubResolver
from BaseSpider.base_component.announcement_page_resolver.SC_Annoucement.tool.tool import *

CONST_PARAM = {
    # 公告标题参数
    'TITLE': '//*[@id="tab-503"]/div/div[2]/div/div/h2/text()',
    'attachments': '//a[@class="attachUrl"]/@href'
}


class SC_SXJ_Annouce_Resolver_CallBid_base(SubResolver):
    """公告页请求解析器"""
    timePattern2 = re.compile(
        "(((\d{4})-(0[13578]|1[02])-(0[1-9]|[12]\d|3[01]))|((\d{4})-(0[469]|11)-(0[1-9]|[12]\d|30))|((\d{4})-(02)-(0[1-9]|1\d|2[0-8]))|((\d{2}(0[48]|[2468][048]|[13579][26]))-(02)-(29))|(((0[48]|[2468][048]|[13579][26])00)-(02)-(29)))")
    def __init__(self):
        self.content = {"title": None, "proj_name": None, "proj_code": None, "call_unit": None,
                   "ancm_time": None, "budget": None,
                   "region": None, "purchase_m": None, "tender_place": None, "bid_time": None,
                   "bid_sale_op_time": None, "bid_sale_m": None, "bid_sale_en_time": None,
                   "bid_price": None, "bid_place": None, "sent_bid_end_time": None, "bid_sale_place": None,
                   "other_ex": None, "proj_item": None,
                   'source_web_name': "四川省政府采购网", "agent_unit_name": None,
                   "web_site": "http://www.ccgp-sichuan.gov.cn/view/srplatform/portal/index.html", "agent_unit_address": "",
                   "call_unit_address":""}

    def resolver_page(self) -> dict:
        try:
            content = self.getCallBidGovernment()
            print(id(content))
            code_dict = getCodeHtml(self)
            at_dict = getAttachment(self.response_text)
            new_page_attr = {'CB_G': content, 'code_dict': code_dict, 'at_dict': at_dict}
            self.page_attr.update(new_page_attr)
            return new_page_attr
        except:
            return self.page_attr

    '''
      获取CB_G采购信息
      '''

    def getCallBidGovernment(self):

        allTd = self.response_text.xpath('//*[@id="myPrintArea"]/table//tr/td')
        resultTd = []
        for td in allTd:
            result = td.xpath('string(.)').get()
            if result != "免责申明：以下信息由采购人或代理机构发布，信息的真实性、合法性、有效性由采购人或代理机构负责。":
                resultTd.append(result)

        messageDict = {}

        keys = resultTd[0: len(allTd): 2]
        values = resultTd[1: len(allTd): 2]
        for i in range(len(keys) - 1):
            key = ''.join(keys[i].split())
            if "时间" not in keys[i] and "日期" not in keys[i]:
                value = ''.join(values[i].split())
            else:
                value = values[i]
            messageDict.update({key: value})

        type = messageDict.get("采购方式", None)
        self.content["sourse_url"] = self.response_url
        self.content["title"] = self.response_text.xpath('/html/body/div[2]/div[2]/h1/text()').get()
        self.content["proj_name"] = messageDict.get("采购项目名称", None)
        self.content["proj_item"] = messageDict.get("采购品目名称", None)
        self.content["proj_code"] = messageDict.get("采购项目编号", None)
        self.content["call_unit"] = messageDict.get("采购人", None)

        if messageDict.get("公告发布时间",None) is None:
            self.content["ancm_time"] = trans_time(self.response_text.xpath('/html/body/div[2]/div[2]/p/text()').get().split("：")[1])
        else:
            self.content["ancm_time"] = trans_time(messageDict.get("公告发布时间", None))
        self.content["budget"] = messageDict.get("预算金额（元）", '无')
        self.content["region"] = messageDict.get("行政区划", None)
        if self.content['region'] is None or self.content["region"] == "":
            self.content["region"] = messageDict.get("行政区域", "四川市县级")

        self.content["agent_unit_name"] = messageDict.get("采购代理机构名称", None)
        if self.content["agent_unit_name"] is None:
            self.content["agent_unit_name"] = messageDict.get("代理机构", None)
            if self.content["agent_unit_name"] is None:
                self.content["agent_unit_name"] = messageDict.get("代理机构名称", None)
        #     网页无代理机构联系人姓名时，用代理机构名代替
        agent_address, agent_p, agent_phone = get_call_bid_agent_unit_message(messageDict)
        self.content["agent_unit_p"] = agent_p
        self.content["agent_unit_m"] = agent_phone
        self.content["agent_unit_address"] = agent_address
        address, peoson, phone = get_call_bid_agent_unit_message(messageDict, 2)
        self.content["call_unit_address"] = address


        p, m = split_P_M(messageDict.get("采购项目联系人姓名和电话", None))
        if p == "":
            p = messageDict.get("采购项目联系人姓名和电话", "")
        self.content["proj_rel_p"] = p
        if m == "":
            m = messageDict.get("采购项目联系人姓名和电话", "")
        self.content["proj_rel_p"] = p
        self.content["proj_rel_m"] = m
        self.content["other_ex"] = messageDict.get("备注", "无")
        if self.content["other_ex"] == " ":
            self.content["other_ex"] = "无"

        self.content["purchase_m"] = messageDict.get("采购方式", None)
        if type == "竞争性磋商采购":
            self.content["bid_price"] = messageDict.get("磋商文件售价", None)
            if self.content["bid_price"] is None:
                self.content["bid_price"] = messageDict.get("磋商文件售价（元）", None)
            self.content["bid_sale_place"] = messageDict.get("磋商文件发售及供应商报名地点", None)
            if self.content["bid_sale_place"] is None:
                self.content["bid_sale_place"] = messageDict.get("获取磋商文件地点")
            self.content["bid_sale_m"] = messageDict.get("磋商文件发售方式", None)
            self.content["bid_sale_op_time"] = messageDict.get("获取磋商文件开始时间", None)
            self.content["bid_sale_en_time"] = messageDict.get("获取磋商文件结束时间", None)
            self.content["bid_end_time"] = messageDict.get("响应文件递交结束时间", "")
            self.content["tender_place"] = messageDict.get("响应文件递交地点", None)
            self.content["bid_time"] = messageDict.get("响应文件开启时间", "")
            self.content["bid_place"] = messageDict.get("响应文件开启地点", None)
        if type == "竞争性磋商":
            self.content["bid_price"] = messageDict.get("磋商文件售价", None)
            self.content["bid_sale_place"] = messageDict.get("磋商文件发售及供应商报名地点", None)
            self.content["bid_sale_m"] = messageDict.get("磋商文件发售方式", None)
            if messageDict.get("磋商文件发售及供应商报名时间",None) is None:
                self.content["bid_sale_op_time"] = trans_time(messageDict.get("获取磋商文件开始时间"))
                self.content["bid_sale_en_time"] = trans_time(messageDict.get("获取磋商文件结束时间"))
            else:
                self.content["bid_sale_op_time"] = trans_time(messageDict.get("磋商文件发售及供应商报名时间", None).split("到")[0])
                self.content["bid_sale_en_time"] = trans_time(messageDict.get("磋商文件发售及供应商报名时间", None).split("到")[1])

            self.content["tender_place"] = messageDict.get("供应商递交响应文件地点", None)
            if messageDict.get("供应商递交响应文件起止时间", None) is None:
                # self.content["sent_bid_op_time"] = trans_time(messageDict.get("响应文件递交开始时间"))

                self.content["bid_end_time"] = trans_time(messageDict.get("响应文件递交结束时间"))
            else:
                self.content["sent_bid_end_time"] = trans_time(messageDict.get("供应商递交响应文件起止时间", None).split("到")[1])
                # self.content["sent_bid_op_time"]  = trans_time(messageDict.get("供应商递交响应文件起止时间", None).split("到")[2])
            if messageDict.get("供应商接受资格审查及参加磋商时间", None) is None:
                self.content["bid_time"] = trans_time(messageDict.get("响应文件开启时间", None))
            else:
                self.content["bid_time"] = trans_time(messageDict.get("供应商接受资格审查及参加磋商时间", None))
            if messageDict.get("供应商接收资格审查及参加磋商地点", None):
                self.content["bid_place"] = messageDict.get("响应文件开启地点")
            else:
                self.content["bid_place"] = messageDict.get("供应商接收资格审查及参加磋商地点", None)
        if type == "公开招标":
            self.content["bid_price"] = messageDict.get("标书售价", None)
            if self.content["bid_price"] is None:
                self.content["bid_price"] = messageDict.get("标书售价（元）", None)
            self.content["bid_sale_place"] = messageDict.get("标书发售地点", None)
            self.content["bid_sale_m"] = messageDict.get("标书发售方式", None)
            self.content["bid_sale_op_time"] = trans_time(messageDict.get("标书发售起止时间", None).split("到")[0])
            self.content["bid_sale_en_time"] = trans_time(messageDict.get("标书发售起止时间", None).split("到")[1])
            self.content["bid_end_time"] = messageDict.get("投标截止时间", "")
            self.content["tender_place"] = messageDict.get("投标地点", None)
            self.content["bid_time"] = messageDict.get("开标时间", "")
            self.content["bid_place"] = messageDict.get("开标地点", None)
        if type == "竞争性谈判":
            self.content["bid_price"] = messageDict.get("获取谈判文件售价", None)
            if self.content["bid_price"] is None:
                self.content["bid_price"] = messageDict.get("获取谈判文件售价（元）")
            self.content["bid_sale_place"] = messageDict.get("获取谈判文件地点", None)
            self.content["bid_sale_m"] = messageDict.get("获取谈判文件方式", None)
            self.content["bid_sale_op_time"] = trans_time(messageDict.get("谈判文件起售时间", ""))
            self.content["bid_sale_en_time"] = trans_time(messageDict.get("谈判文件止售时间", ""))
            self.content["tender_place"] = messageDict.get("谈判响应文件递交地点", None)
            self.content["bid_time"] = messageDict.get("谈判响应文件开启时间", "")
            self.content["bid_end_time"] = trans_time(messageDict.get("谈判响应文件递交截止时间", ""))
            self.content["bid_place"] = messageDict.get("谈判响应文件开启地点", None)
        if type == "单一来源采购":
            self.content["bid_price"] = messageDict.get("采购文件售价", None)
            if self.content["bid_price"] is None:
                self.content["bid_price"] = messageDict.get("采购文件售价（元）", None)
            self.content["bid_sale_place"] = messageDict.get("采购文件发售地点", None)
            self.content["bid_sale_m"] = messageDict.get("采购文件发售方式", None)
            self.content["bid_sale_op_time"] = trans_time(messageDict.get("采购文件发售起止时间", None).split("到")[0])
            self.content["bid_sale_en_time"] = trans_time(messageDict.get("采购文件发售起止时间", None).split("到")[1])
            self.content["bid_end_time"] = trans_time(messageDict.get("洽谈时间", ""))
            self.content["tender_place"] = messageDict.get("洽谈地点", None)
            self.content["bid_time"] = trans_time(messageDict.get("洽谈时间", ""))
            self.content["bid_place"] = messageDict.get("洽谈地点", None)
        if type == "询价采购":

            if messageDict.get("询价文件发售及供应商报名时间", None) is None:
                self.content["bid_price"] = messageDict.get("获取谈判文件售价", None)
                if self.content["bid_price"] is None:
                    self.content["bid_price"] = messageDict.get("获取谈判文件售价（元）")
                self.content["bid_sale_place"] = messageDict.get("获取谈判文件地点", None)
                self.content["bid_sale_m"] = messageDict.get("获取谈判文件方式", None)
                self.content["bid_sale_op_time"] = trans_time(messageDict.get("谈判文件起售时间", ""))
                self.content["bid_sale_en_time"] = trans_time(messageDict.get("谈判文件止售时间", ""))
                self.content["tender_place"] = messageDict.get("谈判响应文件递交地点", None)
                self.content["bid_time"] = messageDict.get("谈判响应文件开启时间", "")
                self.content["bid_end_time"] = trans_time(messageDict.get("谈判响应文件递交截止时间", ""))
                self.content["bid_place"] = messageDict.get("谈判响应文件开启地点", None)

            else:
                self.content["bid_price"] = messageDict.get("标书售价", '无')
                if self.content["bid_price"] is None:
                    self.content["bid_price"] = messageDict.get("标书售价（元）", None)
                self.content["bid_sale_place"] = messageDict.get("询价文件发售及供应商报名地点", None)
                self.content["bid_sale_m"] = messageDict.get("询价文件发售方式", None)
                self.content["bid_sale_op_time"] = trans_time(messageDict.get("询价文件发售及供应商报名时间", None).split("到")[0])
                self.content["bid_sale_en_time"] = trans_time(messageDict.get("询价文件发售及供应商报名时间", None).split("到")[1])
                self.content["bid_end_time"] = trans_time(messageDict.get("供应商递交响应文件起止时间", None).split("到")[1])
                self.content["tender_place"] = messageDict.get("供应商递交响应文件地点", None)
                self.content["bid_time"] = trans_time(messageDict.get("开标时间", ""))
                self.content["bid_place"] = messageDict.get("供应商接收资格审查及参加询价地点", None)
        return self.content

