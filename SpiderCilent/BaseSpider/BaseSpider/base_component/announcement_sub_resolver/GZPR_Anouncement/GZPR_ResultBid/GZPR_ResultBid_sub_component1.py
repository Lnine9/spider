import re

from BaseSpider.base_component.SubResolver import SubResolver
from BaseSpider.tool import DealDate, changeNumberType
from BaseSpider.tool.DealDate import get_one_time_from_str

CONST_PARAM = {
    # 公告标题参数
    'TITLE': '',
}


class GZPRCallBidSubComponent1(SubResolver):
    code = 'true'
    result = ''

    def resolver_page(self) -> dict:
        content = self.getContent()
        wb_supp = self.getWbSupp()
        code_dict = self.getCodeHtml()
        at_dict = self.getAttachment()
        new_page_attr = {'RB_E': content, 'wb_supp': wb_supp, 'code_dict': code_dict, 'at_dict': at_dict}
        self.page_attr.update(new_page_attr)
        print(new_page_attr)
        return self.page_attr

    def getContent(self):
        response = self.response_text
        # 获取文本 text
        text_str = ''.join(response.xpath('//*[@class="view_con"]/*[name(.)!="style"]//text()').extract())
        text_str = text_str.replace('\n', ' ').replace('\r', ' ').replace('\t', '').replace('\xa0', '')
        text = text_str.split(' ')
        text = [i for i in text if i != '']

        contents = {}
        # 设置基本信息
        self.BaseInfo(contents)
        # 添加公告名称及code
        self.content_set_name_and_code(contents, text)
        # 添加联系人信息
        self.contentSetPM(contents, text)

        time_str = text_str[text_str.find("于"):text_str.find('开标')]
        contents['opening_time'] = DealDate.get_one_time_from_str(time_str)

        contents['notice_period'] = ''  # 未找到
        contents['price_ceiling'] = ''  # 未找到
        return contents

    def content_set_name_and_code(self, contents, text):
        contents['proj_name'] = ""
        contents['proj_code'] = ""
        if "项目" in contents['title']:
            contents['proj_name'] = contents['title'][:contents['title'].rfind("项目") + 2]
        elif "中标候选人公示" in contents['title']:
            contents['proj_name'] = contents['title'][:contents['title'].rfind("中标候选人公示")]
        if text[2][0] == '的':
            name_code = text[2][1:]
            regex_str = ".*?([\u4E00-\u9FA5]+).*?"
            name_code_list = re.split(regex_str, name_code)
            if not contents['title']:
                contents['proj_name'] = ''.join(name_code_list[:-1])
            contents['proj_code'] = name_code_list[-1].replace('）', '')

    def contentSetPM(self, contents, text):
        contents['proj_rel_p'] = ""
        i = 0
        for i in range(len(text)):
            if "招标人：" in text[i]:
                contents['proj_unit'] = text[i][text[i].find('：') + 1:]
                i += 1
                break
        contents['proj_rel_m'] = ""
        if i != len(text) and '电话：' in text[i]:
            contents['proj_rel_m'] = text[i][text[i].find('：') + 1:]

        for i in range(len(text)):
            if '代理机构：' in text[i]:
                break
        string = text[i][text[i].find('：') + 1:]
        if string:
            contents['agent_unit_p'] = string
            i += 1
            if i != len(text) and '电话：' in text[i]:
                contents['agent_unit_m'] = text[i][text[i].find('：') + 1:]
            else:
                contents['agent_unit_m'] = ""
        elif '：' not in text[i + 1]:
            contents['agent_unit_p'] = text[i + 1]
            i += 2
            if i != len(text) and '电话：' in text[i]:
                contents['agent_unit_m'] = text[i][text[i].find('：') + 1:]
            else:
                contents['agent_unit_m'] = ""
        else:
            contents['proj_unit'] = ""
            contents['agent_unit_m'] = ""

    def getWbSupp(self):
        response = self.response_text
        text_str = ''.join(response.xpath('//*[@class="view_con"]/*[name(.)!="style"]//text()').extract())

        text_str = text_str.replace('\n', ' ').replace('\r', ' ').replace('\t', '').replace('\xa0', '')
        text = text_str.split(' ')
        text = [i for i in text if i != '']
        lists = []
        index_list = []
        for i in range(len(text)):
            if '中标候选人：' in text[i]:
                index_list.append(i)
        for index in index_list:
            person = {}
            name = text[index]
            person['supp_name'] = name[name.find('：') + 1:]
            key = name[:name.find('：')]
            number = re.findall(r'\d+', changeNumberType.change_number_in_str(key))
            person['supp_ranking'] = ""
            if number:
                person['supp_ranking'] = number[0]
            person['supp_amount'] = ""
            for i in range(len(text) - index):
                v_i = i + index
                if '投标报价（元）/下浮率：' in text[v_i]:
                    person['supp_amount'] = text[v_i][text[v_i].find('：') + 1:]
                    if ';' in person['supp_amount']:
                        person['supp_amount'] = person['supp_amount'][:person['supp_amount'].find(';')]
            lists.append(person)
        return lists

    def getCodeHtml(self):
        code_dict = {}

        code_dict['url'] = self.response_url
        code_dict['file_type'] = 'html'
        code_dict['file_size'] = '-1'
        code_dict['local_path'] = '暂无'
        code_dict['code'] = ''.join(self.response_text.xpath('//*[@class="con_box"]').extract())

        return code_dict

    def getAttachment(self):
        response = self.response_text
        at_dict = []
        fileName = response.xpath('//*[@class="file"]/a/text()').extract()
        fileUrl = response.xpath('//*[@class="file"]/a/@href').extract()
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

    def BaseInfo(self, content):
        """
        设置标题、发布时间、url来源网址
        :param response:
        :param content:
        :return:
        """
        response = self.response_text
        content['title'] = response.xpath('normalize-space(//div[@class="title"]/h3//text())').get()
        content['ancm_time'] = get_one_time_from_str(response.xpath("//*[@class='fbrq']").get())
        content['sourse_url'] = self.response_url
        content['web_site'] = 'http://ggzy.guizhou.gov.cn/'
        content['source_web_name'] = '贵州省公共资源交易信息网'
