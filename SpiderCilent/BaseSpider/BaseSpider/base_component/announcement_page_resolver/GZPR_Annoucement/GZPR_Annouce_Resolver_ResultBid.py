from BaseSpider.base_component.HtmlPageResolver import HtmlPageResolver


class GZPR_Annouce_Resolver_ResultBid(HtmlPageResolver):
    def resolver_page(self) -> dict:
        page_attr = self.get_subcomponent_data()
        return page_attr
