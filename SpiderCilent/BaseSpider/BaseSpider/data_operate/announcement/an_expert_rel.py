from sqlalchemy import BigInteger, Column, VARCHAR

from BaseSpider.data_operate.BaseTable import AnTable


class AnExpertRel(AnTable):
    __tablename__ = 'an_expert_rel'

    id = Column(BigInteger(), primary_key=True,
                comment='公告所属表\\r\\nCB_G: call_bid_government\\r\\nWB_G: win_bid_government\\r\\nFB_G: failure_bid_government\\r\\nMB_G: modify_bid_government\\r\\nCB_E: call_bid_engineering')
    an_id = Column(VARCHAR(30), comment='公告ID')
    exp_id = Column(VARCHAR(30), comment='专家ID')


AnExpertRel.create_table()
