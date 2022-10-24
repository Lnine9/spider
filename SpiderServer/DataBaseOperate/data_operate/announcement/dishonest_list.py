from sqlalchemy import BigInteger, VARCHAR, TEXT, Column, Date, DateTime

from DataBaseOperate.data_operate.BaseTable import AnTable


class DishonestList(AnTable):
    __tablename__ = 'dishonest_list'

    id = Column(BigInteger(), primary_key=True)
    name = Column(VARCHAR(100), comment='企业名称')
    code = Column(VARCHAR(100), comment='统一社会信用代码（或组织机构代码）')
    address = Column(TEXT, comment='企业地址')
    behavior = Column(TEXT, comment='严重违法失信行为的具体情形')
    punishment_result = Column(TEXT, comment='处罚结果')
    punishment_basis = Column(TEXT, comment='处罚依据')
    open_date = Column(DateTime, comment='公布日期')
    punishment_date = Column(Date, comment='处罚日期')
    deadline = Column(Date, comment='公布截止日期')
    law_enforcement_unit = Column(VARCHAR(100), comment='执法单位')
