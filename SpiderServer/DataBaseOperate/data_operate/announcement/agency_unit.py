from sqlalchemy import Column, SmallInteger, BigInteger, DateTime, VARCHAR, DECIMAL, CHAR, Text

from DataBaseOperate.data_operate.BaseTable import AnTable

"""
代理机构类
"""


class AgencyUnit(AnTable):
    __tablename__ = 'agency_unit'

    Id = Column(BigInteger(), primary_key=True)
    OrgName = Column(VARCHAR(100), nullable=False, comment='组织名称')
    OrgCode = Column(VARCHAR(50), nullable=False, comment='机构代码')
    UpId = Column(BigInteger(), comment='上级组织')
    UpName = Column(VARCHAR(100), comment='上级组织名称')
    IdentityState = Column(SmallInteger(), nullable=False, comment='身份状态0：无效，1：有效')
    ImportTime = Column(DateTime, nullable=False, comment='录入时间')
    MainProperty = Column(SmallInteger(), comment='主体性质1、政府   2、企业  3、个体户  4、其它组织')
    BusTerm = Column(VARCHAR(50), comment='营业期限')
    FoundTime = Column(BigInteger(), comment='成立日期')
    RegMoney = Column(DECIMAL(18, 2), comment='注册资金')
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
    PostCode = Column(VARCHAR(50), comment='邮编')
    MainScope = Column(Text, comment='经营范围（主营）')
    ConcurrentlyScope = Column(Text, comment='经营范围（兼营）')
    TradeType = Column(SmallInteger(), comment='行业类型标识')
    TradeTypeName = Column(VARCHAR(50), comment='行业名称：工商 公安 质监 教委 地税 财政 卫生 农委 民政 国土 环保 计生 监狱 '
                                                ' 体育 检察 林业 社保 市政 水利 文广 药监 法院')
    CompanyType = Column(SmallInteger(), comment='公司类型1-总公司 2-分支机构')
    LegalPerson = Column(VARCHAR(100), comment='法人代表')
    LegalPersonIdentity = Column(CHAR(20), comment='法人身份证号')
    LegalPersonEmail = Column(VARCHAR(200), comment='法人邮箱')
    LegalPersonPhone = Column(CHAR(20), comment='法人电话')
    RegAddress = Column(VARCHAR(200), comment='注册地址')
    EffectAreaId = Column(BigInteger(), comment='有效区域标识')
    EffectAreaName = Column(VARCHAR(50), comment='有效区域名称')


# AgencyUnit.create_table()
