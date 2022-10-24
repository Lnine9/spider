from BaseSpider.data_operate.BaseTable import SMTable
from BaseSpider.data_operate.reflect_db_operate.DataEntry import get_base_by_dict
from BaseSpider.data_operate.reflect_db_operate.SwitchPath import switch_mysql_class_path
from BaseSpider.tool.ClassReflection import instantiation_by_path, object_assignment


def addDictsToSm(dicts: list):
    obj_list = []
    for d in dicts:
        obj = getSmObjByDict(d)
        if obj:
            obj_list.append(obj)
    SMTable.add_all(obj_list)


def addDictToSm(d: dict):
    obj = getSmObjByDict(d)
    obj.add_self()


def getSmObjByDict(d: dict):
    type = d['class_type']
    if 'db.sm' in type:
        return get_base_by_dict(d)
    else:
        return None


def get_sm_base(entity_object):
    """
   获得爬虫管理表对象
   :param entity_object:
   :return:
   """
    class_name = entity_object.__class__.__name__
    # 实例化
    base_object = instantiation_by_path(switch_mysql_class_path('db.sm', class_name=class_name))
    # 映射属性
    object_assignment(base_object, entity_object)
    return base_object


def UUID_SHORT():
    return "40"+str(SMTable.UUID_SHORT())[-16:]
