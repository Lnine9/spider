from sqlalchemy import Column, TEXT, BigInteger, VARCHAR, DateTime
from sqlalchemy import DATE

from BaseSpider.data_operate.BaseTable import AnTable


# 招标政府类
class CallBidGovernment(AnTable):
    __tablename__ = 'call_bid_government'

    id = Column(BigInteger(), primary_key=True)
    proj_name = Column(TEXT, nullable=False, comment='采购项目名称')
    proj_code = Column(TEXT, nullable=False, comment='项目编号')
    proj_item = Column(TEXT, comment='品目')
    call_unit = Column(TEXT, comment='采购单位')
    region = Column(TEXT, comment='行政区域')
    ancm_time = Column(DateTime, comment='公告发布时间')
    budget = Column(TEXT, comment='预算金额')
    call_unit_address = Column(VARCHAR(500), comment='采购单位地址')
    proj_rel_p = Column(TEXT, comment='项目联系人')
    proj_rel_m = Column(TEXT, comment='项目联系方式')
    agent_unit_name = Column(VARCHAR(255), comment='代理机构名称')
    agent_unit_address = Column(VARCHAR(500), comment='代理机构地址')
    agent_unit_p = Column(TEXT, comment='代理机构联系人')
    agent_unit_m = Column(TEXT, comment='代理机构联系方式')
    tender_place = Column(TEXT, comment='投标地点')
    bid_sale_m = Column(TEXT, comment='标书发售方式')
    bid_sale_op_time = Column(DateTime, comment='标书发售时间')
    bid_sale_en_time = Column(DateTime, comment='标书发售截止时间')
    bid_sale_place = Column(TEXT, comment='标书发售地点')
    bid_price = Column(TEXT, comment='标书售价')
    bid_place = Column(TEXT, comment='开标地点')
    other_ex = Column(TEXT, comment='其他说明')
    purchase_m = Column(TEXT, comment='采购方式')
    sourse_url = Column(TEXT, comment='公告网页URL')
    bid_time = Column(DateTime, comment='开标时间')
    title = Column(TEXT, comment='公告标题')
    web_site = Column(VARCHAR(255), default=None, comment='对应目标网站')
    source_web_name = Column(VARCHAR(255), default=None, comment='来源网站名网站')
    bid_end_time = Column(DateTime, comment='投标结束时间')


CallBidGovernment.create_table()