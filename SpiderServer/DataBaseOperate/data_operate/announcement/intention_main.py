from sqlalchemy import Column, TEXT, BigInteger, DateTime, VARCHAR, Date, FLOAT, INT

from DataBaseOperate.data_operate.BaseTable import AnTable


class IntentionMain(AnTable):
    __tablename__ = 'intention_main'

    id = Column(BigInteger(), primary_key=True)
    province = Column(VARCHAR(255))
    city = Column(VARCHAR(255))
    region = Column(VARCHAR(255))
    level = Column(INT)
    call_unit = Column(VARCHAR(255))
    purchase_unit = Column(VARCHAR(255))
    title = Column(VARCHAR(255))
    acnm_time = Column(DateTime)
    total_budget = Column(VARCHAR(255))
    source_website = Column(VARCHAR(255))
    source_url = Column(TEXT)
