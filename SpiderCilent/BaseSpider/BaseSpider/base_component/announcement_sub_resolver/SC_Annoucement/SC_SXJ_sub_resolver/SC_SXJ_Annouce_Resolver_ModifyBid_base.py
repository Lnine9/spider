import re

from BaseSpider.base_component.SubResolver import SubResolver
from BaseSpider.base_component.announcement_page_resolver.SC_Annoucement.tool.tool import *
'''更正'''
CONST_PARAM = {
    # 公告标题参数
    'TITLE': '//*[@id="tab-503"]/div/div[2]/div/div/h2/text()',
    'attachments': '//a[@class="attachUrl"]/@href'
}


class SC_SXJ_Annouce_Resolver_ModifyBid_base(SubResolver):
    """公告页请求解析器"""
    timePattern2 = re.compile(
        "(((\d{4})-(0[13578]|1[02])-(0[1-9]|[12]\d|3[01]))|((\d{4})-(0[469]|11)-(0[1-9]|[12]\d|30))|((\d{4})-(02)-(0[1-9]|1\d|2[0-8]))|((\d{2}(0[48]|[2468][048]|[13579][26]))-(02)-(29))|(((0[48]|[2468][048]|[13579][26])00)-(02)-(29)))")

    def __init__(self):
        self.content = {"title": None, "proj_name": None, "proj_code": None, "purchasing_unit_name": None,
               "ancm_time": None, "agent_unit_p": None,"agent_unit_m":None ,"proj_rel_p": None,"proj_rel_m": None,
               "purchase_m": None, "actual_price": None, "provide_unit": None,
               "other_ex": None,"modify_content":None,"agent_unit_name":None,'source_web_name': "四川省政府采购网",
               "web_site":"http://www.ccgp-sichuan.gov.cn/view/srplatform/portal/index.html","agent_unit_address":"",
               "call_ubit_address":""}

    def resolver_page(self) -> dict:

        # try:
            content = self.getCallBidGovernment()
            code_dict = getCodeHtml(self.response_text)
            at_dict = getAttachment(self)
            new_page_attr = {'MB_G': content, 'code_dict': code_dict, 'at_dict': at_dict}
            self.page_attr.update(new_page_attr)
            return self.page_attr

        # except:
        #     return self.page_attr

    def getCallBidGovernment(self):
        allTr = self.response_text.xpath('//*[@id="myPrintArea"]/table//tr')
        trs = []
        allTd = []
        # 一个键对应多个值，即一行内有两个以上td
        muti_messageDict = {}
        for tr in allTr:
            td = tr.xpath("td")
            if len(td) == 2:
                allTd.append(td[0])
                allTd.append(td[1])
            if len(td) > 2:
                key = td[0].xpath('string(.)').get()

                tds = td[1:len(td)]
                muti_messageDict.update({key: tds})

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

        self.content["sourse_url"] = self.response_url
        self.content["title"] = self.response_text.xpath('/html/body/div[2]/div[2]/h1/text()').get()
        self.content["proj_name"] = messageDict.get("采购项目名称", None)
        self.content["proj_code"] = messageDict.get("采购项目编号", None)
        self.content["purchasing_unit_name"] = messageDict.get("采购人", None)
        if messageDict.get("公告发布时间") is not None:
            self.content["ancm_time"] = trans_time(messageDict.get("公告发布时间", None))
        else:
            self.content["ancm_time"] = trans_time(self.response_text.xpath('/html/body/div[2]/div[2]/p/text()').get().split("：")[1])
        self.content["region"] = messageDict.get("行政区划", None)
        if self.content['region'] is None or self.content["region"] == "":
            self.content["region"] = messageDict.get("行政区域", "四川市县级")
        self.content["agent_unit_p"] = messageDict.get("代理机构联系人", None)
        self.content["call_unit_address"] = messageDict.get("采购人地址", None)
        self.content["agent_unit_m"] = messageDict.get("代理机构联系方式", None)
        self.content["agent_unit_address"] = messageDict.get("代理机构地址")
        self.content["agent_unit_name"] = messageDict.get("代理机构", None)
        self.content["proj_rel_p"] = messageDict.get("项目联系人", None)
        self.content["proj_rel_m"] = messageDict.get("项目联系电话", None)
        self.content["other_ex"] = messageDict.get("其他补充事宜", "") + messageDict.get("备注","")
        if self.content["other_ex"] == " " or self.content["other_ex"] == "  ":
            self.content["other_ex"] = "无"

        self.content["purchase_m"] = messageDict.get("采购方式", None)

        if messageDict.get("原公告发布时间", None) is not None:
            self.content["origin_announce_time"] = trans_time(messageDict.get("原公告发布时间", None))
        self.content["modify_content"] = messageDict.get("更正文件更正事项和内容", None)
        if self.content["modify_content"] is None:
            self.content["modify_content"] = messageDict.get("更正事项、内容", None)
            if self.content["modify_content"] is None:
                item = muti_messageDict.get("更正文件更正事项和内容", None)
                if item is None:
                    item = muti_messageDict.get("更正事项、内容", None)
                    if item is not None:
                        self.content["modify_content"] = item[1].xpath('string(.)').get()
                        enclosure = item[0].xpath('/a/@href').get()
                        if enclosure:
                            self.content["modify_content"] += "附件地址：{enclosure}".format(enclosure=enclosure)
        return self.content






