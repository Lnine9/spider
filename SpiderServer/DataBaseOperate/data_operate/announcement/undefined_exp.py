from sqlalchemy import VARCHAR, Column, BigInteger

from DataBaseOperate.data_operate.BaseTable import AnTable


class UndefinedExp(AnTable):
    __tablename__ = 'undefined_exp'

    id = Column(BigInteger(), primary_key=True)
    name = Column(VARCHAR(255))
    sub_an_id = Column(VARCHAR(30), comment='所属公告ID')
