import datetime

from lxml import html
from lxml import etree
"""获取heml"""


def getCodeHtml(message):
    try:
        code_dict = {}
        code_dict['url'] = message.reponse_url
        code_dict['file_type'] = code_dict['url'][code_dict['url'].rfind('.') + 1:]
        code_dict['file_size'] = '-1'
        code_dict['local_path'] = '暂无'
        code = message.reponse_text.xpath('/html/body//div[@class="cont-info"]').extract()[0]
        code_dict['code'] = code
        return code_dict
    except:
        return {}



'''
   获取附件信息
   '''


def getAttachment(response):
    at_dict = []
    item = {}

    completeurl = None
    try:
        completeurl = "http://www.ccgp-sichuan.gov.cn" + response.response_text.xpath(
            '//tr//a[@target="_blank"]/@href').get()
    except:
        completeurl = None
    if completeurl != None:
        item["file_name"] = response.response_url.split("/")[-1].split(".")[0]
        item['url'] = completeurl
        item['file_type'] = item['url'][item['url'].rfind('.') + 1:]
        if len(item['file_type']) > 15:
            item['file_type'] = "unknown"
        item['file_size'] = -1
        item['local_path'] = '暂无'

        at_dict.append(item)
    return at_dict


"""切割联系人和联系方式"""


def split_P_M(p_m) -> ():
    p = ""
    m = ""
    p_m = p_m.replace("，", " ")
    p_m = p_m.replace(";", " ")
    p_m = p_m.replace("；", " ")
    if " " not in p_m and p_m is not None:
        p_m = splitByKey(p_m)
    if p_m is not None:
        items = p_m.split(" ")
        if "：" not in p_m and len(items) == 2:
            p = items[0]
            m = items[1]
        else:
            if len(items) == 1:
                pass
            else:
                for item in items:
                    try:
                        if "联系电话" in item or "电话" in item:
                            m = item.split("：")[1]
                    except:
                        m = ""
                    try:
                        if "联系人" in item or "项目联系人" in item or "联系人/采购项目联系人" in item:
                            p = item.split("：")[1]
                    except:
                        p = ""

                if p == "":
                    p = p_m
                if m == "":
                    m = p_m
        if p == "":
            p = p_m
        if m == "":
            m = p_m

    return p, m


"""格式话联系人和联系方式"""


def splitByKey(p_m) -> ():
    key = ""
    try:
        if "先生" in p_m:
            key = "生"
        if "老师" in p_m:
            key = "师"
        if "女士" in p_m:
            key = "士"
        if key == "":
            if "电话" or "电 话" in p_m:
                key = "电"
            if "联系电话" in p_m:
                key = "联"

        if key in ["生", "士", "师"]:
            items = p_m.split(key)
            items[0] = items[0] + key + " "
            p_m = "".join(items)
        if key in ["联", "电"]:
            items = p_m.split(key)
            items[1] = key + items[1] + ""
            p_m = "".join(items)
    except:
        pass

    return p_m


'''
       获取供应商
       '''


def getProvideUnit(messageDict, key):
    prov_dicts = []
    provideUnit = messageDict.get(key, "")

    for item in provideUnit.split("."):
        single = []
        prov_dict = {}
        if ";" in item:
            single = item.split(";")
        if "；" in item:
            single = item.split("；")
        if single:
            for i in single:
                if "供应商名称" in i or "成交供应商" in i:
                    if ":" in i:
                        prov_dict["name"] = i.split(':')[1]
                        prov_dict["code"] = prov_dict["name"]
                    if "：" in i:
                        prov_dict["name"] = i.split('：')[1]
                        prov_dict["code"] = prov_dict["name"]
                if "供应商地址" in i or "成交供应商地址" in i:
                    if ":" in i:
                        prov_dict["address"] = i.split(':')[1]
                    if "：" in i:
                        prov_dict["address"] = i.split('：')[1]
            if prov_dict:
                key = ""
                if "&" in prov_dict.get("name", ""):
                    key = "&"
                if "、" in prov_dict.get("name", ""):
                    key = "、"
                if "，" in prov_dict.get("name", ""):
                    key = "，"
                if key != "":
                    address = prov_dict["address"].split(key)
                    if not address:
                        address = messageDict.get(key, "")
                    unit = prov_dict["name"].split("、")
                    if len(address) != len(unit):
                        address = [address[0]] * len(unit)
                        print(address)

                    for index, item in enumerate(unit):
                        item_dict = {}
                        item_dict["name"] = item
                        item_dict["code"] = item
                        item_dict["address"] = address[index]
                        prov_dicts.append(item_dict)
                else:
                    prov_dicts.append({"name": "", "code": "", "address": ""})

            else:
                continue

    for index, item in enumerate(prov_dicts):
        if len(item.get("code", "")) > 15:
            prov_dicts[index]["code"] = item["code"][0:14]
        if item.get("name", "") == "":
            prov_dicts[index]["code"] = ""

    return prov_dicts


'''
获取未定义专家
'''


def getUndefinedExp(messageDict, key):
    undefined_exp = []
    experts = messageDict.get(key, "")
    if "、" in experts:
        experts = experts.split("、")

    else:
        if "，" in experts:
            experts = experts.split("，")
        else:
            experts = experts.split()
    for expert in experts:
        item = {}
        item['name'] = expert
        undefined_exp.append(item)

    return undefined_exp


'''
获取专家
'''


def getExpert():
    return []


'''获取采购机构'''


def getCallBidUnit(messageDict):
    call_units = []
    call_unit = {}

    call_unit['name'] = messageDict.get("采购人", "")
    call_unit['address'] = messageDict.get("采购人地址", "")
    if call_unit['address'] is None:
        if ";" in call_unit.get()['address']:
            call_unit['address'] = messageDict.get("采购人地址和联系方式", "").split(";")[0]
    call_unit["code"] = call_unit["name"]
    if "、" in call_unit["name"]:
        units = call_unit['name'].split("、")
        for unit in units:
            realUnit = {}
            realUnit["name"] = unit
            realUnit["code"] = unit
            if len(call_unit["code"]) > 15:
                call_unit["code"] = call_unit["code"][0:14]
            call_units.append(realUnit)
        if "、" in call_unit["address"]:
            for index, address in enumerate(call_unit['address'].split("、")):
                call_units[index]["address"] = address
        for item in call_units:
            if item.get("address", "") == "":
                item["address"] = call_unit["address"]
    else:
        call_units = call_unit
        if len(call_unit["code"]) > 15:
            call_unit["code"] = call_unit["code"][0:14]
    return call_units


'''
获取代理机构
'''


def getAgentUnit(messageDict, type):
    agent_unit = []

    item = {}
    if type == 1:
        item['code'] = messageDict.get("代理机构")
        item['name'] = messageDict.get("代理机构")
        item['address'] = messageDict.get("代理机构地址")
        agent_unit.append(item)
    if type == 2:
        item['code'] = messageDict.get("采购代理机构名称")
        item['name'] = messageDict.get("采购代理机构名称")
        item['address'] = messageDict.get("采购代理机构地址和联系方式", None)
        if item['address'] is None:
            item['address'] = messageDict.get("代理机构地址和联系方式", None)
        address = ""
        key = ""
        if " " in item['address']:
            key = ";"
        if ";" in item['address']:
            key = ";"
        if "；" in item['address']:
            key = "；"
        if key != "":
            address = item["address"].split(key)
        for i in address:
            if "地址" in i:
                if ":" in i:
                    address = i.split(":")[1]

                if "：" in i:
                    address = i.split("：")[1]
                if address != "":
                    item['address'] = address

    return agent_unit


'''招标公告获取代理机构地址，联系人，联系方式，无法解析时返回原网站描述,type默认为1解析代理机构，为2解析采购单位'''


def get_call_bid_agent_unit_message(messageDict,type = 1)->():


    if type == 1:
        message = messageDict.get("采购代理机构地址和联系方式", None)
        if message is None:
            message = messageDict.get("代理机构地址和联系方式", None)
    else:
        message = messageDict.get("采购人地址和联系方式",None)
    key = judge_key(message)
    if key is not "":
        messages = message.split(key)
        result_message = messages
        split_keys = ["：",":"]
        if len(messages) == 2:
            for index,i in enumerate(messages):
                for split_key in split_keys:
                    if split_key in i:
                        result_message[index] = i.split(split_key)[1]
            person = ""
            if type == 1:
                person = messageDict.get("代理机构名称",None)
                if person is None:
                    person = messageDict.get("采购代理机构名称")
            return result_message[0], person, result_message[1]
        if len(messages) == 3:
            for index,i in enumerate(messages):
                for split_key in split_keys:
                    if split_key in i:
                        result_message[index] = i.split(split_key)[1]
            return result_message[0], result_message[1], result_message[2]

    return message, message, message


'''判断切割的key'''


def judge_key(message, keys=[" ", ",", ";", "，", "；"]) -> str:
    key = ""
    for i in keys:
        if i in message:
            key = i
            return key
    return key
def trans_time(time_str):
    count = time_str.count(":")
    count_space = time_str.count(" ")
    if count_space >1:
        time_str = time_str[0:-1]
    if count == 1:
        time_str += ":00"
    return time_str