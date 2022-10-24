from sqlalchemy import Column, VARCHAR, DateTime, BigInteger

from DataBaseOperate.data_operate.BaseTable import SMTable


class CrawlAnRel(SMTable):
    """
    爬取记录对应公告
    """
    __tablename__ = 'crawl_an_rel'
    id = Column(BigInteger(), primary_key=True)
    spider_id = Column(VARCHAR(30), nullable=False, comment='爬虫ID')
    crawl_history_id = Column(VARCHAR(30), nullable=False, comment='爬虫历史ID')
    response_id = Column(BigInteger(), comment='response数据_id')
    exception_type = Column(VARCHAR(255), comment='异常类型')
    exception_id = Column(VARCHAR(255), comment='异常id')
    is_handle = Column(VARCHAR(255), comment='异常处理')
    crawl_time = Column(DateTime, nullable=False, comment='爬取时间')
