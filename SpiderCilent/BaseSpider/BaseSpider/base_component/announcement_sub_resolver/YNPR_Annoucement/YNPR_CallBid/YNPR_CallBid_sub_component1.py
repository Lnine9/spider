import re

from BaseSpider.base_component.SubResolver import SubResolver
from BaseSpider.base_component.utils.util import k_remove, remove1
from BaseSpider.tool.param_tool import process_dict
import time


CONST_PARAM = {
    # 公告标题参数
    'TITLE': '/html/body/div[5]/div/h3/text()',
}

class YNPR_CallBid_sub_component1(SubResolver):


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

        for each in self.response_text.xpath('/html/body/div[5]/div/div/div[1]/table/tr'):
            pre = re.compile(r'<[^>]+>',re.S)
            key = k_remove(pre.sub('',each.xpath('./td[1]').get()))
            value = pre.sub('',each.xpath('./td[2]//*[not(@style="display:none")]').get())
            content[key] = value
        content['公告网页URL'] = self.response_url
        content['项目联系人'] = self.response_text.xpath('/html/body/div[5]/div/div/div[1]/table[2]/tr[1]/td[4]/span/text()').get()
        content['项目联系电话'] = self.response_text.xpath('/html/body/div[5]/div/div/div[1]/table[2]/tr[2]/td[2]/span/text()').get()
        content['代理机构'] = self.response_text.xpath('/html/body/div[5]/div/div/div[1]/table[2]/tr[3]/td[4]/span/text()').get()
        content['代理机构联系方式'] = self.response_text.xpath('/html/body/div[5]/div/div/div[1]/table[2]/tr[4]/td[2]/span/text()').get()
        content['招标文件获取截止时间'] = self.response_text.xpath('//*[@id="ggEndTime_span"]/text()').get()
        content['采购单位名称'] = content['建设单位']
        content['代理机构名称'] = content['招标代理机构']
        content['采购单位地址'] = None
        content['代理机构地址'] = None
        content['行政区域'] = '云南省'
        # 时间格式转化为YY-MM-DD
        if '公告发布开始时间' in content:
            content['公告发布开始时间'] = time.strftime("%Y-%m-%d", time.strptime(remove1(content['公告发布开始时间']), "%Y-%m-%d %H:%M"))
        if '招标文件获取截止时间' in content:
            content['招标文件获取截止时间'] = time.strftime("%Y-%m-%d", time.strptime(remove1(content['招标文件获取截止时间']), "%Y-%m-%d %H:%M"))
        # 匹配关键字段
        content = process_dict(self.annoucement_type,content)
        if content['bid_sale_en_time'] == '':
            content['bid_sale_en_time'] = None
        if content['bid_end_time'] == '':
            content['bid_end_time'] = None
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
        count = 0
        attachmentname = self.response_text.xpath('/html/body/div[5]/div/div/div[1]/table[4]//a/text()')
        url = self.response_text.xpath('/html/body/div[5]/div/div/div[1]/table[4]//a/@href')# 附件源地址
        for i in range(0,len(attachmentname)):
            item = {}
            if len(url)>i and url[i] is not None:
                attachmentname[i] = attachmentname[i].get()
                attachmentname[i] = attachmentname[i].replace(' ','%20')  # 防止url出现空字符
                item['file_type'] = attachmentname[i][attachmentname[i].rfind('.') + 1:]
                item['url'] = url[i].get()
            item['file_size'] = -1
            item['local_path'] = '暂无'
            item['file_name'] = attachmentname[i]
            at_dict.append(item)
        return at_dict

