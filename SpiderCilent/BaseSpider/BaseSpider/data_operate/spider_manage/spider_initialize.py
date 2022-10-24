# coding: utf-8
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from BaseSpider.settings import spid_engine

Base = declarative_base()
metadata = Base.metadata
Session = sessionmaker(bind=spid_engine)
session = Session()


class SpiderInitialize(Base):
    __tablename__ = 'spider_initialize'

    id = Column(VARCHAR(30), primary_key=True, nullable=False)
    model_id = Column(VARCHAR(50),nullable=False,comment='模板id')
    url = Column(TEXT, nullable=False, comment='url地址')
    body = Column(TEXT, nullable=False)
    callback = Column(VARCHAR(20))
    method = Column(VARCHAR(30), nullable=False,comment='POST,GET')


# 新增
def add(item: SpiderInitialize):
    if not isinstance(item, SpiderInitialize):
        raise IndexError('数据类型不匹配')
    global session
    # 新增一条数据
    session.add(item)
    # 提交
    session.commit()
    # 关闭
    session.close()


# 删除
def delete(id=None):
    global session
    # 新增一条数据
    result = session.query(SpiderInitialize).filter_by(id=(SpiderInitialize.id if id is None else id)).delete()
    # 提交
    session.commit()
    # 关闭
    session.close()
    return result


# 查询
def query(id=None,model_id=None):
    global session
    # 新增一条数据
    result = session.query(SpiderInitialize).filter_by(id=(SpiderInitialize.id if id is None else id),
                                                       model_id=(SpiderInitialize.model_id if model_id is None else model_id)).all()
    # 关闭
    session.close()
    return result


# 更新
def update(id: str, model_id=None, url=None,
           body=None, callback=None, method=None):
    for item in session.query(SpiderInitialize).filter(SpiderInitialize.id == id):
        if model_id is not None:
            item.model_id = model_id
        if url is not None:
            item.url = url
        if body is not None:
            item.body = body
        if callback is not None:
            item.callback = callback
        if method is not None:
            item.method = method
    session.commit()
