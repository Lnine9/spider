from BaseSpider.data_operate.BaseTable import AnTable
from BaseSpider.data_operate.reflect_db_operate.DataEntry import get_base_by_dict
from BaseSpider.data_operate.reflect_db_operate.SwitchPath import switch_mysql_class_path
from BaseSpider.tool.ClassReflection import instantiation_by_path, object_assignment


def addEntitys(items: list):
    """
    将实体对象转化为表对象
    批量添加到数据库
    :param items:实体对象列表
    :return:
    """
    dbo_list = []
    for item in items:
        dbo = get_an_base(item)
        dbo_list.append(dbo)
    AnTable.add_all(dbo_list)


def addDictsToAn(dicts: list):
    """
    尝试对一个列表中的字典进行批量入库
    当其中一个发生异常时，所有数据回滚
    :param dicts:
    :return:
    """
    obj_list = []
    for d in dicts:
        obj = getAnObjByDict(d)
        if obj:
            obj_list.append(obj)
    AnTable.add_all(obj_list)


def addDictToAn(d: dict):
    """
    将字典对象进行入库
    :param d:
    :return:
    """
    obj = getAnObjByDict(d)
    obj.add_self()


def getAnObjByDict(d: dict):
    """
    将字典转换为相应的类的对象
    :param d:
    :return:
    """
    type = d['class_type']
    if 'db.ann' in type:
        return get_base_by_dict(d)
    else:
        return None


def get_an_base(entity_object):
    """
    获得公告表对象
    :param entity_object:
    :return:
    """
    class_name = entity_object.__class__.__name__
    # 实例化
    base_object = instantiation_by_path(switch_mysql_class_path('db.ann', class_name=class_name))
    # 映射属性
    object_assignment(base_object, entity_object)
    return base_object


def UUID_SHORT():
    """
    获得公告表uuid_short
    减少AnTable的直接导入
    :return:
    """
    return "40"+str(AnTable.UUID_SHORT())[-16:]
