import logging

from sqlalchemy import BigInteger, Column, VARCHAR
from sqlalchemy.dialects.mysql import MEDIUMTEXT, INTEGER
from RelationAnalysis.data_operate.pool_table import SMTable


class CrawlHtml(SMTable):
    """
     resposne数据表
     """
    __tablename__ = 'crawl_html'

    id = Column(BigInteger(), primary_key=True)
    spider_id = Column(VARCHAR(30), nullable=False, comment='爬虫id')
    url = Column(VARCHAR(500), nullable=False, comment='网页URL')
    content = Column(MEDIUMTEXT, nullable=False, comment='response请求页面内容')
    type = Column(VARCHAR(20), nullable=False, comment='公告类型')
    section = Column(INTEGER, comment='对应段')




