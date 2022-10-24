from sqlalchemy import Column, SmallInteger, BigInteger, DateTime, VARCHAR, DECIMAL, CHAR

from DataBaseOperate.data_operate.BaseTable import RelTable

"""
供应商类
"""


class SupplierInformation(RelTable):
    __tablename__ = 'supplier_information'

    Id = Column(BigInteger(), primary_key=True)
    OrgName = Column(VARCHAR(100), nullable=False, comment='组织名称')
    OrgCode = Column(VARCHAR(50), nullable=False, comment='机构代码')
    UpId = Column(BigInteger(), comment='上级组织')
    UpName = Column(VARCHAR(100), comment='上级组织名称')
    IdentityState = Column(SmallInteger(), nullable=False, comment='身份状态0：无效，1：有效')
    FoundTime = Column(BigInteger(), comment='成立日期')
    ImportTime = Column(DateTime, nullable=False, comment='录入时间')
    MainProperty = Column(SmallInteger(), comment='主体性质1、政府   2、企业  3、个体户  4、其它组织')
    BusTerm = Column(VARCHAR(50), comment='营业期限')
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
    RegMoney = Column(DECIMAL(18, 2), comment='注册资金')
    RegAddress = Column(VARCHAR(200), comment='注册地址')
    RegPhone = Column(VARCHAR(50), comment='注册电话')
    OperAccount = Column(VARCHAR(200), comment='开户行')
    Accounts = Column(VARCHAR(200), comment='帐号')
    MainScope = Column(VARCHAR(4000), comment='经营范围（主营）')
    ConcurrentlyScope = Column(VARCHAR(4000), comment='经营范围（兼营）')
    EconSectorId = Column(BigInteger(), comment='所属经济行业标识')
    EconSectorName = Column(VARCHAR(50), comment='所属经济行业')
    LegalPerson = Column(VARCHAR(100), comment='法人代表')
    LegalPersonIdentity = Column(CHAR(20), comment='法人身份证号')
    EffectAreaId = Column(BigInteger(), comment='有效区域标识')
    EffectAreaName = Column(VARCHAR(50), comment='有效区域名称')
    PurchasingCatalogue = Column(VARCHAR(255), comment='采购目录')

# SupplierInformation.create_table()
