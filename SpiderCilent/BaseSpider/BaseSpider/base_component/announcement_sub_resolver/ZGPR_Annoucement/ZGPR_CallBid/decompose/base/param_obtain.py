from abc import ABC, abstractmethod


def set_attribute(func, **kwargs):
    """
    方法添加属性
    :param func:
    :param kwargs:
    :return:
    """
    for key in kwargs:
        setattr(func, key, kwargs[key])


def getmethod(priority: int, **kwargs):
    """
    注解多种解析方法
    :param kwargs:
    :return:
    """
    if not isinstance(priority, int):
        raise TypeError('注解优先级类型错误，应为int型')
    params = {'annotations': ['getmethod'], 'priority': priority}

    def tag(func):
        set_attribute(func, **params)
        return func

    return tag


class ParamObtain(ABC):

    @classmethod
    def get(cls):
        """
        获取字段
        :return:
        """
        gets = cls.get_getmethod_methods()
        for method in gets:
            try:
                data = method()
                if cls.check(data):
                    return data
            except:
                continue
        return None

    @classmethod
    @abstractmethod
    def check(cls, data) -> bool:
        """
        数据校验
        :param data:
        :return:
        """
        pass

    @classmethod
    def get_getmethod_methods(cls):
        """
        获得表的所有值域方法并排序
        :return:
        """

        methods = cls.get_methods()
        field_methods = [getattr(cls, method) for method in methods if
                         hasattr(getattr(cls, method), 'annotations')
                         and 'getmethod' in getattr(getattr(cls, method), 'annotations')]
        field_methods.sort(key=lambda m: getattr(m, 'priority'))

        return field_methods

    @classmethod
    def get_methods(cls):
        """
        获得类所有方法
        :return:
        """
        return list(
            filter(lambda m: not m.startswith("__") and not m.endswith("__") and callable(getattr(cls, m)), dir(cls)))
