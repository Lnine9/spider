# coding: utf-8
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.mysql import INTEGER, TEXT, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from BaseSpider.settings import spid_engine

Base = declarative_base()
metadata = Base.metadata
Session = sessionmaker(bind=spid_engine)
session = Session()


class ServerList(Base):
    __tablename__ = 'server_list'

    id = Column(VARCHAR(30), primary_key=True, nullable=False)
    name = Column(VARCHAR(20), primary_key=True, nullable=False, comment='服务器名')
    address = Column(VARCHAR(255), primary_key=True, nullable=False, comment='服务器IP地址ַ')
    account = Column(VARCHAR(255), comment='连接远端服务器账号')
    password = Column(VARCHAR(255), comment='连接远端服务器密码')
    other_conf = Column(TEXT, comment='服务器其他配置项，数据类型：json字符串')
    status = Column(VARCHAR(8), comment='服务器状态')


# 新增
def add(item: ServerList):
    if not isinstance(item, ServerList):
        raise IndexError('数据类型不匹配')
    global session
    # 新增一条数据
    session.add(item)
    # 提交
    session.commit()
    # 关闭
    session.close()


# 删除
def delete(id=None, name=None, address=None):
    global session
    # 新增一条数据
    result = session.query(ServerList).filter_by(id=(ServerList.id if id is None else id),
                                                 name=(ServerList.name if name is None else name),
                                                 code=(ServerList.address if address is None else address)).delete()
    # 提交
    session.commit()
    # 关闭
    session.close()
    return result


# 查询
def query(id=None, name=None, address=None):
    global session
    # 新增一条数据
    result = session.query(ServerList).filter_by(id=(ServerList.id if id is None else id),
                                                 name=(ServerList.name if name is None else name),
                                                 code=(ServerList.address if address is None else address)).all()
    # 关闭
    session.close()
    return result


# 更新
def update(id: str, name=None, address=None,
           account=None, password=None, other_conf=None, status=None):
    for item in session.query(ServerList).filter(ServerList.id == id):
        if name is not None:
            item.name = name
        if address is not None:
            item.address = address
        if account is not None:
            item.address = address
        if password is not None:
            item.address = address
        if other_conf is not None:
            item.address = address
        if status is not None:
            item.address = address
    session.commit()
