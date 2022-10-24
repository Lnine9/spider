from sqlalchemy import Column, DateTime, String, Text, Date
from sqlalchemy.dialects.mysql import BIGINT, INTEGER

from RelationAnalysis.data_operate.pool_table import RelTable

"""
失信名单类
"""


class PurchaseDishonesty(RelTable):
    __tablename__ = 'purchase_dishonesty'

    Id = Column(BIGINT(20), primary_key=True, comment='标识')
    OrgName = Column(String(100), comment='名称')
    OrgCode = Column(String(100), comment='编码')
    Address = Column(Text(collation='utf8mb4_general_ci'), comment='地址')
    Behavior = Column(Text(collation='utf8mb4_general_ci'), comment='失信行为')
    Punish = Column(Text(collation='utf8mb4_general_ci'), comment='处罚')
    Basis = Column(Text(collation='utf8mb4_general_ci'), comment='依据')
    PublishTime = Column(DateTime, comment='公布日期')
    PunishTime = Column(Date, comment='处罚日期')
    Enforcement = Column(String(100), comment='执法单位')
    IsPurchase = Column(INTEGER(11), comment='是否资源处理')


# PurchaseDishonesty.create_table()
