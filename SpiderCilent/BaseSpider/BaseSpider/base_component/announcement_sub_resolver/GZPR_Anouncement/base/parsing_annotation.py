def set_attribute(func, **kwargs):
    """
    方法添加属性
    :param func:
    :param kwargs:
    :return:
    """
    for key in kwargs:
        setattr(func, key, kwargs[key])


def field_tag(resolution_version, fields, subordination_table, fields_order, block_number, **kwargs):
    """
    注解标注方法获取字段信息，方法版本号
    @method
    :param resolution_version: 版本号，字符串
    :param fields: 标记字段，数据库字段列表
    :param subordination_table: 从属表
    :param fields_order: 版号序列
    :param block_number: 块号 #用于分块需求
    :param kwargs: 其他参数
    :return:
    """
    params = {'resolution_version': resolution_version, 'fields': fields, 'subordination_table': subordination_table,
              'fields_order': fields_order,'block_number':block_number}

    def tag(func):
        set_attribute(func, **params)
        return func

    return tag


def table_tag(table, table_order, **kwargs):
    """
    注解表类型，序列
    :param table:表名
    :param table_order: 版号序列
    :param kwargs:
    :return:
    """
    params = {'table': table, 'table_order': table_order}

    def tag(func):
        set_attribute(func, **params)
        return func

    return tag
