# coding: utf-8
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIGINT
from DataBaseOperate.data_operate.BaseTable import RelTable


class ProjLinkRel(RelTable):
    __tablename__ = 'proj_link_rel'

    id = Column(BIGINT(20), primary_key=True)
    call_id = Column(BIGINT(20))
    win_id = Column(BIGINT(20))
    proj_id = Column(BIGINT(20))
