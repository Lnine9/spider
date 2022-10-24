from BaseSpider.base_component.HtmlPageResolver import HtmlPageResolver

class YN_Annouce_Resolver_WinBid(HtmlPageResolver):

    def resolver_page(self) -> dict:
        page_attr = self.get_subcomponent_data()
        return page_attr