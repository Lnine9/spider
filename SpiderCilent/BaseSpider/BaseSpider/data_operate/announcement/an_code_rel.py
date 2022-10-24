from sqlalchemy import Column, VARCHAR, BigInteger

from BaseSpider.data_operate.BaseTable import AnTable


class AnCodeRel(AnTable):
    __tablename__ = 'an_code_rel'

    id = Column(BigInteger(), primary_key=True)
    an_table = Column(VARCHAR(20),
                      comment='公告所属表\\r\\nCB_G: call_bid_government\\r\\nWB_G: win_bid_government\\r\\nFB_G: failure_bid_government\\r\\nMB_G: modify_bid_government\\r\\nCB_E: call_bid_engineering')
    an_id = Column(VARCHAR(30), comment='公告ID')
    code_id = Column(VARCHAR(30), comment='网页源码ID')


AnCodeRel.create_table()


