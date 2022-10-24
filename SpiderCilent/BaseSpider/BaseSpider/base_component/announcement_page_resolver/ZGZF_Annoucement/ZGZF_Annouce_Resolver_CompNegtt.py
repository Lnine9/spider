from BaseSpider.base_component.HtmlPageResolver import HtmlPageResolver


class ZGZF_Annouce_Resolver_CompNegtt(HtmlPageResolver):
    def resolver_page(self) -> dict:
        page_attr = self.get_subcomponent_data()
        return page_attr
