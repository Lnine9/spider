from sqlalchemy import Column, TEXT, BigInteger, VARCHAR, DateTime, FLOAT

from DataBaseOperate.data_operate.BaseTable import AnTable


class ResultsBidEngineering(AnTable):
    __tablename__ = 'results_an_engineering'

    id = Column(BigInteger(), primary_key=True)
    title = Column(TEXT, nullable=False)
    proj_name = Column(TEXT, nullable=False, comment='项目名称')
    proj_code = Column(TEXT, comment='项目编号')
    opening_time = Column(DateTime, comment='开标时间')
    notice_period = Column(TEXT, comment='公示期')
    price_ceiling = Column(TEXT, comment='最高限价')
    proj_unit = Column(TEXT, comment='采购单位名称')
    proj_unit_address = Column(VARCHAR(500), comment='采购单位地址')
    proj_rel_p = Column(TEXT, comment='招标人联系人')
    proj_rel_m = Column(TEXT, comment='招标人联系方式')
    agent_unit_p = Column(TEXT, comment='招标代理机构联系人')
    agent_unit_m = Column(TEXT, comment='招标代理机构联系方式')
    agent_unit_address = Column(VARCHAR(500), comment='代理机构地址')
    other_ex = Column(TEXT, comment='其它说明')
    sourse_url = Column(TEXT)
    web_site = Column(VARCHAR(255), default=None, comment='对应目标网站')
    source_web_name = Column(VARCHAR(255), default=None, comment='来源网站名网站')
    ancm_time = Column(DateTime, comment='发布时间')
    resolution_rate = Column(FLOAT, comment='解析率')