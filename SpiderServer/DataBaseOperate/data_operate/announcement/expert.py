from sqlalchemy import Column, VARCHAR, BigInteger

from DataBaseOperate.data_operate.BaseTable import AnTable


class Expert(AnTable):
    __tablename__ = 'expert'

    id = Column(BigInteger(), primary_key=True, nullable=False)
    code = Column(VARCHAR(50), primary_key=True, nullable=False, comment='专家唯一识别编号')
    name = Column(VARCHAR(255), comment='专家名')
