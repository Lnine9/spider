from sqlalchemy import Column, VARCHAR, BigInteger

from DataBaseOperate.data_operate.BaseTable import AnTable


class AnAgentRel(AnTable):
    __tablename__ = 'an_agent_rel'

    id = Column(BigInteger(), primary_key=True)
    an_table = Column(VARCHAR(20),
                      comment='公告所属表\\r\\nCB_G: call_bid_government\\r\\nWB_G: win_bid_government\\r\\nFB_G: failure_bid_government\\r\\nMB_G: modify_bid_government\\r\\nCB_E: call_bid_engineering')
    an_id = Column(VARCHAR(30), comment='公告ID')
    ag_id = Column(VARCHAR(30), comment='代理机构ID')
