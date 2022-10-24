from sqlalchemy import Column, BigInteger, TEXT, VARCHAR

from DataBaseOperate.data_operate.BaseTable import AnTable


class ProvideUnit(AnTable):
    __tablename__ = 'provide_unit'

    id = Column(BigInteger(), primary_key=True, nullable=False)
    code = Column(VARCHAR(50), primary_key=True, nullable=False, comment='供应商唯一识别标识')
    name = Column(VARCHAR(255), comment='供应商名')
    address = Column(TEXT, comment='供应商地址')
