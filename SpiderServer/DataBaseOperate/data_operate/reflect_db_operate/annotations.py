# coding = utf-8
def set_attribute(func, **kwargs):
    """
    方法添加属性
    :param func:
    :param kwargs:
    :return:
    """
    for key in kwargs:
        setattr(func, key, kwargs[key])


def base_info(class_name=None, param_name=None, class_type='db.ann', operate='add', enable=True, **kwargs):
    params = {'class_name': class_name, 'class_type': class_type, 'operate': operate, 'enable': enable,
              'param_name': param_name, 'name': 'base_info'}

    def tag(func):
        set_attribute(func, **params)
        return func

    return tag


def rel_info(class_name=None, param_name=None, class_type='db.ann', operate='add', enable=True, **kwargs):
    if param_name is None:
        param_name = ['', '']
    params = {'class_name': class_name, 'class_type': class_type, 'operate': operate, 'enable': enable,
              'param_name': param_name, 'name': 'rel_info'}

    def tag(func):
        set_attribute(func, **params)
        return func

    return tag
