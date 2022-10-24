from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT

from RelationAnalysis.data_operate.pool_table import RelTable

"""
采购项目采购项目类
"""


class PurchaseProject(RelTable):
    __tablename__ = 'purchase_project'

    Id = Column(BIGINT(20), primary_key=True, comment='标识')
    State = Column(INTEGER(11), comment='状态 4-有效 5-无效')
    IssueTime = Column(DateTime, comment='发布时间')
    DistrictName = Column(String(64), comment='行政区域名称')
    DistrcitCode = Column(String(16), comment='行政区域编码')
    Title = Column(String(512), comment='标题')
    Content = Column(LONGTEXT, comment='内容')
    ProjectName = Column(String(300), comment='项目名称')
    ProjectCode = Column(String(250), comment='项目编号')
    ProjectBudget = Column(String(200), comment='项目预算')
    ProjectPurchaseWay = Column(INTEGER(11), comment='项目采购方式100-公开招标200-邀请招标300-竞争性谈判400-询价500-单一来源600-协议供货6001-电子竞价6002-电子反拍700-定点采购800-竞争性磋商')
    ProjectPurchaseWayName = Column(String(64), comment='项目采购方式名称 100-公开招标200-邀请招标300-竞争性谈判400-询价500-单一来源600-协议供货6001-电子竞价6002-电子反拍700-定点采购800-竞争性磋商')
    ProjectDirectoryName = Column(String(500), comment='项目采购目录名称')
    ProjectDirectoryCode = Column(String(500), comment='项目采购目录编码')
    ProjectIndustryName = Column(String(200), comment='项目行业名称')
    ProjectIndustryCode = Column(String(100), comment='项目行业编码')
    ProjectIndustry = Column(BIGINT(20), comment='项目行业标识')
    Buyer = Column(BIGINT(20), comment='采购人标识')
    BuyerName = Column(String(2000), comment='采购人名称')
    BuyerPerson = Column(String(64), comment='采购人联系人')
    BuyserTEL = Column(String(100), comment='采购人电话')
    Agent = Column(BIGINT(20), comment='代理机构标识')
    AgentName = Column(String(64), comment='代理机构名称')
    AgentPerson = Column(String(64), comment='代理机构联系人')
    AgentTEL = Column(String(100), comment='代理机构电话')
    PurchaseDesWay = Column(INTEGER(11), comment='购买明细描述方式 1-文字描述 2-结构化描述')
    PurchaseDes = Column(LONGTEXT, comment='购买明细 文字（描述方式1)，或者json数组（描述方式2[{packageNum:int,directory:{id:long,name:string,code:string},money:double,number:int,requirement:string,supplier:{id:long,name:string},contact:string },...]每项最多1000字，最多10条')
    BidWinSupplierId = Column(LONGTEXT, comment='中标供应商标识(多个逗号隔开)')
    BidWinSupplier = Column(LONGTEXT, comment='中标供应商名称(多个逗号隔开)')
    BidWinAmount = Column(String(1000), comment='中标金额(多个逗号隔开)')
    SourseUrl = Column(String(500), comment='来源url')
    SourseName = Column(String(100), comment='来源名称')
    sourceType = Column(INTEGER(11), comment='来源 1.政府采购2.行采家3.其他')
    Keyword = Column(LONGTEXT, comment='关键词')
    TradeType = Column(LONGTEXT, comment='行业标识')
    TradeTypeName = Column(LONGTEXT, comment='行业类型：工商 公安 质监 教委 地税 财政 卫生 农委 民政 国土 环保 计生 监狱  体育 检察 林业 社保 市政 水利 文广 药监 法院')


# PurchaseProject.create_table()
