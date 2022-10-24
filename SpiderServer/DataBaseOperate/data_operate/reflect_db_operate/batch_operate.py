from DataBaseOperate.data_operate.reflect_db_operate.DataEntry import get_base_by_dict
from DataBaseOperate.data_operate.reflect_db_operate.switch_path import db_class, switch_mysql_class_path
from DataBaseOperate.tools.ClassReflection import instantiation_by_path


def default(*args, **kwargs):
    raise ValueError('无效操作类型: %s,%s' % (args, kwargs))


def update(session, obj):
    session.merge(obj)


def delete(session, obj):
    value = obj.__dict__
    value.pop('db_server_operate__')
    value.pop('_sa_instance_state')
    session.query(obj.__class__).filter_by(**value).delete()


operate_selector = {
    "add": lambda session, obj: session.add(obj),
    "delete": delete,
    "update": lambda session, obj: session.merge(obj)
}


def get_objs(items):
    """
    根据数据库对所有操作对象进行分类
    :param items:
    :return:
    """
    objs = {}
    for d in items:
        obj = get_base_by_dict(d)
        setattr(obj, 'db_server_operate__', d['operate'])
        if objs.get(d['class_type'], None):
            objs[d['class_type']].append(obj)
        else:
            objs[d['class_type']] = [obj, ]
    return objs


def deal_operate(items):
    """
    增删改操作:
        单个事务
    :param items: eg. [{'class_type': 'db.ann', 'class_name': 'WinBidGovernment', 'operate': 'update',
                         'dict': {'id': '98773531428430445', 'relation_analysis_version': '100101'}}, ]
    :return:
    """
    if isinstance(items, dict):
        items = [items]
    objs = get_objs(items)
    for item in objs.items():
        key, value = item[0], item[1]
        clazz = db_class(key)
        session = clazz.getSession()
        try:
            for obj in value:
                operate_selector.get(getattr(obj, 'db_server_operate__'), default)(session, obj)
        except Exception as e:
            session.rollback()
            print(e)
            raise
        finally:
            session.commit()
            session.close()


def execute_sql(database, sql):
    """
    执行sql语句
    :param database: 数据库
    :param sql: sql
    :return:
    """
    return db_class(database).execute(sql)


def query_operate(class_info, query_info):
    """
    查询操作：
        单条查询
    :param class_info:  <class dict> {'class_type': None,'class_name': None}
    :param query_info: <class dict> {'query_start': 0, 'query_end': None, 'query_numbe': None, 'query_fields': None,
              'query_condition': None, 'condition_rel': "and"} 详见BaseTable.query()
    :return: list
    """
    path = switch_mysql_class_path(class_info['class_type'], class_name=class_info['class_name'])
    base_object = instantiation_by_path(path)
    return base_object.query(**query_info)
