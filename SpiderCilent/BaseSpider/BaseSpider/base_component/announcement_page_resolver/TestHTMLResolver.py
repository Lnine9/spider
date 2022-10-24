from ..HtmlPageResolver import HtmlPageResolver
from ..utils.util import k_remove, remove

CONST_PARAM = {
    # 公告标题参数
    'TITLE': '//div[@class="you"]/div/div/h3/text()',
}


class TestHTMLResolver(HtmlPageResolver):

    def resolver_page(self) -> dict:
        title = self.response.xpath(CONST_PARAM.get('TITLE')).get()
        content = {'公告标题': title}
        for each in self.response.xpath('//div[@id="info"]/ul/li'):
            key = k_remove(str(each.xpath('./span/text()').get()))
            value = remove(str(each.xpath('string(.)').get()))
            result = value.replace(key, '')
            content[key] = result

        return content

