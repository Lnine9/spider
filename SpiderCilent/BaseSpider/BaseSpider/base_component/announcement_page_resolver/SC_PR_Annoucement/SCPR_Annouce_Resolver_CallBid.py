import re

from BaseSpider.base_component.HtmlPageResolver import HtmlPageResolver
from scrapy.selector import Selector

import datetime
import requests
import json

CONST_PARAM = {
    # 公告标题参数
    'TITLE': '//*[@id="tab-503"]/div/div[2]/div/div/h2/text()',
    'attachments': '//a[@class="attachUrl"]/@href'
}


class SCPR_Annouce_Resolver_CallBid(HtmlPageResolver):
    """公告页请求解析器"""

    content = {"title": "", "proj_name": "", "proj_code": "",
               "proj_place": "", "resource_from": "", "ET": "",
               "region": "", "bid_sale_m": "", "bid_sale_op_time": "",
               "bid_sale_en_time": "", "bid_price": "", "bid_sale_place": "",
               "bidding_deadline": "",
               "proj_rel_p_m": "",
               "agent_unit_p_m": "", "other_ex": "",
               "tender_place": "", "releaseTime": "", "sourse_url": "",
               }

    def resolver_page(self) -> dict:
        try:
            content = self.getCallBidGovernment()
            code_dict = self.getCodeHtml()
            at_dict = self.getAttachment()
        except:
            return  {}

        return {'CB_E': content, 'code_dict': code_dict, 'at_dict': at_dict}

    def getCallBidGovernment(self):
        project_code = self.response.xpath('//span[@id="relateinfoid"]/@data-value')[0].get()

        # 源网页
        originalAnnouncementPage = self.response.text

        # 源网页网址
        self.content["sourse_url"] = self.response.url
        data = requests.get(url="http://ggzyjy.sc.gov.cn/staticJson/{project_code}/503.json?_={nowDate}".format(
            project_code=project_code, nowDate=datetime.datetime.microsecond))

        dataDict = json.loads(data.text).get("data")[0]
        publicData = dataDict.get("thepublicinfo", "")
        # 项目名称
        self.content['proj_name'] = publicData.get("PROJECT_NAME", "")
        # 项目编号
        self.content['proj_code'] = publicData.get("PROJECT_CODE", "")
        # 公告标题
        self.content['title'] = dataDict.get("title", "")
        # 资金来源
        self.content['resource_from'] = publicData.get("FUND_SOURCE", "")
        # 项目地址
        self.content['proj_place'] = publicData.get("ADDRESS", "")
        # 招标代理机构联系人及电话
        self.content['agent_unit_p'] = publicData.get("CONTACTOR", "")

        self.content['agent_unit_m'] = publicData.get("CONTACT_INFORMATION", "")
        # 行政区域代码
        self.content['region'] = publicData.get("REGION_CODE", "")
        data = dataDict["infoContent"].replace("<h2>", "<p>")
        data = dataDict["infoContent"].replace("</h2>", "</p>")
        data = dataDict["infoContent"].replace("<h3>", "<p>")
        data = dataDict["infoContent"].replace("</h3>", "</p>")

        allP = Selector(text=data).response.xpath('//p')

        # 信息数组
        messageList = []
        rep = {'年': '-', '月': '-', '日': ' ', "：": ":"}
        rep = dict((re.escape(k), v) for k, v in rep.items())
        splitPattern = re.compile("|".join(rep.keys()))
        # 年月日 时
        timePattern = re.compile(
            "(((\d{4})-(0[13578]|1[02])-(0[1-9]|[12]\d|3[01]))|((\d{4})-(0[469]|11)-(0[1-9]|[12]\d|30))|((\d{4})-(02)-(0[1-9]|1\d|2[0-8]))|((\d{2}(0[48]|[2468][048]|[13579][26]))-(02)-(29))|(((0[48]|[2468][048]|[13579][26])00)-(02)-(29))) ([0-1]?[0-9]|2[0-3])")

        timePattern2 = re.compile(
            "(((\d{4})-(0[13578]|1[02])-(0[1-9]|[12]\d|3[01]))|((\d{4})-(0[469]|11)-(0[1-9]|[12]\d|30))|((\d{4})-(02)-(0[1-9]|1\d|2[0-8]))|((\d{2}(0[48]|[2468][048]|[13579][26]))-(02)-(29))|(((0[48]|[2468][048]|[13579][26])00)-(02)-(29)))")
        # 删除字符串中的中文
        removeWord = re.compile(u'[\u4e00-\u9fa5]')

        """获取目标信息所在的p标签"""

        # 获取p标签中所有文字
        for p in allP:
            messageList.append(p.xpath("normalize-space(string(.))").get())
        messgeDict = {}
        # 浅复制，这里没有嵌套结构，用浅复制就足够了
        message_copy = messageList[:]
        keys = ["招标条件", "项目概况与招标范围", "招标文件的获取", "投标文件的递交", "投标文件的编制和递交", "联系方式"]
        item_key = ""
        for index, item in enumerate(messageList):
            suf_item = item[0:1]
            item_list = []
            for key in keys:
                if key in item:
                    item_key = key
                    for i, message in enumerate(message_copy):
                        message = ''.join(message.split())
                        suf_message = message[0:1]
                        if suf_message == suf_item and message != item:
                            item_list.append(message)
                        else:
                            if item_key == "项目概况与招标范围":
                                if "项目地点" in message or "计划工期" in message:
                                    item_list.append(message)
                                else:
                                    if len(item_list) >= 2:
                                        keys.remove(key)
                                        if item in message_copy:
                                            message_copy.remove(item)
                                        for m in item_list:
                                            if item in message_copy:
                                                message_copy.remove(m)
                                        break
                                    else:
                                        continue

                            else:
                                if item_key == "联系方式" and message != "":
                                    item_list.append(message)

                                else:
                                    # 避免不必要的循环
                                    if item_list:
                                        keys.remove(key)
                                        if item in message_copy:
                                            message_copy.remove(item)
                                        for m in item_list:
                                            if item in message_copy:
                                                message_copy.remove(m)
                                        break
                                    else:
                                        continue
                else:
                    if item in message_copy:
                        message_copy.remove(item)
                    continue
            if item_list:
                messgeDict.update({item_key: item_list})
                if "联系方式" not in keys:
                    break


        self.getFile(messgeDict)
        self.deal_PROJ_Message(messgeDict)
        self.deal_Contact_Message(messgeDict)
        self.send_file_message(messgeDict)
        return self.content

    '''
        获取源文件信息
        '''

    def getCodeHtml(self):
        code_dict = {}

        code_dict['url'] = self.response.url
        code_dict['file_type'] = 'html'
        code_dict['file_size'] = '-1'
        code_dict['local_path'] = '暂无'

        return code_dict

    '''
    获取附件信息
    '''

    def getAttachment(self):
        at_dict = []
        count = 0
        attachmentname = self.response.xpath('//a[@class="attachUrl"]/@title')
        url = self.response.xpath('//a[@class="attachUrl"]/@href')  # 附件源地址
        for i in range(0, len(attachmentname)):
            item = {}
            if url[i] is not None:
                attachmentname[i] = attachmentname[i].get()
                attachmentname[i] = attachmentname[i].replace(' ', '%20')  # 防止url出现空字符
                item['file_type'] = attachmentname[i][attachmentname[i].rfind('.') + 1:]
                item['url'] = url[i].get()
            item['file_size'] = -1
            item['local_path'] = '暂无'
            at_dict.append(item)
        return at_dict

    def deal_PROJ_Message(self, message):
        for item in message.get("项目概况与招标范围", None):
            if "项目地点" in item:
                self.content['proj_place'] = item.split("：")[1]
            if "计划工期" in item:
                self.content['ET'] = item.split("：")[1]

    def getFile(self, messge_dict):
        rep = {'年': '-', '月': '-', '日': ' ', "：": ":"}
        rep = dict((re.escape(k), v) for k, v in rep.items())
        splitPattern = re.compile("|".join(rep.keys()))
        # 年月日 时
        timePattern = re.compile(
            "(((\d{4})-(0[13578]|1[02])-(0[1-9]|[12]\d|3[01]))|((\d{4})-(0[469]|11)-(0[1-9]|[12]\d|30))|((\d{4})-(02)-(0[1-9]|1\d|2[0-8]))|((\d{2}(0[48]|[2468][048]|[13579][26]))-(02)-(29))|(((0[48]|[2468][048]|[13579][26])00)-(02)-(29))) ([0-1]?[0-9]|2[0-3])")

        timePattern2 = re.compile(
            "(((\d{4})-(0[13578]|1[02])-(0[1-9]|[12]\d|3[01]))|((\d{4})-(0[469]|11)-(0[1-9]|[12]\d|30))|((\d{4})-(02)-(0[1-9]|1\d|2[0-8]))|((\d{2}(0[48]|[2468][048]|[13579][26]))-(02)-(29))|(((0[48]|[2468][048]|[13579][26])00)-(02)-(29)))")
        message = messge_dict.get("招标文件的获取", None)
        if message:
            self.content["bid_sale_m"] = message[0][2:len(message[0]) - 1]
            for item in message:
                if "招标文件" and "售价" in item:
                    item = item.split("，")
                    target = ""
                    for i in item:
                        if "元" in i and "售价" in i:
                            target = i
                            try:
                                number = i.split("售价")[1]
                                self.content['bid_price'] = number.replace("元","")
                            except:
                                self.content['bid_price'] = ""
                    if self.content['bid_price'] == "" :
                        self.content['bid_price'] = i

                if "年" in item and "月" in item:
                    item = item.split("，")
                    for i in item:
                        if "年" in i and "月" in i:

                            targetItem = ''.join(i.split())
                            my_str = splitPattern.sub(lambda m: rep[re.escape(m.group(0))], targetItem)
                            print(my_str)
                            timeList = []

                            timeList = timePattern2.findall(my_str)

                            if len(timeList) > 1:
                                self.content["bid_sale_op_time"] = timeList[0][0]
                                self.content["bid_sale_en_time"] = timeList[1][0]
                                break
                            else:
                                if len(timeList) > 0:
                                    self.content["bid_sale_op_time"] = timeList[0][0]
                                    break

    def deal_Contact_Message(self, message):
        flag_index = 1000
        agent_message = []
        proj_message = []
        for index, item in enumerate(message.get("联系方式", None)):
            item = "".join(item.split())
            if "招标代理机构" in item:
                flag_index = index
            if index < flag_index:
                agent_message.append(item)
            if index >= flag_index:
                proj_message.append(item)

        for item in proj_message:
            if "联系人" in item:
                self.content['proj_rel_p'] = item.split("：")[1]
            if "电话" in item:
                self.content["proj_rel_m"] = item.split("：")[1]

    def send_file_message(self, message_dict):
        message = message_dict.get("投标文件的递交", None)
        if message is None:
            message = message_dict.get("投标文件的编制和递交", None)
        if message is not None:
            for item in message:
                for i in item.split("，"):

                    if "地点为" in i:
                        item = i.replace("地点为", "")
                        self.content["tender_place"] = item
        else:
            self.content["tender_place"] = ""


