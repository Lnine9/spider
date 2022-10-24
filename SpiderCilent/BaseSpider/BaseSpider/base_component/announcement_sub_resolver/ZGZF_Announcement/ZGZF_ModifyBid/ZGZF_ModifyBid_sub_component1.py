import re

from BaseSpider.base_component.SubResolver import SubResolver
from BaseSpider.base_component.announcement_page_resolver.ZGZF_Annoucement import getValue
from BaseSpider.base_component.announcement_page_resolver.ZGZF_Annoucement.getValue import standardization
from BaseSpider.base_component.announcement_page_resolver.ZGZF_Annoucement.table_contents import \
    transverse_table_contents, simple_direction_table_contents
from BaseSpider.base_component.announcement_page_resolver.ZGZF_Annoucement.text_contents import search_all_by_xpath, \
    dismantling
from BaseSpider.tool.DealDate import get_one_time_from_str
from BaseSpider.tool.param_tool import process_dict_mo


CONST_PARAM = {
    # 公告标题参数
    'TITLE': '//*[@class="tc"][1]/text()',
}


class ZGZF_Announce_Resolver_ModifyBid_component1(SubResolver):
    def __init__(self):
        self.content = {"proj_name": None, "proj_code": None, "proj_item": None, "region": None, "ancm_time": None,
               "proj_rel_p": None, "proj_rel_m": None, "agent_unit_p": None, "agent_unit_m": None, "other_ex": None,
               "purchase_m": None, "sourse_url": None, "title": None, "modify_content": None, "origin_announce_time": None,
               "agent_unit_name": None, "agent_unit_address": None, "purchasing_unit_name": None,"call_unit_address": None,
               'web_site': 'http://http://www.ccgp.gov.cn/', 'source_web_name': '中国政府采购网'
               }

    def resolver_page(self) -> dict:
        try:
            content = standardization(self.getModifyBidGovernment())
            code_dict = self.getCodeHtml()
            at_dict = self.getAttachment()
        except:
            return self.page_attr
        else:
            new_page_attr = {'MB_G': content, 'code_dict': code_dict, 'at_dict': at_dict}
            # print(new_page_attr)
            self.page_attr.update(new_page_attr)
            return self.page_attr

    '''
    获取MB_G更正信息
    '''

    def getModifyBidGovernment(self):
        response = self.response_text
        # 页面解析
        item1 = transverse_table_contents(response)
        item2 = dismantling(response, 'p', '：')
        # 普通数据获取
        all_item = getValue.dictionary_dict(item1, item2)
        content = process_dict_mo(all_item)
        # 复杂数据获取
        # print(self.response_url)
        content['title'] = response.xpath('//*[@class="tc"][1]/text()').get()
        content['proj_name'] = response.xpath('//div[@class="table"]//table//tr[2]/td[2]/text()').get()
        content['sourse_url'] = self.response_url
        content['purchase_m'] = '更正'
        other_info = search_all_by_xpath('其它补充事宜', '联系方式', response, 'p', '')

        content['other_ex'] = other_info.replace('\n', ' ')
        content['modify_content'] = search_all_by_xpath('更正信息', '其它补充事宜', response, 'p', '', 2)
        if content['modify_content'] == '':
            content['modify_content'] = search_all_by_xpath('更正内容', '更正日期', response, 'p', '', 2)
        if content['modify_content'] == '':
            content['modify_content'] = search_all_by_xpath('更正事项、内容', '其它补充事宜', response, 'p', '', 2)
        content['web_site'] = 'http://http://www.ccgp.gov.cn/'
        content['source_web_name'] = '中国政府采购网'

        # 获取项目编号
        content['proj_code'] = getValue.get_proj_code(response)

        # # 数据格式修改
        content['ancm_time'] = get_one_time_from_str(content['ancm_time'])
        content['origin_announce_time'] = get_one_time_from_str(content['origin_announce_time'])
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
