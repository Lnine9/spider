from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, BIGINT, DATETIME
from BaseSpider.data_operate.BaseTable import SMTable


class AnnouceResolveInfo(SMTable):
    __tablename__ = 'annouce_resolve_info'

    id = Column(VARCHAR(30), primary_key=True)
    response_id = Column(BIGINT, nullable=False, comment="公告Id")
    spider_id = Column(VARCHAR(30), nullable=False, comment="爬虫Id")
    finish_time = Column(DATETIME, comment="完成时间")
    type = Column(VARCHAR(20), nullable=False, comment="公告类型")
    state = Column(VARCHAR(30), comment="解析状态")

