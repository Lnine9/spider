# coding: utf-8
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR
from DataBaseOperate.data_operate.BaseTable import RelTable


class PurchaserIndustry(RelTable):
    __tablename__ = 'purchaser_industry'

    id = Column(INTEGER(11), primary_key=True)
    include = Column(VARCHAR(255))
    noinclude = Column(VARCHAR(255))
    value = Column(VARCHAR(255))
