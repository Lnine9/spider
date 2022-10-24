# coding: utf-8
from RelationAnalysis.data_operate.relation_analysis.purchaser_industry import PurchaserIndustry
from RelationAnalysis.resolve.Industry import Industry


class IndustryDivide():

    _trades = PurchaserIndustry.query_all()
    _tradeslist = [None for x in range(0, len(_trades))]  # 创建实例列表

    def __init__(self):
        # 实例加入列表
        for index, item in enumerate(self._trades):
            self._tradeslist[index] = Industry(id=item.id, value=item.value, include=item.include, no_include=item.noinclude)
        # 串联责任链实例
        for index in range(0, len(self._trades)-1):
            self._tradeslist[index].NextIndustry(self._tradeslist[index+1])

    def get_industry(self, name):
        result = self._tradeslist[0].analysis(name)
        if not result:
            result = [{'id': '39', 'name': '其他'}]
        return result

