from lxml import etree

from BaseSpider.base_component.announcement_sub_resolver.GZPR_Anouncement.GZPR_CallBid.gzpr_tools import *
from BaseSpider.base_component.announcement_sub_resolver.GZPR_Anouncement.base.parser_architecture import \
    ParserArchitecture
from BaseSpider.base_component.announcement_sub_resolver.GZPR_Anouncement.base.parsing_annotation import field_tag, \
    table_tag
from BaseSpider.tool import DealDate


class GZPRCallBidSubComponent1(ParserArchitecture):
    def resolver_page(self) -> dict:
        content = self.get_block(1)['dict']
        code_dict = self.get_block(2)['dict']
        at_dict = self.get_block(3)['list']
        new_page_attr = {'CB_E': content, 'code_dict': code_dict, 'at_dict': at_dict}
        self.page_attr.update(new_page_attr)
        print(new_page_attr)
        return self.page_attr
        # return self.update_version(version='0')

    def url(self):
        """
        网址url
        :return:
        """
        return self.response_url

    @field_tag(resolution_version=1,
               fields=['title', 'web_site', 'source_web_name', 'ancm_time', 'source_url', 'sourse_url'],
               subordination_table='call_bid_engineering', fields_order=1, block_number=1)
    def anc_info(self):
        """
        公告信息
        :return:
        """
        info = {}
        info['title'] = self.response_text.xpath('normalize-space(//div[@class="title"]/h3//text())').get()
        info['web_site'] = 'http://ggzy.guizhou.gov.cn/'
        info['source_web_name'] = '贵州省公共资源交易信息网'
        info['ancm_time'] = DealDate.get_one_time_from_str(self.response_text.xpath("//*[@class='fbrq']").get())
        info['sourse_url'] = self.url()
        return info

    @field_tag(resolution_version=1, fields=['proj_name', 'proj_code', 'proj_place', 'resource_from', 'ET', 'region'],
               subordination_table='call_bid_engineering', fields_order=2, block_number=1)
    def project_info(self):
        """
        项目信息
        :return:
        """
        response = self.response_text
        lists = response.xpath('//*[@class="view_con"]/*[name(.)!="style"]').extract()
        if len(lists) == 1:
            lists = response.xpath('//*[@class="view_con"]/*/*[name(.)!="style"]').extract()
        text = []
        for l in lists:
            selector = etree.HTML(l)
            text.append(''.join(selector.xpath('//text()')))
        for i in range(len(text)):
            text[i] = text[i].replace('\n', '').replace('\r', '').replace('\t', '').replace('\xa0', '').replace('  ',
                                                                                                                ' ')
        info = {}
        title = self.response_text.xpath('normalize-space(//div[@class="title"]/h3//text())').get()  # 公告标题

        content = self.response_text.xpath('//*[@id="Zoom"]')
        proj_name_name = ['项目名称：', '项目名称:']
        info['proj_name'] = get_one_point_str(search_in_list(text, proj_name_name), proj_name_name)
        if info['proj_name']:  # 去除key
            info['proj_name'] = splitString(info['proj_name'])[1]
        else:  # 切割标题
            info['proj_name'] = info['title'].replace('招标公告', '').replace('公告', '')
        info['proj_name'] = first_end(info['proj_name'])

        # 资金来源
        resource_from_name = ['资金来源']
        info['resource_from'] = get_one_point_str(search_in_list(text, resource_from_name), resource_from_name)
        if info['resource_from']:  # 去除key
            info['resource_from'] = splitString(info['resource_from'])[1]
        info['resource_from'] = first_end(info['resource_from'])

        # 项目编号  R
        proj_code_name = ['项目编号：', '项目编号:', '招标编号：']
        info['proj_code'] = get_one_point_str(search_in_list(text, proj_code_name), proj_code_name)
        if info['proj_code']:  # 去除key
            info['proj_code'] = splitString(info['proj_code'])[1]
        info['proj_code'] = first_end(info['proj_code'])
        info['proj_code'] = delete_chinese_char(info['proj_code']).replace('()', '').replace('（）', '')

        # 项目地点
        proj_place_name = ['项目地点：', '项目地点:', '工程地点']
        info['proj_place'] = get_one_point_str(search_in_list(text, proj_place_name), proj_place_name)
        if info['proj_place']:  # 去除key
            info['proj_place'] = splitString(info['proj_place'])[1]
        info['proj_place'] = first_end(info['proj_place'])

        # 工期
        ET_name = ['计划工期', '设计周期']
        info['ET'] = get_one_point_str(search_in_list(text, ET_name), ET_name)
        if info['ET']:  # 去除key
            info['ET'] = info['ET'][len(splitString(info['ET'])[0]) + 1:]
        if '； ' in info['ET']:
            info['ET'] = info['ET'][:info['ET'].find('； ')]  # 部分网页需要结束符

        info['region'] = search_in_list(text, ['行政区域'])
        if not info['region']:
            info['region'] = '贵州省'
        else:
            info['region'] = first_end(info['region'])

        return info

    @field_tag(resolution_version=1,
               fields=['proj_unit', 'proj_unit_address', 'proj_rel_p', 'proj_rel_m', 'agent_unit', 'agent_unit_p',
                       'agent_unit_m', 'agent_unit_address'],
               subordination_table='call_bid_engineering', fields_order=3, block_number=1)
    def contact(self):
        """
        联系人信息
        :return:
        """
        response = self.response_text
        contact_next_one = '//*[@id="Zoom"]//*[contains(.,"联系方式")]/following-sibling::*[1]'
        contact_next_one_info = response.xpath(contact_next_one)
        table_type_info = contact_next_one_info.xpath('//table//text()').extract()
        p_type = '//*[@id="Zoom"]//*[contains(.,"联系方式")]/following-sibling::p//text()'
        p_type_info = response.xpath(p_type).extract()
        contact_data = table_type_info + p_type_info
        title = ['招标代理机构', '代理机构', '该项目联系人', '该项目联系电话', '招标人', '地址', '联系人', '电话', '发布日期', '传真', '招标代理', '邮编', '：', ':']

        # 定义变量
        proj_rel_name = None  # 采购单位名称
        proj_rel_p = None
        proj_rel_m = None
        proj_rel_address = None  # 采购单位地址
        agent_unit = None
        agent_unit_p = None
        agent_unit_m = None
        agent_unit_address = None

        proj_rel_name_number = getListIndex(['招标人'], contact_data)
        if proj_rel_name_number:
            proj_rel_name = deleteKeyWords(contact_data[proj_rel_name_number[0]], title)

        agent_unit_number = getListIndex(['代理机构', '招标代理'], contact_data)
        if agent_unit_number:
            agent_unit = deleteKeyWords(contact_data[agent_unit_number[0]], title)

        address_number = getListIndex(['地址'], contact_data)
        if address_number:
            proj_rel_address = deleteKeyWords(contact_data[address_number[0]], title)
            if len(address_number) >= 2:
                agent_unit_address = deleteKeyWords(contact_data[address_number[1]], title)

        p_number = getListIndex(['联系人'], contact_data)
        if p_number:
            proj_rel_p = deleteKeyWords(contact_data[p_number[0]], title)
            if len(p_number) >= 2:
                agent_unit_p = deleteKeyWords(contact_data[p_number[1]], title)

        m_number = getListIndex(['电话'], contact_data)
        if m_number:
            proj_rel_m = deleteKeyWords(contact_data[m_number[0]], title)
            if len(m_number) >= 2:
                agent_unit_m = deleteKeyWords(contact_data[m_number[1]], title)
        content = {}
        content['proj_unit'] = proj_rel_name
        content['proj_rel_p'] = proj_rel_p
        content['proj_rel_m'] = proj_rel_m
        content['proj_unit_address'] = proj_rel_address
        content['agent_unit'] = agent_unit
        content['agent_unit_p'] = agent_unit_p
        content['agent_unit_m'] = agent_unit_m
        content['agent_unit_address'] = agent_unit_address
        return content

    @field_tag(resolution_version=1,
               fields=['tender_place', 'bid_sale_m', 'bid_sale_op_time', 'bid_sale_en_time', 'bid_price',
                       'bid_sale_place', 'bid_end_time'], subordination_table='call_bid_engineering', fields_order=4,
               block_number=1)
    def bid_info(self):
        """
        标书信息
        :return:
        """
        info = {}
        sale_begin_title = ['招标文件的获取']
        sale_begin = self.response_text.xpath(
            '//*[@id="Zoom"]//*[' + get_contains_str(sale_begin_title) + ']/following-sibling::*//text()').extract()
        for i in range(len(sale_begin)):
            sale_begin[i] = sale_begin[i].replace('\n', '') \
                .replace('\r', '').replace('\t', '') \
                .replace('\xa0', '').replace('  ', ' ')
        info['tender_place'] = splitString(search_with_start_and_end(sale_begin, ['递交投标文件', '地点']))[-1]
        if not info['tender_place']:
            info['tender_place'] = splitString(search_with_start_and_end(sale_begin, ['投标文件递交', '地点']))[-1]
        info['bid_end_time'] = DealDate.get_one_time_from_str(
            search_with_start_and_end(sale_begin, ['递交', '投标文件', '截止时间为'], end=['。']))

        info['bid_sale_op_time'] = DealDate.get_one_time_from_str(
            search_with_start_and_end(sale_begin, ['（一）招标文件', '于'], end=['至']))
        if not info['bid_sale_op_time']:
            info['bid_sale_op_time'] = DealDate.get_one_time_from_str(
                search_with_start_and_end(sale_begin, ['有意', '于'], end=['至']))
        info['bid_sale_en_time'] = DealDate.get_one_time_from_str(
            search_with_start_and_end(sale_begin, ['（一）招标文件', '于', '至'], end=['在']))
        if not info['bid_sale_en_time']:
            info['bid_sale_en_time'] = DealDate.get_one_time_from_str(
                search_with_start_and_end(sale_begin, ['有意参加', '于', '至'], end=['在']))

        price = search_with_start_and_end(sale_begin, ['招标文件', '售价'])
        if price:
            info['bid_price'] = '招标文件' + price
        else:
            info['bid_price'] = ''
        info['bid_sale_place'] = search_with_start_and_end(sale_begin, ['招标文件', '于', '至', '在'])
        if not info['bid_sale_place']:
            info['bid_sale_place'] = search_with_start_and_end(sale_begin, ['有意', '于', '至', '在'])

        # 未找到字段
        info['bid_sale_m'] = ''
        return info

    @field_tag(resolution_version=1, fields=['other_ex'], subordination_table='call_bid_engineering', fields_order=6,
               block_number=1)
    def other(self):
        """
        其他
        :return:
        """
        contents = {}
        contents['other_ex'] = ''
        return contents

    @field_tag(resolution_version=1, fields=['file_type', 'file_size', 'url', 'local_path', 'code'],
               subordination_table='code_html', fields_order=1, block_number=2)
    def code_html_dict(self):
        """
        code_html_dict
        :return:
        """
        code_dict = {}

        code_dict['url'] = self.response_url
        code_dict['file_type'] = 'html'
        code_dict['file_size'] = '-1'
        code_dict['local_path'] = '暂无'
        code_dict['code'] = ''.join(self.response_text.xpath('//*[@class="con_box"]').extract())

        return code_dict

    @field_tag(resolution_version=1, fields=['file_name', 'file_type', 'file_size', 'url', 'local_path'],
               subordination_table='attachment', fields_order=1, block_number=3)
    def attachment_dict(self):
        """
        附件字典
        :return: list
        """
        at_dict = []
        fileName = self.response_text.xpath('//*[@class="file"]/a/text()').extract()
        fileUrl = self.response_text.xpath('//*[@class="file"]/a/@href').extract()
        for i in range(0, len(fileName)):
            item = {}
            if fileUrl[i] is not None:
                fileName[i] = fileName[i]
                fileName[i] = fileName[i].replace(' ', '%20')  # 防止url出现空字符
                item['file_name'] = fileName[i]
                item['file_type'] = fileName[i][fileName[i].rfind('.') + 1:]
                item['url'] = fileUrl[i]
            item['file_size'] = -1
            item['local_path'] = '暂无'
            at_dict.append(item)
        return at_dict

    @table_tag(table='call_bid_engineering', table_order=1)
    def anc_table(self):
        """
        公告表
        :param needs:
        :return:
        """
        pass

    @table_tag(table='code_html', table_order=2)
    def code_html(self):
        """
        code_html表
        :param needs:
        :return:
        """
        pass

    @table_tag(table='attachment', table_order=3)
    def attachment(self):
        """
        附件表
        :param needs:
        :return:
        """
        pass
