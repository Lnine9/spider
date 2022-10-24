import re

from BaseSpider.base_component.SubResolver import SubResolver


class ParserArchitecture(SubResolver):
    def __init__(self):
        self.check_order()
        table_methods = self.get_table_methods()
        self.table_order = [method.__name__ for method in table_methods]
        self.version = self.get_all_version()

    def resolver_page(self) -> dict:
        return self.update_version(version='0')

    def get_block(self, block):
        """
        获得值域方法、块解析方法
        :param block:
        :return:
        """
        field_methods = self.get_block_methods(block)
        dicts = {}
        lists = []
        for method in field_methods:
            back = getattr(self, method.__name__)()
            if isinstance(back, dict):
                dicts = {**dicts, **back}
            elif isinstance(back, list):
                lists += back
        return {'dict': dicts, 'list': lists}

    def update_version(self, version='0'):
        """
        获得返回字典
        :param version:
        :return:
        """
        update_dict = {}
        now_versions = re.split(r':', str(version))
        new_versions = re.split(r':', self.version)

        for i in range(len(new_versions)):
            # 判断表版本号是否相等
            if not (len(now_versions) > i and now_versions[i] == new_versions[i]):
                table_dict = {}
                table_dicts = []
                # 获得表方法
                table_method = getattr(self, self.table_order[i])
                # 获得表名
                table_name = getattr(table_method, 'table')
                # 获得值域方法、表解析方法
                field_methods = self.get_field_methods(table_name)

                # 列表化值域版本号
                if len(now_versions) > i:
                    now_field_versions = re.split(r'\.', now_versions[i])
                else:
                    now_field_versions = '0'
                new_field_versions = re.split(r'\.', new_versions[i])
                for j in range(len(new_field_versions)):
                    # 判断当前值域是否需要更新，版本号是否相等
                    if not (len(now_field_versions) > j and now_field_versions[j] == new_field_versions[j]):
                        back_dict = getattr(self, field_methods[j].__name__)()
                        if isinstance(back_dict, dict):  # 字典合并
                            table_dict = {**table_dict, **back_dict}
                        elif isinstance(back_dict, list):  # 列表合并
                            table_dicts += back_dict
                        else:
                            pass
                            # raise ValueError(field_methods[j].__name__ + '返回值错误')
                update_dict[table_name] = table_dicts if table_dicts else table_dict

        return update_dict  # 返回更新字典

    def update_data(self, data):
        if not data:
            return {}
        update_dict = {}
        for key in data:
            methods = self.get_field_method(table_name=key, fields=data[key])

            table_dict = {}
            table_dicts = []
            for method in methods:
                back_dict = getattr(self, method.__name__)()
                if isinstance(back_dict, dict):  # 字典合并
                    table_dict = {**table_dict, **back_dict}
                elif isinstance(back_dict, list):  # 列表合并
                    table_dicts += back_dict
                else:
                    pass
                    # raise ValueError(field_methods[j].__name__ + '返回值错误')
            update_dict[key] = table_dicts if table_dicts else table_dict

        return update_dict

    @classmethod
    def get_all_version(cls):
        """
        获得所有版本号
        :return:
        """
        table_methods = cls.get_table_methods()
        table_versions = [cls.get_table_version(getattr(method, 'table')) for method in table_methods]
        return ':'.join(table_versions)

    @classmethod
    def get_table_version(cls, table_name):
        """
        获得表版本号
        :param table_name:
        :return:
        """
        table_fields = cls.get_field_methods(table_name)
        field_versions = [str(getattr(method, 'resolution_version')) for method in table_fields]
        return '.'.join(field_versions)

    @classmethod
    def get_block_methods(cls, block):
        """
        获得块方法
        方法无序，相同块返回数据一致
        字典随机合并
        :param block:
        :return:
        """
        methods = cls.get_methods()
        field_methods = [getattr(cls, method) for method in methods
                         if hasattr(getattr(cls, method), 'block_number')
                         and getattr(getattr(cls, method), 'block_number') == block]

        return field_methods

    @classmethod
    def get_table_methods(cls):
        """
        获得所有表方法
        :return:
        """
        methods = cls.get_methods()
        table_methods = [getattr(cls, method) for method in methods if hasattr(getattr(cls, method), 'table')]
        table_methods.sort(key=lambda m: getattr(m, 'table_order'))

        return table_methods

    @classmethod
    def get_field_methods(cls, table_name):
        """
        获得表的所有值域方法并排序
        :param table_name:
        :return:
        """

        methods = cls.get_methods()
        field_methods = [getattr(cls, method) for method in methods if
                         hasattr(getattr(cls, method), 'subordination_table') and getattr(getattr(cls, method),
                                                                                          'subordination_table') == table_name]
        field_methods.sort(key=lambda m: getattr(m, 'fields_order'))

        return field_methods

    @classmethod
    def get_methods(cls):
        """
        获得类所有方法
        :return:
        """
        return list(
            filter(lambda m: not m.startswith("__") and not m.endswith("__") and callable(getattr(cls, m)), dir(cls)))

    @classmethod
    def check_order(cls):
        """
        检查序列是否重复
        :return:
        """
        table_methods = cls.get_table_methods()
        for i in range(len(table_methods) - 1):
            if getattr(table_methods[i], 'table_order') == getattr(table_methods[i + 1], 'table_order'):
                raise ValueError(
                    'table_order 重复：' + getattr(table_methods[i], 'table') + " and " + getattr(table_methods[i + 1],
                                                                                               'table'))
        for method in table_methods:
            table_name = getattr(method, 'table')
            field_methods = cls.get_field_methods(table_name)
            for i in range(len(field_methods) - 1):
                if getattr(field_methods[i], 'fields_order') == getattr(field_methods[i + 1], 'fields_order'):
                    raise ValueError(
                        'fields_order 重复：' + getattr(field_methods[i], 'field') + " and " + getattr(
                            field_methods[i + 1],
                            'field'))

    @classmethod
    def get_field_method(cls, table_name, fields=None):
        field_methods = cls.get_field_methods(table_name=table_name)
        if not fields:
            return field_methods

        fields_list = [getattr(method, 'fields') for method in field_methods]

        find_methods = []
        for f in fields:
            for fl in range(len(fields_list)):
                if f in fields_list[fl]:
                    if fields_list[fl] in find_methods:
                        break
                    else:
                        find_methods.append(field_methods[fl])
        return find_methods
