

from BaseSpider.base_component.SubResolver import SubResolver
from BaseSpider.base_component.utils.util import k_remove, remove1
from BaseSpider.tool.param_tool import process_dict
import time
import re

CONST_PARAM = {
    # 公告标题参数
    'TITLE': '//*[@id="bt_be"]/div/text()',
}
class YN_WinBid_sub_component1(SubResolver):


    def resolver_page(self) -> dict:
        try:
            content = self.getWinBidGovernment()
            code_dict = self.getCodeHtml()
            at_dict = self.getAttachment()
            prov_dict = self.getProvideUnit()
            undefined_exp = self.getUndefinedExp()
            experts = self.getExpert()
            call_unit = self.getCallBidUnit()
            agent_unit = self.getAgentUnit()
            content['web_site']='http://www.ccgp-yunnan.gov.cn/'
            content['source_web_name']='云南省政府采购系统'

            new_page_attr = {'WB_G': content, 'code_dict': code_dict, 'at_dict': at_dict,
                             'prov_dict': prov_dict, 'undefined_exp': undefined_exp, 'experts': experts,
                             'call_unit': call_unit, 'agent_unit': agent_unit}
            self.page_attr.update(new_page_attr)
        except:
            return self.page_attr

        return self.page_attr

    '''
    获取WB_G中标信息
    '''
    def getWinBidGovernment(self):
        title = self.response_text.xpath(CONST_PARAM.get('TITLE'))
        content = {'公告标题': title}

        # 形成字典
        for each in self.response_text.xpath('//*[@id="searchPanel"]/div'):
            key = k_remove(str(each.xpath('./label/text()').get()))
            value = remove1(each.xpath('./div[1]/text()').get())
            content[key] = value
        # 时间格式转化为YY-MM-DD
        try:
            if time.strptime( content['开标时间'], "%Y-%m-%d"):
                content['开标时间'] = time.strftime("%Y-%m-%d", time.strptime(remove1(content['开标时间']), "%Y-%m-%d"))
        except:
            try:
                if time.strptime( content['开标时间'], "%Y-%m-%d %H:%M:%S"):
                    content['开标时间'] = time.strftime("%Y-%m-%d", time.strptime(remove1(content['开标时间']), "%Y-%m-%d %H:%M:%S"))
            except:
                content['开标时间'] = None
        content['行政区域'] = '云南省'
        # 匹配关键字段
        content = process_dict(self.annoucement_type,content)
        content['actual_price'] = content['actual_price']+'(万元)'
        content['sourse_url'] = self.response_url
        return content

    '''
    获取源文件信息
    '''
    def getCodeHtml(self):
        code_dict = {}

        code_dict['url'] = self.response_url
        code_dict['file_type'] = 'html'
        code_dict['file_size'] = '-1'
        code_dict['local_path'] = '暂无'
        code_dict['code'] =''.join(self.response_text.xpath('//*[@id="searchPanel"]').extract())

        return code_dict

    '''
    获取附件信息
    '''
    def getAttachment(self):
        at_dict = []
        item = {}
        message = self.response_text.xpath('//*[@id="searchPanel"]')
        completeurl = self.response_text.xpath('normalize-space(//*[@id="completeurl"]/@value)').get()
        completeurl = completeurl.replace("/","%2F")
        filename =self.response_text.xpath('normalize-space(//*[@id="filedel"]/text())').get()
        filename1 = filename.encode('gbk')
        filename1 =eval(repr(filename1).replace('\\x', '%'))
        filename1 = filename1.decode('utf-8')
        item['url'] = 'http://www.ccgp-yunnan.gov.cn/newbulletin_zz.do?method=downloadFile&completeurl='+completeurl+'&file_name='+filename1 # 附件源地址
        if item['url'] == 'http://www.ccgp-yunnan.gov.cn/newbulletin_zz.do?method=downloadFile&completeurl=&file_name=':
            item['url'] = None
            item['file_type'] = None
        else:
            attachments_url = 'http://www.ccgp-yunnan.gov.cn/newbulletin_zz.do?method=downloadFile&completeurl='+completeurl+'&file_name='+filename1
            attachments_url=attachments_url.replace(' ','%20')  # 防止url出现空字符
            item['url'] = attachments_url  # 附件源地址
            item['file_type'] = item['url'][item['url'].rfind('.') + 1:]
        item['file_size'] = -1
        item['local_path'] = '暂无'
        item['file_name'] = filename

        at_dict.append(item)
        return at_dict

    '''
    获取供应商
    '''
    def getProvideUnit(self):
        return []

    '''
    获取未定义专家
    '''
    def getUndefinedExp(self):
        undefined_exp = []

        experts=self.response_text.xpath('//*[@id="bj"]/div[1]/text()').get()
        experts =re.split('[、 ]', experts)
        for expert in experts:
            item = {}
            item['name'] = expert
            undefined_exp.append(item)

        return undefined_exp

    '''
    获取专家
    '''
    def getExpert(self):
        return []

    '''
    获取采购机构
    '''
    def getCallBidUnit(self):
        call_unit = {}

        call_unit['name'] = self.response_text.xpath('//*[@id="hiddenCgr"]/div[1]/text()').get()
        call_unit['address'] = self.response_text.xpath('//*[@id="hiddenCgr_2"]/div[1]/text()').get()
        call_unit['code'] = call_unit['name']

        return call_unit


    '''
    获取代理机构
    '''
    def getAgentUnit(self):
        agent_unit = []

        item = {}
        item['code'] = self.response_text.xpath('//*[@id="pn_pn"]/div[1]/text()').get()
        item['name'] = self.response_text.xpath('//*[@id="bc_an_2"]/div[1]/text()').get()
        item['address'] = self.response_text.xpath('//*[@id="aa_ac"]/div[1]/text()').get()
        agent_unit.append(item)

        return agent_unit

