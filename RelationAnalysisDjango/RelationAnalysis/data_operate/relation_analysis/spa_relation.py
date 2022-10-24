from sqlalchemy import Column, SmallInteger, BigInteger, DateTime, VARCHAR

from RelationAnalysis.data_operate.pool_table import RelTable

"""
采购人-供应商-代理机构关系类
"""


class SpaRelation(RelTable):
    __tablename__ = 'spa_relation'

    id = Column(BigInteger(), primary_key=True)
    supplier_id = Column(BigInteger())
    purchaser_id = Column(BigInteger())
    agency_id = Column(BigInteger())


# SpaRelation.create_table()
