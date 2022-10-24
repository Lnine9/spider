from BaseSpider.base_component.SubResolver import SubResolver
from BaseSpider.base_component.utils.util import k_remove, remove1, remove
from BaseSpider.tool.param_tool import process_dict
import time


CONST_PARAM = {
    # 公告标题参数
    'TITLE': '//*[@id="bt_be"]/div/text()',
}

class YN_TenderBid_sub_component1(SubResolver):


    def resolver_page(self) -> dict:
        try:
            content = self.getCallBidGovernment()
            code_dict = self.getCodeHtml()
            at_dict = self.getAttachment()
            content['web_site']='http://www.ccgp-yunnan.gov.cn/'
            content['source_web_name']='云南省政府采购系统'

            new_page_attr = {'CB_G':content,'code_dict':code_dict,'at_dict':at_dict}
            self.page_attr.update(new_page_attr)
        except:
            return self.page_attr

        return self.page_attr


    '''
    获取CB_G采购信息
    '''
    def getCallBidGovernment(self):
        title = self.response_text.xpath(CONST_PARAM.get('TITLE'))
        content = {'公告标题': title}

        # 形成字典
        for each in self.response_text.xpath('//*[@id="searchPanel"]/div'):
            key = k_remove(str(each.xpath('./label/text()').get()))
            value = remove1(each.xpath('normalize-space(./div[1]/text())').get())
            content[key] = value
        content['获取资格预审文件/招标文件/谈判文件/磋商文件开始时间或者询价公告报名开始时间'] = self.response_text.xpath('//*[@id="bctb"]/div[1]/div/text()').get()
        content['获取资格预审文件/招标文件/谈判文件/磋商文件结束时间或者询价公告报名结束时间'] = self.response_text.xpath('//*[@id="bcte"]/div[1]/div/text()').get()
        content['开标时间'] = self.response_text.xpath('//*[@id="bcot"]/div[1]/div/text()').get()
        content['品目'] = remove(self.response_text.xpath('//*[@id="pin"]/div/div/text()').get())
        content['响应文件递交结束时间'] = self.response_text.xpath('//*[@id="brfct"]/div[1]/div/text()').get()
        # 时间格式转化为YY-MM-DD
        try:
            content['开标时间'] = time.strftime("%Y-%m-%d", time.strptime(remove1(content['开标时间']), "%Y-%m-%d %H:%M:%S"))
        except:
            content['开标时间'] = None
        try:
            content['获取资格预审文件/招标文件/谈判文件/磋商文件开始时间或者询价公告报名开始时间'] = time.strftime("%Y-%m-%d", time.strptime(remove1(content['获取资格预审文件/招标文件/谈判文件/磋商文件开始时间或者询价公告报名开始时间']), "%Y-%m-%d %H:%M:%S"))
        except:
            content['获取资格预审文件/招标文件/谈判文件/磋商文件开始时间或者询价公告报名开始时间'] = None
        try:
            content['获取资格预审文件/招标文件/谈判文件/磋商文件结束时间或者询价公告报名结束时间'] = time.strftime("%Y-%m-%d", time.strptime(remove1(content['获取资格预审文件/招标文件/谈判文件/磋商文件结束时间或者询价公告报名结束时间']), "%Y-%m-%d %H:%M:%S"))
        except:
            content['获取资格预审文件/招标文件/谈判文件/磋商文件结束时间或者询价公告报名结束时间'] = None
        if content['响应文件递交结束时间'] == '\r\n\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t':
            content['响应文件递交结束时间'] = None
        content['行政区域'] = '云南省'

        # 匹配关键字段
        content = process_dict(self.annoucement_type,content)
        content['budget'] = content['budget']+'(万元)'
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
