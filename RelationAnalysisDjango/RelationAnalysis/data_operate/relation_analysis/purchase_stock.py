from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT

from RelationAnalysis.data_operate.pool_table import RelTable

"""
采购单位类
"""


class PurchaseStock(RelTable):
    __tablename__ = 'purchase_stock'

    Id = Column(BIGINT(20), primary_key=True, comment='标识')
    OrgId = Column(BIGINT(20), comment='单位标识')
    OrgName = Column(String(100), comment='组织名称')
    OrgCode = Column(String(50), comment='机构代码')
    UpId = Column(BIGINT(20), comment='上级组织标识')
    UpName = Column(String(100), comment='上级组织名称')
    LogoUrl = Column(String(200), comment='LOG图片路径')
    IdentityState = Column(INTEGER(11), comment='身份状态0：无效，1：有效')
    ImportTime = Column(DateTime, comment='录入时间')
    MainProperty = Column(INTEGER(11), comment='主体性质1、政府   2、企业  3、个体户  4、其它组织')
    BusTerm = Column(String(50), comment='营业期限')
    FoundTime = Column(DateTime, comment='成立日期')
    PostCode = Column(String(50), comment='邮编')
    Linkman = Column(BIGINT(20), comment='单位联系人')
    LinkmanName = Column(String(100), comment='单位联系人名称')
    LinkmanPhone = Column(String(100), comment='单位联系人电话')
    Remark = Column(LONGTEXT, comment='描述')
    LocalProv = Column(BIGINT(20), comment='所在省')
    LocalProvName = Column(String(50), comment='所在省名')
    LocalCity = Column(BIGINT(20), comment='所在市')
    LocalCityName = Column(String(50), comment='所在市名')
    LocalCounty = Column(BIGINT(20), comment='所在区县')
    LocalCountyName = Column(String(50), comment='所在区县名')
    LocalAddr = Column(String(500), comment='所在详细地址')
    EffectAreaName = Column(String(50), comment='有效区域名称')
    EffectAreaId = Column(BIGINT(20), comment='有效区域标识')
    TradeType = Column(LONGTEXT, comment='行业标识')
    TradeTypeName = Column(LONGTEXT, comment='行业类型：工商 公安 质监 教委 地税 财政 卫生 农委 民政 国土 环保 计生 监狱  体育 检察 林业 社保 市政 水利 文广 药监 法院')
    ProjectDirectoryCode = Column(LONGTEXT, comment='采购目录编码')
    ProjectDirectoryName = Column(LONGTEXT, comment='采购目录名称')
    TotalNum = Column(INTEGER(11), comment='总项目数')
    WinBidNum = Column(INTEGER(11), comment='中标项目数')


# PurchaseStock.create_table()
