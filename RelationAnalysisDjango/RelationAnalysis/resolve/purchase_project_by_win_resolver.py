"""
采购项目解析器（中标）
"""
import re
import time

from RelationAnalysis.data_operate.announcement.call_bid_government import CallBidGovernment
from RelationAnalysis.data_operate.announcement.win_bid_government import WinBidGovernment
from RelationAnalysis.data_operate.pool_table import RelTable
from RelationAnalysis.data_operate.relation_analysis.proj_link_rel import ProjLinkRel
from RelationAnalysis.data_operate.relation_analysis.purchase_agent import PurchaseAgent
from RelationAnalysis.data_operate.relation_analysis.purchase_project import PurchaseProject
from RelationAnalysis.data_operate.relation_analysis.purchase_provider import PurchaseProvider
from RelationAnalysis.data_operate.relation_analysis.purchase_stock import PurchaseStock
from RelationAnalysis.resolve.address_identification import AddressIdentification
from RelationAnalysis.resolve.chaintext import IndustryDivide
from RelationAnalysis.resolve.key_words import get_key_words
from RelationAnalysis.resolve.resolve_tools import get_purchase_method, get_phone, get_name, \
    get_item_and_code, merge_item, get_distrcit_name_and_code
from RelationAnalysis.resolve.resolver_interface import ResolverInterface

industry_divide = IndustryDivide()
address_identification = AddressIdentification()


class PurchaseProjectByWinResolver(ResolverInterface):
    """
    中标公告生成采购项目
    """

    def __init__(self):
        self.all_item = {}

    """
    解析
    """

    def analysis(self, announcement_info: WinBidGovernment):

        back = {'update': [], 'add': [], 'history': []}

        # 用该项目编号找到采购项目
        project_list = []
        if announcement_info.proj_code:
            project_list = PurchaseProject.query(ProjectCode=announcement_info.proj_code)

        # 关联成功，在原采购项目中添加中标信息
        if len(project_list) > 0 and project_list[0].ProjectName:

            # 采购单位信息补充（关联成功）
            stock = self.success_stock_information_supplement(project_list, announcement_info)
            # 代理机构信息补充（关联成功）
            agent = self.success_agent_information_supplement(project_list, announcement_info)
            # 供应商信息补充（关联成功）
            provider = list(self.success_provider_information_supplement(project_list, announcement_info))
            # 采购项目信息补充（关联成功）
            project = self.success_project_information_supplement(project_list, announcement_info)
            # 解析关系更新
            call_bid_government_list = CallBidGovernment.query(proj_code=announcement_info.proj_code)
            call_id = call_bid_government_list[0].id if len(call_bid_government_list) > 0 else None
            rel = self.create_resolver_relation(call_id, announcement_info.id, project_list[0])

            back['update'].append(project)
            back['update'].append(stock)
            back['update'].append(agent)
            back['update'] += list(provider)
            back['add'].append(rel)

        # 关联失败，用中标公告生成采购项目
        else:
            project = PurchaseProject()
        #     # 采购人信息补充（关联失败）
        #     stock = self.defeat_stock_information_supplement(self, project, announcement_info)
        #     # 代理机构信息补充（关联失败）
        #     agent = self.defeat_agent_information_supplement(self, project, announcement_info)
            # 供应商信息补充（关联失败）
            provider = list(self.defeat_provider_information_supplement(project, announcement_info))
        #     # 采购项目信息生成（关联失败）
        #     project = self.defeat_project_information_supplement(project, announcement_info)
            # 解析关系入库
            rel = self.create_resolver_relation(None, announcement_info.id, project)
        #
        #     if not isinstance(stock, dict):
        #         back['update'].append(stock)
        #     else:
        #         back['add'] += stock.get('add')
        #         back['history'].append(stock.get('history'))
        #
        #     if not isinstance(agent, dict):
        #         back['update'].append(agent)
        #     else:
        #         back['add'] += agent.get('add')
        #         back['history'].append(agent.get('history'))
        #
        #     back['add'].append(project)
            back['update'] += provider
            back['add'].append(rel)

        # 暂时只处理成功，已缩进
        back['history'].append({'resolver_id': getattr(self, 'id'), 'announcement_id': announcement_info.id,
                                'relation': project})
        return back

    @staticmethod
    def create_resolver_relation(call_id, win_id, project):
        """
        解析关系入库
        :param call_id:
        :param win_id:
        :param project:
        :return:
        """
        resolver_relation = ProjLinkRel()
        resolver_relation.id = RelTable.UUID_SHORT()
        resolver_relation.call_id = call_id
        resolver_relation.win_id = win_id
        resolver_relation._relation = project
        return resolver_relation

    @staticmethod
    def success_project_information_supplement(project_list, announcement_info):
        """
        采购项目信息补充（关联成功）
        :param project_list:
        :param announcement_info:
        :return:
        """
        project_list[0].BidWinSupplierId = project_list[0].BidWinSupplierId[:-1]
        project_list[0].BidWinSupplier = project_list[0].BidWinSupplier[:-1]
        project_list[0].BidWinAmount = announcement_info.actual_price
        return project_list[0]

    @staticmethod
    def defeat_project_information_supplement(project, announcement_info):
        """
        采购项目信息生成（关联失败）
        :param project:
        :param announcement_info:
        :return:
        """
        # 基础信息
        project.Title = announcement_info.title
        project.Content = announcement_info.proj_name
        project.ProjectName = announcement_info.proj_name
        project.ProjectCode = announcement_info.proj_code
        project.IssueTime = announcement_info.ancm_time
        project.State = 4
        project.ProjectBudget = None

        # 行政区域（用采购人地址补充）
        region_dic = get_distrcit_name_and_code(announcement_info.call_unit_address,
                                                announcement_info.call_unit,
                                                announcement_info.region)
        project.DistrcitCode = region_dic.get("DistrcitCode")
        project.DistrictName = region_dic.get("DistrictName")

        # 获取采购方式及其编码
        purchase_method_dit = get_purchase_method(announcement_info.purchase_m, announcement_info.sourse_url)
        project.ProjectPurchaseWay = purchase_method_dit.get('purchase_code')
        project.ProjectPurchaseWayName = purchase_method_dit.get('purchase_method')

        # 关键字
        project.Keyword = '，'.join(get_key_words(str(announcement_info.to_json()), 10, False))

        # 采购人、代理机构、供应商、采购项目的行业划分相同
        # 用采购公告生成采购项目，用中标公告补充其中的中标信息，若采购公告不存在，用中标公告生成采购项目。

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
        # 采购单位信息
        project.BuyerName = announcement_info.call_unit
        project.BuyerPerson = get_name(announcement_info.proj_rel_p)
        project.BuyserTEL = get_phone(announcement_info.proj_rel_m)
        # 代理机构信息
        project.AgentName = announcement_info.agent_unit_name
        project.AgentPerson = get_name(announcement_info.agent_unit_m)
        project.AgentTEL = get_phone(announcement_info.agent_unit_m)
        # 供应商信息
        project.BidWinAmount = announcement_info.actual_price
        project.BidWinSupplierId = project.BidWinSupplierId[:-1]
        project.BidWinSupplier = project.BidWinSupplier[:-1]
        # 来源信息
        project.SourseUrl = announcement_info.sourse_url
        project.SourseName = announcement_info.source_web_name
        project.sourceType = 3
        # 购买明细
        project.PurchaseDesWay = None  # 暂不处理
        project.PurchaseDes = None  # 暂不处理

        return project

    @staticmethod
    def success_stock_information_supplement(project_list, announcement_info):
        """
        采购人信息补充（关联成功）
        :param project_list:
        :param announcement_info:
        :return:
        """
        if not announcement_info.call_unit:
            announcement_info.call_unit = ''
        announcement_info.call_unit = re.sub(r'[?？：: 　]', '', announcement_info.call_unit).strip()
        stock_address_dic = address_identification.address_identification(announcement_info.call_unit_address,
                                                                          announcement_info.call_unit,
                                                                          announcement_info.region)
        purchase_stock_query = PurchaseStock.query(OrgName=announcement_info.call_unit,
                                                   LocalProv=stock_address_dic.get('province_id'))
        if len(purchase_stock_query) > 0 and purchase_stock_query[0].OrgName:
            # 修改采购单位中标项目数
            purchase_stock_query[0].WinBidNum += 1
            return purchase_stock_query[0]

    @staticmethod
    def defeat_stock_information_supplement(self, project, announcement_info):
        """
        采购人信息补充或新增（关联失败）
        :param project:
        :param announcement_info:
        :return:
        """
        if not announcement_info.call_unit:
            announcement_info.call_unit = ''
        announcement_info.call_unit = re.sub(r'[?？：: 　]', '', announcement_info.call_unit).strip()
        stock_address_dic = address_identification.address_identification(announcement_info.call_unit_address,
                                                                          announcement_info.call_unit,
                                                                          announcement_info.region)
        purchase_stock_query = PurchaseStock.query(OrgName=announcement_info.call_unit,
                                                   LocalProv=stock_address_dic.get('province_id'))
        if len(purchase_stock_query) > 0:
            project.Buyer = purchase_stock_query[0].Id
            # 修改采购单位采购目录
            purchase_stock_directory_set = merge_item(purchase_stock_query[0].ProjectDirectoryCode,
                                                      purchase_stock_query[0].ProjectDirectoryName,
                                                      project.ProjectDirectoryCode,
                                                      project.ProjectDirectoryName)
            purchase_stock_query[0].ProjectDirectoryCode = '，'.join(item[0] for item in purchase_stock_directory_set)
            purchase_stock_query[0].ProjectDirectoryName = '，'.join(item[1] for item in purchase_stock_directory_set)
            # 修改采购单位中标项目数
            purchase_stock_query[0].WinBidNum += 1
            # 修改采购单位行业划分
            purchase_stock_trade_type_set = merge_item(purchase_stock_query[0].TradeType,
                                                       purchase_stock_query[0].TradeTypeName,
                                                       project.TradeType,
                                                       project.TradeTypeName)
            purchase_stock_query[0].TradeType = '，'.join(item[0] for item in purchase_stock_trade_type_set)
            purchase_stock_query[0].TradeTypeName = '，'.join(item[1] for item in purchase_stock_trade_type_set)
            return purchase_stock_query[0]
        else:
            return PurchaseProjectByWinResolver.purchase_stock_by_win_resolve(self, announcement_info)

    @staticmethod
    def success_agent_information_supplement(project_list, announcement_info):
        """
        代理机构信息补充（关联成功）
        :param project_list:
        :param announcement_info:
        :return:
        """
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
        if len(purchase_agent_query) > 0:
            # 修改代理机构中标项目数
            purchase_agent_query[0].WinBidNum += 1
            # 修改供应商服务专业
            key_word_list = []
            service_major_list = []
            if project_list[0].Keyword:
                key_word_list = list(project_list[0].Keyword.split('，'))
            if purchase_agent_query[0].ServiceMajor:
                service_major_list = list(purchase_agent_query[0].ServiceMajor.split('，'))
            service_major_list += key_word_list
            purchase_agent_query[0].ServiceMajor = '，'.join(set(service_major_list))
            # 修改供应商服务区域
            district_name_list = []
            service_area_list = []
            if project_list[0].DistrictName:
                district_name_list = list(project_list[0].DistrictName.split('，'))
            if purchase_agent_query[0].ServiceArea:
                service_area_list = list(purchase_agent_query[0].ServiceArea.split('，'))
            service_area_list += district_name_list
            purchase_agent_query[0].ServiceArea = '，'.join(set(service_area_list))
            return purchase_agent_query[0]

    @staticmethod
    def defeat_agent_information_supplement(self, project, announcement_info):
        """
        代理机构信息补充（关联失败）
        :param project:
        :param announcement_info:
        :return:
        """
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
            # 修改代理机构中标项目数
            purchase_agent_query[0].WinBidNum += 1
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
            return purchase_agent_query[0]
        else:
            return PurchaseProjectByWinResolver.purchase_agent_by_win_resolve(self, announcement_info)

    @staticmethod
    def success_provider_information_supplement(project_list, announcement_info):
        """
        供应商信息补充（关联成功）
        :param project_list:
        :param announcement_info:
        :return:
        """
        supplier_name_list = []
        if announcement_info.provide_unit is not None:
            supplier_name_list = re.split(r'[/，,、]', announcement_info.provide_unit)
        project_list[0].BidWinSupplierId = ''
        project_list[0].BidWinSupplier = ''

        for index, supplier_name in enumerate(supplier_name_list):

            supplier_name = re.sub(r'[?？：: ."\']|(?:\d+\w+)分标', '', supplier_name).strip()
            # 如果供应商名称出现一些不该出现的字符，说明供应商和地址解析错误，后面的都停止解析
            if re.search(r'^无$|.*(?:名称|品牌|要求|地址|范围|规格型号|附件|规模|乡|镇|县)(?:（.*）)?$|^$', supplier_name):
                break
            # 单个名称有问题，跳过该名称
            if re.search(r'[^\u4E00-\u9FA50-9a-zA-Z()（）<>《》]|[某Xx]|^[0-9a-zA-Z.,，。 ()（）]*$|《.*》((?!(公司|社)).)*$',
                         supplier_name) or len(supplier_name) < 4:
                continue
            # 整个供应商名称被括号包围
            if re.search(r'^（.*）$|^\(.*\)$', supplier_name):
                supplier_name = supplier_name[1:-1]

            # 供应商名称存在才解析
            if supplier_name:
                # 用供应商名称为条件去查询该供应商
                purchase_provider_query = PurchaseProvider.query(OrgName=supplier_name)

                if len(purchase_provider_query) > 0 and purchase_provider_query[0].OrgName:
                    project_list[0].BidWinSupplierId += str(purchase_provider_query[0].Id) + '，'
                    project_list[0].BidWinSupplier += supplier_name + '，'
                    # 修改供应商采购目录
                    purchase_provider_query[0].ProjectDirectoryCode = project_list[0].ProjectDirectoryCode
                    purchase_provider_query[0].ProjectDirectoryName = project_list[0].ProjectDirectoryName
                    purchase_provider_directory_set = merge_item(purchase_provider_query[0].ProjectDirectoryCode,
                                                                 purchase_provider_query[0].ProjectDirectoryName,
                                                                 project_list[0].ProjectDirectoryCode,
                                                                 project_list[0].ProjectDirectoryName)
                    purchase_provider_query[0].ProjectDirectoryCode = '，'.join(
                        item[0] for item in purchase_provider_directory_set)
                    purchase_provider_query[0].ProjectDirectoryName = '，'.join(
                        item[1] for item in purchase_provider_directory_set)
                    # 修改供应商总项目数（暂时不写）
                    # purchase_provider_query[0].TotalNum += 1
                    # 修改供应商服务专业
                    key_word_list = []
                    service_major_list = []
                    if project_list[0].Keyword:
                        key_word_list = list(project_list[0].Keyword.split('，'))
                    if purchase_provider_query[0].ServiceMajor:
                        service_major_list = list(purchase_provider_query[0].ServiceMajor.split('，'))
                    service_major_list += key_word_list
                    purchase_provider_query[0].ServiceMajor = '，'.join(set(service_major_list))
                    # 修改供应商服务区域
                    district_name_list = []
                    service_area_list = []
                    if project_list[0].DistrictName:
                        district_name_list = list(project_list[0].DistrictName.split('，'))
                    if purchase_provider_query[0].ServiceArea:
                        service_area_list = list(purchase_provider_query[0].ServiceArea.split('，'))
                    service_area_list += district_name_list
                    purchase_provider_query[0].ServiceArea = '，'.join(set(service_area_list))
                    # 修改供应商行业划分
                    purchase_provider_trade_type_set = merge_item(purchase_provider_query[0].TradeType,
                                                                  purchase_provider_query[0].TradeTypeName,
                                                                  project_list[0].TradeType,
                                                                  project_list[0].TradeTypeName)
                    purchase_provider_query[0].TradeType = '，'.join(
                        item[0] for item in purchase_provider_trade_type_set)
                    purchase_provider_query[0].TradeTypeName = '，'.join(
                        item[1] for item in purchase_provider_trade_type_set)
                    yield purchase_provider_query[0]

    @staticmethod
    def defeat_provider_information_supplement(project, announcement_info):
        """
        供应商信息补充（关联失败）
        :param project:
        :param announcement_info:
        :return:
        """
        supplier_name_list = []
        if announcement_info.provide_unit is not None:
            supplier_name_list = re.split(r'[/，,、]', announcement_info.provide_unit)
        project.BidWinSupplierId = ''
        project.BidWinSupplier = ''
        for index, supplier_name in enumerate(supplier_name_list):
            supplier_name = re.sub(r'[?？：: ."\']|(?:\d+\w+)分标', '', supplier_name).strip()
            # 如果供应商名称出现一些不该出现的字符，说明供应商和地址解析错误，后面的都停止解析
            if re.search(r'^无$|.*(?:名称|品牌|要求|地址|范围|规格型号|附件|规模|乡|镇|县)(?:（.*）)?$|^$', supplier_name):
                break
            # 单个名称有问题，跳过该名称
            if re.search(r'[^\u4E00-\u9FA50-9a-zA-Z()（）<>《》]|[某Xx]|^[0-9a-zA-Z.,，。 ()（）]*$|《.*》((?!(公司|社)).)*$',
                         supplier_name) or len(supplier_name) < 4:
                continue
            # 整个供应商名称被括号包围
            if re.search(r'^（.*）$|^\(.*\)$', supplier_name):
                supplier_name = supplier_name[1:-1]

            if supplier_name != '' and supplier_name is not None:
                purchase_provider_query = PurchaseProvider.query(OrgName=supplier_name)

                if len(purchase_provider_query) > 0 and purchase_provider_query[0].OrgName:
                    project.BidWinSupplierId += str(purchase_provider_query[0].Id) + '，'
                    project.BidWinSupplier += supplier_name + '，'
                    # 修改供应商采购目录
                    purchase_provider_query[0].ProjectDirectoryCode = project.ProjectDirectoryCode
                    purchase_provider_query[0].ProjectDirectoryName = project.ProjectDirectoryName
                    purchase_provider_directory_set = merge_item(purchase_provider_query[0].ProjectDirectoryCode,
                                                                 purchase_provider_query[0].ProjectDirectoryName,
                                                                 project.ProjectDirectoryCode,
                                                                 project.ProjectDirectoryName)
                    purchase_provider_query[0].ProjectDirectoryCode = '，'.join(
                        item[0] for item in purchase_provider_directory_set)
                    purchase_provider_query[0].ProjectDirectoryName = '，'.join(
                        item[1] for item in purchase_provider_directory_set)
                    # 修改供应商总项目数（暂时不写）
                    # purchase_provider_query[0].TotalNum += 1
                    # 修改供应商服务专业
                    key_word_list = []
                    service_major_list = []
                    if project.Keyword:
                        key_word_list = list(project.Keyword.split('，'))
                    if purchase_provider_query[0].ServiceMajor:
                        service_major_list = list(purchase_provider_query[0].ServiceMajor.split('，'))
                    service_major_list += key_word_list
                    purchase_provider_query[0].ServiceMajor = '，'.join(set(service_major_list))
                    # 修改供应商服务区域
                    district_name_list = []
                    service_area_list = []
                    if project.DistrictName:
                        district_name_list = list(project.DistrictName.split('，'))
                    if purchase_provider_query[0].ServiceArea:
                        service_area_list = list(purchase_provider_query[0].ServiceArea.split('，'))
                    service_area_list += district_name_list
                    purchase_provider_query[0].ServiceArea = '，'.join(set(service_area_list))
                    # 修改供应商行业划分
                    purchase_provider_trade_type_set = merge_item(purchase_provider_query[0].TradeType,
                                                                  purchase_provider_query[0].TradeTypeName,
                                                                  project.TradeType,
                                                                  project.TradeTypeName)
                    purchase_provider_query[0].TradeType = '，'.join(
                        item[0] for item in purchase_provider_trade_type_set)
                    purchase_provider_query[0].TradeTypeName = '，'.join(
                        item[1] for item in purchase_provider_trade_type_set)
                    yield purchase_provider_query[0]

    @staticmethod
    def purchase_stock_by_win_resolve(self, announcement_info):
        """
        中标公告生成采购单位
        :param self:
        :param announcement_info:
        :return:
        """
        purchaser = PurchaseStock()
        call_unit = announcement_info.call_unit if announcement_info.call_unit else ''
        call_unit = re.sub(r'[?？：: ]', '', call_unit).strip()
        if call_unit and len(call_unit) >= 4 and not re.findall(
                r'[^\u4E00-\u9FA50-9a-zA-Z()（）<>《》]|[某Xx]|^[0-9a-zA-Z.,，。 ]*$|《.*》((?!(公司|社)).)*$', call_unit):
            purchaser.OrgName = call_unit
            purchaser.IdentityState = '1'
            purchaser.ImportTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            # 采购单位地域标识
            dic = address_identification.address_identification(announcement_info.call_unit,
                                                                announcement_info.call_unit_address)
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

    @staticmethod
    def purchase_agent_by_win_resolve(self, announcement_info):
        """
        中标公告生成代理机构
        :param self:
        :param announcement_info:
        :return:
        """

        agency = PurchaseAgent()
        agency_org_name = announcement_info.agent_unit_name if announcement_info.agent_unit_name else ''
        agency_org_name = re.sub(r'[?？：: ]', '', agency_org_name).strip()
        if agency_org_name and len(agency_org_name) >= 4 and not re.findall(
                r'[^\u4E00-\u9FA50-9a-zA-Z()（）<>《》]|[某Xx]|^[0-9a-zA-Z.,，。 ]*$|《.*》((?!(公司|社)).)*$', agency_org_name):
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
