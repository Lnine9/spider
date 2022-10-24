import re

from BaseSpider.base_component.SubResolver import SubResolver
from BaseSpider.tool import param_tool

CONST_PARAM = {
    # 公告标题参数
    'TITLE': '//div[@class="you"]/div/div/h3/text()',
    # 主要信息
    'Main_Ul_Li': '//div[@id="info"]/ul/li',
    # 次要信息
    'Secondary_Ul_Li': '//div[@id="info"]/ul/ul/li',
    # 公告时间
    'Publish_Time': '/html/body/div[3]/div/div[2]/div[1]/div/div[2]/text()',
    # 附件url列表
    'Files': '//*[@id="info"]/li/ul/li/table/tbody/tr/td/ol/li/a',

    # 采购预算
    'Budget': '//div[@id="info"]/ul/ul[1]/li[3]/text()',

    # 标书发售方式
    'saleWay': '//div[@id="info"]/ul/ul[3]/li[3]/text()',

    # 标书发售截止时间
    'saleTime': '//*[@id="info"]/ul[1]/ul[3]/li[1]/span/text()',

    # 标书售价
    'price': '//*[@id="info"]/ul[1]/ul[3]/li[4]/span/text()',

    # 标书购买地点
    'place': '//div[@id="info"]/ul/ul[3]/li[2]/text()',

    # 公告url
    'Announcement_Url': '/html/head/script[8]/text()',

    # 附件地址
    'AT': '//*[@id="info"]/li/ul/li/table/tbody/tr/td/ol/li/a/@href',

    # 附件名及type
    'NAME_TYPE': '//*[@id="info"]/li/ul/li/table/tbody/tr/td/ol/li/a'
}


# 贵州省市县级基础信息子组件
class GZ_XJ_Purchase_Sub_Component_Base(SubResolver):
    def resolver_page(self) -> dict:
        # 差品目、行政区域、其他说明
        content = {'公告标题': self.get_title(),
                   '项目名称': self.get_project_name(),
                   '项目编号': self.get_poj_code(),
                   '品目': '',
                   '行政区域': self.get_area(),
                   '其他说明': '无',
                   '采购单位': self.get_unit(),
                   '公告发布时间': self.get_publish_times(),
                   '预算金额': self.response_text.xpath(CONST_PARAM.get('Budget')).get(),
                   '项目联系人': self.get_poj_rel(),
                   '项目联系电话': self.get_rel_num(),
                   '代理机构': self.get_agency(),
                   '代理机构联系方式': self.get_agency_rel_num(),
                   '采购方式': self.get_call_way(),
                   '开标时间': self.get_open_time(),
                   '标书发售方式': self.response_text.xpath(CONST_PARAM.get('saleWay')).get(),
                   '标书发售时间': self.get_publish_start_time(),
                   '标书发售截止时间': self.get_publish_end_time(),
                   '标书售价': self.get_price(),
                   '标书发售地点': self.response_text.xpath(CONST_PARAM.get('place')).get(),
                   '投标截止时间': self.get_end_time(),
                   '开标地点': self.get_open_area(),
                   '公告网页URL': self.get_url(),

                   }

        code_dict = {'code': ''.join(self.response_text.xpath('//*[@id="info"]').extract()), 'file_type': 'html',
                     'file_size': '-1', 'url': self.get_url(), 'local_path': '暂无'}

        at_dict = self.get_at_dict(code_dict['code'])

        content = param_tool.process_dict('CB_G', content)
        content['source_web_name'] = '贵州省市县级政府采购网'
        content['web_site'] = 'http://www.ccgp-guizhou.gov.cn/'
        new_page_attr = {'CB_G': content, 'code_dict': code_dict, 'at_dict': at_dict}

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
        return self.response_text.xpath('//*[@id="info"]/ul/li[2]/text()').get().strip()

    # 获得项目联系人
    def get_poj_rel(self):
        return self.response_text.xpath('//*[@id="info"]/ul/li[4]/text()').get().strip()

    # 获得项目联系电话
    def get_rel_num(self):
        return self.response_text.xpath('//*[@id="info"]/ul/li[5]/text()').get().strip()

    # 获得发布时间
    def get_publish_times(self):
        return self.response_text.xpath(CONST_PARAM.get('Publish_Time')).get().split('：')[3].strip()

    # 获得采购机构
    def get_unit(self):
        if self.response_text.xpath('//*[@id="info"]/ul[1]/li[14]/span').get() is not None:
            if '采购人名称' in self.response_text.xpath('//*[@id="info"]/ul[1]/li[14]/span').get():
                return self.response_text.xpath('//*[@id="info"]/ul/li[14]/text()').get().strip()
        if self.response_text.xpath('//*[@id="info"]/ul[1]/li[15]/span').get() is not None:
            if '采购人名称' in self.response_text.xpath('//*[@id="info"]/ul[1]/li[15]/span').get():
                return self.response_text.xpath('//*[@id="info"]/ul/li[15]/text()').get().strip()
        return None

    # 获得采购方式
    def get_call_way(self):
        return self.response_text.xpath('//*[@id="info"]/ul/li[6]/text()').get().strip()

    # 获得开标时间
    def get_open_time(self):
        return self.response_text.xpath('//*[@id="info"]/ul/li[11]/text()').get().strip()

    # 获得投标截止时间
    def get_end_time(self):
        return self.response_text.xpath('//*[@id="info"]/ul/li[10]/text()').get().strip()[:20]

    # 获得开标地点
    def get_open_area(self):
        return self.response_text.xpath('//*[@id="info"]/ul/li[12]/text()').get().strip()

    # 获得代理机构
    def get_agency(self):
        if self.response_text.xpath('//*[@id="info"]/ul/li[16]/span').get() is not None:
            if '采购代理机构全称' in self.response_text.xpath('//*[@id="info"]/ul/li[16]/span').get():
                return self.response_text.xpath('//*[@id="info"]/ul/li[16]/text()').get().strip()
        if self.response_text.xpath('//*[@id="info"]/ul/li[17]/span').get() is not None:
            if '采购代理机构全称' in self.response_text.xpath('//*[@id="info"]/ul/li[17]/span').get():
                return self.response_text.xpath('//*[@id="info"]/ul/li[17]/text()').get().strip()
        else:
            return None

    # 获得代理机构联系人
    def get_agency_rel(self):
        return self.response_text.xpath('//*[@id="info"]/ul/ul[6]/li[2]/text()').get().strip()

    # 获得代理机构地址
    def get_agency_address(self):
        return self.response_text.xpath('//*[@id="info"]/ul/ul[6]/li[1]/text()').get().strip()

    # 获得代理机构联系人电话
    def get_agency_rel_num(self):
        return self.response_text.xpath('//*[@id="info"]/ul/ul[6]/li[3]/text()').get().strip()

    # 获得标书发售开始时间
    def get_publish_start_time(self):
        return self.response_text.xpath(CONST_PARAM.get('saleTime')).get().split(':', 1)[1].split('至')[0].strip()

    # 获得标书发售截止时间
    def get_publish_end_time(self):
        return self.response_text.xpath(CONST_PARAM.get('saleTime')).get().split('至')[1].strip()

    # 获得标书价格
    def get_price(self):
        return self.response_text.xpath(CONST_PARAM.get('price')).get().split(':')[1].strip()

    # 获得品目
    def get_item(self):
        return self.response_text.xpath('//*[@id="info"]/ul/ul[1]/li[1]/text()').get().strip()

    # 获得其他说明
    def get_other(self):
        return self.response_text.xpath('//*[@id="info"]/ul/ul[1]/li/text()').get().strip()

    # 获得精准区域
    def get_area(self):
        return '贵州省' + self.response_text.xpath('//*[@id="info"]/ul/ul[5]/li[1]/text()').get().strip()

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

        return 'http://www.ccgp-guizhou.gov.cn/view-1153797950913584-' + contenId + '.html?siteId=1' if contenId != '/' else 'url解析失败'

    def get_at_dict(self, html):
        at_dict = []
        pattern = '<a.*?href="([^"]*)".*?>([\S\s]*?)</a>'

        href = re.findall(pattern, str(html))
        for atuple in href:
            item = {}
            item['url'] = 'http://www.ccgp-guizhou.gov.cn' + atuple[0]
            files = atuple[1].split('.')
            item['file_name'] = files[0]
            item['file_type'] = files[1]
            item['file_size'] = -1
            at_dict.append(item)

        return at_dict