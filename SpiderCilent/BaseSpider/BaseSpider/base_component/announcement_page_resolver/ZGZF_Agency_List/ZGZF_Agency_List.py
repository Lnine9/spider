from BaseSpider.base_component.HtmlPageResolver import HtmlPageResolver


class ZGZF_Agency_list_Resolver(HtmlPageResolver):
    def resolver_page(self) -> dict:
        page_attr = self.get_subcomponent_data()
        return page_attr
