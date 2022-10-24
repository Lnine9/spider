from sqlalchemy import Column, TEXT, BigInteger, Integer, VARCHAR

from BaseSpider.data_operate.BaseTable import AnTable


class WbSupplier(AnTable):
    __tablename__ = 'wb_supplier'

    id = Column(BigInteger(), primary_key=True)
    supp_name = Column(VARCHAR(255), nullable=False, comment='中标供应商')
    supp_code = Column(VARCHAR(50), comment='中标供应商编号')
    supp_ranking = Column(VARCHAR(1), comment='中标供应商名次')
    supp_amount = Column(TEXT, comment='中标金额')


WbSupplier.create_table()