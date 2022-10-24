
from BaseSpider.base_component.HtmlPageResolver import HtmlPageResolver

'''流标'''
CONST_PARAM = {
    # 公告标题参数
    'TITLE': '//*[@id="tab-503"]/div/div[2]/div/div/h2/text()',
    'attachments': '//a[@class="attachUrl"]/@href'
}


class SC_SXJ_Annouce_Resolver_FailureBid(HtmlPageResolver):
    def resolver_page(self) -> dict:
        page_attr = self.get_subcomponent_data()
        return page_attr