from BaseSpider.base_component.SubResolver import SubResolver
from BaseSpider.base_component.announcement_sub_resolver.ZGZF_dishonest_list.table_contents import \
    transverse_table_contents


class ZGZFDishonestList(SubResolver):
    def __init__(self):
        self.content = {'name': '', 'code': '', 'address': '', 'behavior': '', 'punishment_result': '',
                        'punishment_basis': '', 'open_date': '', 'punishment_date': '', 'deadline': '',
                        'law_enforcement_unit': ''}

    def resolver_page(self) -> dict:
        self.content.update(self.get_content())
        self.page_attr.update({'DL': self.content})
        return self.page_attr

    def get_content(self) -> dict:
        table = self.response_text.xpath('//*[@id="detail"]')
        items = transverse_table_contents(table)
        contents = {'title': 'pass', 'name': self.contain(items, '企业名称'), 'code': self.contain(items, '信用代码'),
                    'address': self.contain(items, '企业地址'), 'behavior': self.contain(items, '具体情形'),
                    'punishment_result': self.contain(items, '处罚结果'), 'punishment_basis': self.contain(items, '处罚依据'),
                    'open_date': self.contain(items, '公布日期'), 'punishment_date': self.contain(items, '处罚日期'),
                    'deadline': self.contain(items, '公布截止日期'), 'law_enforcement_unit': self.contain(items, '执法单位')}
        return contents

    @staticmethod
    def contain(item, find):
        """
        查询key值包含
        :param item:
        :param find:
        :return:
        """
        for key, value in item.items():
            if find in key:
                return value
