import re

from BaseSpider.base_component.SubResolver import SubResolver
from BaseSpider.tool import param_tool


# 贵州省市县级废标基本信息子组件
class GZ_XJ_Failure_Sub_Component_Base(SubResolver):
    def resolver_page(self) -> dict:
        # 差品目、行政区域、其他说明
        content = {'公告标题': self.get_title(),
                   '项目名称':  self.get_project_name(),
                   '项目编号': self.get_project_code(),
                   '品目': '无',
                   '行政区域': self.get_unit(),
                   '其他说明': '无',
                   '采购单位': self.get_unit(),
                   '公告发布时间': self.get_publish_times(),
                   '项目联系人': self.get_poj_rel(),
                   '项目联系电话': self.get_rel_num(),
                   '代理机构': self.get_agency(),
                   '代理机构联系方式': self.get_agency_num(),
                   '采购方式': self.get_call_way(),
                   '公告网页URL': self.get_url(),
                   '开标时间': self.get_kai_time(),
                   '流标内容': self.get_failure_content(),
                   }

        code_dict = {'code': ''.join(self.response_text.xpath('//*[@id="info"]').extract()),
                     'file_type': 'html', 'file_size': '-1', 'url': self.get_url(), 'local_path': '暂无'}

        at_dict = self.get_at_dict(code_dict['code'])

        content = param_tool.process_dict('FB_G', content)
        content['source_web_name'] = '贵州省政府市县级采购网'
        content['web_site'] = 'http://www.ccgp-guizhou.gov.cn/'

        new_page_attr = {'FB_G': content, 'code_dict': code_dict, 'at_dict': at_dict}
        self.page_attr.update(new_page_attr)
        return self.page_attr

    # 获得公告标题
    def get_title(self):
        return self.response_text.xpath('//div[@class="you"]/div/div/h3/text()').get().strip()

    # 获得采购项目名称
    def get_project_name(self):
        return self.response_text.xpath('//*[@id="info"]/ul/li[2]/text()').get().split('：')[1].strip()

    # 获得项目编号
    def get_project_code(self):
        return self.response_text.xpath('//*[@id="info"]/ul/li[1]/text()').get().strip().split('：')[1]

    # 获得项目联系人
    def get_poj_rel(self):
        if self.response_text.xpath('//*[@id="info"]/ul/li[11]/text()[1]').get() is not None:    # 不为空，但是里面不包含项目联系人字段
            if '项目联系人' in self.response_text.xpath('//*[@id="info"]/ul/li[11]/text()[1]').get():
                return self.response_text.xpath('//*[@id="info"]/ul/li[11]/text()[1]').get().strip().split('：')[-1]
        if self.response_text.xpath('//*[@id="info"]/ul/li[12]/text()[1]').get() is not None:  # 不为空，里面包含项目联系人字段
            if '项目联系人' in self.response_text.xpath('//*[@id="info"]/ul/li[12]/text()[1]').get():
                return self.response_text.xpath('//*[@id="info"]/ul/li[12]/text()[1]').get().strip().split('：')[-1]     # 应该能取出来才对
        else:
            return None

    # 获得开标时间
    def get_kai_time(self):
        return self.response_text.xpath('//*[@id="info"]/ul/li[7]/text()').get().strip().split('：')[-1]

    # 获得项目联系电话
    def get_rel_num(self):
        if self.response_text.xpath('//*[@id="info"]/ul/li[11]/text()[2]').get() is not None:
            if '联系电话' in self.response_text.xpath('//*[@id="info"]/ul/li[11]/text()[2]').get():
                return self.response_text.xpath('//*[@id="info"]/ul/li[11]/text()[2]').get().strip().split('：')[-1]
        if self.response_text.xpath('//*[@id="info"]/ul/li[12]/text()[2]').get() is not None:
            if '联系电话' in self.response_text.xpath('//*[@id="info"]/ul/li[12]/text()[2]').get():
                return self.response_text.xpath('//*[@id="info"]/ul/li[12]/text()[2]').get().strip().split('：')[-1]
        else:
            return None

    # 获得发布时间
    def get_publish_times(self):
        return self.response_text.xpath('//*[@id="info"]/ul/li[6]/text()').get().strip().split('：')[-1]

    # 获得采购机构
    def get_unit(self):
        return self.response_text.xpath('//*[@id="info"]/ul/li[3]/text()').get().strip().split('：')[-1]

    # 获得采购方式
    def get_call_way(self):
        return self.response_text.xpath('//*[@id="info"]/ul/li[5]/text()').get().strip().split('：')[-1]

    # 获得更正内容
    def get_failure_content(self):
        if self.response_text.xpath('//*[@id="info"]/ul/li[10]/text()').get() is not None:
            if '废标原因' in self.response_text.xpath('//*[@id="info"]/ul/li[10]/text()').get():
                return self.response_text.xpath('//*[@id="info"]/ul/li[10]/text()').get().strip().split('：')[-1]
        if self.response_text.xpath('//*[@id="info"]/ul/li[11]/text()').get() is not None:
            if '废标原因' in self.response_text.xpath('//*[@id="info"]/ul/li[11]/text()').get():
                return self.response_text.xpath('//*[@id="info"]/ul/li[11]/text()').get().strip().split('：')[-1]
        else:
            return None

    # 获得代理机构
    def get_agency(self):
        return self.response_text.xpath('//*[@id="info"]/ul/li[4]/text()[1]').get().strip().split('：')[-1]

    # 获得代理机构联系方式
    def get_agency_num(self):
        agency = self.response_text.xpath('//*[@id="info"]/ul/li[4]').get() if self.response_text.xpath('//*[@id="info"]/ul/li[4]').get() is not None else '无'
        length = len(agency)
        start_index = agency.find('电话：', 0, length)
        return agency[start_index + 3: length - 17].strip()

    # 获得品目
    def get_item(self):
        return self.response_text.xpath('//*[@id="info"]/ul/ul[1]/li[1]/text()').get().strip()

    # 获得其他说明
    def get_other(self):
        return self.response_text.xpath('//*[@id="info"]/ul/ul[1]/li/text()').get().strip()

    # 获得公告url
    def get_url(self):
        an_url_json = self.response_text.xpath('/html/head/script[8]/text()').get()
        json_length = len(an_url_json)
        index = an_url_json.find('contentId', 0, json_length)

        if index != -1:
            titleIndex = an_url_json.find('title', index, json_length)
            contenId = an_url_json[index + 12:titleIndex - 3]
        else:
            contenId = '/'

        return 'http://www.ccgp-guizhou.gov.cn/view-1153845808113747-' + contenId + '.html?siteId=1' if contenId != '/' else 'url解析失败'

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