# coding = utf-8
from DataBaseOperate.server import batch_operate
from DataBaseOperate.data_operate.reflect_db_operate.annotations import base_info, rel_info


class AnnouncementDecomposition:
    """
    公告分解基类
    """

    @classmethod
    def check_ann(cls, item) -> bool:
        """
        数据预处理
        :param item:
        :return:
        """
        return True

    @classmethod
    def method_pretreatment(cls, item):
        for key, value in item.items():
            if not value:
                item[key] = None

    @classmethod
    def query_exist(cls, class_type, class_name, **kwargs):
        kwargs['query_number'] = 1
        find = batch_operate.query_operate({'class_type': class_type, 'class_name': class_name}, kwargs)
        if find:
            return find[0]


class AG_L(AnnouncementDecomposition):
    @classmethod
    @base_info(class_name='AgencyInformation', param_name='AG_L', class_type='db.rel')
    def ann_info(cls, item):
        """
        公告信息
        :param item:
        :return:
        """
        cls.method_pretreatment(item)
        find = cls.query_exist(class_name='AgencyInformation', class_type='db.rel', OrgName=item['OrgName'])
        if find is None:
            return item
        return {'id': find.id, 'exist': True}


class CB_G(AnnouncementDecomposition):
    @classmethod
    @base_info(class_name='CallBidGovernment', param_name='CB_G', class_type='db.ann')
    def ann_info(cls, item):
        """
        公告信息
        :param item:
        :return:
        """
        cls.method_pretreatment(item)
        find = cls.query_exist(class_name='CallBidGovernment', class_type='db.ann', sourse_url=item['sourse_url'], proj_code=item['proj_code'])
        if find is None:
            return item
        return {'id': find.id, 'exist': True}

    @classmethod
    @base_info(class_name='Attachment', param_name='at_dict', class_type='db.ann')
    def at_dict(cls, item):
        """
        附件信息入库
        :param item:
        :return:
        """
        return item

    @classmethod
    @rel_info(class_name='AnAtRel', param_name=['CB_G', 'at_dict'], class_type='db.ann')
    def an_at_rel(cls, id1, id2):
        """
        附件信息入库
        :param item:
        :return:
        """
        return [{'an_table': 'CB_G', 'an_id': id1, 'at_id': id, 'at_table': 'attachment'} for id in id2]

    @classmethod
    @base_info(class_name='CallBidUnit', param_name='call_unit', class_type='db.ann')
    def call_bid_unit(cls, item):
        if isinstance(item, dict):
            item = [item]
        back = []
        for one in item:
            if one:
                cls.method_pretreatment(one)
                find = cls.query_exist(class_name='CallBidUnit', class_type='db.ann', name=one['name'])
                if find is None:
                    back.append(one)
                else:
                    back.append({'id': find.id, 'exist': True})
        return back

    @classmethod
    @rel_info(class_name='AnCallunitRel', param_name=['CB_G', 'call_unit'], class_type='db.ann')
    def an_callunit_rel(cls, CB_G, call_unit):
        return [{'callunit_id': id, 'an_id': CB_G, 'an_table': 'CB_G'} for id in call_unit]


class WB_G(AnnouncementDecomposition):
    @classmethod
    @base_info(class_name='WinBidGovernment', param_name='WB_G', class_type='db.ann')
    def ann_info(cls, item):
        """
        公告信息
        :param item:
        :return:
        """
        cls.method_pretreatment(item)
        find = cls.query_exist(class_name='WinBidGovernment', class_type='db.ann', sourse_url=item['sourse_url'])
        if find is None:
            return item
        return {'id': find.id, 'exist': True}

    @classmethod
    @base_info(class_name='Attachment', param_name='at_dict', class_type='db.ann')
    def at_dict(cls, item):
        """
        附件信息入库
        :param item:
        :return:
        """
        return item

    @classmethod
    @rel_info(class_name='AnAtRel', param_name=['WB_G', 'at_dict'], class_type='db.ann')
    def an_at_rel(cls, WB_G, at_dict):
        """
        附件信息入库
        :param item:
        :return:
        """
        return [{'an_table': 'CB_G', 'an_id': WB_G, 'at_id': id, 'at_table': 'attachment'} for id in at_dict]

    @classmethod
    @base_info(class_name='ProvideUnit', param_name='prov_dict', class_type='db.ann')
    def provide_unit(cls, item):
        if isinstance(item, dict):
            item = [item]
        back = []
        for one in item:
            if one:
                cls.method_pretreatment(one)
                find = cls.query_exist(class_name='ProvideUnit', class_type='db.ann', name=one['name'])
                if find is None:
                    back.append(one)
                else:
                    back.append({'id': find.id, 'exist': True})

        return back

    @classmethod
    @rel_info(class_name='AnProvRel', param_name=['WB_G', 'prov_dict'], class_type='db.ann')
    def an_prov_rel(cls, WB_G, prov_dict):
        return [{'prov_id': id, 'an_id': WB_G} for id in prov_dict]

    @classmethod
    @base_info(class_name='UndefinedExp', param_name='undefined_exp', class_type='db.ann')
    def undefined_exp(cls, item):
        return item

    @classmethod
    @base_info(class_name='CallBidUnit', param_name='call_unit', class_type='db.ann')
    def call_bid_unit(cls, item):
        if isinstance(item, dict):
            item = [item]
        back = []
        for one in item:
            if one:
                cls.method_pretreatment(one)
                find = cls.query_exist(class_name='CallBidUnit', class_type='db.ann', name=one['name'])
                if find is None:
                    back.append(one)
                else:
                    back.append({'id': find.id, 'exist': True})
        return back

    @classmethod
    @rel_info(class_name='AnCallunitRel', param_name=['WB_G', 'call_unit'], class_type='db.ann')
    def an_callunit_rel(cls, WB_G, call_unit):
        return [{'callunit_id': id, 'an_id': WB_G, 'an_table': 'WB_G'} for id in call_unit]

    @classmethod
    @base_info(class_name='AgentUnit', param_name='agent_unit', class_type='db.ann')
    def agent_unit(cls, item):
        if isinstance(item, dict):
            item = [item]
        back = []
        for one in item:
            if one:
                cls.method_pretreatment(one)
                find = cls.query_exist(class_name='AgentUnit', class_type='db.ann', name=one['name'])
                if find is None:
                    back.append(one)
                else:
                    back.append({'id': find.id, 'exist': True})
        return back

    @classmethod
    @rel_info(class_name='AnAgentRel', param_name=['WB_G', 'agent_unit'], class_type='db.ann')
    def an_agent_rel(cls, WB_G, agent_unit):
        return [{'ag_id': id, 'an_id': WB_G, 'an_table': 'WB_G'} for id in agent_unit]


class FB_G(AnnouncementDecomposition):
    @classmethod
    @base_info(class_name='FailureBidGovernment', param_name='FB_G', class_type='db.ann')
    def ann_info(cls, item):
        """
        公告信息
        :param item:
        :return:
        """
        cls.method_pretreatment(item)
        find = cls.query_exist(class_name='FailureBidGovernment', class_type='db.ann', sourse_url=item['sourse_url'])
        if find is None:
            return item
        return {'id': find.id, 'exist': True}

    @classmethod
    @base_info(class_name='Attachment', param_name='at_dict', class_type='db.ann')
    def at_dict(cls, item):
        """
        附件信息入库
        :param item:
        :return:
        """
        return item

    @classmethod
    @rel_info(class_name='AnAtRel', param_name=['FB_G', 'at_dict'], class_type='db.ann')
    def an_at_rel(cls, id1, id2):
        """
        附件信息入库
        :param item:
        :return:
        """
        return [{'an_table': 'CB_G', 'an_id': id1, 'at_id': id, 'at_table': 'attachment'} for id in id2]


class MB_G(AnnouncementDecomposition):
    @classmethod
    @base_info(class_name='ModifyBidGovernment', param_name='MB_G', class_type='db.ann')
    def ann_info(cls, item):
        """
        公告信息
        :param item:
        :return:
        """
        cls.method_pretreatment(item)
        find = cls.query_exist(class_name='ModifyBidGovernment', class_type='db.ann', sourse_url=item['sourse_url'])
        if find is None:
            return item
        return {'id': find.id, 'exist': True}

    @classmethod
    @base_info(class_name='Attachment', param_name='at_dict', class_type='db.ann')
    def at_dict(cls, item):
        """
        附件信息入库
        :param item:
        :return:
        """
        return item

    @classmethod
    @rel_info(class_name='AnAtRel', param_name=['MB_G', 'at_dict'], class_type='db.ann')
    def an_at_rel(cls, id1, id2):
        """
        附件信息入库
        :param item:
        :return:
        """
        return [{'an_table': 'CB_G', 'an_id': id1, 'at_id': id, 'at_table': 'attachment'} for id in id2]


class CB_E(AnnouncementDecomposition):
    @classmethod
    @base_info(class_name='CallBidEngineering', param_name='CB_E', class_type='db.ann')
    def ann_info(cls, item):
        """
        公告信息
        :param item:
        :return:
        """
        cls.method_pretreatment(item)
        find = cls.query_exist(class_name='CallBidEngineering', class_type='db.ann', sourse_url=item['sourse_url'])
        if find is None:
            return item
        return {'id': find.id, 'exist': True}

    @classmethod
    @base_info(class_name='Attachment', param_name='at_dict', class_type='db.ann')
    def at_dict(cls, item):
        """
        附件信息入库
        :param item:
        :return:
        """
        return item

    @classmethod
    @rel_info(class_name='AnAtRel', param_name=['CB_E', 'at_dict'], class_type='db.ann')
    def an_at_rel(cls, id1, id2):
        """
        附件信息入库
        :param item:
        :return:
        """
        return [{'an_table': 'CB_G', 'an_id': id1, 'at_id': id, 'at_table': 'attachment'} for id in id2]

    @classmethod
    @base_info(class_name='CallBidUnit', param_name='call_unit', class_type='db.ann')
    def call_bid_unit(cls, item):
        if isinstance(item, dict):
            item = [item]
        back = []
        for one in item:
            if one:
                cls.method_pretreatment(one)
                find = cls.query_exist(class_name='CallBidUnit', class_type='db.ann', name=one['name'])
                if find is None:
                    back.append(one)
                else:
                    back.append({'id': find.id, 'exist': True})
        return back

    @classmethod
    @rel_info(class_name='AnCallunitRel', param_name=['CB_E', 'call_unit'], class_type='db.ann')
    def an_callunit_rel(cls, CB_E, call_unit):
        return [{'callunit_id': id, 'an_id': CB_E, 'an_table': 'CB_E'} for id in call_unit]


class RB_E(AnnouncementDecomposition):

    @classmethod
    @base_info(class_name='ResultsBidEngineering', param_name='RB_E', class_type='db.ann')
    def ann_info(cls, item):
        """
        公告信息
        :param item:
        :return:
        """
        cls.method_pretreatment(item)
        find = cls.query_exist(class_name='ResultsBidEngineering', class_type='db.ann', sourse_url=item['sourse_url'])
        if find is None:
            return item
        return {'id': find.id, 'exist': True}

    @classmethod
    @base_info(class_name='WbSupplier', param_name='wb_supp', class_type='db.ann')
    def wb_supplier(cls, item):
        """
        附件信息入库
        todo 去重处理
        :param item:
        :return:
        """
        return item

    @classmethod
    @rel_info(class_name='AnSuppRel', param_name=['RB_E', 'wb_supp'], class_type='db.ann')
    def an_supp_rel(cls, RB_E, wb_supp):
        """
        附件信息入库
        :param item:
        :return:
        """
        return [{'an_id': RB_E, 'supp_id': id} for id in wb_supp]

    @classmethod
    @base_info(class_name='Attachment', param_name='at_dict', class_type='db.ann')
    def at_dict(cls, item):
        """
        附件信息入库
        :param item:
        :return:
        """
        return item

    @classmethod
    @rel_info(class_name='AnAtRel', param_name=['RB_E', 'at_dict'], class_type='db.ann')
    def an_at_rel(cls, id1, id2):
        """
        附件信息入库
        :param item:
        :return:
        """
        return [{'an_table': 'CB_G', 'an_id': id1, 'at_id': id, 'at_table': 'attachment'} for id in id2]

    @classmethod
    @base_info(class_name='CallBidUnit', param_name='call_unit', class_type='db.ann')
    def call_bid_unit(cls, item):
        if isinstance(item, dict):
            item = [item]
        back = []
        for one in item:
            if one:
                cls.method_pretreatment(one)
                find = cls.query_exist(class_name='CallBidUnit', class_type='db.ann', name=one['name'])
                if find is None:
                    back.append(one)
                else:
                    back.append({'id': find.id, 'exist': True})
        return back

    @classmethod
    @rel_info(class_name='AnCallunitRel', param_name=['RB_E', 'call_unit'], class_type='db.ann')
    def an_callunit_rel(cls, RB_E, call_unit):
        return [{'callunit_id': id, 'an_id': RB_E, 'an_table': 'RB_E'} for id in call_unit]


class DL(AnnouncementDecomposition):
    @classmethod
    @base_info(class_name='DishonestList', param_name='DL', class_type='db.ann')
    def ann_info(cls, item):
        """
        公告信息
        :param item:
        :return:
        """
        return item


class I_G(AnnouncementDecomposition):
    @classmethod
    @base_info(class_name='IntentionMain', param_name='I_G', class_type='db.ann')
    def ann_info(cls, item):
        """
        公告信息
        :param item:
        :return:
        """
        cls.method_pretreatment(item)
        find = cls.query_exist(class_name='IntentionMain', class_type='db.ann', source_url=item['source_url'])
        if find is None:
            return item
        return {'id': find.id, 'exist': True}

    @classmethod
    @base_info(class_name='IntentionDetail', param_name='details', class_type='db.ann')
    def at_dict(cls, item):
        """
        附件信息入库
        :param item:
        :return:
        """
        return item

    @classmethod
    @rel_info(class_name='IntentionRel', param_name=['I_G', 'details'], class_type='db.ann')
    def an_at_rel(cls, id1, id2):
        """
        附件信息入库
        :param item:
        :return:
        """
        return [{'main_id': id1, 'detail_id': id} for id in id2]

class F_M(AnnouncementDecomposition):
    @classmethod
    @base_info(class_name='FarmMarket', param_name='F_M', class_type='db.ann')
    def ann_info(cls, item):
        """
        公告信息
        :param item:
        :return:
        """
        res = []
        for i in item:
            find = cls.query_exist(class_name='FarmMarket', class_type='db.ann', market=i['market'], time=i['time'], variety=i['variety'])
            if find is None:
                res.append(i)
            else:
                res.append({'id': find.id, 'exist': True})
        return res
