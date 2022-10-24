from sqlalchemy import Column, SmallInteger, BigInteger, DateTime, VARCHAR

from DataBaseOperate.data_operate.BaseTable import RelTable

"""
采购人类
"""


class PurchaserInformation(RelTable):
    __tablename__ = 'purchaser_information'

    Id = Column(BigInteger(), primary_key=True)
    OrgName = Column(VARCHAR(100), nullable=False, comment='组织名称')
    OrgCode = Column(VARCHAR(50), nullable=False, comment='机构代码')
    UpId = Column(BigInteger(), comment='上级组织')
    UpName = Column(VARCHAR(100), comment='上级组织名称')
    IdentityState = Column(SmallInteger(), nullable=False, comment='身份状态0：无效，1：有效')
    ImportTime = Column(DateTime, nullable=False, comment='录入时间')
    MainProperty = Column(SmallInteger(), comment='主体性质1、政府   2、企业  3、个体户  4、其它组织')
    BusTerm = Column(VARCHAR(50), comment='营业期限')
    FoundTime = Column(DateTime, comment='成立日期')
    PostCode = Column(VARCHAR(50), comment='邮编')
    Linkman = Column(BigInteger(), comment='单位联系人')
    LinkmanName = Column(VARCHAR(100), comment='单位联系人名称')
    LinkmanPhone = Column(VARCHAR(100), comment='单位联系人电话')
    Remark = Column(VARCHAR(2000), comment='描述')
    LocalProv = Column(BigInteger(), comment='所在省')
    LocalProvName = Column(VARCHAR(50), comment='所在省名')
    LocalCity = Column(BigInteger(), comment='所在市')
    LocalCityName = Column(VARCHAR(50), comment='所在市名')
    LocalCounty = Column(BigInteger(), comment='所在区县')
    LocalCountyName = Column(VARCHAR(50), comment='所在区县名')
    LocalAddr = Column(VARCHAR(500), comment='所在详细地址')
    TradeType = Column(SmallInteger(), comment='行业类型标识')
    TradeTypeName = Column(VARCHAR(50), comment='行业类型：工商 公安 质监 教委 地税 财政 卫生 农委 民政 国土 环保 计生 监狱 '
                                                ' 体育 检察 林业 社保 市政 水利 文广 药监 法院')
    TradeDept = Column(SmallInteger(), comment='行业部门1行政政法 2教科文 3经济建设 4农业 5社会保障 6企业')
    EffectAreaName = Column(VARCHAR(50), comment='有效区域名称')
    EffectAreaId = Column(BigInteger(), comment='有效区域标识')


# PurchaserInformation.create_table()
