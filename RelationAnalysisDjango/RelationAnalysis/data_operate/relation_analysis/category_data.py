from sqlalchemy import Column, VARCHAR, DateTime, BigInteger

from RelationAnalysis.data_operate.pool_table import RelTable


class CategoryData(RelTable):
    """
    爬取记录对应公告
    """
    __tablename__ = 'category_data'
    id = Column(BigInteger(), primary_key=True, comment='id')
    an_id = Column(BigInteger(), nullable=False, comment='公告id')
    supplier_name = Column(VARCHAR(255), comment='供应商名称')
    category_name = Column(VARCHAR(255), comment='货物名称')
    item = Column(VARCHAR(255), comment='品目')
    brand = Column(VARCHAR(255), comment='品牌')
    type = Column(VARCHAR(255), comment='型号')
    number = Column(VARCHAR(255), comment='数量')
    unit_price = Column(VARCHAR(255), comment='单价')
    total_price = Column(VARCHAR(255), comment='总价')
