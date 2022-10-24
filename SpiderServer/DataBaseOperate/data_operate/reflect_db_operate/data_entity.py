# coding = utf-8
import warnings

from DataBaseOperate.data_operate.BaseTable import AnTable, SMTable
from DataBaseOperate.data_operate.reflect_db_operate.switch_path import switch_mysql_class_path
from DataBaseOperate.tools.ClassReflection import instantiation_by_path, object_assignment, dictionary_assignment


def get_entity(base_object):
    """
    获得表对象的实体对象
    :param base_object:
    :return:
    """
    warnings.warn("这个方法已经过时，数据库实体类将被抛弃", DeprecationWarning)
    if isinstance(base_object, AnTable):
        entity_path = 'en.ann'
    elif isinstance(base_object, SMTable):
        entity_path = 'en.sm'
    else:
        raise TypeError('传入参数不是指定对象：' + base_object.__class__.__name__ + " 不属于 " + SMTable.__name__)

    class_name = base_object.__class__.__name__
    # 实例化
    entity_object = instantiation_by_path(
        switch_mysql_class_path(entity_path, module_name=class_name, class_name=class_name))
    # 映射属性
    object_assignment(entity_object, base_object)
    return entity_object


def get_base_by_dict(d):
    """
    通过字典生成Base对象
    :param d:
    :return:
    """
    try:
        path = switch_mysql_class_path(d['class_type'], class_name=d['class_name'])
        # 实例化
        base_object = instantiation_by_path(path)
        dictionary_assignment(base_object, d['dict'])
        return base_object
    except:
        raise ValueError('传入信息有误')
