from sqlalchemy import Column, VARCHAR, BigInteger

from DataBaseOperate.data_operate.BaseTable import AnTable


class AnSuppRel(AnTable):
    __tablename__ = 'an_supp_rel'

    id = Column(BigInteger(), primary_key=True)
    an_id = Column(VARCHAR(30), comment='公告ID')
    supp_id = Column(VARCHAR(30), comment='供货商ID')
