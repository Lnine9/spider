import re

from RelationAnalysis.entity.exceptions import WinBidAssociationFailureException
from RelationAnalysis.server.repeat_check import change_to_update
from RelationAnalysis.tool.logging import logger
from RelationAnalysis.data_operate.pool_table import RelTable
from RelationAnalysis.data_operate.relation_analysis.proj_link_rel import ProjLinkRel
from RelationAnalysis.resolve.resolve_tools import update_resolve


def check_default(obj):
    """
    默认检查方法（检查方法示例）：未检查
    :param obj:
    :return:
    """
    # if obj.__class__.__name__ != 'PurchaseProvider':
    logger.warning(f"未找到新增数据检查方法；类型：{obj.__class__.__name__}")
    return {'key': 'add', 'value': obj}


def purchase_stock(purchaser):
    """
    采购单位信息入库校验
    :param purchaser:
    :return:relation_id
    """
    back = {'key': 'add', 'value': None}
    # 采购单位中出现[省市区县]，省份简称或大学，则仅采用名称去重
    if re.search(r'[省市区县]|北京|天津|河北|山西|内蒙古|辽宁|吉林|黑龙江|上海|江苏|浙江|安徽|福建|江西|山东|河南|湖北|湖南|广东|广西|海南|'
                 r'重庆|四川|贵州|云南|西藏|陕西|甘肃|青海|宁夏|新疆|台湾|香港|澳门|大学|自治州', purchaser.OrgName):
        query_list = purchaser.query(OrgName=purchaser.OrgName)
    else:
        query_list = purchaser.query(OrgName=purchaser.OrgName,
                                     LocalProv=purchaser.LocalProv)
    if len(query_list) == 0:
        if purchaser.LocalProv:
            purchaser.Id = purchaser.OrgId = purchaser.id = RelTable.UUID_SHORT()
            purchaser.TotalNum = 0
            purchaser.WinBidNum = 0
        else:
            return back
    else:
        purchaser.Id = purchaser.OrgId = purchaser.id = query_list[0].Id
        # 如果新解析对象省市区级地址完整，旧解析对象不完整，则先将旧解析对象省市区级地址置空，再用新解析对象的省市区级地址填充
        if purchaser.LocalProv and purchaser.LocalCity and purchaser.LocalCounty \
                and (not query_list[0].LocalProv or not query_list[0].LocalCity or not query_list[0].LocalCounty):
            query_list[0].LocalProv = query_list[0].LocalCity = query_list[0].LocalCounty = None
            query_list[0].LocalProvName = query_list[0].LocalCityName = query_list[0].LocalCountyName = query_list[0].LocalAddr = None
        purchaser = update_resolve(purchaser, query_list[0])
        back['key'] = 'update'

    back['value'] = purchaser
    return back


def purchase_agent(agency):
    """
    代理机构信息
    :param agency:
    :return:
    """
    back = {'key': 'add', 'value': None}
    # 查询代理机构实体是否已存在
    if agency.OrgName == '公共资源交易中心':
        query_list = agency.query(OrgName=agency.OrgName, LocalProv=agency.LocalProv)
    else:
        query_list = agency.query(OrgName=agency.OrgName)

    if len(query_list) == 0:
        agency.Id = agency.OrgId = agency.id = RelTable.UUID_SHORT()
        agency.TotalNum = 0
        agency.WinBidNum = 0
    else:
        agency.Id = agency.OrgId = agency.id = query_list[0].Id
        agency = update_resolve(agency, query_list[0])
        back['key'] = 'update'

    back['value'] = agency
    return back


def purchase_project(project):
    """
    采购项目信息入库
    :param project:
    """
    back = {'key': 'add', 'value': None}
    # 查询采购项目实体是否已存在
    query_list = project.query(ProjectName=project.ProjectName, ProjectCode=project.ProjectCode)

    if len(query_list) == 0:
        project.Id = project.id = RelTable.UUID_SHORT()
    else:
        project.Id = project.id = query_list[0].Id
        project = update_resolve(project, query_list[0])
        back['key'] = 'update'

    back['value'] = project
    return back


def proj_link_rel(resolver_relation):
    """
    解析关系入库
    :return:
    """
    back = {'key': 'add', 'value': None}
    # 查询解析关系是否已存在
    proj_id = getattr(resolver_relation._relation, 'id', getattr(resolver_relation._relation, 'Id', None))
    if proj_id is None:
        raise WinBidAssociationFailureException("proj_link_rel--proj_id获取失败")
    query_list = ProjLinkRel.query(proj_id=proj_id)
    if len(query_list) == 0:
        # 新增解析关系
        resolver_relation.id = RelTable.UUID_SHORT()
        resolver_relation.proj_id = proj_id
    else:
        # 更新解析关系
        query_list[0].call_id = resolver_relation.call_id
        query_list[0].win_id = resolver_relation.win_id
        query_list[0].proj_id = proj_id
        resolver_relation = query_list[0]
        back['key'] = 'update'

    back['value'] = resolver_relation
    return back


add_check = {
    'PurchaseStock': purchase_stock,
    'PurchaseAgent': purchase_agent,
    'PurchaseProject': purchase_project,
    'ProjLinkRel': proj_link_rel,
}


def check_having(add):
    """
    数据去重与变更为更新
    :param add: 检查新增数据
    :return:
    """

    checked = {'add': [], 'update': []}

    for obj in add:
        check_info = add_check.get(obj.__class__.__name__, check_default)(obj)
        if check_info and check_info.get('value', None):
            checked[check_info.get('key', 'add')].append(check_info.get('value'))

    return checked
