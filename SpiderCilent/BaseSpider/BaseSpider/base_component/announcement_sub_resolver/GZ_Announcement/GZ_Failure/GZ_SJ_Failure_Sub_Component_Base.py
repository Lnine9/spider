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


class GZ_SJ_Failure_Sub_Component_Base(SubResolver):
    def resolver_page(self) -> dict:

        # agent = ''
        # if self.response_text.xpath(CONST_PARAM.get('Agent')).get() is not None:
        #     agent = self.response_text.xpath(CONST_PARAM.get('Agent')).get()
        # elif self.response_text.xpath('//*[@id="info"]/ul/li[13]/ul/li[2]/text()').get() is not None:
        #     agent = self.response_text.xpath('//*[@id="info"]/ul/li[13]/ul/li[2]/text()').get()

        agency = ''
        if self.response_text.xpath('//*[@id="info"]/ul/li[4]').get() is not None:
            agency = self.response_text.xpath('//*[@id="info"]/ul/li[4]').get()
        else:
            agency = '无'

        length = len(agency)

        start_index = agency.find('电话：', 0, length)
        agency = agency[start_index + 3: length - 17].strip()

        # 差品目、行政区域、其他说明
        content = {'公告标题': self.getTitle(),
                   '项目名称':  self.get_projec_name(),
                   '项目编号': self.get_poj_code(),
                   '品目': '无',
                   '行政区域': self.get_unit(),
                   '其他说明': '无',
                   '采购单位名称': self.get_unit(),
                   '公告发布时间': self.get_publish_times(),
                   '项目联系人': self.get_poj_rel(),
                   '项目联系电话': self.get_rel_num(),
                   '代理机构联系人': self.get_agency(),
                   '代理机构联系方式': agency,
                   '代理机构名称': self.get_agent_name(),
                   '代理机构地址': self.get_agent_address(),
                   '采购方式': self.get_call_way(),
                   '公告网页URL': self.get_url(),
                   '开标时间': self.get_kai_time(),
                   '流标内容': self.get_failure_content(),
                   }

        code_dict = {'code': ''.join(self.response_text.xpath('//*[@id="info"]').extract()),
                     'file_type': 'html', 'file_size': '-1', 'url': self.get_url(), 'local_path': '暂无'}

        at_dict = self.get_at_dict(code_dict['code'])

        content = param_tool.process_dict('FB_G', content)
        content['source_web_name'] = '贵州省政府采购网'
        content['web_site'] = 'http://www.ccgp-guizhou.gov.cn/'

        new_page_attr = {'FB_G': content, 'code_dict': code_dict, 'at_dict': at_dict}
        self.page_attr.update(new_page_attr)
        return self.page_attr

    # 获得公告标题
    def getTitle(self):
        title = self.response_text.xpath(CONST_PARAM.get('TITLE')).get()
        return title.strip()

    # 获得采购项目名称
    def get_projec_name(self):
        project_name = self.response_text.xpath('//*[@id="info"]/ul/li[2]/text()').get()

        project_name = project_name.split('：')

        result = project_name[1].strip()

        return result

    # 获得项目编号
    def get_poj_code(self):
        poj_code = self.response_text.xpath('//*[@id="info"]/ul/li[1]/text()').get()

        poj_code = poj_code.strip()
        poj_code = poj_code.split('：')

        return poj_code[1]

    # 获得项目联系人
    def get_poj_rel(self):
        poj_rel = ''

        if '联系人' in self.response_text.xpath('//*[@id="info"]/ul[1]/li[12]').get():
            poj_rel = self.response_text.xpath('//*[@id="info"]/ul[1]/li[12]').get()
        elif '联系人' in self.response_text.xpath('//*[@id="info"]/ul[1]/li[11]').get():
            poj_rel = self.response_text.xpath('//*[@id="info"]/ul[1]/li[11]').get()

        re = poj_rel
        reIndex = len(re)
        start_index = re.find('ght">', 0, reIndex)
        end_index = re.find('<br>', start_index, reIndex)
        poj_rel = re[start_index + 7:end_index]
        poj_rel = poj_rel.strip()
        poj_rel = poj_rel.split('：')
        result = poj_rel[1].split('<br>')[0]
        result = result.strip()

        return result

    def get_kai_time(self):
        kai_time = self.response_text.xpath('//*[@id="info"]/ul/li[6]/text()').get()

        kai_time = kai_time.strip()
        kai_time = kai_time.split('：')

        return kai_time[1]

    # 获得项目联系电话
    def get_rel_num(self):
        poj_rel_num = self.response_text.xpath('//*[@id="info"]/ul[1]/li[7]').get()

        re = poj_rel_num
        reIndex = len(re)
        start_index = re.find('<br>', 0, reIndex)
        end_index = re.find('<br>', start_index, reIndex)
        poj_rel_num = re[start_index + 7:end_index]
        poj_rel_num = poj_rel_num.strip()
        poj_rel_num = poj_rel_num.split('：')

        return poj_rel_num[1][0:10]

    # 获得发布时间
    def get_publish_times(self):
        publish_times = self.response_text.xpath(CONST_PARAM.get('Publish_Time')).get().split('   ')
        length = len(publish_times[1])
        publish_time = publish_times[1][5:length]

        return publish_time.strip()

    # 获得采购机构
    def get_unit(self):
        unit = self.response_text.xpath('//*[@id="info"]/ul/li[3]/text()').get()
        result = unit.split('：')[1].strip()

        return result

    # 获得采购方式
    def get_call_way(self):
        cal_way = self.response_text.xpath('//*[@id="info"]/ul/li[5]/text()').get()

        cal_way = cal_way.strip()
        cal_way = cal_way.split('：')

        return cal_way[1]

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
    def get_failure_content(self):
        reason = ''
        if '原因' in self.response_text.xpath('//*[@id="info"]/ul/li[11]/text()').get():
            reason = self.response_text.xpath('//*[@id="info"]/ul/li[11]/text()').get()
        elif '原因' in self.response_text.xpath('//*[@id="info"]/ul/li[10]/text()').get():
            reason = self.response_text.xpath('//*[@id="info"]/ul/li[10]/text()').get()

        failure_content = reason.split('：')[1].strip()

        result = ''
        for str in failure_content[1:len(failure_content)]:
            result += str

        return result

    # 获得代理机构
    def get_agency(self):

        agency = self.response_text.xpath('//*[@id="info"]/ul[1]/li[4]').get()

        re = agency
        reIndex = len(re)
        start_index = re.find('ght">', 0, reIndex)
        end_index = re.find('<br>', start_index, reIndex)
        agency = re[start_index + 7:end_index]
        agency = agency.strip()
        agency = agency.split('：')
        result = agency[1].split('<br>')[0]
        result = result.strip()

        return result

    def get_agent_name(self):
        agent_name = ''.join(self.response_text.xpath('//*[@id="info"]/ul/li[4]/text()[1]').extract()).split('：')
        agent_name[1] = agent_name[1].strip()

        return agent_name[1]


    def get_agent_address(self):

        address = ''.join(self.response_text.xpath('//*[@id="info"]/ul/li[4]/text()[2]').extract())
        address = address.strip()
        address = address.split('：')

        return address[1]

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

        try:
            href = re.findall(pattern, str(html))

            if isinstance(href, str):
                return at_dict
            else:
                for atuple in href:
                    item = {}
                    item['url'] = 'http://www.ccgp-guizhou.gov.cn' + atuple[0]
                    files = atuple[1].split('.')
                    item['file_name'] = files[0]
                    item['file_type'] = files[1]
                    item['file_size'] = -1
                    at_dict.append(item)

        except Exception as e:
            pass

        return at_dict