from sqlalchemy import Column, TEXT, BigInteger, DateTime, VARCHAR
from RelationAnalysis.data_operate.pool_table import AnTable
from RelationAnalysis.entity.announcement_info import AnnouncementInfoEntity


# 更正政府类
class ModifyBidGovernment(AnTable, AnnouncementInfoEntity):
    __tablename__ = 'modify_bid_government'

    id = Column(BigInteger(), primary_key=True)
    proj_name = Column(TEXT, nullable=False, comment='采购项目名')
    proj_code = Column(TEXT, nullable=False, comment='项目编号')
    region = Column(TEXT, comment='行政区域')
    ancm_time = Column(DateTime, comment='公告发布时间')
    purchasing_unit_name = Column(VARCHAR(255), comment='采购单位名称')
    call_unit_address = Column(VARCHAR(500), comment='采购单位地址')
    proj_rel_p = Column(TEXT, comment='项目联系人')
    proj_rel_m = Column(TEXT, comment='项目联系方式')
    agent_unit_name = Column(VARCHAR(255), comment='代理机构名称')
    agent_unit_address = Column(VARCHAR(500), comment='代理机构地址')
    agent_unit_p = Column(TEXT, comment='代理机构联系人')
    agent_unit_m = Column(TEXT, comment='代理机构联系方式')
    other_ex = Column(TEXT, comment='其他说明')
    purchase_m = Column(TEXT, comment='采购方式')
    sourse_url = Column(TEXT, comment='公告URL')
    title = Column(TEXT, comment='公告标题')
    modify_content = Column(TEXT, comment='更正内容')
    origin_announce_time = Column(DateTime, comment='起始发布时间')
    web_site = Column(VARCHAR(255), default=None, comment='对应目标网站')
    source_web_name = Column(VARCHAR(255), default=None, comment='来源网站名网站')


# ModifyBidGovernment.create_table()
