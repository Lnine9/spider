"""
代理机构解析器（新版）
"""
import re
import time

from RelationAnalysis.data_operate.announcement.call_bid_government import CallBidGovernment
from RelationAnalysis.data_operate.relation_analysis.purchase_agent import PurchaseAgent
from RelationAnalysis.resolve.address_identification import AddressIdentification
from RelationAnalysis.resolve.resolve_tools import get_name, get_phone
from RelationAnalysis.resolve.resolver_interface import ResolverInterface

address_identification = AddressIdentification()


class PurchaseAgentResolver(ResolverInterface):

    def __init__(self):
        self.all_item = {}

    def analysis(self, announcement_info: CallBidGovernment):
        """
        解析
        :param announcement_info:
        :return:
        """

        agency = PurchaseAgent()
        agency_org_name = announcement_info.agent_unit_name if announcement_info.agent_unit_name else ''
        agency_org_name = re.sub(r'[?？：: ]', '', agency_org_name).strip()
        if agency_org_name and len(agency_org_name) >= 4 and not re.findall(
                r'[^\u4E00-\u9FA50-9a-zA-Z()（）<>《》]|[某Xx]|^[0-9a-zA-Z.,，。 ()（）]*$|《.*》((?!(公司|社)).)*$', agency_org_name):
            agency.OrgName = agency_org_name
            agency.IdentityState = 1
            agency.ImportTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            # 代理机构联系人、联系电话
            agency.LinkmanName = get_name(announcement_info.agent_unit_m)
            agency.LinkmanPhone = get_phone(announcement_info.agent_unit_m)

            # 代理机构地域标识
            dic = address_identification.address_identification(announcement_info.agent_unit_address,
                                                                announcement_info.agent_unit_name)

            agency.LocalProv = dic.get("province_id")
            agency.LocalCity = dic.get("city_id")
            agency.LocalCounty = dic.get("district_id")
            agency.LocalProvName = dic.get("province")
            agency.LocalCityName = dic.get("city")
            agency.LocalCountyName = dic.get("district")
            agency.LocalAddr = announcement_info.agent_unit_address

            return {'add': [agency],
                    'history': {'resolver_id': getattr(self, 'id'), 'announcement_id': announcement_info.id,
                                'relation': agency}}
