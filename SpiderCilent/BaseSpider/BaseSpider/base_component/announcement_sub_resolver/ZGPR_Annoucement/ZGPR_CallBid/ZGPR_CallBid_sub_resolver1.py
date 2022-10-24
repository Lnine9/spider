from urllib import request

import chardet
from lxml import etree

from BaseSpider.base_component.announcement_sub_resolver.GZPR_Anouncement.base.parser_architecture import \
    ParserArchitecture
from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose import proj_place, \
    resource_from, ET, region, contact, \
    tender_place, bid_sale_m, bid_sale_time, bid_price, bid_sale_place, bid_end_time
from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose import title, web_site, \
    source_web_name, ancm_time, source_url, proj_name, proj_code
from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.source_datas import \
    SourceDatas
from BaseSpider.base_component.announcement_sub_resolver.ZGPR_Annoucement.ZGPR_CallBid.decompose.tools import page_text


def download(url, data=None):
    """
    请求读取
    :param url:
    :param data: bytes(urllib.parse.urlencode({'word': 'hello'}), encoding='utf8')
    :return:
    """
    return request.urlopen(url, data=data).read()


class ZGPRCallBidSubComponent1(ParserArchitecture):

    def resolver_page(self) -> dict:
        content = self.getContent()
        code_dict = self.getCodeHtml()
        at_dict = self.getAttr()
        new_page_attr = {'CB_E': content, 'code_dict': code_dict, 'at_dict': at_dict}
        self.page_attr.update(new_page_attr)
        return self.page_attr

    def getContent(self):
        content_url = self.response_url.replace("/a/", "/b/")
        print(content_url)
        content = download(content_url)
        char_type = chardet.detect(content)
        content_utf8 = content.decode(char_type['encoding'])
        response = etree.HTML(content_utf8)
        SourceDatas.response = response
        SourceDatas.text = page_text.get_text(response)
        #print(SourceDatas.text)
        content = {}
        content['title'] = title.Title.get()
        content['web_site'] = web_site.WebSite.get()
        content['source_web_name'] = source_web_name.SourceWebName.get()
        content['ancm_time'] = ancm_time.AncmTime.get()
        content['sourse_url'] = source_url.SourceUrl.get()
        SourceDatas.title = content['title']

        content['proj_name'] = proj_name.ProjName.get()
        content['proj_code'] = proj_code.ProjCode.get()
        content['proj_place'] = proj_place.ProjPlace.get()
        content['resource_from'] = resource_from.ResourceFrom.get()
        content['ET'] = ET.ET.get()
        content['region'] = region.Region.get()

        content['tender_place'] = tender_place.TenderPlace.get()
        content['bid_sale_m'] = bid_sale_m.BidSaleM.get()  # 待完善
        content['bid_price'] = bid_price.BidPrice.get()
        content['bid_sale_place'] = bid_sale_place.BidSalePlace.get()  # 待完善
        content['bid_end_time'] = bid_end_time.BidEndTime.get()
        bid_sale_times = bid_sale_time.BidSaleTime.get()
        if bid_sale_times:
            content.update(bid_sale_times)
        else:
            content.update({'bid_sale_op_time': None, 'bid_sale_en_time': None})

        contact_dict = contact.Contact.get()
        if contact_dict:
            content.update(contact_dict)
        else:
            content.update(
                {'proj_unit': None, 'proj_unit_address': None, 'proj_rel_p': None, 'proj_rel_m': None,
                 'agent_unit': None, 'agent_unit_p': None, 'agent_unit_m': None,
                 'agent_unit_address': None})

        content['other_ex'] = ''
        print(self.check(content))
        return content

    def getCodeHtml(self):
        code_dict = {}

        code_dict['url'] = self.response_url
        code_dict['file_type'] = 'html'
        code_dict['file_size'] = '-1'
        code_dict['local_path'] = '暂无'
        code_dict['code'] = ''.join(self.response_text.xpath('//*').extract())
        return code_dict

    def getAttr(self):
        return []

    def check(self, dicts):
        lists = []
        for key in dicts:
            if not dicts[key]:
                lists.append(key)
        return lists
