# coding = utf-8
"""
数据库路径反射管理
"""

# base类路径
from RelationAnalysis.data_operate.pool_table import AnTable, SMTable, RelTable
from RelationAnalysis.tool.letter_case_name import hump_case_name, lower_case_name

db_package_path = 'RelationAnalysis.data_operate'  # 基础路径
db_an_path = db_package_path + '.announcement'  # 公告类
db_sm_path = db_package_path + '.spider_manage'  # 爬虫管理表类
db_rel_path = db_package_path + '.relation_analysis'


def default():
    return None


switch = {
    'db': db_package_path,
    'db.ann': db_an_path,
    'db.sm': db_sm_path,
    'db.rel': db_rel_path,
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
        return path + '.' + module_name + '.' + hump_case_name(module_name)
    elif module_name is None and class_name is not None:
        return path + '.' + lower_case_name(class_name) + '.' + class_name
    else:
        return path + '.' + module_name + '.' + class_name
