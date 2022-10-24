import re

from BaseSpider.base_component.SubResolver import SubResolver
from BaseSpider.tool.param_tool import process_dict



CONST_PARAM = {
    # 公告标题参数
    'TITLE': '/html/body/div[5]/div/h3/text()',
}

class YNPR_ResultBid_sub_component2(SubResolver):


    def resolver_page(self) -> dict:
        try:
            content = self.getResultsBidEngineering()
            wb_supp = self.getWbSupplier()
            code_dict = self.getCodeHtml()
            at_dict = self.getAttachment()
            content['web_site']='http://ggzy.yn.gov.cn/'
            content['source_web_name']='云南省公共资源交易电子服务系统'

            new_page_attr = {'RB_E':content,'wb_supp':wb_supp,'code_dict':code_dict,'at_dict':at_dict}
            self.page_attr.update(new_page_attr)
        except:
            return self.page_attr

        return self.page_attr

    '''
     获取RB_E中标信息
     '''
    def getResultsBidEngineering(self):
        title = self.response_text.xpath(CONST_PARAM.get('TITLE')).get()
        content = {'公告标题': title}
        content['发布时间'] = (re.findall(r"发布时间(.*)", self.response_text.xpath('/html/body/div[5]/div/p/text()').get()))[0]

        # 形成字典
        contents = self.response.xpath('/html/body/div[5]/div/div/table/tr/td')
        for item in contents:
            pre = re.compile(r'<[^>]+>',re.S)
            strbr = pre.sub('',item.get())
            if '备案登记编号：' in strbr:
                content['项目编号'] =''.join(strbr.split('：',1)[1:])
        content['项目名称'] = self.response_text.xpath('/html/body/div[5]/div/div/table/tr[5]/td[2]/text()').get()
        content['开标时间'] = self.response_text.xpath('/html/body/div[5]/div/div/table/tr[6]/td[2]/text()').get()
        content['公示期'] = ''
        content['最高限价'] = ''
        content['招标人联系人'] = self.response_text.xpath('/html/body/div[5]/div/div/table/tr[3]/td[2]/text()').get()
        content['招标人联系方式'] = self.response_text.xpath('/html/body/div[5]/div/div/table/tr[3]/td[4]/text()').get()
        content['招标代理机构联系人'] = self.response_text.xpath('/html/body/div[5]/div/div/table/tr[4]/td[2]/text()').get()
        content['招标代理机构联系方式'] = self.response_text.xpath('/html/body/div[5]/div/div/table/tr[4]/td[4]/text()').get()
        content['其他说明'] = self.response_text.xpath('/html/body/div[5]/div/div/table/tr[9]/td[2]/text()').get()
        content['采购单位'] = None
        content['采购单位地址'] = None
        content['代理机构地址'] = None
        # 匹配关键字段
        content = process_dict(self.annoucement_type,content)
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
        code_dict['code'] =''.join(self.response_text.xpath('/html/body/div[5]/div').extract())
        return code_dict

    '''
    获取附件信息
    '''
    def getAttachment(self):
        at_dict = []
        count = 0
        # attachmentname = self.response.xpath('/html/body/div[5]/div/div/div[1]/table[4]//a/text()')
        # url = self.response.xpath('/html/body/div[5]/div/div/div[1]/table[4]//a/@href')# 附件源地址
        # for i in range(0,len(attachmentname)):
        #     item = {}
        #     if len(url)>i and url[i] is not None:
        #         attachmentname[i] = attachmentname[i].get()
        #         attachmentname[i] = attachmentname[i].replace(' ','%20')  # 防止url出现空字符
        #         item['file_type'] = attachmentname[i][attachmentname[i].rfind('.') + 1:]
        #         item['url'] = url[i].get()
        #     item['file_size'] = -1
        #     item['local_path'] = '暂无'
        #     item['file_name'] = attachmentname[i]
        #     at_dict.append(item)
        return at_dict

    def getWbSupplier(self):
        wb_supp = []
        content = {}
        item = {}
        item['supp_name'] = self.response_text.xpath('/html/body/div[5]/div/div/table/tr[8]/td/table/tr[2]/td[1]/text()').get()
        item['supp_code'] = ''
        item['supp_ranking'] = '1'
        item['supp_amount'] = self.response_text.xpath('/html/body/div[5]/div/div/table/tr[8]/td/table/tr[2]/td[6]/text()').get()
        wb_supp.append(item)
        return wb_supp

