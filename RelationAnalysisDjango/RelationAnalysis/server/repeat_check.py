import re

from RelationAnalysis.data_operate.pool_table import RelTable
from RelationAnalysis.data_operate.relation_analysis.proj_link_rel import ProjLinkRel
from RelationAnalysis.entity.exceptions import WinBidAssociationFailureException
from RelationAnalysis.resolve.resolve_tools import update_resolve


def check_default(obj, relations, index=-1):
    return relations


def purchase_provider(obj, relations, index=-1):
    for one in relations['add'][index + 1:]:
        if obj.OrgName == one.OrgName:
            relations['add'].remove(one)

    query_list = obj.query(OrgName=obj.OrgName)
    if len(query_list) == 0:  # 不存在，则新建Id
        obj.Id = obj.OrgId = obj.id = RelTable.UUID_SHORT()
        obj.WinBidNum = 1
    else:  # 已存在，则用已存在的Id
        obj.WinBidNum = query_list[0].WinBidNum + 1
        obj.Id = obj.OrgId = obj.id = query_list[0].Id
        # 用旧解析对象来完善新解析对象
        obj = update_resolve(obj, query_list[0])
        relations = change_to_update(obj, relations)

    return relations


def purchase_stock(obj, relations, index=-1):
    """
    采购单位信息入库校验
    :param obj:
    :param relations:
    :param index:
    :return:relation_id
    """

    # 采购单位中出现[省市区县]，省份简称或大学，则仅采用名称进行查询去重
    if re.search(r'[省市区县]|北京|天津|河北|山西|内蒙古|辽宁|吉林|黑龙江|上海|江苏|浙江|安徽|福建|江西|山东|河南|湖北|湖南|广东|广西|海南|'
                 r'重庆|四川|贵州|云南|西藏|陕西|甘肃|青海|宁夏|新疆|台湾|香港|澳门|大学|自治州', obj.OrgName):
        query_list = obj.query(OrgName=obj.OrgName)
    else:
        query_list = obj.query(OrgName=obj.OrgName,
                               LocalProv=obj.LocalProv)
    if len(query_list) == 0:
        if obj.LocalProv:
            obj.Id = obj.OrgId = obj.id = RelTable.UUID_SHORT()
            obj.TotalNum = 0
            obj.WinBidNum = 0
    else:
        obj.Id = obj.OrgId = obj.id = query_list[0].Id
        # 如果新解析对象省市区级地址完整，旧解析对象不完整，则先将旧解析对象省市区级地址置空，再用新解析对象的省市区级地址填充
        if obj.LocalProv and obj.LocalCity and obj.LocalCounty \
                and (not query_list[0].LocalProv or not query_list[0].LocalCity or not query_list[0].LocalCounty):
            query_list[0].LocalProv = query_list[0].LocalCity = query_list[0].LocalCounty = None
            query_list[0].LocalProvName = query_list[0].LocalCityName = query_list[0].LocalCountyName = query_list[
                0].LocalAddr = None
        obj = update_resolve(obj, query_list[0])
        relations = change_to_update(obj, relations)

    return relations


def purchase_agent(obj, relations, index=-1):
    """
    代理机构信息
    :param obj:
    :param relations:
    :param index:
    :return:relations
    """

    # 查询代理机构实体是否已存在
    if obj.OrgName == '公共资源交易中心':
        query_list = obj.query(OrgName=obj.OrgName, LocalProv=obj.LocalProv)
    else:
        query_list = obj.query(OrgName=obj.OrgName)

    if len(query_list) == 0:
        obj.Id = obj.OrgId = obj.id = RelTable.UUID_SHORT()
        obj.TotalNum = 0
        obj.WinBidNum = 0
    else:
        obj.Id = obj.OrgId = obj.id = query_list[0].Id
        obj = update_resolve(obj, query_list[0])
        relations = change_to_update(obj, relations)

    return relations


def purchase_project(obj, relations, index=-1):
    """
    采购项目信息入库
    :param obj:
    :param relations:
    :param index:
    :return:relations
    """

    # 查询采购项目实体是否已存在
    query_list = obj.query(ProjectName=obj.ProjectName, ProjectCode=obj.ProjectCode)

    if len(query_list) == 0:
        obj.Id = obj.id = RelTable.UUID_SHORT()
    else:
        obj.Id = obj.id = query_list[0].Id
        obj = update_resolve(obj, query_list[0])
        relations = change_to_update(obj, relations)

    return relations


def proj_link_rel(obj, relations, index=-1):
    """
    解析关系入库
    :param obj:
    :param relations:
    :param index:
    :return:relations
    """
    # 查询解析关系是否已存在
    proj_id = getattr(obj._relation, 'id', getattr(obj._relation, 'Id', None))
    if proj_id is None:
        raise WinBidAssociationFailureException("proj_link_rel--proj_id获取失败")
    query_list = ProjLinkRel.query(proj_id=proj_id)
    if len(query_list) == 0:
        # 新增解析关系
        obj.id = RelTable.UUID_SHORT()
        obj.proj_id = proj_id
    else:
        # 更新解析关系
        obj.id = query_list[0].id
        obj.proj_id = proj_id
        relations = change_to_update(obj, relations)

    return relations


def change_to_update(obj, relations):
    relations['add'].remove(obj)
    relations['update'].append(obj)
    return relations


def category_data(obj, relations, index=-1):
    obj.id = RelTable.UUID_SHORT()
    return relations


repeat_check_func = {
    'PurchaseProvider': purchase_provider,
    'PurchaseStock': purchase_stock,
    'PurchaseAgent': purchase_agent,
    'PurchaseProject': purchase_project,
    'ProjLinkRel': proj_link_rel,
    "CategoryData": category_data
}


def check_having(relations):
    """
    数据去重与变更为更新
    :param relations:
    :return:
    """
    index = 0
    while index < len(relations['add']):
        obj = relations['add'][index]
        relations = repeat_check_func.get(obj.__class__.__name__, check_default)(obj, relations, index)
        if obj in relations['add']:
            index += 1
    return relations
