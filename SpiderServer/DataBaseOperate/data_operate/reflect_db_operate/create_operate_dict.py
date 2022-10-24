# coding = utf-8
import inspect

from DataBaseOperate.data_operate import decompositions
from DataBaseOperate.data_operate.reflect_db_operate import switch_path
from DataBaseOperate.server import batch_operate


class OperateAnnType:
    clazz_tuple = inspect.getmembers(decompositions, inspect.isclass)
    clazzs = {name: clazz for name, clazz in clazz_tuple}

    @staticmethod
    def add_anns(item):
        deal_list, an_id = OperateAnnType.create_operate_list(item)  # 创建操作列表
        batch_operate.deal_operate(deal_list)  # 执行操作
        return an_id

    @staticmethod
    def create_operate_list(item):
        """
        根据公告创建操作列表
        :param item:
        :return:
        """

        clazz = OperateAnnType.clazzs.get(item['an_type'], None)  # 获得分解类
        if clazz and clazz.check_ann(item):
            operates_dicts, rel_ids = OperateAnnType.decomposition(clazz, item)  # 获得基础表执行操作
            operates_dicts += OperateAnnType.deal_relations(clazz, rel_ids)  # 获得关联执行操作
            return operates_dicts, rel_ids[item['an_type']]
        return [], None

    @staticmethod
    def create_operate(class_type, class_name, item):
        """
        生成新增操作字典
        :param class_type:
        :param class_name:
        :param item:
        :return:
        """
        return {'class_type': class_type, 'class_name': class_name, 'operate': 'add', 'dict': item}

    @staticmethod
    def decomposition(clazz, item):
        """
        基础表数据
        :param clazz:
        :param item:
        :return:
        """
        operates_dicts = []
        rel_ids = {}
        methods = OperateAnnType.get_field_methods(clazz, 'base_info')  # 获取类中所有base_info注解的方法
        for method in methods:
            # 获得注解属性
            class_name = getattr(method, 'class_name')
            class_type = getattr(method, 'class_type')
            param = getattr(method, 'param_name')
            back = method(item[param])
            if isinstance(back, list):  # 多个字典返回
                rel_ids[param] = []
                for one in back:
                    if one.get('exist', None) is None:  # 数据库存在标识
                        one['id'] = switch_path.db_class(class_type).UUID_SHORT()  # 生成id
                        operate_dict = OperateAnnType.create_operate(class_type, class_name, one)  # 生成操作字典
                        operates_dicts.append(operate_dict)
                    rel_ids[param].append(one['id'])  # 记录id
            elif isinstance(back, dict):  # 单个字典返回
                if back.get('exist', None) is None:  # 数据库存在标识
                    back['id'] = switch_path.db_class(class_type).UUID_SHORT()  # 生成id
                    operate_dict = OperateAnnType.create_operate(class_type, class_name, back)  # 生成操作字典
                    operates_dicts.append(operate_dict)
                rel_ids[param] = back['id']  # 记录id
        return operates_dicts, rel_ids

    @staticmethod
    def deal_relations(clazz, rel_ids):
        """
        关联多张表数据
        :param clazz:
        :param rel_ids:
        :return:
        """
        operates_dicts = []
        methods = OperateAnnType.get_field_methods(clazz, 'rel_info')  # 获得关联解析方法
        for method in methods:
            # 获得注解属性
            class_name = getattr(method, 'class_name')
            class_type = getattr(method, 'class_type')
            param1, param2 = getattr(method, 'param_name')
            back = method(rel_ids[param1], rel_ids[param2])
            if isinstance(back, list):
                for one in back:
                    if one.get('exist', None) is None:  # 数据库存在标识
                        one['id'] = switch_path.db_class(class_type).UUID_SHORT()
                        operate_dict = OperateAnnType.create_operate(class_type, class_name, one)
                        operates_dicts.append(operate_dict)
            elif isinstance(back, dict) and back.get('exist', None) is None:
                back['id'] = switch_path.db_class(class_type).UUID_SHORT()
                operate_dict = OperateAnnType.create_operate(class_type, class_name, back)
                operates_dicts.append(operate_dict)
        return operates_dicts

    @staticmethod
    def get_field_methods(clazz, annotation_name):
        """
        获得所有可使用的数据库反射字典生成方法
        :param clazz:
        :return:
        """

        methods = OperateAnnType.get_methods(clazz)
        field_methods = [getattr(clazz, method)
                         for method in methods
                         if hasattr(getattr(clazz, method), 'enable') and getattr(getattr(clazz, method), 'name')
                         and getattr(getattr(clazz, method), 'name') == annotation_name]

        return field_methods

    @staticmethod
    def get_methods(clazz):
        """
        获得类所有方法
        :param clazz
        :return:
        """
        return list(
            filter(lambda m: not m.startswith("__") and not m.endswith("__") and callable(getattr(clazz, m)),
                   dir(clazz)))

