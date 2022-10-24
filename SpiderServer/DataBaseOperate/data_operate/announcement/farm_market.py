from sqlalchemy import Column, TEXT, BigInteger, DateTime, VARCHAR, Date, FLOAT, INT

from DataBaseOperate.data_operate.BaseTable import AnTable


class FarmMarket(AnTable):
    __tablename__ = 'farm_market'

    id = Column(BigInteger(), primary_key=True)
    market = Column(VARCHAR(255))
    category = Column(VARCHAR(255))
    variety = Column(VARCHAR(255))
    method = Column(VARCHAR(255))
    unit = Column(VARCHAR(255))
    price = Column(FLOAT())
    time = Column(DateTime)
    yesterdaynum = Column(VARCHAR(255))
