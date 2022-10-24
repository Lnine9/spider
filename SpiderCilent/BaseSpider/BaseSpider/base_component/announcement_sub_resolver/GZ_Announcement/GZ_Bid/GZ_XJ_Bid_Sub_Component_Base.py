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
    'Files': '//*[@id="info"]/li/ul/li/table/tbody/tr/td/ol/li/a',  # 问题

    # 采购预算
    'Budget': '//div[@id="info"]/ul/ul[1]/li[3]/text()',

    # 代理机构联系人、联系方式
    'Agent': '//ul[@id="agentContact"]/li[2]/text()',
    'Agent_re': '//ul[@id="agentContact"]/li[3]/text()',

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


# 贵州省市县级中标基本信息子组件
class GZ_XJ_Bid_Sub_Component_Base(SubResolver):
    def resolver_page(self) -> dict:
        # 差品目、行政区域、其他说明
        content = {'公告标题': self.get_title(),
                   '项目名称': self.get_project_name(),
                   '项目编号': self.get_poj_code(),
                   '品目': self.get_item(),
                   '行政区域': self.get_area(),
                   '其他说明': '',
                   '采购单位': self.get_unit(),
                   '公告发布时间': self.get_publish_times(),
                   '项目联系人': self.get_poj_rel(),
                   '项目联系电话': self.get_rel_num(),
                   '代理机构': self.get_agency(),
                   '代理机构联系方式': self.get_agency_phone(),
                   '采购方式': self.get_call_way(),
                   '开标时间': self.get_open_time(),
                   '公告网页URL': self.get_url(),
                   '中标供应商': self.bid_supplier(),
                   '评审时间': self.get_judge_time(),
                   '评审地点': self.get_judge_are(),
                   '代理机构收费标准': self.charge_standard(),
                   '代理机构收费金额': self.charge_amount(),
                   '中标金额': self.get_bid_amount(),
                   }

        code_dict = {'code': ''.join(self.response_text.xpath('//*[@id="info"]').extract()), 'file_type': 'html',
                     'file_size': '-1', 'url': self.get_url(), 'local_path': '暂无'}

        at_dict = self.get_at_dict(code_dict['code'], ''.join(self.response_text.xpath('//*[@id="0"]').extract()))

        content = param_tool.process_dict('WB_G', content)
        content['source_web_name'] = '贵州省政府采购网'
        content['web_site'] = 'http://www.ccgp-guizhou.gov.cn/'
        call_unit = {'name': self.get_unit(), 'address': self.get_unit_address(), 'code': ''}
        call_unit['code'] = call_unit['name']

        agent_unit = []
        agent_unit_item = {'name': self.get_agency(), 'address': self.get_agency_address(), 'code': ''}
        agent_unit_item['code'] = agent_unit_item['name']
        agent_unit.append(agent_unit_item)
        new_page_attr = {'WB_G': content, 'code_dict': code_dict, 'at_dict': at_dict,
                            'prov_dict': self.get_prov_dict(), 'undefined_exp': self.get_undefined_exp(), 'experts': [],
                            'call_unit': call_unit, 'agent_unit': agent_unit}
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

    # 获得行政区域
    def get_area(self):
        return '贵州省' + self.response_text.xpath('//*[@id="purchasingContact"]/li[1]/text()').get().strip()

    # 获得采购单位
    def get_unit(self):
        if self.response_text.xpath('//*[@id="info"]/ul/li[15]/span').get() is not None:
            if '采购人名称' in self.response_text.xpath('//*[@id="info"]/ul/li[15]/span').get():
                return self.response_text.xpath('//*[@id="info"]/ul/li[15]/text()').get().strip()
        if self.response_text.xpath('//*[@id="info"]/ul/li[16]/span').get() is not None:
            if '采购人名称' in self.response_text.xpath('//*[@id="info"]/ul/li[16]/span').get():
                return self.response_text.xpath('//*[@id="info"]/ul/li[16]/text()').get().strip()
        else:
            return None

    # 获得公告发布时间
    def get_publish_times(self):
        return self.response_text.xpath('/html/body/div[3]/div/div[2]/div[1]/div/div[2]/text()').get().split('：')[3].strip()

    # 获得项目联系人
    def get_poj_rel(self):
        return self.response_text.xpath('//*[@id="info"]/ul/li[4]/text()').get().strip()

    # 获得项目联系电话
    def get_rel_num(self):
        return self.response_text.xpath('//*[@id="info"]/ul/li[5]/text()').get().strip()

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

    # 获得代理机构联系电话
    def get_agency_phone(self):
        return self.response_text.xpath('//*[@id="agentContact"]/li[3]/text()').get().strip()

    # 获得采购方式
    def get_call_way(self):
        return self.response_text.xpath('//*[@id="info"]/ul/li[7]/text()').get().strip()

    # 获得开标时间
    def get_open_time(self):
        return self.response_text.xpath('//*[@id="info"]/ul/li[13]/text()').get().strip()

    # 获得中标供应商
    def bid_supplier(self):
        return self.response_text.xpath('//*[@id="0"]/td[2]/text()').get().strip()

    # 获得评审时间
    def get_judge_time(self):
        return self.response_text.xpath('//*[@id="info"]/ul/li[10]/text()').get().strip()

    # 获得评审地点
    def get_judge_are(self):
        return self.response_text.xpath('//*[@id="info"]/ul/li[11]/text()').get().strip()

    # 获得代理机构收费标准
    def charge_standard(self):
        if self.response_text.xpath('//*[@id="info"]/ul/li[18]/ul/li[1]/text()').get() is not None:
            return self.response_text.xpath('//*[@id="info"]/ul/li[18]/ul/li[1]/text()').get().strip()
        else:
            return '无'

    # 获得代理机构收费金额
    def charge_amount(self):
        if self.response_text.xpath('//*[@id="info"]/ul/li[18]/ul/li[2]/text()').get() is not None:
            return self.response_text.xpath('//*[@id="info"]/ul/li[18]/ul/li[2]/text()').get().strip()
        else:
            return '无'

    # 获得中标金额
    def get_bid_amount(self):
        return self.response_text.xpath('//*[@id="turnoverAmount"]/text()').get().strip()

    def get_prov_dict(self):
        html = ''.join(self.response_text.xpath('//*[@id="0"]').extract())
        count = html.count('id="0"')

        prov_dict = []
        for i in range(count):
            length = len(html)
            start_index = html.find('<td>', html.find('number', 0, length), length) + 4
            end_index = html.find('</td>', start_index, length)

            item = {'code': '', 'name': '', 'address': ''}
            item['code'] = html[start_index:end_index]
            item['name'] = item['code']
            address_start_index = html.find('<td>', end_index, length) + 4
            address_end_index = html.find('</td>', address_start_index, length)
            item['address'] = html[address_start_index: address_end_index]
            prov_dict.append(item)

            html = html[address_end_index: length]

        return prov_dict

    def get_undefined_exp(self):
        exps = self.response_text.xpath('//*[@id="info"]/ul[1]/li[12]').get()
        undefined_exp = []
        re = exps
        reIndex = len(re)
        start_index = re.find('<br>', 0, reIndex)
        end_index = re.find('</li>', start_index, reIndex)
        exps = re[start_index + 4:end_index].strip()
        experts = exps.split('、')
        for expert in experts:
            item = {}
            item['name'] = expert
            undefined_exp.append(item)

        return undefined_exp

    # 获得采购人地址（无用）
    def get_unit_address(self):
        return self.response_text.xpath('//*[@id="purchasingContact"]/li[1]/text()').get().strip()

    # 获得代理机构联系人姓名(无用)
    def get_agency_name(self):
        return self.response_text.xpath('//*[@id="info"]/ul/li[17]/ul/li[2]/text()').get().strip()

    # 获得代理机构联系地址(无用)
    def get_agency_address(self):
        return self.response_text.xpath('//*[@id="info"]/ul/li[17]/ul/li[1]/text()').get().strip()

    # 获得品目
    def get_item(self):
        if self.response_text.xpath('//*[@id="0"]/td[4]').get() is not None:
            return self.response_text.xpath('//*[@id="0"]/td[4]').get().strip()
        else:
            return ''

    # 获得其他说明(没用)
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

        an_url = 'http://www.ccgp-guizhou.gov.cn/view-1153905922931045-' + contenId + '.html?siteId=1' if contenId != '/' else 'url解析失败'

        return an_url.strip()

    def get_at_dict(self, html, company_html):
        at_dict = []
        pattern = '<a.*?href="([^"]*)".*?>([\S\s]*?)</a>'

        href = re.findall(pattern, str(html))

        company_count = company_html.count('id="0"')
        for atuple in href[company_count: len(href)]:
            item = {}
            item['url'] = 'http://www.ccgp-guizhou.gov.cn' + atuple[0]
            files = atuple[1].split('.')
            item['file_name'] = files[0]
            item['file_type'] = files[1]
            item['file_size'] = -1
            at_dict.append(item)
        return at_dict