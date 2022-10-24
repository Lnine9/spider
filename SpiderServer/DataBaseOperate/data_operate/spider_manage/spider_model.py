# coding: utf-8
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import  TEXT, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from DataBaseOperate.setting import spid_engine

Base = declarative_base()
metadata = Base.metadata
Session = sessionmaker(bind=spid_engine)
session = Session()


class SpiderModel(Base):
    __tablename__ = 'spider_model'

    id = Column(VARCHAR(30), primary_key=True)
    model_name = Column(VARCHAR(20), nullable=False)
    base_key = Column(VARCHAR(20), nullable=False, comment='在redis存储基本键值ֵ')
    discription = Column(TEXT, comment='模板描述')
    enable = Column(VARCHAR(10),nullable=False,  comment='是否可用')

# 新增
def add(item: SpiderModel):
    if not isinstance(item, SpiderModel):
        raise IndexError('数据类型不匹配')
    global session
    # 新增一条数据
    session.add(item)
    # 提交
    session.commit()
    # 关闭
    session.close()


# 删除
def delete(id=None, model_name=None):
    global session
    # 新增一条数据
    result = session.query(SpiderModel).filter_by(id=(SpiderModel.id if id is None else id),
                                                  model_name=(
                                                      SpiderModel.model_name if model_name is None else model_name)).delete()
    # 提交
    session.commit()
    # 关闭
    session.close()
    return result


# 查询
def query(id=None, model_name=None):
    global session
    # 新增一条数据
    result = session.query(SpiderModel).filter_by(id=(SpiderModel.id if id is None else id),
                                                  model_name=(
                                                      SpiderModel.model_name if model_name is None else model_name)).all()
    # 关闭
    session.close()
    return result

# 查询
def queryid():
    global session
    # 新增一条数据
    result = session.query(SpiderModel).all()
    # 关闭
    session.close()
    return result


# 更新
def update(id: str, model_name=None, base_key=None,
           discription=None):
    for item in session.query(SpiderModel).filter(SpiderModel.id == id):
        if model_name is not None:
            item.model_name = model_name
        if base_key is not None:
            item.base_key = base_key
        if discription is not None:
            item.discription = discription
    session.commit()
