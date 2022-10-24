from sqlalchemy import Column, TEXT, BigInteger, DateTime, VARCHAR

from BaseSpider.data_operate.BaseTable import AnTable


# 中标政府类
class WinBidGovernment(AnTable):
    __tablename__ = 'win_bid_government'

    id = Column(BigInteger(), primary_key=True)
    proj_name = Column(TEXT, nullable=False, comment='采购项目名称')
    proj_code = Column(TEXT, nullable=False, comment='项目编号')
    proj_item = Column(TEXT, comment='品目')
    call_unit = Column(TEXT, comment='采购单位')
    region = Column(TEXT, comment='行政区域')
    ancm_time = Column(DateTime, comment='公告发布时间')
    actual_price = Column(TEXT, comment='中标金额')
    call_unit_address = Column(VARCHAR(500), comment='采购单位地址')
    proj_rel_p = Column(TEXT, comment='项目联系人')
    proj_rel_m = Column(TEXT, comment='项目联系方式')
    agent_unit_name = Column(VARCHAR(255), comment='代理机构名称')
    agent_unit_address = Column(VARCHAR(500), comment='代理机构地址')
    agent_unit_p = Column(TEXT, comment='代理机构联系人')
    agent_unit_m = Column(TEXT, comment='代理机构联系方式')
    other_ex = Column(TEXT, comment='其他说明')
    purchase_m = Column(TEXT, comment='采购方式')
    sourse_url = Column(TEXT, comment='公告网页URL')
    bid_time = Column(DateTime, comment='开标时间')
    provide_unit = Column(TEXT, comment='供应商名称')
    provide_address = Column(TEXT, comment='供应商地址')
    review_time = Column(TEXT, comment='评审时间')
    review_place = Column(TEXT, comment='评审地点')
    pxy_fee_standard = Column(TEXT, comment='代理机构收费标准')
    pxy_fee = Column(TEXT, comment='代理机构收费金额')
    title = Column(TEXT, comment='公告标题')
    web_site = Column(VARCHAR(255), default=None, comment='对应目标网站')
    source_web_name = Column(VARCHAR(255), default=None, comment='来源网站名网站')