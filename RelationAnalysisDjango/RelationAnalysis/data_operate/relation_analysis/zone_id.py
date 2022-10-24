from sqlalchemy import Column, Integer,  VARCHAR

from RelationAnalysis.data_operate.pool_table import RelTable

"""
采购品目代码表
"""


class ZoneId(RelTable):
    __tablename__ = 'zone_id'

    id = Column(Integer(), primary_key=True)
    code = Column(VARCHAR(12), nullable=False, comment='代码')
    value = Column(VARCHAR(255), nullable=False, comment='地区')


# ZoneId.create_table()