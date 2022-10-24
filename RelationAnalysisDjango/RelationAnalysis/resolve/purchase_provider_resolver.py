"""
供应商解析器（新版）
"""
import re
import time

from RelationAnalysis.data_operate.announcement.win_bid_government import WinBidGovernment
from RelationAnalysis.data_operate.pool_table import RelTable
from RelationAnalysis.data_operate.relation_analysis.purchase_provider import PurchaseProvider
from RelationAnalysis.data_operate.relation_analysis.resolve_history import ResolveHistory
from RelationAnalysis.resolve.address_identification import AddressIdentification
from RelationAnalysis.resolve.resolve_tools import update_resolve
from RelationAnalysis.resolve.resolver_interface import ResolverInterface
from RelationAnalysis.tool.logging import logger

address_identification = AddressIdentification()


class PurchaseProviderResolver(ResolverInterface):

    def __init__(self):
        self.all_item = {}

    def analysis(self, announcement_info: WinBidGovernment):
        """
        解析
        :param announcement_info:
        :return:
        """
        back = {'update': [], 'add': [], 'history': []}
        supplier_list = []
        address_list = []
        if announcement_info.provide_unit is not None:
            supplier_list = re.split(r'[/，,、]', announcement_info.provide_unit)
        if announcement_info.provide_address is not None:
            address_list = re.split(r'[/，,、]', announcement_info.provide_address)

        for index, supplier in enumerate(supplier_list):
            supplier = re.sub(r'[?？：: ."\']|(?:\d+\w+)分标', '', supplier).strip()
            # 如果供应商名称出现一些不该出现的字符，说明供应商和地址解析错误，后面的都停止解析
            if re.search(r'^无$|.*(?:名称|品牌|要求|地址|范围|规格型号|附件|规模|乡|镇|县)(?:（.*）)?$|^$', supplier):
                break
            # 单个名称有问题，跳过该名称
            if re.search(r'[^\u4E00-\u9FA50-9a-zA-Z()（）<>《》]|[某Xx]|^[0-9a-zA-Z.,，。 ()（）]*$|《.*》((?!(公司|社)).)*$',
                         supplier) or len(supplier) < 4:
                continue
            # 整个供应商名称被括号包围
            if re.search(r'^（.*）$|^\(.*\)$', supplier):
                supplier = supplier[1:-1]
            provider = PurchaseProvider()
            provider.OrgName = supplier
            provider_address = ''

            if len(address_list) > index:
                provider_address = address_list[index]

            provider.IdentityState = 1
            provider.ImportTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            # 供应商地域标识
            dic = address_identification.address_identification(supplier, provider_address)
            provider.LocalProv = dic.get("province_id")
            provider.LocalCity = dic.get("city_id")
            provider.LocalCounty = dic.get("district_id")
            provider.LocalProvName = dic.get("province")
            provider.LocalCityName = dic.get("city")
            provider.LocalCountyName = dic.get("district")
            provider.LocalAddr = provider_address

            # 经营范围（需要休眠太耗时，此处不解析，单独写了个解析器去解析）
            provider.ConcurrentlyScope = None

            back['add'].append(provider)
            back['history'].append({'resolver_id': getattr(self, 'id'), 'announcement_id': announcement_info.id,
                                    'relation': provider})
        return back
