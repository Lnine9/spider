"""
采购人解析器
"""
import re
import time

from RelationAnalysis.data_operate.announcement.call_bid_government import CallBidGovernment
from RelationAnalysis.data_operate.relation_analysis.purchase_stock import PurchaseStock
from RelationAnalysis.resolve.address_identification import AddressIdentification
from RelationAnalysis.resolve.resolve_tools import get_name, get_phone
from RelationAnalysis.resolve.resolver_interface import ResolverInterface

address_identification = AddressIdentification()


class PurchaserStockResolver(ResolverInterface):

    def __init__(self):
        self.all_item = {}

    def analysis(self, announcement_info: CallBidGovernment):
        """
        解析
        :param announcement_info:
        :return:
        """

        purchaser = PurchaseStock()
        call_unit = announcement_info.call_unit if announcement_info.call_unit else ''
        call_unit = re.sub(r'[?？：: 　]', '', call_unit).strip()
        if call_unit and len(call_unit) >= 4 and not re.findall(
                r'[^\u4E00-\u9FA50-9a-zA-Z()（）<>《》]|[某Xx]|^[0-9a-zA-Z.,，。 ]*$|《.*》((?!(公司|社)).)*$|项目名称|详见|采购内容', call_unit):
            purchaser.OrgName = call_unit
            purchaser.IdentityState = '1'
            purchaser.ImportTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            # 采购单位地域标识
            dic = address_identification.address_identification(announcement_info.call_unit_address,
                                                                announcement_info.call_unit,
                                                                announcement_info.region,)
            purchaser.LocalProv = dic.get("province_id")
            purchaser.LocalCity = dic.get("city_id")
            purchaser.LocalCounty = dic.get("district_id")
            purchaser.LocalProvName = dic.get("province")
            purchaser.LocalCityName = dic.get("city")
            purchaser.LocalCountyName = dic.get("district")
            purchaser.LocalAddr = announcement_info.call_unit_address

            purchaser.LinkmanName = get_name(announcement_info.proj_rel_p)
            purchaser.LinkmanPhone = get_phone(announcement_info.proj_rel_m)

            return {'add': [purchaser],
                    'history': {'resolver_id': getattr(self, 'id'), 'announcement_id': announcement_info.id,
                                'relation': purchaser}}
