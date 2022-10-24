from BaseSpider.base_component.HtmlPageResolver import HtmlPageResolver


# 贵州省市县级采购公告解析器
class GZ_XJ_Annouce_Purchase_Html(HtmlPageResolver):
    def resolver_page(self) -> dict:
        page_attr = self.get_subcomponent_data()
        return page_attr