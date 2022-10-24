# coding=gbk
from sqlalchemy import Column, VARCHAR, DateTime

from DataBaseOperate.data_operate.BaseTable import SMTable
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from DataBaseOperate.setting import spid_engine

Base = declarative_base()
metadata = Base.metadata
Session = sessionmaker(bind=spid_engine)
session = Session()

class Client(SMTable):
    """
    客户端公告
    """
    __tablename__ = 'client'
    name = Column(VARCHAR(50), primary_key=True,comment='PC名称')
    ip = Column(VARCHAR(50), nullable=False, comment='PC_IP')
    status = Column(VARCHAR(10), nullable=False, comment='PC状态')
    start_time = Column(DateTime(), nullable=False, comment='爬虫启动时间')
    is_using = Column(VARCHAR(10), nullable=False, comment='是否在使用')


def update(name, ip=None, status=None, start_time=None, is_using=None):
    session = Session()
    for item in session.query(Client).filter(Client.name == name):
        if ip is not None:
            item.ip = ip
    if status is not None:
        item.status = status
    if start_time is not None:
        item.start_time = start_time
    if is_using is not None:
        item.is_using = is_using
    session.commit()
    session.close()