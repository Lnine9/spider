# coding: utf-8
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.mysql import TEXT, VARCHAR

from DataBaseOperate.data_operate.BaseTable import SMTable


class ResolverExceptionRecord(SMTable):
    __tablename__ = 'resolver_exception_record'

    id = Column(VARCHAR(30), primary_key=True)
    spider_id = Column(VARCHAR(30), nullable=False, comment='启动的爬虫ID')
    crawl_url = Column(TEXT, nullable=False, comment='异常的公告网址URl')
    redis_key = Column(VARCHAR(30), nullable=False)
    server_id = Column(VARCHAR(30), nullable=False, comment='本次爬虫进程所属服务器ID')
    server_name = Column(VARCHAR(255), nullable=False, comment='本次爬虫进程所属服务器名')
    crawl_time = Column(DateTime)
    reason = Column(TEXT, comment='原因')
