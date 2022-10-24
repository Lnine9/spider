from sqlalchemy import Column, Integer,  VARCHAR

from DataBaseOperate.data_operate.BaseTable import RelTable

"""
供应商行业划分代码表
"""


class BidIndustryCode(RelTable):
    __tablename__ = 'bid_industry_code'

    id = Column(Integer(), primary_key=True)
    code = Column(VARCHAR(12), nullable=False, comment='代码')
    value = Column(VARCHAR(255), nullable=False, comment='值')


# BidIndustryCode.create_table()
