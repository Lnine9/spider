import warnings
from abc import abstractmethod

from sqlalchemy import inspect, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class BaseTable(Base):
    """
    数据库操作整合
    必须实现 engine 再使用
    仅实现单表操作，多表操作自行进行
    engine=create_engine("mysql+mysqlconnector://root:password@localhost/db")  # 需要精确到具体的数据库，减少指定库操作
    通过getSession可以获得session进行其他操作
    可通过commit直接提交外部对实体的更改
    """
    __abstract__ = True
    engine = None  # 连接引擎 须实例化，用于创建表
    __DBSession = None

    def add_self(self):
        """
        将当前对象加入数据库
        :return:
        """
        session = self.getSession()

        try:
            session.add(self)
            session.commit()
            return self.get_pk_value()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def update_self(self, **kwargs):
        """
        更新对象
        :param kwargs:待更新数据
        :return:
        """
        with self.session_manage("w") as session:
            item = session.merge(self)
            for key in kwargs:
                if hasattr(item, key):
                    setattr(item, key, kwargs[key])
                else:
                    raise KeyError('数据错误，未知字段: ' + key)
            session.commit()
            # 修改当前对象
            for key in kwargs:
                if hasattr(self, key):
                    setattr(self, key, kwargs[key])
                else:
                    raise KeyError('数据错误，未知字段: ' + key)

    def delete_self(self):
        with self.session_manage("w") as session:
            item = session.merge(self)
            session.delete(item)

    def get_pk_value(self):
        """
        获得第一主键值
        :return:
        """
        pkn = self.get_pk_name()
        pkv = getattr(self, pkn)
        return pkv

    @classmethod
    def get_pk_name(cls, table_class=None):
        """
        获取当前表的第一主键名
        :param table_class:类名
        :return:
        """
        return inspect(table_class if table_class else cls).primary_key[0].name

    @classmethod
    def add_all(cls, objs):
        """
        添加到数据库
        通过具体的表类进行选择添加
        递归实现列表与元组的批量添加
        :param objs: 待添加数据，cls类、cls类的列表与元组
        :return:
        """
        with cls.session_manage("w") as session:
            if isinstance(objs, (list, tuple)):
                for item in objs:
                    if isinstance(item, BaseTable):
                        session.add(item)
                    else:
                        raise TypeError('数据类型不匹配: ' + item)
            elif isinstance(objs, BaseTable):
                session.add(objs)
            else:
                raise TypeError('数据类型不匹配: ' + objs)

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

        if query_condition is None:
            query_condition = {}
        with cls.session_manage() as session:
            query = cls.__query_fields__(session, query_fields)
            query_condition.update(kwargs)
            if condition_rel == "or":
                query = query.filter_by(or_(**query_condition))
            else:
                query = query.filter_by(**query_condition)
            all_query = query.all()
        return all_query

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
        with cls.session_manage("r") as session:
            query = cls.__query_fields__(session, query_fields)
            if query_condition is None:
                query_condition = {}
            query_condition.update(kwargs)
            if condition_rel == "or":
                query = query.filter_by(or_(**query_condition))
            else:
                query = query.filter_by(**query_condition)
            all_query = query.first()
        return all_query

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
        with cls.session_manage() as session:
            query = cls.__query_fields__(session, query_fields)
            # 条件查询
            if query_condition is None:
                query_condition = {}
            query_condition.update(kwargs)
            if condition_rel == "or":
                query = query.filter_by(or_(**query_condition))
            else:
                query = query.filter_by(**query_condition)

            # 查询限制条件
            if query_number and query_number > 0:
                limit = query_number
            elif query_end and query_end > query_start:
                limit = query_end - query_start
            else:
                limit = None
            all_query = query.offset(query_start).limit(limit).all()
        return all_query

    @classmethod
    def delete_all(cls, **kwargs):
        with cls.session_manage("w") as session:
            session.query(cls).filter_by(**kwargs).delete(synchronize_session=False)

    @classmethod
    def delete_one(cls, **kwargs):
        """
        删除一条数据
        :param kwargs:
        :return:
        """
        obj = cls.query_one(**kwargs)
        obj.delete_self()
        return obj

    @classmethod
    def delete_pk(cls, pkv):
        """
        通过主键值进行删除
        :param pkv:
        :return:
        """
        with cls.session_manage("w") as session:
            pk = cls.get_pk_name()
            session.query(cls).filter_by(**{pk: pkv}).delete(synchronize_session=False)

    @classmethod
    def update(cls, pkv: object, update_data: dict):
        """
        若已经获取对象实例，须重新刷新实例
        :param pkv: 第一主键值
        :param update_data: 待更改数据字典
        :return:
        """
        pk = cls.get_pk_name()
        obj = cls.query_one(**{pk: pkv})
        obj.update_self(**update_data)

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
        with cls.session_manage("w") as session:
            for obj in items:
                item = session.merge(obj)
                print(item.__dict__)
                for key in kwargs:
                    if hasattr(item, key):
                        setattr(item, key, kwargs[key])
                    else:
                        raise KeyError('数据错误，未知字段: ' + key)
                # 修改当前对象
                for key in kwargs:
                    if hasattr(obj, key):
                        setattr(obj, key, kwargs[key])
                    else:
                        raise KeyError('数据错误，未知字段: ' + key)

    @classmethod
    def update_objs(cls, objs: list, **kwargs):
        """
        更新数据库映射对象
        仅用于从数据库中查找的对象
        :param objs:
        :param kwargs:
        :return:
        """
        with cls.session_manage("w") as session:
            for obj in objs:
                item = session.merge(obj)
                print(item.__dict__)
                for key in kwargs:
                    if hasattr(item, key):
                        setattr(item, key, kwargs[key])
                    else:
                        raise KeyError('数据错误，未知字段: ' + key)
                # 修改当前对象
                for key in kwargs:
                    if hasattr(obj, key):
                        setattr(obj, key, kwargs[key])
                    else:
                        raise KeyError('数据错误，未知字段: ' + key)

    @classmethod
    def update_all_conditions(cls, condition_data=None, condition_rel="and", update_data: dict = None):
        """
        更新
        :param condition_data: dict 查询条件
        :param condition_rel: str and、or 全体条件连接
        :param update_data: 更新字段
        :return:
        """
        if condition_data is None:
            condition_data = {}
        if update_data is None:
            update_data = {}
        with cls.session_manage("w") as session:
            if condition_rel == "and":
                query = session.query(cls).filter_by(**condition_data)
            elif condition_rel == "or":
                query = session.query(cls).filter_by(or_(**condition_data))
            query.update(update_data)

    @classmethod
    def getSession(cls):
        """
        获得session
        :return:
        """
        if cls.__DBSession:
            return cls.__DBSession()
        elif not cls.__DBSession:
            cls.__DBSession = sessionmaker(bind=cls.engine)
            return cls.__DBSession()
        else:
            raise AttributeError(
                '缺少数据库引擎，__engine = create_engine("mysql+mysqlconnector://root:password@localhost/db")')

    @classmethod
    def commit(cls, session):
        """
        提交
        :return:
        """
        try:
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    @classmethod
    def execute(cls, sql):
        """
        执行sql语句
        :param sql:
        :return:
        """
        not_query = "update" in sql.lower() or "insert" in sql.lower() or "delete" in sql.lower()
        session = cls.getSession()
        cursor = session.execute(sql)
        if not_query:
            try:
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()
        else:
            result = cursor.fetchall()
            session.close()
            for index, entry in enumerate(result):
                result[index] = list(entry)
            return result

    @classmethod
    def UUID_SHORT(cls):
        """
        在当前数据库查询uuid_short()
        :return:
        """
        session = cls.getSession()
        try:
            result = session.execute('select UUID_SHORT() as uuid limit 1')
            for i in result:
                return i.uuid
        except:
            session.rollback()
            try:
                result = session.execute('select UUID_SHORT() as uuid limit 1')
                for i in result:
                    return i.uuid
            except:
                raise AttributeError('数据库连接异常，无法查询uuid_short')

    @classmethod
    def create_table(cls):
        """
        创建表
        :return:
        """
        if cls.check_class():
            Base.metadata.create_all(cls.engine)
        else:
            raise AttributeError(
                '缺少数据库引擎，__engine = create_engine("mysql+mysqlconnector://root:password@localhost/db")')

    @classmethod
    def __query_fields__(cls, session, query_fields):
        """
        返回select xx语句
        :param session:
        :param query_fields:
        :return:
        """
        if query_fields and type(query_fields) == set:
            return session.query(*query_fields)
        else:
            return session.query(cls)

    @classmethod
    @abstractmethod
    def check_class(cls):
        if issubclass(cls, BaseTable):
            if cls != BaseTable:
                return True
        return False

    @classmethod
    def session_manage(cls, type="r"):
        return SessionManage(cls, type)


class SessionManage(object):
    """
    session的with控制器
    """

    def __init__(self, clazz, type="r"):
        self.clazz = clazz
        self.type = type

    def __enter__(self):
        self.session = self.clazz.getSession()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self.type == "w":
                self.session.commit()
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()
