from BaseSpider.base_component.HtmlPageResolver import HtmlPageResolver
from BaseSpider.base_component.utils.util import k_remove, remove
from BaseSpider.tool import param_tool
import re


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

    #代理机构联系人、联系方式
    'Agent':'//ul[@id="agentContact"]/li[2]/text()',
    'Agent_re': '//ul[@id="agentContact"]/li[3]/text()',

    #标书发售方式
    'saleWay': '//div[@id="info"]/ul/ul[3]/li[3]/text()',

    #标书发售截止时间
    'saleTime': '//*[@id="info"]/ul[1]/ul[3]/li[1]/span/text()',

    #标书售价
    'price': '//*[@id="info"]/ul[1]/ul[3]/li[4]/span/text()',

    #标书购买地点
    'place': '//div[@id="info"]/ul/ul[3]/li[2]/text()',

    #公告url
    'Announcement_Url': '/html/head/script[8]/text()',

    # 附件地址
    'AT': '//*[@id="info"]/li/ul/li/table/tbody/tr/td/ol/li/a/@href',

    # 附件名及type
    'NAME_TYPE': '//*[@id="info"]/li/ul/li/table/tbody/tr/td/ol/li/a'
}


class GZ_SJ_County_Bid_Html(HtmlPageResolver):

    def resolver_page(self) -> dict:
        # print('中标供应商')
        # print(self.response.xpath('//*[@id="tabrow"]').get())
        # print('代理机构和联系方式')
        # print(self.response.xpath(CONST_PARAM.get('Agent')).get() + ' ' +self.response.xpath(CONST_PARAM.get('Agent_re')).get())
        # print('代理机构收费标准')
        # print()
        # 代理机构收费标准
        charge_standard = ''
        if self.response.xpath('//*[@id="info"]/ul/li[18]/ul/li[1]/text()').get() is not None:
            charge_standard = self.response.xpath('//*[@id="info"]/ul/li[18]/ul/li[1]/text()').get().strip()
        else:
            charge_standard = '无'

        charge_amount = ''
        if self.response.xpath('//*[@id="info"]/ul/li[18]/ul/li[2]/text()').get() is not None:
            charge_amount = self.response.xpath('//*[@id="info"]/ul/li[18]/ul/li[2]/text()').get().strip()
        else:
            charge_amount = '无'

        # print('代理机构收费金额')
        # print(self.response.xpath('//*[@id="info"]/ul/li[18]/ul/li[2]/text()').get())
        # print('中标金额')
        # print(self.response.xpath('//*[@id="turnoverAmount"]/text()').get())

        # 差品目、行政区域、其他说明
        content = {'公告标题': self.getTitle(),
                   '项目名称':  self.get_projec_name(),
                   '项目编号': self.get_poj_code(),
                   '品目': '',
                   '行政区域': self.get_area(),
                   '其他说明': '',
                   '采购单位': self.get_unit(),
                   '公告发布时间': self.get_publish_times(),
                   '项目联系人': self.get_poj_rel(),
                   '项目联系电话': self.get_rel_num(),
                   '代理机构联系人': self.get_agency(),
                   '代理机构名称': self.get_agent_name(),
                   '代理机构地址': self.get_agent_address(),
                   '代理机构联系方式': self.response.xpath(CONST_PARAM.get('Agent_re')).get(),
                   '采购方式': self.get_call_way(),
                   '开标时间': self.get_open_time(),
                   '公告网页URL': self.get_url(),
                   '中标供应商': ''.join(self.response.xpath('//*[@id="info"]/ul/li[14]/ul').extract()),
                   '评审时间': self.get_judge_time(),
                   '评审地点': self.get_judge_are(),
                   '代理机构收费标准': charge_standard,
                   '代理机构收费金额': charge_amount,
                   '中标金额': '包含在中标供应商里',
                   }

        code_dict = {'code': ''.join(self.response.xpath('//*[@id="info"]').extract()), 'file_type': 'html',
                     'file_size': '-1', 'url': self.get_url(), 'local_path': '暂无'}

        at_dict = self.get_at_dict(code_dict['code'], ''.join(self.response.xpath('//*[@id="0"]').extract()))

        content = param_tool.process_dict('WB_G', content)
        content['source_web_name'] = '贵州省政府采购网'
        content['web_site'] = 'http://www.ccgp-guizhou.gov.cn/'
        call_unit ={'name': self.get_unit(), 'address': self.get_unit_address(), 'code': ''}
        call_unit['code'] = call_unit['name']

        agent_unit = []
        agent_unit_item ={'name': self.get_agency(), 'address' : self.get_agency_address(), 'code' : ''}
        agent_unit_item['code'] = agent_unit_item['name']
        agent_unit.append(agent_unit_item)

        return {'WB_G': content, 'code_dict': code_dict, 'at_dict': at_dict,
                'prov_dict': self.get_prov_dict(), 'undefined_exp': self.get_undefined_exp(), 'experts': [],
                'call_unit': call_unit, 'agent_unit': agent_unit}

    # 获得公告标题
    def getTitle(self):
        title = self.response.xpath(CONST_PARAM.get('TITLE')).get()
        return title.strip()

    def get_prov_dict(self):
        html = ''.join(self.response.xpath('//*[@id="0"]').extract())
        count = html.count('id="0"')

        prov_dict = []
        for i in range(count):
            length = len(html)
            start_index = html.find('<td>', html.find('number', 0, length), length) + 4
            end_index = html.find('</td>', start_index, length)

            item = {'code': '', 'name': '', 'address' : ''}
            item['code'] = html[start_index:end_index]
            item['name'] = item['code']
            address_start_index = html.find('<td>', end_index, length) + 4
            address_end_index = html.find('</td>', address_start_index, length)
            item['address'] = html[address_start_index: address_end_index]
            prov_dict.append(item)

            html = html[address_end_index: length]

        return prov_dict

    # 获得采购项目名称
    def get_projec_name(self):
        project_name = self.response.xpath('//*[@id="info"]/ul[1]/li[1]').get()

        re = project_name
        reIndex = len(re)
        start_index = re.find('</span>', 0, reIndex)
        end_index = re.find('</li>', start_index, reIndex)
        project_name = re[start_index + 7:end_index].strip()

        return project_name

    # 获得项目编号
    def get_poj_code(self):
        poj_code = self.response.xpath('//*[@id="info"]/ul[1]/li[2]').get()

        re = poj_code
        reIndex = len(re)
        start_index = re.find('</span>', 0, reIndex)
        end_index = re.find('</li>', start_index, reIndex)
        poj_code = re[start_index + 7:end_index].strip()

        return poj_code

    # 获得项目联系人
    def get_poj_rel(self):
        poj_rel = self.response.xpath('//*[@id="info"]/ul[1]/li[4]').get()

        re = poj_rel
        reIndex = len(re)
        start_index = re.find('</span>', 0, reIndex)
        end_index = re.find('</li>', start_index, reIndex)
        poj_rel = re[start_index + 7:end_index].strip()

        return poj_rel

    # 获得项目联系电话
    def get_rel_num(self):
        poj_rel_num = self.response.xpath('//*[@id="info"]/ul[1]/li[5]').get()

        re = poj_rel_num
        reIndex = len(re)
        start_index = re.find('</span>', 0, reIndex)
        end_index = re.find('</li>', start_index, reIndex)
        poj_rel_num = re[start_index + 7:end_index].strip()

        return poj_rel_num

    # 获得发布时间
    def get_publish_times(self):
        publish_times = self.response.xpath(CONST_PARAM.get('Publish_Time')).get().split('   ')
        length = len(publish_times[1])
        publish_time = publish_times[1][5:length]

        return publish_time.strip()

    # 获得采购机构
    def get_unit(self):
        unit = ''
        # if '采购人名称' in self.response.xpath('//*[@id="info"]/ul[1]/li[15]/span/text()').get():
        #     unit = self.response.xpath('//*[@id="info"]/ul[1]/li[15]').get()
        # elif '采购人名称' in self.response.xpath('//*[@id="info"]/ul[1]/li[14]/span/text()').get():
        #     unit = self.response.xpath('//*[@id="info"]/ul[1]/li[14]').get()

        unit = self.response.xpath('//*[@id="info"]/ul/li[16]').get()

        re = unit
        reIndex = len(re)
        start_index = re.find('</span>', 0, reIndex)
        end_index = re.find('<ul', start_index, reIndex)
        unit = re[start_index + 7:end_index - 7]
        unit = unit.strip()

        return unit

    def get_agent_name(self):
        agent_name = ''

        if '代理机构' in self.response.xpath('//*[@id="info"]/ul/li[17]').get():
            agent_name = self.response.xpath('//*[@id="info"]/ul/li[17]').get()
        elif '代理机构' in self.response.xpath('//*[@id="info"]/ul/li[16]').get():
            agent_name = self.response.xpath('//*[@id="info"]/ul/li[16]').get()

        re = agent_name
        reIndex = len(re)
        start_index = re.find('</span>', 0, reIndex)
        end_index = re.find('<ul', start_index, reIndex)
        agent_name = re[start_index + 7:end_index - 7]
        agent_name = agent_name.strip()

        return agent_name

    def get_agent_address(self):
        address = ''

        if '代理机构' in self.response.xpath('//*[@id="info"]/ul/li[17]').get():
            address = self.response.xpath('//*[@id="info"]/ul/li[17]/ul/li[1]').get()
        elif '代理机构' in self.response.xpath('//*[@id="info"]/ul/li[16]').get():
            address = self.response.xpath('//*[@id="info"]/ul/li[16]/ul/li[1]').get()

        re = address
        reIndex = len(re)
        start_index = re.find('</span>', 0, reIndex)
        end_index = re.find('</li>', start_index, reIndex)
        address = re[start_index + 7:end_index].strip()

        return address


    def get_unit_address(self):
        address = self.response.xpath('//*[@id="purchasingContact"]/li[1]').get()

        re = address
        reIndex = len(re)
        start_index = re.find('</span>', 0, reIndex)
        end_index = re.find('</li>', start_index, reIndex)
        address = re[start_index + 7:end_index].strip()

        return address

    # 获得采购方式
    def get_call_way(self):
        cal_way = self.response.xpath('//*[@id="info"]/ul[1]/li[7]').get()

        re = cal_way
        reIndex = len(re)
        start_index = re.find('</span>', 0, reIndex)
        end_index = re.find('</li>', start_index, reIndex)
        cal_way = re[start_index + 7:end_index].strip()

        return cal_way

    # 获得评审时间
    def get_judge_time(self):
        judge_time = self.response.xpath('//*[@id="info"]/ul[1]/li[10]').get()

        re = judge_time
        reIndex = len(re)
        start_index = re.find('</span>', 0, reIndex)
        end_index = re.find('</li>', start_index, reIndex)
        judge_time = re[start_index + 7:end_index].strip()

        return judge_time

    # 获得评审地点
    def get_judge_are(self):
        judge_are = self.response.xpath('//*[@id="info"]/ul[1]/li[11]').get()

        re = judge_are
        reIndex = len(re)
        start_index = re.find('</span>', 0, reIndex)
        end_index = re.find('</li>', start_index, reIndex)
        judge_are = re[start_index + 7:end_index].strip()

        return judge_are

    def get_undefined_exp(self):
        exps = self.response.xpath('//*[@id="info"]/ul[1]/li[12]').get()
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


    # 获得开标时间
    def get_open_time(self):
        open_time = self.response.xpath('//*[@id="info"]/ul[1]/li[13]').get()

        re = open_time
        reIndex = len(re)
        start_index = re.find('</span>', 0, reIndex)
        end_index = re.find('</li>', start_index, reIndex)
        open_time = re[start_index + 7:end_index - 5].strip()
        if open_time == '':
            return None
        return open_time

    # 获得投标截止时间
    def get_end_time(self):
        end_time = self.response.xpath('//*[@id="info"]/ul[1]/li[10]').get()

        re = end_time
        reIndex = len(re)
        start_index = re.find('</span>', 0, reIndex)
        end_index = re.find('</li>', start_index, reIndex)
        end_time = re[start_index + 7:end_index]

        return end_time.strip()

    # 获得开标地点
    def get_open_area(self):
        open_area = self.response.xpath('//*[@id="info"]/ul[1]/li[12]').get()

        re = open_area
        reIndex = len(re)
        start_index = re.find('</span>', 0, reIndex)
        end_index = re.find('</li>', start_index, reIndex)
        open_area = re[start_index + 7:end_index].strip()

        return open_area

    # 获得代理机构
    def get_agency(self):
        agency=''
        if self.response.xpath('//*[@id="info"]/ul[1]/li[17]/span/text()').get() is not None and '采购代理机构' in self.response.xpath('//*[@id="info"]/ul[1]/li[17]/span/text()').get():
            agency = self.response.xpath('//*[@id="info"]/ul[1]/li[17]').get()
        elif '采购代理机构' in self.response.xpath('//*[@id="info"]/ul[1]/li[16]/span/text()').get():
            agency = self.response.xpath('//*[@id="info"]/ul[1]/li[16]').get()

        aIndex = len(agency)
        a_start_index = agency.find('</span>', 0, aIndex)
        a_end_index = agency.find('<ul', a_start_index, aIndex)

        agency = agency[a_start_index + 7:a_end_index - 7].strip()
        agency = agency.strip()

        return agency

    def get_agency_address(self):
        address = self.response.xpath('//*[@id="info"]/ul/li[17]/ul/li[1]').get()

        re = address
        reIndex = len(re)
        start_index = re.find('</span>', 0, reIndex)
        end_index = re.find('</li>', start_index, reIndex)
        address = re[start_index + 7:end_index].strip()

        return address

    # 获得标书发售开始和截止时间
    def get_times(self):
        times = self.response.xpath(CONST_PARAM.get('saleTime')).get().split(':', 1)
        times = times[1].split('至')

        return times

    # 获得标书价格
    def get_price(self):
        prices = self.response.xpath(CONST_PARAM.get('price')).get().split(':')
        price = prices[1]

        return price.strip()

    # 获得品目
    def get_item(self):

        return self.response.xpath('//*[@id="info"]/ul/ul[1]/li[1]/text()').get().strip()

    # 获得其他说明
    def get_other(self):

        return self.response.xpath('//*[@id="info"]/ul/ul[1]/li/text()').get().strip()

    # 获得精准区域
    def get_area(self):
        area = self.response.xpath('//*[@id="purchasingContact"]/li[1]/text()').get().strip()
        area = '贵州省' + area

        return area

    # 获得公告url
    def get_url(self):
        an_url_json = self.response.xpath(CONST_PARAM.get('Announcement_Url')).get()
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

    def get_at_dict(self, html, company_html):
        at_dict = []
        pattern = '<a.*?href="([^"]*)".*?>([\S\s]*?)</a>'

        href = re.findall(pattern, str(html))

        company_count = company_html.count('id="0"')
        for atuple in href[company_count: len(href)]:
            item = {}
            item['url'] =  'http://www.ccgp-guizhou.gov.cn' + atuple[0]
            files = atuple[1].split('.')
            item['file_name'] = files[0]
            item['file_type'] = files[1]
            item['file_size'] = -1
            at_dict.append(item)
        return at_dict




