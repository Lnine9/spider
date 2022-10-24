import re

from BaseSpider.base_component.SubResolver import SubResolver
from BaseSpider.tool import param_tool

CONST_PARAM = {
    # 公告标题参数
    'TITLE': '//div[@class="you"]/div/div/h3/text()',

    # 公告时间
    'Publish_Time': '/html/body/div[3]/div/div[2]/div[1]/div/div[2]/text()',

    #代理机构联系人、联系方式
    'Agent':'//*[@id="info"]/ul/li[14]/ul/li[2]/text()',
    'Agent_re': '//*[@id="info"]/ul/li[14]/ul/li[3]/text()',

    #公告url
    'Announcement_Url': '/html/head/script[8]/text()',
}


class GZ_SJ_Modify_Sub_Component_Base(SubResolver):
    def resolver_page(self) -> dict:

        agent = ''
        if self.response_text.xpath(CONST_PARAM.get('Agent')).get() is not None:
            agent = self.response_text.xpath(CONST_PARAM.get('Agent')).get()
        elif self.response_text.xpath('//*[@id="info"]/ul/li[13]/ul/li[2]/text()').get() is not None:
            agent = self.response_text.xpath('//*[@id="info"]/ul/li[13]/ul/li[2]/text()').get()

        agency = ''
        if self.response_text.xpath(CONST_PARAM.get('Agent_re')).get() is not None:
            agency = self.response_text.xpath(CONST_PARAM.get('Agent_re')).get()
        elif self.response_text.xpath('//*[@id="info"]/ul/li[13]/ul/li[3]/text()').get() is not None:
            agency = self.response_text.xpath('//*[@id="info"]/ul/li[13]/ul/li[3]/text()').get()



        # 差品目、行政区域、其他说明
        content = {'公告标题': self.getTitle(),
                   '项目名称':  self.get_projec_name(),
                   '项目编号': self.get_poj_code(),
                   # '品目': self.get_item(),
                   '行政区域': self.get_unit(),
                   # '其他说明': self.get_other(),
                   '采购单位名称': self.get_unit(),
                   '公告发布时间': self.get_publish_times(),
                   '项目联系人': self.get_poj_rel(),
                   '项目联系电话': self.get_rel_num(),
                   '代理机构联系人': self.get_agency(),
                   '代理机构联系方式': agent + ' ' + agency,
                   '代理机构名称': self.get_agent_name(),
                   '代理机构地址': self.get_agent_address(),
                   '采购方式': self.get_call_way(),
                   '公告网页URL': self.get_url(),
                   '更正内容': self.get_modify_content(),
                   '首次公告日期': self.get_open_time(),
                   }

        code_dict = {'code': ''.join(self.response_text.xpath('//*[@id="info"]').extract()), 'file_type': 'html',
                     'file_size': '-1', 'url': self.get_url(), 'local_path': '暂无'}

        at_dict = self.get_at_dict(code_dict['code'])

        content = param_tool.process_dict('MB_G', content)
        content['source_web_name'] = '贵州省政府采购网'
        content['web_site'] = 'http://www.ccgp-guizhou.gov.cn/'

        new_page_attr = {'MB_G': content, 'code_dict': code_dict, 'at_dict': at_dict, 'result': [], 'code': 'true'}
        self.page_attr.update(new_page_attr)
        return self.page_attr

    # 获得公告标题
    def getTitle(self):
        title = self.response_text.xpath(CONST_PARAM.get('TITLE')).get()

        return title.strip()
    # 获得采购项目名称
    def get_projec_name(self):
        project_name = self.response_text.xpath('//*[@id="info"]/ul[1]/li[1]').get()

        re = project_name
        reIndex = len(re)
        start_index = re.find('</span>', 0, reIndex)
        end_index = re.find('</li>', start_index, reIndex)
        project_name = re[start_index + 7:end_index].strip()

        return project_name

    # 获得项目编号
    def get_poj_code(self):
        poj_code = self.response_text.xpath('//*[@id="info"]/ul/li[4]').get()

        re = poj_code
        reIndex = len(re)
        start_index = re.find('</span>', 0, reIndex)
        end_index = re.find('</li>', start_index, reIndex)
        poj_code = re[start_index + 7:end_index].strip()

        return poj_code

    def get_agent_name(self):
        name = ''
        if self.response_text.xpath('//*[@id="info"]/ul/li[14]').get() is not None and '代理机构' in self.response_text.xpath('//*[@id="info"]/ul/li[14]').get():
            name = self.response_text.xpath('//*[@id="info"]/ul/li[14]/text()[2]').get()
            name = name.strip()
        elif self.response_text.xpath('//*[@id="info"]/ul/li[13]').get() is not None and '代理机构' in self.response_text.xpath('//*[@id="info"]/ul/li[13]').get():
            name = self.response_text.xpath('//*[@id="info"]/ul/li[13]/text()[2]').get()
            name = name.strip()

        return name


    def get_agent_address(self):
        address = ''
        if self.response_text.xpath('//*[@id="info"]/ul/li[14]').get() is not None and '代理机构' in self.response_text.xpath('//*[@id="info"]/ul/li[14]').get():
            address = ''.join(self.response_text.xpath('//*[@id="info"]/ul/li[14]/ul/li[1]/text()').extract())
        elif self.response_text.xpath('//*[@id="info"]/ul/li[13]').get() is not None and '代理机构' in self.response_text.xpath('//*[@id="info"]/ul/li[13]').get():
            address = ''.join(self.response_text.xpath('//*[@id="info"]/ul/li[13]/ul/li[1]/text()').extract())

        address = address.strip()

        return address

    # 获得项目联系人
    def get_poj_rel(self):
        poj_rel = self.response_text.xpath('//*[@id="info"]/ul[1]/li[6]').get()

        re = poj_rel
        reIndex = len(re)
        start_index = re.find('</span>', 0, reIndex)
        end_index = re.find('</li>', start_index, reIndex)
        poj_rel = re[start_index + 7:end_index].strip()

        return poj_rel

    # 获得项目联系电话
    def get_rel_num(self):
        poj_rel_num = self.response_text.xpath('//*[@id="info"]/ul[1]/li[7]').get()

        re = poj_rel_num
        reIndex = len(re)
        start_index = re.find('</span>', 0, reIndex)
        end_index = re.find('</li>', start_index, reIndex)
        poj_rel_num = re[start_index + 7:end_index].strip()

        return poj_rel_num

    # 获得发布时间
    def get_publish_times(self):
        publish_times = self.response_text.xpath(CONST_PARAM.get('Publish_Time')).get().split('   ')
        length = len(publish_times[1])
        publish_time = publish_times[1][5:length]

        return publish_time.strip()

    # 获得采购机构
    def get_unit(self):
        unit = ''
        if '采购人名称' in self.response_text.xpath('//*[@id="info"]/ul[1]/li[13]/span/text()').get():
            unit = self.response_text.xpath('//*[@id="info"]/ul[1]/li[13]').get()
        elif '采购人名称' in self.response_text.xpath('//*[@id="info"]/ul[1]/li[12]/span/text()').get():
            unit = self.response_text.xpath('//*[@id="info"]/ul[1]/li[12]').get()

        re = unit
        reIndex = len(re)
        start_index = re.find('</span>', 0, reIndex)
        end_index = re.find('<ul', start_index, reIndex)
        unit = re[start_index + 7:end_index - 7]
        unit = unit.strip()

        return unit

    # 获得采购方式
    def get_call_way(self):
        cal_way = self.response_text.xpath('//*[@id="info"]/ul[1]/li[8]').get()

        re = cal_way
        reIndex = len(re)
        start_index = re.find('</span>', 0, reIndex)
        end_index = re.find('</li>', start_index, reIndex)
        cal_way = re[start_index + 7:end_index].strip()

        return cal_way

    # 获得首次公告日期
    def get_open_time(self):
        open_time = self.response_text.xpath('//*[@id="info"]/ul[1]/li[9]').get()

        re = open_time
        reIndex = len(re)
        start_index = re.find('</span>', 0, reIndex)
        end_index = re.find('</li>', start_index, reIndex)
        open_time = re[start_index + 7:end_index - 3].strip()

        return open_time

    # 获得更正内容
    def get_modify_content(self):
        modify_content = self.response_text.xpath('//*[@id="info"]/ul[1]/li[10]').get()

        re = modify_content
        reIndex = len(re)
        start_index = re.find('<br>', 0, reIndex)
        end_index = re.find('</li>', start_index, reIndex)
        modify_content = re[start_index + 7:end_index].strip()

        return modify_content

    # 获得代理机构
    def get_agency(self):
        agency=''
        if self.response_text.xpath('//*[@id="info"]/ul[1]/li[14]/span/text()').get() is not None and '采购代理机构' in self.response_text.xpath('//*[@id="info"]/ul[1]/li[14]/span/text()').get():
            agency = self.response_text.xpath('//*[@id="info"]/ul[1]/li[14]').get()
        elif '采购代理机构' in self.response_text.xpath('//*[@id="info"]/ul[1]/li[13]/span/text()').get():
            agency = self.response_text.xpath('//*[@id="info"]/ul[1]/li[13]').get()

        aIndex = len(agency)
        a_start_index = agency.find('</span>', 0, aIndex)
        a_end_index = agency.find('<ul', a_start_index, aIndex)

        agency = agency[a_start_index + 7:a_end_index - 7].strip()
        agency = agency.strip()

        return agency

    # 获得品目
    def get_item(self):
        return self.response_text.xpath('//*[@id="info"]/ul/ul[1]/li[1]/text()').get().strip()

    # 获得其他说明
    def get_other(self):
        return self.response_text.xpath('//*[@id="info"]/ul/ul[1]/li/text()').get().strip()

    # 获得公告url
    def get_url(self):
        an_url_json = self.response_text.xpath(CONST_PARAM.get('Announcement_Url')).get()
        json_length = len(an_url_json)
        index = an_url_json.find('contentId', 0, json_length)

        contenId = ''
        if index != -1:
            titleIndex = an_url_json.find('title', index, json_length)
            contenId = an_url_json[index + 12:titleIndex - 3]
        else:
            contenId = '/'

        an_url = 'http://www.ccgp-guizhou.gov.cn/view-1153418052184995-' + contenId + '.html?siteId=1' if contenId != '/' else 'url解析失败'
        return an_url.strip()

    def get_at_dict(self, html):
        at_dict = []
        pattern = '<a.*?href="([^"]*)".*?>([\S\s]*?)</a>'

        href = re.findall(pattern, str(html))

        for atuple in href:
            item = {}
            item['url'] =  'http://www.ccgp-guizhou.gov.cn' + atuple[0]
            files = atuple[1].split('.')
            item['file_name'] = files[0]
            item['file_type'] = files[1]
            item['file_size'] = -1
            at_dict.append(item)
        return at_dict