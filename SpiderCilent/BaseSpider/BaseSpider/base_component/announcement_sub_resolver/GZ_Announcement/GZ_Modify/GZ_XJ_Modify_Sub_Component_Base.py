import re

from BaseSpider.base_component.SubResolver import SubResolver
from BaseSpider.tool import param_tool

CONST_PARAM = {
    # 公告标题参数
    'TITLE': '//div[@class="you"]/div/div/h3/text()',

    # 公告时间
    'Publish_Time': '/html/body/div[3]/div/div[2]/div[1]/div/div[2]/text()',

    # 代理机构联系人、联系方式
    'Agent':'//*[@id="info"]/ul/li[14]/ul/li[2]/text()',
    'Agent_re': '//*[@id="info"]/ul/li[14]/ul/li[3]/text()',

    # 公告url
    'Announcement_Url': '/html/head/script[8]/text()',
}


# 贵州省市县级更正基本信息子组件
class GZ_XJ_Modify_Sub_Component_Base(SubResolver):
    def resolver_page(self) -> dict:
        # 差品目、行政区域、其他说明
        content = {'公告标题': self.get_title(),
                   '项目名称':  self.get_project_name(),
                   '项目编号': self.get_poj_code(),
                   '品目': '无',
                   '行政区域': self.get_unit(),
                   '其他说明': '无',
                   '采购单位': self.get_unit(),
                   '公告发布时间': self.get_publish_times(),
                   '项目联系人': self.get_poj_rel(),
                   '项目联系电话': self.get_rel_num(),
                   '代理机构': self.get_agency(),
                   '代理机构联系方式': self.get_agency_rel_phone(),
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
    def get_title(self):
        return self.response_text.xpath(CONST_PARAM.get('TITLE')).get().strip()

    # 获得采购项目名称
    def get_project_name(self):
        return self.response_text.xpath('//*[@id="info"]/ul/li[1]/text()').get().strip()

    # 获得项目编号
    def get_poj_code(self):
        return self.response_text.xpath('//*[@id="info"]/ul/li[4]/text()').get().strip()

    # 获得项目联系人
    def get_poj_rel(self):
        return self.response_text.xpath('//*[@id="info"]/ul/li[6]/text()').get().strip()

    # 获得项目联系电话
    def get_rel_num(self):
        return self.response_text.xpath('//*[@id="info"]/ul/li[7]/text()').get().strip()

    # 获得发布时间
    def get_publish_times(self):
        return self.response_text.xpath(CONST_PARAM.get('Publish_Time')).get().split('：')[3].strip()

    # 获得采购机构
    def get_unit(self):
        if self.response_text.xpath('//*[@id="info"]/ul/li[12]/span').get() is not None:
            if '采购人名称' in self.response_text.xpath('//*[@id="info"]/ul/li[12]/span').get():
                return self.response_text.xpath('//*[@id="info"]/ul/li[12]/text()').get().strip()
        if self.response_text.xpath('//*[@id="info"]/ul/li[13]/span').get() is not None:
            if '采购人名称' in self.response_text.xpath('//*[@id="info"]/ul/li[13]/span').get():
                return self.response_text.xpath('//*[@id="info"]/ul/li[13]/text()').get().strip()
        else:
            return None

    # 获得采购方式
    def get_call_way(self):
        return self.response_text.xpath('//*[@id="info"]/ul/li[8]/text()').get().strip()

    # 获得首次公告日期
    def get_open_time(self):
        return self.response_text.xpath('//*[@id="info"]/ul/li[9]/text()').get().strip()

    # 获得更正内容
    def get_modify_content(self):
        return self.response_text.xpath('//*[@id="info"]/ul/li[10]/text()').get().strip()

    # 获得代理机构
    def get_agency(self):
        if self.response_text.xpath('//*[@id="info"]/ul/li[13]/span').get() is not None:
            if '采购代理机构全称' in self.response_text.xpath('//*[@id="info"]/ul/li[13]/span').get():
                return self.response_text.xpath('//*[@id="info"]/ul/li[13]/text()').get().strip()
        if self.response_text.xpath('//*[@id="info"]/ul/li[14]/span').get() is not None:
            if '采购代理机构全称' in self.response_text.xpath('//*[@id="info"]/ul/li[14]/span').get():
                return self.response_text.xpath('//*[@id="info"]/ul/li[14]/text()').get().strip()
        else:
            return None

    # 获得代理机构地址
    def get_agency_address(self):
        if self.response_text.xpath('//*[@id="info"]/ul/li[13]/ul/li[1]/span').get() is not None:
            if '采购代理机构地址' in self.response_text.xpath('//*[@id="info"]/ul/li[13]/ul/li[1]/span').get():
                return self.response_text.xpath('//*[@id="info"]/ul/li[13]/ul/li[1]/text()').get().strip()
        if self.response_text.xpath('//*[@id="info"]/ul/li[14]/ul/li[1]/span').get() is not None:
            if '采购代理机构地址' in self.response_text.xpath('//*[@id="info"]/ul/li[14]/ul/li[1]/span').get():
                return self.response_text.xpath('//*[@id="info"]/ul/li[14]/ul/li[1]/text()').get().strip()
        else:
            return None

    # 获得代理机构联系人
    def get_agency_rel(self):
        if self.response_text.xpath('//*[@id="info"]/ul/li[13]/ul/li[2]/span').get() is not None:
            if '项目联系人' in self.response_text.xpath('//*[@id="info"]/ul/li[13]/ul/li[2]/span').get():
                return self.response_text.xpath('//*[@id="info"]/ul/li[13]/ul/li[2]/text()').get().strip()
        if self.response_text.xpath('//*[@id="info"]/ul/li[14]/ul/li[2]/span').get() is not None:
            if '项目联系人' in self.response_text.xpath('//*[@id="info"]/ul/li[14]/ul/li[2]/span').get():
                return self.response_text.xpath('//*[@id="info"]/ul/li[14]/ul/li[2]/text()').get().strip()
        else:
            return None

    # 获得代理机构联系人电话
    def get_agency_rel_phone(self):
        if self.response_text.xpath('//*[@id="info"]/ul/li[13]/ul/li[3]/span').get() is not None:
            if '联系电话' in self.response_text.xpath('//*[@id="info"]/ul/li[13]/ul/li[3]/span').get():
                return self.response_text.xpath('//*[@id="info"]/ul/li[13]/ul/li[3]/text()').get().strip()
        if self.response_text.xpath('//*[@id="info"]/ul/li[14]/ul/li[3]/span').get() is not None:
            if '联系电话' in self.response_text.xpath('//*[@id="info"]/ul/li[14]/ul/li[3]/span').get():
                return self.response_text.xpath('//*[@id="info"]/ul/li[14]/ul/li[3]/text()').get().strip()
        else:
            return None

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

        if index != -1:
            titleIndex = an_url_json.find('title', index, json_length)
            contenId = an_url_json[index + 12:titleIndex - 3]
        else:
            contenId = '/'

        return 'http://www.ccgp-guizhou.gov.cn/view-1153817836808214-' + contenId + '.html?siteId=1' if contenId != '/' else 'url解析失败'

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