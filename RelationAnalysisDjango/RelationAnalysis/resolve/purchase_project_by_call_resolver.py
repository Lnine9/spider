"""
采购项目解析器
"""
import re

from RelationAnalysis.data_operate.announcement.call_bid_government import CallBidGovernment
from RelationAnalysis.data_operate.relation_analysis.proj_link_rel import ProjLinkRel
from RelationAnalysis.data_operate.relation_analysis.purchase_agent import PurchaseAgent
from RelationAnalysis.data_operate.relation_analysis.purchase_project import PurchaseProject
from RelationAnalysis.data_operate.relation_analysis.purchase_stock import PurchaseStock
from RelationAnalysis.resolve.address_identification import AddressIdentification
from RelationAnalysis.resolve.chaintext import IndustryDivide
from RelationAnalysis.resolve.key_words import get_key_words
from RelationAnalysis.resolve.resolve_tools import get_purchase_method, get_phone, get_name, \
    get_item_and_code, merge_item, get_distrcit_name_and_code
from RelationAnalysis.resolve.resolver_interface import ResolverInterface

industry_divide = IndustryDivide()
address_identification = AddressIdentification()


class PurchaseProjectByCallResolver(ResolverInterface):
    """
    采购公告生成采购项目
    """

    def __init__(self):
        self.all_item = {}

    """
    解析
    """

    def analysis(self, announcement_info: CallBidGovernment):
        back = {'update': []}
        project = PurchaseProject()

        project.State = 4
        project.IssueTime = announcement_info.ancm_time

        # 行政区域（用采购人地址补充）
        region_dic = get_distrcit_name_and_code(announcement_info.call_unit_address,
                                                announcement_info.call_unit,
                                                announcement_info.region)
        project.DistrcitCode = region_dic.get("DistrcitCode")
        project.DistrictName = region_dic.get("DistrictName")

        project.Title = announcement_info.title
        project.Content = announcement_info.proj_name
        project.ProjectName = announcement_info.proj_name
        project.ProjectCode = announcement_info.proj_code

        if announcement_info.budget and '0E' in announcement_info.budget:
            project.ProjectBudget = 0.0
        else:
            project.ProjectBudget = announcement_info.budget

        # 获取采购方式及其编码
        purchase_method_dit = get_purchase_method(announcement_info.purchase_m, announcement_info.sourse_url)
        project.ProjectPurchaseWay = purchase_method_dit.get('purchase_code')
        project.ProjectPurchaseWayName = purchase_method_dit.get('purchase_method')

        # 采购项目品目
        item_code_result = get_item_and_code(announcement_info.proj_item)
        project.ProjectDirectoryCode = ''
        project.ProjectDirectoryName = ''
        for item in item_code_result:
            if item.get('code') is not None and item.get('name') is not None:
                project.ProjectDirectoryCode += str(item.get('code')) + '，'
                project.ProjectDirectoryName += item.get('name') + '，'
        project.ProjectDirectoryCode = project.ProjectDirectoryCode[:-1]
        project.ProjectDirectoryName = project.ProjectDirectoryName[:-1]
        # 去重
        project_directory_set = merge_item(None, None, project.ProjectDirectoryCode, project.ProjectDirectoryName)
        project.ProjectDirectoryCode = '，'.join(item[0] for item in project_directory_set)
        project.ProjectDirectoryName = '，'.join(item[1] for item in project_directory_set)

        # 采购人、代理机构、供应商、采购项目的行业划分相同
        # 从采购公告中提取采购项目的信息，用中标公告补充其中的中标信息，若采购公告不存在，从中标公告中获取。

        # 采购人行业划分
        project.TradeType = ''
        project.TradeTypeName = ''

        industry_divide_result = industry_divide.get_industry(announcement_info.call_unit)
        for item in industry_divide_result:
            if item.get('id') is not None and item.get('name') is not None:
                project.TradeType += str(item.get('id')) + '，'
                project.TradeTypeName += item.get('name') + '，'
        project.TradeType = project.TradeType[:-1]
        project.TradeTypeName = project.TradeTypeName[:-1]

        # 供应商行业划分
        project.ProjectIndustryCode = project.TradeType
        project.ProjectIndustryName = project.TradeTypeName
        project.ProjectIndustry = None  # 暂不处理

        # 关键字
        project.Keyword = '，'.join(get_key_words(str(announcement_info.to_json()), 10, False))

        '''
        采购人信息填充
        '''
        # 需要地址编号去唯一区别同名公司，这里再次解析地址编号
        if not announcement_info.call_unit:
            announcement_info.call_unit = ''
        announcement_info.call_unit = re.sub(r'[?？：: 　]', '', announcement_info.call_unit).strip()
        stock_address_dic = address_identification.address_identification(announcement_info.call_unit_address,
                                                                          announcement_info.call_unit,
                                                                          announcement_info.region)
        purchase_stock_query = PurchaseStock.query(OrgName=announcement_info.call_unit,
                                                   LocalProv=stock_address_dic.get('province_id'))
        if len(purchase_stock_query) > 0 and purchase_stock_query[0].OrgName:
            project.Buyer = purchase_stock_query[0].Id
            # 修改采购单位采购目录
            purchase_stock_directory_set = merge_item(purchase_stock_query[0].ProjectDirectoryCode,
                                                      purchase_stock_query[0].ProjectDirectoryName,
                                                      project.ProjectDirectoryCode,
                                                      project.ProjectDirectoryName)
            purchase_stock_query[0].ProjectDirectoryCode = '，'.join(item[0] for item in purchase_stock_directory_set)
            purchase_stock_query[0].ProjectDirectoryName = '，'.join(item[1] for item in purchase_stock_directory_set)
            # 修改采购单位总项目数
            purchase_stock_query[0].TotalNum = (purchase_stock_query[0].TotalNum if purchase_stock_query[
                0].TotalNum else 0) + 1
            # 修改采购单位行业划分
            purchase_stock_trade_type_set = merge_item(purchase_stock_query[0].TradeType,
                                                       purchase_stock_query[0].TradeTypeName,
                                                       project.TradeType,
                                                       project.TradeTypeName)
            purchase_stock_query[0].TradeType = '，'.join(item[0] for item in purchase_stock_trade_type_set)
            purchase_stock_query[0].TradeTypeName = '，'.join(item[1] for item in purchase_stock_trade_type_set)
            back['update'].append(purchase_stock_query[0])

        project.BuyerName = announcement_info.call_unit
        project.BuyerPerson = get_name(announcement_info.proj_rel_p)
        project.BuyserTEL = get_phone(announcement_info.proj_rel_m)

        '''
        代理机构信息填充
        '''
        if not announcement_info.agent_unit_name:
            announcement_info.agent_unit_name = ''
        announcement_info.agent_unit_name = re.sub(r'[?？：: 　]', '', announcement_info.agent_unit_name).strip()
        agent_address_dic = address_identification.address_identification(announcement_info.agent_unit_address,
                                                                          announcement_info.agent_unit_name)
        if announcement_info.agent_unit_name == '公共资源交易中心':
            purchase_agent_query = PurchaseAgent.query(OrgName=announcement_info.agent_unit_name,
                                                       LocalProv=agent_address_dic.get('province_id'))
        else:
            purchase_agent_query = PurchaseAgent.query(OrgName=announcement_info.agent_unit_name)
        if len(purchase_agent_query) > 0 and purchase_agent_query[0].OrgName:
            project.Agent = purchase_agent_query[0].Id
            # 修改代理机构采购目录
            purchase_agent_directory_set = merge_item(purchase_agent_query[0].ProjectDirectoryCode,
                                                      purchase_agent_query[0].ProjectDirectoryName,
                                                      project.ProjectDirectoryCode,
                                                      project.ProjectDirectoryName)
            purchase_agent_query[0].ProjectDirectoryCode = '，'.join(item[0] for item in purchase_agent_directory_set)
            purchase_agent_query[0].ProjectDirectoryName = '，'.join(item[1] for item in purchase_agent_directory_set)
            # 修改代理机构总项目数
            purchase_agent_query[0].TotalNum += 1
            # 修改代理机构服务专业
            key_word_list = []
            service_major_list = []
            if project.Keyword:
                key_word_list = list(project.Keyword.split('，'))
            if purchase_agent_query[0].ServiceMajor:
                service_major_list = list(purchase_agent_query[0].ServiceMajor.split('，'))
            service_major_list += key_word_list
            purchase_agent_query[0].ServiceMajor = '，'.join(set(service_major_list))
            # 修改代理机构服务区域
            district_name_list = []
            service_area_list = []
            if project.DistrictName:
                district_name_list = list(project.DistrictName.split('，'))
            if purchase_agent_query[0].ServiceArea:
                service_area_list = list(purchase_agent_query[0].ServiceArea.split('，'))
            service_area_list += district_name_list
            purchase_agent_query[0].ServiceArea = '，'.join(set(service_area_list))
            # 修改代理机构行业划分
            purchase_agent_trade_type_set = merge_item(purchase_agent_query[0].TradeType,
                                                       purchase_agent_query[0].TradeTypeName,
                                                       project.TradeType,
                                                       project.TradeTypeName)
            purchase_agent_query[0].TradeType = '，'.join(item[0] for item in purchase_agent_trade_type_set)
            purchase_agent_query[0].TradeTypeName = '，'.join(item[1] for item in purchase_agent_trade_type_set)
            back['update'].append(purchase_agent_query[0])

        project.AgentName = announcement_info.agent_unit_name
        project.AgentPerson = get_name(announcement_info.agent_unit_m)
        project.AgentTEL = get_phone(announcement_info.agent_unit_m)

        # 购买明细
        project.PurchaseDesWay = None  # 暂不处理
        project.PurchaseDes = None  # 暂不处理

        # 中标供应商（此处不填写，解析中标时匹配填充）
        project.BidWinSupplierId = None
        project.BidWinSupplier = None
        project.BidWinAmount = None

        project.SourseUrl = announcement_info.sourse_url
        project.SourseName = announcement_info.source_web_name
        project.sourceType = 3

        rel = self.create_rel(announcement_info.id, None, project)
        back['add'] = [project, rel]
        back['history'] = {'resolver_id': getattr(self, 'id'), 'announcement_id': announcement_info.id,
                           'relation': project}
        return back

    @staticmethod
    def create_rel(call_id, win_id, project):
        resolver_relation = ProjLinkRel()
        resolver_relation.call_id = call_id
        resolver_relation.win_id = win_id
        resolver_relation._relation = project
        return resolver_relation
