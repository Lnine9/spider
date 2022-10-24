# coding: utf-8
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, TEXT, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from BaseSpider.settings import spid_engine

Base = declarative_base()
metadata = Base.metadata
Session = sessionmaker(bind=spid_engine)
session = Session()


class Resolver(Base):
    __tablename__ = 'resolver'

    id = Column(VARCHAR(30), primary_key=True)
    sub_model_id = Column(VARCHAR(30), nullable=False, comment='所属爬虫ID')
    name = Column(VARCHAR(50), nullable=False)
    type = Column(VARCHAR(20), nullable=False, comment='')
    class_path = Column(TEXT, nullable=False, comment='解析器全路径类名')
    discription = Column(TEXT, comment='解析器描述')
    version_no = Column(VARCHAR(30), comment='版本号')
    priority = Column(INTEGER(10), comment='解析器优先级')

# 新增
def add(item: Resolver):
    if not isinstance(item, Resolver):
        raise IndexError('数据类型不匹配')
    session = Session()
    # 新增一条数据
    session.add(item)
    # 提交
    session.commit()
    # 关闭
    session.close()


# 删除
def delete(id=None):
    session = Session()
    # 新增一条数据
    result = session.query(Resolver).filter_by(id=(Resolver.id if id is None else id)).delete()
    # 提交
    session.commit()
    # 关闭
    session.close()
    return result


# 查询
def query(id=None,sub_model_id=None,type=None, priority=None, class_path=None):
    session = Session()
    # 新增一条数据
    result = session.query(Resolver).filter_by(id=(Resolver.id if id is None else id),
                                               sub_model_id=(Resolver.sub_model_id if sub_model_id is None else sub_model_id),
                                               priority=(Resolver.priority if priority is None else priority),
                                               class_path=(Resolver.class_path if class_path is None else class_path),
                                               type=(Resolver.type if type is None else type)).order_by(Resolver.priority.asc()).all()
    # 关闭
    session.close()
    return result

# 查询
def queryid():
    session = Session()
    # 新增一条数据
    result = session.query(Resolver).group_by('sub_model_id').all()
    # 关闭
    session.close()
    return result



def query_version_no(id=None):
    session = Session()
    # 新增一条数据
    result = session.query(Resolver).filter_by(id=(Resolver.id if id is None else id)).all()
    # 关闭
    session.close()
    return result[0].version_no

# 更新
def update(id: str, version_no=None):
    session = Session()
    for item in session.query(Resolver).filter(Resolver.id == id):
        if version_no is not None:
            item.version_no = version_no
    session.commit()
    session.close()