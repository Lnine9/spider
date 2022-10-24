import re

from BaseSpider.base_component.SubResolver import SubResolver
from BaseSpider.base_component.announcement_page_resolver.ZGZF_Annoucement.getValue import standardization
from BaseSpider.tool.DealDate import get_one_time_from_str
import BaseSpider.base_component.announcement_sub_resolver.GGZY_Announcement.util as util
from BaseSpider.tool.judge_tool.content_count import content_count


class GGZY_WinBid_GCJS_sub_component1(SubResolver):

    def __init__(self):
        self.content = {}

        self.wb_supp = []

        self.countlist = ['title', 'proj_name', 'proj_code', 'opening_time', 'notice_period', 'price_ceiling',
                          'proj_unit', 'proj_unit_address',
                          'proj_rel_p', 'proj_rel_m', 'agent_unit_p', 'agent_unit_m', 'agent_unit_address', 'ancm_time']

    def resolver_page(self) -> dict:
        try:
            self.content = standardization(self.getWinBidGovernment())
            code_dict = self.getCodeHtml()
            at_dict = self.get_attach(self.response_text)
            call_unit = self.getCallBidUnit(self.content)

        except Exception as e:
            print(e)
            new_page_attr = {'RB_E': self.content, 'code_dict': {}, 'at_dict': [], 'wb_supp': []}
            self.page_attr.update(new_page_attr)
            return self.page_attr
        else:
            new_page_attr = {'RB_E': self.content, 'code_dict': code_dict, 'at_dict': at_dict, 'wb_supp': self.wb_supp,
                             'call_unit': call_unit}
            self.page_attr.update(new_page_attr)
            return self.page_attr

    def get_attach(self, response_text):
        file_name_list = response_text.xpath("//a[not(text()='原文链接地址')]/text()").extract()
        file_url_list = response_text.xpath("//a[not(text()='原文链接地址')]/@href").extract()

        at_dict = []
        for i in range(len(file_url_list)):
            item = {'url': file_url_list[i],
                    'file_name': file_name_list[i],
                    'file_type': file_name_list[i][file_name_list[i].rfind('.') + 1:],
                    'file_size': -1,
                    'local_path': '暂无'}
            at_dict.append(item)
        return at_dict

    def getWinBidGovernment(self):
        """
        获取WB_G中标信息
        """

        response = self.response_text
        text = response.response.body.decode('utf-8')

        html_list = util.parseHtml_list(text)

        dict_title = util.parse2dict_title(html_list)

        # todo 判断是否表格 替换item


        all_item = util.parse2dict(html_list)

        self.content = {}

        # 复杂数据获取
        self.content['title'] = response.xpath('//h4[@class="h4_o"]/text()').extract_first()
        self.content['proj_name'] = re.sub('(?:中标|结果|公示|公告).*$', '', self.content['title'])
        self.content['proj_item'] = '工程建设'
        self.content['ancm_time'] = get_one_time_from_str(
            response.xpath('//p[@class="p_o"]//span[1]/text()').extract_first())
        self.content['sourse_url'] = self.response_url
        self.content['web_site'] = 'http://www.ggzy.gov.cn/'
        self.content['source_web_name'] = '公共资源交易平台'
        self.content['proj_code'] = util.search_code(html_list)
        ex = response.xpath('//label[@id="platformName"]/text()').extract_first()
        self.content['region'] = util.get_region_from_str(self.content['title'], ex)

        self.content.update(util.process_callbid_other_ex(dict_title))
        self.content.update(util.process_callbid_contact_gcjs(dict_title))
        self.content.update(util.process_winbid_common_GCJS(html_list))

        if 'proj_unit' not in self.content \
                or not self.content['proj_unit'] \
                or self.content['proj_unit'] == '' \
                or not re.search(r'局|政府|公司', self.content['proj_unit']):
            self.content.update(self.process_contact(html_list))

        # 数据格式修改
        self.content['opening_time'] = get_one_time_from_str(self.content['opening_time'])
        self.content['ancm_time'] = get_one_time_from_str(self.content['ancm_time'])
        self.content['proj_unit'] = re.sub(r'[^\u4e00-\u9fa5|,]+', '', self.content['proj_unit'])
        self.content['agent_unit_p'] = re.sub(r'[^\u4e00-\u9fa5|,]+', '', self.content['agent_unit_p'])

        resolution_rate = content_count(self.content, self.countlist)
        self.content['resolution_rate'] = '%.2f' % resolution_rate

        self.wb_supp = []
        wb_supp = util.get_wb_supplier(html_list)
        if 'supp_name' in wb_supp:
            self.wb_supp.append(wb_supp)

        return self.content

    def clean_content(self, standard_content):
        for key in list(self.content.keys()):
            if key not in standard_content:
                del self.content[key]

    def getCodeHtml(self):
        code_dict = {}

        code_dict['url'] = self.response_url
        code_dict['file_type'] = self.response_url[self.response_url.rfind('.') + 1:]
        code_dict['file_size'] = '-1'
        code_dict['local_path'] = '暂无'
        code_dict['code'] = self.response_text.xpath('//div[@class="detail"]').extract_first()

        return code_dict

    def process_contact(self, html_list: list):
        item = {}
        for row in html_list:
            row = re.sub(r'\s+', '', row)
            if 'proj_unit' not in item:
                proj_unit = re.findall(r'招标人(?:[:：]|名称|)(.*?(?:公司|局|政府|[，。；]))', row)
                if len(proj_unit) > 0:
                    item['proj_unit'] = proj_unit[0]

            if 'proj_rel_m' not in item:
                proj_rel_m = re.findall(r'招标人(?:联系|)电话(?:[:：]|)([\d-]+)', row)
                if len(proj_rel_m) > 0:
                    item['proj_rel_m'] = proj_rel_m[0]

            if 'agent_unit_p' not in item:
                agent_unit = re.findall(r'代理机构(?:名称|信息|)(?:[:：]|)(.*?(?:公司|[，。；]))', row)
                if len(agent_unit) > 0:
                    item['agent_unit_p'] = agent_unit[0]

            if 'agent_unit_m' not in item:
                agent_unit_m = re.findall(r'代理机构(?:联系|)电话(?:[:：]|)([\d-]+)', row)
                if len(agent_unit_m) > 0:
                    item['agent_unit_m'] = agent_unit_m[0]

        return item

    def getCallBidUnit(self, content):
        call_unit = {}
        if 'proj_unit' in content and not content['proj_unit'] == '':
            call_unit['name'] = content['proj_unit']
            call_unit['code'] = content['proj_unit']
        else:
            return {}
        if 'proj_unit_address' in content and not content['proj_unit_address'] == '':
            call_unit['address'] = content['proj_unit_address']
        else:
            return {}

        return call_unit
