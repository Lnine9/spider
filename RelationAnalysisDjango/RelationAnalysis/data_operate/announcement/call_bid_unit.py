from sqlalchemy import Column, TEXT, BigInteger, VARCHAR

from RelationAnalysis.data_operate.pool_table import AnTable
from RelationAnalysis.data_operate.connection_server import ClassType
from RelationAnalysis.entity.announcement_info import AnnouncementInfoEntity


class CallBidUnit(AnTable, AnnouncementInfoEntity):
    """
    采购单位
    """
    __tablename__ = 'call_bid_unit'
    class_type = ClassType.ANNOUNCEMENT

    id = Column(BigInteger(), primary_key=True)
    code = Column(VARCHAR(50), nullable=False, comment='采购单位识别编号')
    name = Column(VARCHAR(255), nullable=False, comment='采购单位名称')
    address = Column(TEXT, comment='采购单位地址')

