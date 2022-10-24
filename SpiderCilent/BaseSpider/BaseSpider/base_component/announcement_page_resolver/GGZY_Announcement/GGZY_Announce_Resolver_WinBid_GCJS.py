from BaseSpider.base_component.HtmlPageResolver import HtmlPageResolver


class GGZY_Announce_Resolver_WinBid_GCJS(HtmlPageResolver):
    def resolver_page(self) -> dict:
        page_attr = self.get_subcomponent_data()
        return page_attr
