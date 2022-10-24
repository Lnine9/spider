from sqlalchemy import Column, TEXT, BigInteger, DateTime, VARCHAR

from RelationAnalysis.data_operate.base_server_table import BaseServerTable
from RelationAnalysis.data_operate.pool_table import AnTable
from RelationAnalysis.data_operate.connection_server import ClassType
from RelationAnalysis.entity.announcement_info import AnnouncementInfoEntity


class ProvideUnit(AnTable, AnnouncementInfoEntity):
    """
    供应商
    """
    __tablename__ = 'provide_unit'
    class_type = ClassType.ANNOUNCEMENT

    id = Column(BigInteger(), primary_key=True)
    code = Column(VARCHAR(50), nullable=False, comment='供应商识别编号')
    name = Column(VARCHAR(255), nullable=False, comment='供应商名称')
    address = Column(TEXT, comment='供应商地址')

