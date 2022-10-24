from sqlalchemy import Column, TEXT, BigInteger, DateTime, VARCHAR

from RelationAnalysis.data_operate.base_server_table import BaseServerTable
from RelationAnalysis.data_operate.pool_table import AnTable
from RelationAnalysis.data_operate.connection_server import ClassType
from RelationAnalysis.entity.announcement_info import AnnouncementInfoEntity


class AgentUnit(AnTable, AnnouncementInfoEntity):
    """
    代理机构
    """
    __tablename__ = 'agent_unit'
    class_type = ClassType.ANNOUNCEMENT

    id = Column(BigInteger(), primary_key=True)
    code = Column(VARCHAR(50), nullable=False, comment='代理机构识别编号')
    name = Column(VARCHAR(255), nullable=False, comment='代理机构名称')
    address = Column(TEXT, comment='代理机构地址')

