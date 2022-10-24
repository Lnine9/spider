from sqlalchemy import Column, SmallInteger, BigInteger, DateTime, VARCHAR

from RelationAnalysis.data_operate.pool_table import RelTable

"""
解析历史记录类
"""


class ResolveHistory(RelTable):
    __tablename__ = 'resolve_history'

    id = Column(BigInteger(), primary_key=True)
    parsing_time = Column(DateTime(), nullable=False, comment='解析时间')
    relation_type = Column(VARCHAR(100), comment='解析类型')
    announcement_id = Column(BigInteger(), comment='公告id')
    relation_id = Column(BigInteger(), comment='关系id')
    resolver_id = Column(VARCHAR(), comment='解析器id')
