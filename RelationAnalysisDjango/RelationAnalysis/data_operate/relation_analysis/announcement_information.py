from sqlalchemy import Column, SmallInteger, BigInteger, Integer, DateTime, VARCHAR, TEXT

from RelationAnalysis.data_operate.pool_table import RelTable

"""
公告类
"""


class AnnouncementInformation(RelTable):
    __tablename__ = 'announcement_information'

    id = Column(BigInteger(), primary_key=True)
    noticeType = Column(Integer(), comment='公告类型，描述过长，请参见建表语句（查询：“announcementinfomation”）')
    issueTime = Column(DateTime(), comment='发布时间')
    districtName = Column(VARCHAR(64), comment='行政区域名称')
    distrcitCode = Column(VARCHAR(16), comment='行政区域编码')
    title = Column(VARCHAR(512), comment='标题')
    content = Column(TEXT(), comment='流标原因/更正内容，单一来源为原因及说明')
    projectName = Column(VARCHAR(300), comment='项目名称')
    projectCode = Column(VARCHAR(128), comment='项目编号')
    projectBudget = Column(VARCHAR(200), comment='项目预算')
    projectDirectoryName = Column(VARCHAR(200), comment='项目采购目录名称')
    projectDirectoryCode = Column(VARCHAR(100), comment='项目采购目录编码')
    projectIndustryName = Column(VARCHAR(200), comment='项目行业名称')
    projectIndustryCode = Column(VARCHAR(100), comment='项目行业编码')
    projectDescibe = Column(TEXT(), comment='项目描述')
    projectPurchaseWayName = Column(VARCHAR(64), comment='项目采购方式名称 100-公开招标200-邀请招标300-竞争性谈判400-'
                                                         '询价500-单一来源600-协议供货6001-电子竞价6002-电子反拍700-定点采购800-竞争性磋商')
    buyerName = Column(VARCHAR(2000), comment='采购人名称')
    buyerPerson = Column(VARCHAR(64), comment='采购人联系人')
    buyserTEL = Column(VARCHAR(100), comment='采购人电话')
    agentName = Column(VARCHAR(64), comment='代理机构名称')
    agentPerson = Column(VARCHAR(64), comment='代理机构联系人')
    agentTEL = Column(VARCHAR(100), comment='代理机构电话')
    purchaseDesWay = Column(Integer(), comment='购买明细描述方式 1-文字描述 2-结构化描述')
    purchaseDes = Column(TEXT(), comment='购买明细 文字（描述方式1)，或者json数组（描述方式2[{packageNum:int,'
                                         'directory:{id:long,name:string,code:string},money:double,number:int,'
                                         'requirement:string,supplier:{id:long,name:string},contact:string },...]'
                                         '每项最多1000字，最多10条')
    auditTime = Column(DateTime(), comment='评审/流标/更正/审核时间')
    auditReason = Column(VARCHAR(512), comment='评审/流标/更正/审核原因')
    bidBeginTime = Column(DateTime(), comment='公示/投标开始时间')
    bidEndTime = Column(DateTime(), comment='公示/投标结束时间')
    bidAddress = Column(VARCHAR(128), comment='投标地点')
    openBidTime = Column(DateTime(), comment='开标时间')
    opernBidAddress = Column(VARCHAR(256), comment='开标地点')
    others = Column(VARCHAR(2048), comment='其它描述json数组 [{label:"xxx",value:"xxx"},,...],每项500字最多10条')
    attachments = Column(VARCHAR(2048), comment='附件json数组[{name:string, url:string},...],每项最多100字符，最多10条')
    jury = Column(VARCHAR(512), comment='评审成员列表json数组[{"xxx",...}],每项5字，最多100项。单一来源为专家信息及论证意见')
    supplyQuaRequments = Column(TEXT(), comment='供应商资格要求json字符串数组[ {label:"xxx",value:"xxx"}],每项500字，'
                                                '最多10项单一来源为拟采购供应商全称及地址')
    tenderFile = Column(TEXT(), comment='获取文件json对象{price:double, begin:date,end:data,address:string,desc:string } ')
    responseFile = Column(TEXT(), comment='审核文件json')
    ppp = Column(TEXT(), comment='PPP项目json对象{isUnit:boolean,isLimit:boolean,isCountry:boolean,bodyName:string,'
                                 'limitStandard:string,introduceREQ:string,guaranteeREQ:string}')
    proExeCode = Column(VARCHAR(100), comment='采购执行编码')
    buyerJson = Column(TEXT(), comment='多个采购人')
    agentJson = Column(TEXT(), comment='多个代理机构')
    chargeStandard = Column(VARCHAR(2000), comment='收费标准')
    chargeMoney = Column(VARCHAR(2000), comment='收费金额')
    policyDescribe = Column(TEXT(), comment='政策描述')
    isResult = Column(SmallInteger(), comment='是否结果公告 1.基础公告 2.结果公告')
    hide = Column(SmallInteger(), comment='是否显示 1.不显示 0显示')
    solr = Column(SmallInteger(), comment='是否分词 0否 1是')
    bidSellAddress = Column(VARCHAR(256), comment='标书发售地点')
    bidSellMethod = Column(VARCHAR(256), comment='标书发售方式')
    bidSellStart = Column(DateTime(), comment='标书发售开始时间')
    bidSellEnd = Column(DateTime(), comment='标书发售结束时间')
    bidSellPrice = Column(VARCHAR(200), comment='标书售价')
    bidWinSupplier = Column(VARCHAR(64), comment='中标供应商')
    bidWinAmount = Column(VARCHAR(200), comment='中标金额')
    sourseUrl = Column(VARCHAR(500), comment='来源url')
    sourseNamel = Column(VARCHAR(100), comment='来源名称')
    buyerAddress = Column(VARCHAR(256), comment='采购人地址')
    agentAddress = Column(VARCHAR(256), comment='代理机构地址')
    viewCount = Column(BigInteger(), comment='预览量')


# AnnouncementInformation.create_table()
