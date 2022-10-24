import importlib


def dictionary_assignment(obj: object, attr_dict: dict):
    """
    对属性进行赋值
    :param obj: 待赋值对象
    :param attr_dict: 需要赋值的字典
    :return:
    """
    for attr in attr_dict.keys():
        setattr(obj, attr, attr_dict[attr])


def object_assignment(aim_obj: object, attr_obj: object):
    """
    通过一个对象对另一个对象的属性进行赋值
    :param aim_obj: 目标对象
    :param attr_obj: 属性对象
    :return:
    """
    for attr in attr_obj.__dict__.keys():
        setattr(aim_obj, attr, getattr(attr_obj, attr))


def instantiation_by_path(classpath: str):
    """
    通过路径实例化对象
    :param classpath: 类路径
    :return:
    """
    # 将全路径类名切割获得类名及类路径
    ret, cls_name = classpath.rsplit(".", maxsplit=1)

    m = importlib.import_module(ret)
    obj = getattr(m, cls_name)()
    return obj
