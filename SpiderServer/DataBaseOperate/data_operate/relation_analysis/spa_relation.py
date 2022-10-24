from sqlalchemy import Column, BigInteger

from DataBaseOperate.data_operate.BaseTable import RelTable

"""
采购人-供应商-代理机构关系类
"""


class SpaRelation(RelTable):
    __tablename__ = 'spa_relation'

    id = Column(BigInteger(), primary_key=True)
    supplier_id = Column(BigInteger())
    purchaser_id = Column(BigInteger())
    agency_id = Column(BigInteger())

# SPARelation.create_table()
