import warnings

from RelationAnalysis.tool.class_reflection import dictionary_assignment

from RelationAnalysis.data_operate.connection_server import DBService, ClassType


class BaseServerTable:
    """
    数据库操作整合 - 服务器版
    """

    class_type = ClassType.DEFAULT

    @classmethod
    def __deal_objs(cls, objs, type):
        deal_items = []
        for obj in objs:
            item = DBService.get_deal_item(cls.class_type, cls.__name__, type, obj)
            deal_items.append(item)
        DBService.deal_operate(deal_items)

    def add_self(self):
        """
        将当前对象加入数据库
        :return:
        """
        self.__deal_objs([self, ], 'add')

    def update_self(self, **kwargs):
        """
        更新对象
        :param kwargs:待更新数据
        :return:
        """
        dictionary_assignment(self, kwargs)
        self.__deal_objs([self, ], 'update')

    def delete_self(self):
        """
        删除当前对象
        :return:
        """
        self.__deal_objs([self, ], 'delete')

    @classmethod
    def add_all(cls, objs):
        """
        添加到数据库
        通过具体的表类进行选择添加
        递归实现列表与元组的批量添加
        :param objs: 待添加数据，cls类、cls类的列表与元组
        :return:
        """
        if not isinstance(objs, list):
            objs = [objs, ]
        cls.__deal_objs(objs, 'add')

    @classmethod
    def query_all(cls, query_fields=None, query_condition=None, condition_rel="and", **kwargs):
        """
        查询所有数据
        :param query_fields: set value:{cls.xxx, cls.xx}、None 查询项，当该项存在时返回字典
        :param condition_rel: str value: and、or 查询条件关系
        :param query_condition: dict 查询字段
        :param kwargs: 条件字典
        :return:
        """
        return cls.query(query_fields=query_fields, query_condition=query_condition, condition_rel=condition_rel,
                         **kwargs)

    @classmethod
    def query_one(cls, query_fields=None, query_condition=None, condition_rel="and", **kwargs):
        """
        查询首个数据
        :param query_fields: set value:{cls.xxx, cls.xx}、None 查询项，当该项存在时返回字典
        :param condition_rel: str value: and、or 查询条件关系
        :param query_condition: dict 查询字段
        :param kwargs: 条件字典
        :return:
        """
        objs = cls.query(query_fields=query_fields, query_number=1, query_condition=query_condition,
                         condition_rel=condition_rel, **kwargs)
        if objs:
            return objs[0]

    @classmethod
    def query(cls, query_start=0, query_end=None, query_number=None, query_fields=None,
              query_condition=None, condition_rel="and", **kwargs):
        """
        查询指定条件所有数据
        :param query_number: int 查询数量
        :param query_end: int 查询结束位置
        :param query_start: int value:0 查询开始位置 默认为0，从头开始
        :param query_fields: set value:{cls.xxx, cls.xx}、None 查询项，当该项存在时返回字典
        :param condition_rel: str value: and、or 查询条件关系
        :param query_condition: dict 查询字段
        :param kwargs: 查询字段
        :return:
        """
        query_info = {'query_number': query_number, 'query_end': query_end, 'query_start': query_start,
                      'query_fields': query_fields,
                      'condition_rel': condition_rel, 'query_condition': query_condition}
        query_info.update(kwargs)
        ann_datas = DBService.query(cls.class_type, cls.__name__, query_info)
        if ann_datas is None:
            ann_datas = []
        anns = []
        for ann in ann_datas:
            win = cls()
            if query_fields and (isinstance(ann, list) or isinstance(ann, tuple)):
                ann = dict(zip(query_fields, ann))
            dictionary_assignment(win, ann)
            anns.append(win)
        return anns

    @classmethod
    def delete_all(cls, **kwargs):
        cls.__deal_objs([kwargs], 'delete')

    @classmethod
    def delete_one(cls, **kwargs):
        """
        删除一条数据
        :param kwargs:
        :return:
        """

        warnings.warn("this function is not created,please use others", DeprecationWarning)

    @classmethod
    def delete_pk(cls, pkv):
        """
        通过主键值进行删除
        :param pkv:
        :return:
        """
        warnings.warn("this function is not created,please use others", DeprecationWarning)

    @classmethod
    def update(cls, pkv: object, update_data: dict):
        """
        若已经获取对象实例，须重新刷新实例
        :param pkv: 第一主键值
        :param update_data: 待更改数据字典
        :return:
        """
        kwargs = {'id': pkv}
        kwargs.update(update_data)
        cls.__deal_objs([kwargs], 'update')

    @classmethod
    def update_all(cls, items: list, **kwargs):
        """
        更新数据库映射对象
        仅用于从数据库中查找的对象
        :param items:
        :param kwargs:
        :return:
        """
        warnings.warn("this function is deprecated.\n Please use update_objs(objs,**kwargs) to replace it",
                      DeprecationWarning)
        for obj in items:
            for para in kwargs.items():
                setattr(obj, para[0], para[1])
        cls.__deal_objs(items, 'update')

    @classmethod
    def update_objs(cls, objs: list, **kwargs):
        """
        更新数据库映射对象
        仅用于从数据库中查找的对象
        :param objs:
        :param kwargs:
        :return:
        """
        for obj in objs:
            for para in kwargs.items():
                setattr(obj, para[0], para[1])
        cls.__deal_objs(objs, 'update')

    @classmethod
    def update_all_conditions(cls, condition_data=None, condition_rel="and", update_data: dict = None):
        """
        更新
        :param condition_data: dict 查询条件
        :param condition_rel: str and、or 全体条件连接
        :param update_data: 更新字段
        :return:
        """
        warnings.warn("this function is not created,please use others", DeprecationWarning)

    @classmethod
    def UUID_SHORT(cls):
        """
        在当前数据库查询uuid_short()
        :return:
        """
        return DBService.execute_sql(cls.class_type, 'select UUID_SHORT() as uuid limit 1')[0][0]

    def to_json(self):
        json_obj = {}
        for col in self._sa_class_manager.mapper.mapped_table.columns:
            json_obj[col.name] = getattr(self, col.name)
        return json_obj
