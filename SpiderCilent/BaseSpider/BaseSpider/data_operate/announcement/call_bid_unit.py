from sqlalchemy import Column, VARCHAR, TEXT, BigInteger

from BaseSpider.data_operate.BaseTable import AnTable


class CallBidUnit(AnTable):
    __tablename__ = 'call_bid_unit'
    id = Column(BigInteger(), primary_key=True, nullable=False)
    code = Column(VARCHAR(50), primary_key=True, nullable=False, comment='采购机构唯一识别码')
    name = Column(VARCHAR(255), comment='采购机构名')
    address = Column(TEXT, comment='采购机构地址')


CallBidUnit.create_table()