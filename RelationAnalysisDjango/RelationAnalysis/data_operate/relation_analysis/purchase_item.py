from sqlalchemy import Column, Integer,  VARCHAR

from RelationAnalysis.data_operate.pool_table import RelTable

"""
采购品目代码表
"""


class PurchaseItem(RelTable):
    __tablename__ = 'purchase_item'

    id = Column(Integer(), primary_key=True)
    code = Column(VARCHAR(12), nullable=False, comment='代码')
    value = Column(VARCHAR(255), nullable=False, comment='值')


# PurchaseItem.create_table()
