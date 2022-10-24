"""
通过item创建公告实体对象，
要求item满足对应字段
"""
from BaseSpider.data_operate.reflect_db_operate.GainAnnObject import *


def default(item):
    pass


def call_bid_government(item):
    """
    政府采购
    item: {
        'CB_G':{<class CallBidGovernment>},
        'code_dict':{<class CodeHtml>},
        'at_dict':[{<class Attachment>},...],
    }
    :param item:
    :return:
    """
    lists = []
    an_table = "CB_G"
    # 采购公告数据
    cbg = getCallBidGovernment(CB_G=item['CB_G'])
    lists.append(cbg)
    # 存储html-code
    lists += list(getCodeHtml(code_dict=item['code_dict'], an_id=cbg.id, an_table=an_table))
    # 储存附件
    lists += list(getAttachment(at_dict=item['at_dict'], an_id=cbg.id, at_table="ACT", an_table=an_table))

    return {'list': lists, 'an_id': cbg.id}


# 中标公告
def win_bid_government(item):
    """
    政府中标
    item: {
        'WB_G':{<class WinBidGovernment>},
        'code_dict':{<class CodeHtml>},
        'at_dict':[{<class Attachment>},...],
        'prov_dict':[{<class ProvideUnit>},...],
        'undefined_exp':[{<class UndefinedExp>},...],
        'experts':[{<class Expert>},...],
        'call_unit':[{<class CallBidUnit>},...] / {<class CallBidUnit>},
        'agent_unit':[{<class AgentUnit>},...]
    }
    :param item:
    :return:
    """
    lists = []
    an_table = "WB_G"
    # 公告数据
    wbg = getWinBidGovernment(WB_G=item['WB_G'])
    lists.append(wbg)
    # 存储html-code
    lists += list(getCodeHtml(code_dict=item['code_dict'], an_id=wbg.id, an_table=an_table))
    # 储存附件
    lists += list(getAttachment(at_dict=item['at_dict'], an_id=wbg.id, at_table="ACT", an_table=an_table))
    #
    lists += list(getProvideUnit(prov_dict=item['prov_dict'], an_id=wbg.id))
    #
    lists += list(getUndefinedExp(un_fined_exp=item['undefined_exp'], an_id=wbg.id))
    #
    lists += list(getExpert(experts=item['experts'], an_id=wbg.id))
    #
    lists += list(getCallBidUnit(call_unit=item['call_unit'], an_table=an_table, an_id=wbg.id))
    #
    lists += list(getAgentUnit(agent_units=item['agent_unit'], an_table=an_table, an_id=wbg.id))

    return {'list': lists, 'an_id': wbg.id}


def failure_bid_government(item):
    """
    政府废弃终止
    item: {
        'FB_G':{<class FailureBidGovernment>},
        'code_dict':{<class CodeHtml>},
        'at_dict':[{<class Attachment>},...],
    }
    :param item:
    :return:
    """
    lists = []
    an_table = "FB_G"
    # 公告数据
    fbg = getFailureBidGovernment(FB_G=item['FB_G'])
    lists.append(fbg)
    # 存储html-code
    lists += list(getCodeHtml(code_dict=item['code_dict'], an_id=fbg.id, an_table=an_table))
    # 储存附件
    lists += list(getAttachment(at_dict=item['at_dict'], an_id=fbg.id, at_table="ACT", an_table=an_table))

    return {'list': lists, 'an_id': fbg.id}


def modify_bid_government(item):
    """
    政府更正
    item: {
        'MB_G':{<class ModifyBidGovernment>},
        'code_dict':{<class CodeHtml>},
        'at_dict':[{<class Attachment>},...],
    }
    :param item:
    :return:
    """
    lists = []
    an_table = "MB_G"
    # 公告数据
    mbg = getModifyBidGovernment(MB_G=item['MB_G'])
    lists.append(mbg)
    # 存储html-code
    lists += list(getCodeHtml(code_dict=item['code_dict'], an_id=mbg.id, an_table=an_table))
    # 储存附件
    lists += list(getAttachment(at_dict=item['at_dict'], an_id=mbg.id, at_table="ACT", an_table=an_table))

    return {'list': lists, 'an_id': mbg.id}


def call_bid_engineering(item):
    """
    工程招标
    item: {
        'CB_E':{<class CallBidEngineering>},
        'code_dict':{<class CodeHtml>},
        'at_dict':[{<class Attachment>},...],
    }
    :param item:
    :return:
    """
    lists = []
    an_table = "CB_E"
    # 公告数据
    cbe = getCallBidEngineering(CB_E=item['CB_E'])
    lists.append(cbe)
    # 存储html-code
    lists += list(getCodeHtml(code_dict=item['code_dict'], an_id=cbe.id, an_table=an_table))
    # 储存附件
    lists += list(getAttachment(at_dict=item['at_dict'], an_id=cbe.id, at_table="ACT", an_table=an_table))

    return {'list': lists, 'an_id': cbe.id}


def results_bid_engineering(item):
    """
    工程招标结果
    item: {
        'RB_E':{<class ResultsBidEngineering>},
        'code_dict':{<class CodeHtml>},
        'at_dict':[{<class Attachment>},...],
        'wb_supp':[{<class WbSupplier>},...],
    }
    :param item:
    :return:
    """
    lists = []
    an_table = 'RB_E'
    # 公告数据
    rbe = getResultsBidEngineering(RB_E=item[an_table])
    lists.append(rbe)
    # 中标供应商信息
    lists += list(getWbSupplier(wb_supp=item['wb_supp'], an_id=rbe.id))
    # 存储html-code
    lists += list(getCodeHtml(code_dict=item['code_dict'], an_id=rbe.id, an_table=an_table))
    # 储存附件
    lists += list(getAttachment(at_dict=item['at_dict'], an_id=rbe.id, at_table="ACT", an_table=an_table))

    return {'list': lists, 'an_id': rbe.id}


switch = {'CB_G': call_bid_government,
          'WB_G': win_bid_government,
          'FB_G': failure_bid_government,
          'MB_G': modify_bid_government,
          'CB_E': call_bid_engineering,
          'RB_E': results_bid_engineering
          }


def create_an_entity_list(item):
    """
    创建指定类型的公告实体对象
    返回一个字典：'list':是生成的实体对象列表；'an_id':记录对应公告id
    :param item:
    :return:
    """
    return switch.get(item["an_type"], default)(item)

