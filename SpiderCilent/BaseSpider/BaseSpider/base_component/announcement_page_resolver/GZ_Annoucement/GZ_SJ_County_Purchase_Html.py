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
    'Agent':'//div[@id="info"]/ul/ul[6]/li[2]/text()',
    'Agent_re': '//div[@id="info"]/ul/ul[6]/li[3]/text()',

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


class GZ_SJ_County_Purchase_Html(HtmlPageResolver):

    def resolver_page(self) -> dict:
        #标书发售时间与截止时间
        start_end_time = self.get_times()

        item = self.get_item().replace('？', '')
        item = item.strip()

        # 差品目、行政区域、其他说明
        content = {'公告标题': self.getTitle(),
                   '项目名称':  self.get_projec_name(),
                   '项目编号': self.get_poj_code(),
                   '品目': item,
                   '行政区域': self.get_area(),
                   '其他说明': self.get_other(),
                   '采购单位': self.get_unit(),
                   '公告发布时间': self.get_publish_times(),
                   '预算金额': self.response.xpath(CONST_PARAM.get('Budget')).get(),
                   '项目联系人': self.get_poj_rel(),
                   '项目联系电话': self.get_rel_num(),
                   '代理机构联系人': self.get_agency(),
                   '代理机构名称': self.response.xpath(CONST_PARAM.get('Agent')).get(),
                   '代理机构地址': self.response.xpath('//div[@id="info"]/ul/ul[6]/li[1]/text()').get(),
                   '代理机构联系方式': self.response.xpath(CONST_PARAM.get('Agent_re')).get(),
                   '采购方式': self.get_call_way(),
                   '开标时间': self.get_open_time(),
                   '标书发售方式': self.response.xpath(CONST_PARAM.get('saleWay')).get(),
                   '标书发售时间': start_end_time[0],
                   '标书发售截止时间': start_end_time[1],
                   '标书售价': self.get_price(),
                   '标书发售地点': self.response.xpath(CONST_PARAM.get('place')).get(),
                   '投标截止时间':  self.get_end_time(),
                   '开标地点': self.get_open_area(),
                   '公告网页URL': self.get_url(),

                   }

        code_dict = {'code': ''.join(self.response.xpath('//*[@id="info"]').extract()), 'file_type': 'html',
                     'file_size': '-1', 'url': self.get_url(), 'local_path': '暂无'}

        at_dict = self.get_at_dict(code_dict['code'])

        content = param_tool.process_dict('CB_G', content)
        content['source_web_name'] = '贵州省政府采购网'
        content['web_site'] = 'http://www.ccgp-guizhou.gov.cn/'

        return {'CB_G': content, 'code_dict': code_dict, 'at_dict': at_dict}

    # 获得公告标题
    def getTitle(self):
        title = self.response.xpath(CONST_PARAM.get('TITLE')).get()

        return title.strip()
    # 获得采购项目名称
    def get_projec_name(self):
        project_name = self.response.xpath('//*[@id="info"]/ul[1]/li[1]').get()

        re = project_name
        reIndex = len(re)
        start_index = re.find('</span>', 0, reIndex)
        end_index = re.find('</li>', start_index, reIndex)
        project_name = re[start_index + 7:end_index]

        return project_name.strip()

    # 获得项目编号
    def get_poj_code(self):
        poj_code = self.response.xpath('//*[@id="info"]/ul[1]/li[2]').get()

        re = poj_code
        reIndex = len(re)
        start_index = re.find('</span>', 0, reIndex)
        end_index = re.find('</li>', start_index, reIndex)
        poj_code = re[start_index + 7:end_index]

        return poj_code.strip()

    # 获得项目联系人
    def get_poj_rel(self):
        poj_rel = self.response.xpath('//*[@id="info"]/ul[1]/li[4]').get()

        re = poj_rel
        reIndex = len(re)
        start_index = re.find('</span>', 0, reIndex)
        end_index = re.find('</li>', start_index, reIndex)
        poj_rel = re[start_index + 7:end_index]

        return poj_rel.strip()

    # 获得项目联系电话
    def get_rel_num(self):
        poj_rel_num = self.response.xpath('//*[@id="info"]/ul[1]/li[5]').get()

        re = poj_rel_num
        reIndex = len(re)
        start_index = re.find('</span>', 0, reIndex)
        end_index = re.find('</li>', start_index, reIndex)
        poj_rel_num = re[start_index + 7:end_index]

        return poj_rel_num.strip()

    # 获得发布时间
    def get_publish_times(self):
        publish_times = self.response.xpath(CONST_PARAM.get('Publish_Time')).get().split('   ')
        length = len(publish_times[1])
        publish_time = publish_times[1][5:length]

        return publish_time.strip()

    # 获得采购机构
    def get_unit(self):
        unit = ''
        if '采购人名称' in self.response.xpath('//*[@id="info"]/ul[1]/li[15]/span/text()').get():
            unit = self.response.xpath('//*[@id="info"]/ul[1]/li[15]').get()
        elif '采购人名称' in self.response.xpath('//*[@id="info"]/ul[1]/li[14]/span/text()').get():
            unit = self.response.xpath('//*[@id="info"]/ul[1]/li[14]').get()

        re = unit
        reIndex = len(re)
        start_index = re.find('</span>', 0, reIndex)
        end_index = re.find('</li>', start_index, reIndex)
        unit = re[start_index + 7:end_index]

        return unit.strip()

    # 获得采购方式
    def get_call_way(self):
        cal_way = self.response.xpath('//*[@id="info"]/ul[1]/li[6]').get()

        re = cal_way
        reIndex = len(re)
        start_index = re.find('</span>', 0, reIndex)
        end_index = re.find('</li>', start_index, reIndex)
        cal_way = re[start_index + 7:end_index]

        return cal_way.strip()

    # 获得开标时间
    def get_open_time(self):
        open_time = self.response.xpath('//*[@id="info"]/ul[1]/li[11]').get()

        re = open_time
        reIndex = len(re)
        start_index = re.find('</span>', 0, reIndex)
        end_index = re.find('</li>', start_index, reIndex)
        open_time = re[start_index + 7:end_index]

        return open_time.strip()

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
        open_area = re[start_index + 7:end_index]

        return open_area.strip()

    # 获得代理机构
    def get_agency(self):
        agency=''
        if self.response.xpath('//*[@id="info"]/ul[1]/li[17]/span/text()').get() is not None and '采购代理机构' in self.response.xpath('//*[@id="info"]/ul[1]/li[17]/span/text()').get():
            agency = self.response.xpath('//*[@id="info"]/ul[1]/li[17]').get()
        elif '采购代理机构' in self.response.xpath('//*[@id="info"]/ul[1]/li[16]/span/text()').get():
            agency = self.response.xpath('//*[@id="info"]/ul[1]/li[16]').get()

        aIndex = len(agency)
        a_start_index = agency.find('</span>', 0, aIndex)
        a_end_index = agency.find('</li>', a_start_index, aIndex)
        agency = agency[a_start_index + 7:a_end_index].strip()

        return agency.strip()

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
        area = self.response.xpath('//*[@id="info"]/ul/ul[5]/li[1]/text()').get().strip()
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




