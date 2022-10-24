from sqlalchemy import Column, TEXT, BigInteger, VARCHAR, DateTime, FLOAT

from DataBaseOperate.data_operate.BaseTable import AnTable


class CallBidEngineering(AnTable):
    __tablename__ = 'call_bid_engineering'

    id = Column(BigInteger(), primary_key=True)
    proj_name = Column(TEXT, nullable=False, comment='项目名称')
    proj_code = Column(TEXT, nullable=False, comment='项目编号')
    resource_from = Column(TEXT, comment='资金来源')
    ET = Column(TEXT, comment='计划工期')
    region = Column(TEXT, comment='行政区域')
    proj_unit = Column(TEXT, comment='采购单位名称')
    proj_unit_address = Column(VARCHAR(500), comment='采购单位地址')
    proj_rel_p = Column(TEXT, comment='招标人联系人')
    proj_rel_m = Column(TEXT, comment='招标人联系方式')
    agent_unit = Column(TEXT, comment='代理机构名称')
    agent_unit_p = Column(TEXT, comment='招标代理机构联系人')
    agent_unit_m = Column(TEXT, comment='招标代理机构联系方式')
    agent_unit_address = Column(VARCHAR(500), comment='代理机构地址')
    tender_place = Column(TEXT, comment='投标地点')
    bid_sale_m = Column(TEXT, comment='标书发售方式')
    bid_sale_op_time = Column(DateTime, comment='标书发售起止时间')
    bid_sale_en_time = Column(DateTime, comment='标书发售起止时间')
    bid_price = Column(TEXT, comment='标书售价')
    bid_sale_place = Column(TEXT, comment='标书发售地点')
    bid_end_time = Column(DateTime, comment='投标结束时间')
    other_ex = Column(TEXT, comment='其它说明')
    sourse_url = Column(TEXT)
    title = Column(TEXT)
    proj_place = Column(TEXT, comment='项目地点')
    web_site = Column(VARCHAR(255), default=None, comment='对应目标网站')
    source_web_name = Column(VARCHAR(255), default=None, comment='来源网站名网站')
    ancm_time = Column(DateTime, comment='发布时间')
    resolution_rate = Column(FLOAT, comment='解析率')
