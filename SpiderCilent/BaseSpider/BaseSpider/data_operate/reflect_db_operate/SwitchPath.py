# base类路径
from BaseSpider.tool.letter_case_name import getHumpCaseName, getLowerCaseName

db_package_path = 'BaseSpider.data_operate'  # 基础路径
db_an_path = db_package_path + '.announcement'  # 公告类
db_sm_path = db_package_path + '.spider_manage'  # 爬虫管理表类
# 实体对象路径
entity_package_path = 'BaseSpider.entity'  # 基础路径
entity_an_path = entity_package_path + '.announcement'  # 公告类
entity_sm_path = entity_package_path + '.spider_manage'  # 爬虫管理类


def default():
    return None


def getDBPath():
    return db_package_path


def getDBAnnPath():
    return db_an_path


def getDBSmPath():
    return db_sm_path


def getEnPath():
    return entity_package_path


def getEnAnnPath():
    return entity_an_path


def getENSmPath():
    return entity_sm_path


switch = {
    'db': getDBPath,
    'db.ann': getDBAnnPath,
    'db.sm': getDBSmPath,
    'en': getEnPath,
    'en.ann': getEnAnnPath,
    'en.sm': getENSmPath,
}


def switch_path(string):
    return switch.get(string, default)()


def switch_mysql_class_path(string, module_name=None, class_name=None):
    """
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
