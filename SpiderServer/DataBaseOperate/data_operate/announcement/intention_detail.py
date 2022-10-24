from sqlalchemy import Column, TEXT, BigInteger, DateTime, VARCHAR, Date, FLOAT, INT

from DataBaseOperate.data_operate.BaseTable import AnTable


class IntentionDetail(AnTable):
    __tablename__ = 'intention_detail'

    id = Column(BigInteger(), primary_key=True)
    proj_name = Column(VARCHAR(255))
    survey = Column(TEXT)
    budget = Column(VARCHAR(255))
    purchase_time = Column(DateTime)
    other = Column(TEXT)
