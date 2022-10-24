from BaseSpider.base_component.HtmlPageResolver import HtmlPageResolver


class YNPR_Annouce_Resolver_ResultsBid2(HtmlPageResolver):
    def resolver_page(self) -> dict:
        page_attr = self.get_subcomponent_data()
        return page_attr