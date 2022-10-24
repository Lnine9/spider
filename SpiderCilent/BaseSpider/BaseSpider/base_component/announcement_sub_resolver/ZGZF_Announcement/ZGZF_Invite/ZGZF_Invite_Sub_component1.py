import re

from BaseSpider.base_component.SubResolver import SubResolver
from BaseSpider.base_component.announcement_page_resolver.ZGZF_Annoucement import getValue
from BaseSpider.base_component.announcement_page_resolver.ZGZF_Annoucement.getValue import standardization, \
    unit_name_standardization
from BaseSpider.base_component.announcement_page_resolver.ZGZF_Annoucement.table_contents import \
    transverse_table_contents, simple_direction_table_contents
from BaseSpider.base_component.announcement_page_resolver.ZGZF_Annoucement.text_contents import search_all_by_xpath, \
    dismantling
from BaseSpider.tool.DealDate import get_one_time_from_str
from BaseSpider.tool.param_tool import process_dict_call


CONST_PARAM = {
    # 公告标题参数
    'TITLE': '//*[@class="tc"][1]/text()',
}


class ZGZF_Invite_Sub_component1(SubResolver):
    def __init__(self):
        self.content = {"proj_name": None, "proj_code": None, "proj_item": None, "call_unit": None,
               "region": None, "ancm_time": None, "budget": None, "proj_rel_p": None,
               "proj_rel_m": None, "agent_unit_p": None, "agent_unit_m": None, "tender_place": None,
               "bid_sale_m": None, "bid_sale_op_time": None, "bid_sale_en_time": None,
               "bid_sale_place": None, "bid_price": None, "bid_place": None, "other_ex": None,
               "purchase_m": None, "sourse_url": None, "bid_time": None, "title": None,
               "agent_unit_name": None, "agent_unit_address": None, "purchasing_unit_name": None,
               "call_unit_address": None,
               'web_site': 'http://http://www.ccgp.gov.cn/', 'source_web_name': '中国政府采购网'
               }

    def resolver_page(self) -> dict:
        try:
            content = standardization(self.getInquiryGovernment())
            code_dict = self.getCodeHtml()
            at_dict = self.getAttachment()


        except:
            return self.page_attr
        else:
            new_page_attr = {'CB_G': content, 'code_dict': code_dict, 'at_dict': at_dict}
            # print(new_page_attr)
            self.page_attr.update(new_page_attr)
            return self.page_attr

    '''
    获取CB_G询价信息
    '''

    def getInquiryGovernment(self):
        response = self.response_text
        # 页面解析
        item1 = transverse_table_contents(response)
        item2 = dismantling(response, 'p', '：')
        # 普通数据获取
        all_item = getValue.dictionary_dict(item1, item2)
        # print(all_item)
        content = process_dict_call(all_item)
        # 复杂数据获取
        # print(self.response_url)
        content['title'] = response.xpath('//*[@class="tc"][1]/text()').get()
        content['proj_name'] = response.xpath("//table//tr[2]/td[2]/text()").get()
        content['sourse_url'] = self.response_url
        content['purchase_m'] = '邀请招标'
        content['bid_end_time'] = search_all_by_xpath('投标截止时间', '开标日期和地点', response, 'p', '').strip()
        content['bid_sale_op_time'] = search_all_by_xpath('获取招标文件时间和地点', '获取招标文件的地点', response, 'p', '').strip()

        sale_file = search_all_by_xpath('获取招标文件', '提交投标文件截止时间、开标时间和地点', response, 'p', '：', 1)
        # print(sale_file)

        if sale_file.get('时间') is not None:
            temp = re.compile(r'（.*）|：|:', re.S).sub('', sale_file.get('时间')).split('至')
            if len(temp) > 1:
                content['bid_sale_op_time'] = temp[0]
                content['bid_sale_en_time'] = temp[1]

        content['bid_sale_place'] = sale_file.get('地点') if content['bid_sale_place'] == '' else content['bid_sale_place']
        content['bid_sale_m'] = sale_file.get('方式') if content['bid_sale_m'] == '' else content['bid_sale_m']
        content['bid_price'] = sale_file.get('售价') if content['bid_price'] == '' else content['bid_price']

        bid_time_place = search_all_by_xpath('提交投标文件截止时间、开标时间和地点', '公告期限', response, 'p', '：', 1)
        # print(bid_time_place)

        content['bid_time'] = bid_time_place.get('开标时间') if content['bid_time'] == '' else content['bid_time']
        content['bid_place'] = bid_time_place.get('地点') if content['bid_place'] == '' else content['bid_place']
        content['tender_place'] = content['bid_place']

        content['web_site'] = 'http://http://www.ccgp.gov.cn/'
        content['source_web_name'] = '中国政府采购网'
        # 获取项目编号
        content['proj_code'] = getValue.get_proj_code(response)
        # 其它补充事宜
        other_info = search_all_by_xpath('其它补充事宜', '', response, 'p', '')
        content['other_ex'] = other_info.split('\n')[1].replace('\n', ' ').replace('  ', ' ') if other_info else None
        # 数据格式修改
        content['ancm_time'] = get_one_time_from_str(content['ancm_time'])
        content['call_unit'] = unit_name_standardization(content['call_unit'])
        content['agent_unit_name'] = unit_name_standardization(content['agent_unit_name'])
        content['bid_sale_op_time'] = get_one_time_from_str(content['bid_sale_op_time'])
        content['bid_sale_en_time'] = get_one_time_from_str(content['bid_sale_en_time'])
        content['bid_time'] = get_one_time_from_str(content['bid_time'])
        content['bid_end_time'] = get_one_time_from_str(content['bid_end_time'])
        content['bid_price'] = getValue.change_money(content['bid_price'])
        content['budget'] = getValue.change_money(content['budget'])

        return content

    '''
    获取源文件信息
    '''

    def getCodeHtml(self):
        code_dict = {}

        code_dict['url'] = self.response_url
        code_dict['file_type'] = code_dict['url'][code_dict['url'].rfind('.') + 1:]
        code_dict['file_size'] = '-1'
        code_dict['local_path'] = '暂无'
        code_dict['code'] = ''.join(self.response_text.xpath('//*[@id="detail"]/div[2]/div/div[2]').extract())

        return code_dict

    '''
    获取附件信息
    '''

    def getAttachment(self):
        file_name_list = self.response_text.xpath('//a[@class="bizDownload"]/text()').extract()
        file_url_list = self.response_text.xpath('//a[@class="bizDownload"]/@id').extract()
        for i, j in enumerate(file_url_list):
            file_url_list[i] = 'http://www.ccgp.gov.cn/oss/download?uuid=' + file_url_list[i]

        at_dict = []
        for i in range(len(file_url_list)):
            item = {}
            item['url'] = file_url_list[i]
            item['file_name'] = file_name_list[i]
            item['file_type'] = file_name_list[i][file_name_list[i].rfind('.') + 1:]
            item['file_size'] = -1
            item['local_path'] = '暂无'
            at_dict.append(item)
        return at_dict


