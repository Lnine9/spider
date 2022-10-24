# coding = utf-8
"""
数据库路径反射管理
"""

# base类路径
from DataBaseOperate.data_operate.BaseTable import AnTable, SMTable, RelTable
from DataBaseOperate.tools.letter_case_name import getHumpCaseName, getLowerCaseName

db_package_path = 'DataBaseOperate.data_operate'  # 基础路径
db_an_path = db_package_path + '.announcement'  # 公告类
db_sm_path = db_package_path + '.spider_manage'  # 爬虫管理表类
db_rel_path = db_package_path + '.relation_analysis'
# 实体对象路径
entity_package_path = 'DataBaseOperate.data_operate.entity'  # 基础路径
entity_an_path = entity_package_path + '.announcement'  # 公告类
entity_sm_path = entity_package_path + '.spider_manage'  # 爬虫管理类


def default():
    return None


switch = {
    'db': db_package_path,
    'db.ann': db_an_path,
    'db.sm': db_sm_path,
    'db.rel': db_rel_path,
    'en': entity_package_path,
    'en.ann': entity_an_path,
    'en.sm': entity_sm_path,
}

db_selector = {
    'db.ann': AnTable,
    'db.sm': SMTable,
    'db.rel': RelTable,
}


def switch_path(string):
    """
    库路径选择器
    :param string:
    :return:
    """
    return switch.get(string, default)


def db_class(string):
    """
    库类选择器
    :param string:
    :return:
    """
    return db_selector.get(string)


def switch_mysql_class_path(string, module_name=None, class_name=None):
    """
    数据库表类路径
    数据表 默认module_name为小写下划线;class_name为驼峰式
    :param string:
    :param class_name:
    :return:
    """
    path = switch_path(string)
    if not path:
        return None
    if module_name is None and class_name is None:
        return path
    elif module_name is not None and class_name is None:
        return path + '.' + module_name + '.' + getHumpCaseName(module_name)
    elif module_name is None and class_name is not None:
        return path + '.' + getLowerCaseName(class_name) + '.' + class_name
    else:
        return path + '.' + module_name + '.' + class_name
