from sqlalchemy import Column, VARCHAR, TEXT, BigInteger

from DataBaseOperate.data_operate.BaseTable import AnTable


class AgentUnit(AnTable):
    """
    表结构类 -- 代理机构
    """
    __tablename__ = 'agent_unit'

    id = Column(BigInteger(), primary_key=True, nullable=False)
    code = Column(VARCHAR(50), primary_key=True, nullable=True, comment='代理机构识别编号')
    name = Column(VARCHAR(255), comment='代理机构名称')
    address = Column(TEXT, comment='代理机构地址')
