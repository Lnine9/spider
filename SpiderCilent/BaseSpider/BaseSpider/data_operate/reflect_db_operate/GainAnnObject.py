"""
通过指定的类名反射entity.announcement下的类，生成相应的对象，
并通过传入的属性字典对属性赋值
"""

from BaseSpider.data_operate import get_uuid_short
from BaseSpider.data_operate.announcement import provide_unit, expert, call_bid_unit, agent_unit
from BaseSpider.data_operate.reflect_db_operate import BatchOperaAnn
from BaseSpider.data_operate.reflect_db_operate.SwitchPath import switch_mysql_class_path
from BaseSpider.tool.ClassReflection import instantiation_by_path, dictionary_assignment


def getAgentUnit(agent_units, an_id, an_table):
    # code数据去重
    snd = []
    for index, d in enumerate(agent_units[:-1]):
        flag = True
        for m in agent_units[index + 1:]:
            if d['code'] == m['code']:
                flag = False
                break
        if flag:
            snd.append(d)
    if agent_units:
        snd.append(agent_units[-1])

    for au in snd:
        ag_l = agent_unit.AgentUnit.query_all(code=au['code'])
        if not ag_l:
            agentUnit = reflecte_to_object('AgentUnit', au)
            agentUnit.id = randomId()
            yield getAnAgentRel(an_id, agentUnit.id, an_table)
            yield agentUnit
        else:
            ag_id = ag_l[0].id
            yield getAnAgentRel(an_id, ag_id, an_table)


def getAnAgentRel(an_id, ag_id, an_table):
    item = reflecte_to_object('AnAgentRel', {'id': randomId(), 'an_table': an_table, 'an_id': an_id, 'ag_id': ag_id})
    return item


# 附件关系表
# an_table：公告表
# an_id: 公告id
# at_id: 附件id
# at_table: 附件表
def getAnAtRel(an_table, an_id, at_id, at_table):
    item = reflecte_to_object('AnAtRel', {'id': randomId(), 'an_table': an_table, 'an_id': an_id, 'at_id': at_id,
                                          'at_table': at_table})
    return item


def getAnCallunitRel(an_id, an_table, callunit_id):
    item = reflecte_to_object('AnCallunitRel',
                              {'id': randomId(), 'an_table': an_table, 'an_id': an_id, 'callunit_id': callunit_id})
    return item


# 源文件关联
# an_id: 公告id
# code_id: 文件id
# an_table: 公告表（类型）
def getAnCodeRel(an_id, code_id, an_table):
    item = reflecte_to_object('AnCodeRel',
                              {'id': randomId(), 'an_table': an_table, 'an_id': an_id, 'code_id': code_id})
    return item


#
def getAnExpertRel(an_id, expert_id):
    item = reflecte_to_object('AnExpertRel', {'id': randomId(), 'expert_id': expert_id, 'an_id': an_id})
    return item


# 供应商关联表
def getAnProvRel(an_id, prov_id):
    item = reflecte_to_object('AnProvRel', {'id': randomId(), 'prov_id': prov_id, 'an_id': an_id})
    return item


# 附件获取 isOk
# 通过判断attachments长度运行并调用关系表
# at_dict: 附件信息
# an_id: 附件id
# at_table: 附件表
# an_table: 公告表
def getAttachment(at_dict, an_id, at_table, an_table):
    for att in at_dict:
        attachment = reflecte_to_object('Attachment', att)
        attachment.id = randomId()
        yield getAnAtRel(an_id=an_id, at_id=attachment.id, at_table=at_table, an_table=an_table)
        yield attachment


# 工程招标
def getCallBidEngineering(CB_E):
    item = reflecte_to_object('CallBidEngineering', CB_E)
    item.id = randomId()
    return item


# 政府采购
# CB_G: 政府采购信息
def getCallBidGovernment(CB_G):
    item = reflecte_to_object('CallBidGovernment', CB_G)
    item.id = randomId()
    return item


# 采购机构
# if callunit_code is not None and callunit_code !=""
# 调用关联表
def getCallBidUnit(call_unit, an_id, an_table):
    if not isinstance(call_unit, list):
        call_unit = [call_unit]

    snd = []
    for index, d in enumerate(call_unit[:-1]):
        flag = True
        for m in call_unit[index + 1:]:
            if d['code'] == m['code']:
                flag = False
                break
        if flag:
            snd.append(d)
    if call_unit:
        snd.append(call_unit[-1])

    for cu in snd:
        c_l = call_bid_unit.CallBidUnit.query_all(code=cu['code'])
        if not c_l:
            item = reflecte_to_object('CallBidUnit', cu)
            item.id = randomId()
            yield getAnCallunitRel(an_id=an_id, an_table=an_table, callunit_id=item.id)
            yield item
        else:
            c_id = c_l[0].id
            yield getAnCallunitRel(an_id=an_id, an_table=an_table, callunit_id=c_id)


# 源代码文件
# 调用文件关联表
# code_dict: 源文件信息
# an_id: 公告id
# an_table: 公告表（类型）
def getCodeHtml(code_dict, an_id, an_table):
    item = reflecte_to_object('CodeHtml', code_dict)
    item.id = randomId()
    yield getAnCodeRel(an_id=an_id, code_id=item.id, an_table=an_table)
    yield item


# 唯一标识专家表
# yield getAnExpertRel(an_id, item.id)
def getExpert(experts, an_id):
    snd = []
    for index, d in enumerate(experts[:-1]):
        flag = True
        for m in experts[index + 1:]:
            if d['code'] == m['code']:
                flag = False
                break
        if flag:
            snd.append(d)
    if experts:
        snd.append(experts[-1])

    for e in snd:
        e_l = expert.Expert.query_all(code=e['code'])
        if not e_l:
            item = reflecte_to_object('Expert', e)
            item.id = randomId()
            yield getAnExpertRel(an_id, item.id)
            yield item
        else:
            e_id = e_l[0].id
            yield getAnExpertRel(an_id, e_id)


# 政府流标
def getFailureBidGovernment(FB_G):
    item = reflecte_to_object('FailureBidGovernment', FB_G)
    item.id = randomId()
    return item


def getFileList(file_list, an_id, an_table, at_table):
    for fl in file_list:
        item = reflecte_to_object('FileList', fl)
        item.id = randomId()
        yield getAnAtRel(an_id=an_id, at_id=item.id, at_table=at_table, an_table=an_table)
        yield item


# 更正公告
def getModifyBidGovernment(MB_G):
    item = reflecte_to_object('ModifyBidGovernment', MB_G)
    item.id = randomId()
    return item


# 供应商
# if data_dict["provide_unit_code"] is not None and data_dict["provide_unit_code"] != "":
# an_prov_rel
def getProvideUnit(prov_dict, an_id):
    # code数据去重
    snd = []
    for index, d in enumerate(prov_dict[:-1]):
        flag = True
        for m in prov_dict[index + 1:]:
            if d['code'] == m['code']:
                flag = False
                break
        if flag:
            snd.append(d)
    if prov_dict:
        snd.append(prov_dict[-1])
    # 生成对象
    for i in snd:
        prov_l = provide_unit.ProvideUnit.query_all(code=i["code"])
        if not prov_l:
            item = reflecte_to_object('ProvideUnit', i)
            item.id = randomId()
            yield getAnProvRel(an_id=an_id, prov_id=item.id)
            yield item
        else:
            prov_id = prov_l[0].id
            yield getAnProvRel(an_id=an_id, prov_id=prov_id)


# 未验证专家
def getUndefinedExp(un_fined_exp, an_id):
    for undefinedExp in un_fined_exp:
        if isinstance(undefinedExp, dict):
            item = reflecte_to_object('UndefinedExp', undefinedExp)
        elif isinstance(undefinedExp, str):
            item = instantiation_by_path(
                switch_mysql_class_path('en.ann', module_name='UndefinedExp', class_name='UndefinedExp'))
            item.name = undefinedExp
        else:
            raise TypeError('无法识别类型')
        item.id = randomId()
        item.sub_an_id = an_id
        yield item


# 工程结果公告信息
def getResultsBidEngineering(RB_E):
    item = reflecte_to_object('ResultsBidEngineering', RB_E)
    item.id = randomId()
    return item


# 工程中标供应商
def getWbSupplier(wb_supp, an_id):
    for supp in wb_supp:
        item = reflecte_to_object('WbSupplier', supp)
        item.id = randomId()
        yield item
        yield getAnSuppRel(an_id, item.id)


# 工程结果公告与中标供应商关系表
def getAnSuppRel(an_id, supp_id):
    item = reflecte_to_object('AnSuppRel', {'id': randomId(), 'supp_id': supp_id, 'an_id': an_id})
    return item


# 中标
# WB_G中标信息
def getWinBidGovernment(WB_G):
    item = reflecte_to_object('WinBidGovernment', WB_G)
    item.id = randomId()
    return item


# uuid_short
def randomId():
    return BatchOperaAnn.UUID_SHORT()


# 生成带attribute属性的指定对象
# class_attribute：属性字典
def reflecte_to_object(class_name, class_attribute):
    reflection_object = instantiation_by_path(
        switch_mysql_class_path('en.ann', module_name=class_name, class_name=class_name))
    dictionary_assignment(reflection_object, class_attribute)
    return reflection_object
