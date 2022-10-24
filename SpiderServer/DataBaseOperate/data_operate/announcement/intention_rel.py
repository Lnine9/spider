from sqlalchemy import Column, VARCHAR, BigInteger

from DataBaseOperate.data_operate.BaseTable import AnTable


class IntentionRel(AnTable):
    __tablename__ = 'intention_rel'

    id = Column(BigInteger(), primary_key=True)
    main_id = Column(VARCHAR(30), nullable=False)
    detail_id = Column(VARCHAR(30), nullable=False)

