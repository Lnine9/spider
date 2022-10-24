import re

from BaseSpider.base_component.SubResolver import SubResolver
from BaseSpider.base_component.utils.util import  remove1
from BaseSpider.tool.param_tool import process_dict
import time


CONST_PARAM = {
    # 公告标题参数
    'TITLE': '/html/body/div[5]/div/h3/text()',
}

class YNPR_CallBid_sub_component2(SubResolver):


    def resolver_page(self) -> dict:
        try:
            content = self.getCallBidEngineering()
            code_dict = self.getCodeHtml()
            at_dict = self.getAttachment()
            content['web_site']='http://ggzy.yn.gov.cn/'
            content['source_web_name']='云南省公共资源交易电子服务系统'

            new_page_attr = {'CB_E':content,'code_dict':code_dict,'at_dict':at_dict}
            self.page_attr.update(new_page_attr)
        except:
            return self.page_attr

        return self.page_attr

    '''
    获取CB_E采购信息
    '''
    def getCallBidEngineering(self):
        title = self.response_text.xpath(CONST_PARAM.get('TITLE')).get()
        content = {'公告标题': title}
        content['发布时间'] = (re.findall(r"发布时间(.*)", self.response_text.xpath('/html/body/div[5]/div/p/text()').get()))[0]
        # 形成字典

        contents = self.response_text.xpath('/html/body/div[5]/div/div/table/tr/td')
        for item in contents:
            pre = re.compile(r'<[^>]+>',re.S)
            strbr = pre.sub('',item.get())
            if '资金来源：' in strbr:
                content['资源来源'] = re.findall(r"来源：(.*)[。]", strbr)
                if len(content['资源来源']) >= 1:
                    content['资源来源'] =  content['资源来源'][0]
                else:
                    content['资源来源'] = ''
            if '招标人名称：' in strbr:
                content['采购单位名称'] =''.join(strbr.split('：',1)[1:])
            if '招标人地址：' in strbr:
                content['采购单位地址'] =''.join(strbr.split('：',1)[1:])
            if '招标代理名称：' in strbr:
                content['代理机构名称'] = ''.join(strbr.split('：',1)[1:])
            if ' 招标代理地址：' in strbr:
                content['代理机构地址'] = ''.join(strbr.split('：',1)[1:])
            if '招标联系人：' in strbr:
                content['项目联系人'] =''.join(strbr.split('：',1)[1:])
            if '招标人联系电话：' in strbr:
                content['项目联系电话'] = ''.join(strbr.split('：',1)[1:])
            if '招标代理联系人：' in strbr:
                content['代理机构'] = ''.join(strbr.split('：',1)[1:])
            if '招标代理联系电话：' in strbr:
                content['代理机构联系方式'] = ''.join(strbr.split('：',1)[1:])
            if '项目实施地点：' in strbr or '项目地点：' in strbr or '建设地点：':
                content['项目地点'] = re.findall(r"地点：(.*)[。]", strbr)
                if len(content['项目地点']) >= 1:
                    content['项目地点'] =  content['项目地点'][0]
                else:
                    content['项目地点'] = ''
            if '网上递交：' in strbr:
                content['投标地点'] = re.findall(r"地[址点] (.*)[。]", strbr)
                if len(content['投标地点']) >= 1:
                    content['投标地点'] =  content['投标地点'][0]
                else:
                    content['投标地点'] = ''
            if '凡有意参加投标者，' in strbr:
                content['标书发售方式'] =strbr
                times = re.findall(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})",strbr)
                content['招标文件获取开始时间'] = time.strftime("%Y-%m-%d", time.strptime(remove1(times[0]), "%Y-%m-%d %H:%M"))
                if content['招标文件获取开始时间'] == '':
                    content['招标文件获取开始时间'] = None
                content['招标文件获取截止时间'] = time.strftime("%Y-%m-%d", time.strptime(remove1(times[1]), "%Y-%m-%d %H:%M"))
                if content['招标文件获取截止时间'] == '':
                    content['招标文件获取截止时间'] = None
            if '投标文件递交的截止时间' in strbr:
                times = re.findall(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})",strbr)
                content['投标截止时间'] = times[0]
            if '其他：' in strbr:
                content['其他说明'] = ''.join(strbr.split('：',1)[1:])
        # 匹配关键字段
        content['项目名称'] = re.sub(r'招标公告|公告','',content['公告标题'])
        content['项目编号'] = ''
        content['计划工期'] = ''
        content['行政区域'] = ''
        content['标书售价'] = ''
        content['投标地点'] = ''
        content['标书发售地点'] = ''
        content['公告网页URL'] = self.response_url
        content['行政区域'] = '云南省'
        content = process_dict(self.annoucement_type,content)

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
        code_dict['code'] =''.join(self.response_text.xpath('/html/body/div[5]/div').extract())

        return code_dict

    '''
    获取附件信息
    '''
    def getAttachment(self):
        at_dict = []
        item = {}
        attachmentname = self.response_text.xpath('/html/body/div[5]/div/div/div[1]/table[4]/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/a').get()
        item['url'] = self.response_text.xpath('/html/body/div[5]/div/div/div[1]/table[4]/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/a/@href').get() # 附件源地址
        if item['url'] is not None:
            attachmentname = attachmentname.replace(' ','%20')  # 防止url出现空字符
            item['file_type'] = attachmentname[attachmentname.rfind('.') + 1:]
        item['file_size'] = -1
        item['local_path'] = '暂无'
        item['file_name'] = attachmentname

        at_dict.append(item)
        return at_dict

